Migrating from Keras to PyTorch in 2020
#######################################

:thumbnail: https://pytorch.org/assets/images/pytorch-logo.png 
:category: Tutorials
:date: 2020-05-05
:tags: Keras, PyTorch, TensorFlow, CNNs, computer vision, tutorials

*Note: this specifically applies to PyTorch 1.5 and tf.Keras 2.1.0. As
long as the final number in the version is the same, this should still
be applicable, but otherwise, YMMV*

While completing my fellowship at `Insight <insightdatascience.com>`__,
I reached a point in my `recyclable classification
project <github.com/dendrondal/CIf3R>`__ where I wanted to implement a
`siamese network <https://sorenbouma.github.io/blog/oneshot/>`__ to improve the generalizability of my model,
while requiring less training data. The ad-hoc siamese networks I
created in Keras had acceptable results, but were certainly not
production-ready. I began looking on `papers with code <paperswithcode.com>`__ for a more
SOTA model, and realized that Keras implementations are few and far
between. In fact, PyTorch seems to have `exploded in popularity <https://paperswithcode.com/trends>`__ to
the point where it is now the #1 framework on papers with code. With
this in mind, I decided it was time to start learning PyTorch.

Why move?
---------

In addition to the predominance of PyTorch on paperswithcode, there are
several advantages it offers. Back when I began learning Keras,
TensorFlow was the dominant framework partially due to easier
productionalization of models using tf.Serve. However, since then, the
productionalization gap `appears to be
closing <https://engineering.fb.com/ai-research/announcing-pytorch-1-0-for-both-research-and-production/>`__.
In addition, PyTorch comes with out-of-the-box asynchronous behavior
when loading, whereas this still has to be specified and configured when
using tf.Datasets. TensorBoard was, and still is, the predominant
monitoring solution for model training, but it’s now fully supported by
PyTorch. Finally, in my opinion, TensorFlow has made some rather strange
api decisions, whereas PyTorch seems to bear more similarity to Numpy.

..
    I would highly reccomend checking out the `60 minute
    blitz <https://pytorch.org/tutorials/beginner/blitz/neural_networks_tutorial.html>`__for
    a grasp of some of the core concepts of PyTorch. This article serves as
    a high-level overview for migration from Keras

Defining the computation graph
------------------------------

Since Keras has both the sequential and functional api, it’s worth doing
a comparison of both with the preferred way of instantiating a PyTorch
network. Here, let’s use a `simple feedforward
MLP <https://www.google.com/books/edition/Deep_Learning_with_Python/Yo3CAQAACAAJ?hl=en>`__
as an example:

.. code:: python

   #Keras sequential api
   model = Sequential()
   model.add(layers.Dense(32, activation='relu', input_shape=(64,)))
   model.add(layers.Dense(32, activation='relu'))
   model.add(layers.Dense(10, activation='softmax'))

   #Keras functional api
   input_layer = Input(shape=(64,))
   x = layers.Dense(32, activation='relu')(input_layer)
   x = layers.Dense(32, activation='relu')(x)
   output = layers.Dense(10, activation='softmax')(x)

   model = Model(input_layer, output)

   #Pytorch example
   class Model(nn.Module):
       def __init__(self):
           super(Model, self).__init__()
           self.dense1 = nn.Linear(64, 32)
           self.dense2 = nn.Linear(32, 32)
           self.output = nn.linear(32, 10)

The obvious difference here is that the standard practice for PyTorch
models is encapsulation into a class, and instantiating the parent
``Module`` class. Another less obvious difference is that both the input
and output sizes of each layer have to be specified in PyTorch. Other
than that, it’s a pretty straightforward difference. Let’s try a less
trivial example that’s more suited to the Keras functional API: a
siamese network for image similarity classification, based on the
`original paper <https://www.cs.cmu.edu/~rsalakhu/papers/oneshot1.pdf>`__ with several convolutional layers taken out for
the sake of length. This employs custom layers, shared weights, and
gives an overview of how a multi-input, single output neural network can
be implemented in the two frameworks.

.. code:: python

   #Keras example
   input_shape = (105, 105, 3)

   img_input = Input(shape=input_shape)
   left_input = Input(shape=input_shape)
   right_input = Input(shape=input_shape)

   x = Conv2D(64,(10,10), activation='relu', input_shape=input_shape)(img_input)
   x = MaxPooling2D()(x)
   x = Conv2D(128, (4, 4), activation='relu')(x)
   x = Flatten()(x)
   x = Dropout(0.5)(x)
   out = Dense(2048, activation="sigmoid")(x)

   twin = Model(img_input, out)

   # get the image embeddings, sharing weights between the two networks
   encoded_l = twin(left_input)
   encoded_r = twin(right_input)

   # merge two encoded inputs with the l1 distance between them
   L1_layer = Lambda(lambda x: tf.math.abs(x[0] - x[1]))
   L1_distance = L1_layer([encoded_l, encoded_r])

   prediction = Dense(1, activation='sigmoid')(L1_distance)

   siamese_net = Model(inputs=[left_input, right_input], outputs=prediction)

   # The same model in PyTorch    correct = 0
   class SiameseNetwork(nn.Module):
       def __init__(self):
               nn.Conv2d(3, 64, 10)
               nn.ReLU(inplace=True)
               nn.MaxPool2d(2, 2)
               nn.Conv2d(64, 128, 4)
               nn.ReLU(inplace=True)
               nn.Flatten(),
               nn.Dropout(p=0.5)
               nn.Linear(2048, 2048)
               nn.Sigmoid()
           )

Unlike Keras, convolutional layers in PyTorch have arguments in the
order of
``in_channel size, out_channels size, kernel_size, stride, padding``,
with the default stride and padding being 1 and 0, respectively. You’re
probably noticing that with the PyTorch model, we stopped around the
``twin`` definition in the Keras model. The reason being is that the
biggest difference between keras and pytorch is how you train the model,
aka the training loop.

Training the model
------------------

Defining the model isn’t very different between Keras and PyTorch, but
training the model certainly is. Rather than calling
``model.compile()``, you instead define your forward pass as a method of
your model. Also, your loss function, optimizer, and learning rate are
usually defined in the training loop. Let’s start with the forward pass
and training loop for our first MLP:

.. code:: python

   # Defining the forward pass. Note that this is a method of Model
       def forward(self, x):
           x = self.dense1(x)
           # F is an alias for torch.nn.functional
           x = F.relu(x)
           x = self.dense2(x)
           x = F.relu(x)
           x = self.output(x)
           out = F.softmax(x)
           return out

This shows two methods of model creation: for the siamese model, we
define the entire model intially, making the forward pass as simple as
``return twin(x)``. With the MLP, we defined the layers individually.
Which method is better definitely depends on your use case, but my
intuition is that a neural network that can be drawn as a linear
progression of layers lends itself well to the MLP method, whereas
defining your entire model as an attribute works well for more advanced
graphs such as ResNet/Inception type models, or models with multimodal
input/outputs. Alright, so we have our model and how our data flows
through it. The next step is training and evaluation. This is indeed far
more code than is needed by using ``callbacks`` in Keras, but the
training loop adds complexity in exchange for significantly more
flexibility.

.. code:: python

   # train_loader is some predefined Torch DataLoader instance
   # device is your cpu/gpu name
   def train(model, device, train_loader, optimizer, epoch):
       model.train()
       for batch, (X, y) in enumerate(train_loader):
           # Assuming X and y are torch tensors, you can also just call X.cuda() instead if 
           # you know you don't need to switch devices.
           X, y = X.to(device), y.to(device)
           # We re-instantiate the gradients during each iteration
           optimizer.zero_grad()
           y_hat = model(X)
           loss = F.mse_loss(y_hat, y)
           # Now we back-propagate
           loss.backward()
           optimizer.step()
           # Report accuracy every 10 batches
           if batch % 10 == 0:
               print(f'Loss of {loss} after {batch} epochs on training set')

The function above is meant to be used in a ``for`` loop with a preset
number of epochs. Optimizers are called in a similar manner compared to
Keras. Similar to the LearningRateScheduler in Keras’ callbacks, we now
have several built-in `adaptive learning
rates <https://pytorch.org/docs/stable/optim.html?highlight=scheduler#torch.optim.lr_scheduler.StepLR>`__.
We have our training function, now for the test one:

.. code:: python

   # Again, test_loader is a DataLoader instance
   def test(model, device, test_loader):
       model.eval()
       test_loss = 0
       correct = 0
       # We don't want to change the gradients, so we freeze the model here
       with torch.no_grad():
           for X, y in test_loader:
               X, y = X.to(device), y.to(device)
               y_hat = model(X)
               test_loss += F.mse_loss(y_hat, y, reduction='sum').item()
               pred = y_hat.argmax(dim=1) # For binary classification
               # For multiclass, pass keepdim=True above
               # Now we format the actual target and compare it to the predicted one
               correct += pred.eq(y.view_as(pred)).sum().item()
       
       test_loss /= len(test_loader.dataset)
       print(f'Average loss: {test_loss}\nAccuracy: {correct/len(test_loader.dataset)*100}')

Now we have our model with its foward propagation method, a training
function, and a testing function. We presume there is a data loading
function in there somewhere as well. So the final step is putting it all
together, either in script for or in a ``main`` function for CLI
execution. Here is the last bit in script form:

.. code:: python

   # With Torch, we have to specify GPU/CPU computation
   use_cuda = torch.cuda.is_available()
   device = torch.device("cuda:0" if use_cuda else "cpu")
   # First we load the model onto the GPU
   model = Model().to(device)
   # Now we load our optimizer
   optimizer = torch.optim.Adam(lr=0.001)
   # Let's also apply a learning rate decay
   scheduler = torch.optim.lr_scheduler.StepLR(optimizer)
   # Now let's train for 100 epochs
   for epoch in range(100):
      train(model, device, train_loader, optimizer, epoch)
      test(model, device, test_loader)
      scheduler.step()
   #Saving the weights of the model to a pickle file
   torch.save(model.state_dict(), 'torch_example.pt')

Whew, that’s a lot of code for a 3 layer MLP! Of course, this is only a
starting point. You’ll probably want some kind of early stopping
mechanism, monitoring with tensorboard or custom visualizations, a tqdm
progress bar, and/or logging. In performing this excercise, I’m of the
mind that the additional code is actually a good thing, as debugging
becomes far easier as you can isolate the line causing the issue with a
visual debugger (*cough* or a print statement *cough*), as opposed to
Keras abstracting that complexity away.

So this post doesn’t get too long, I’m going to direct you to `the
repository for my Insight project <https://github.com/dendrondal/CIf3R>`__ if you want to see the siamese
network in PyTorch. Overall, PyTorch is pretty great, and a smoother
transition than I originally thought. I’ll have to see if this is just a
honeymoon phase, but I figure there’s likely a reason there are so many
converts as of late. Happy hacking, and thanks for reading!

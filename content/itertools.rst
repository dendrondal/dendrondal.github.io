A wild itertools appeared!
##########################

:date: 2019-08-23
:category: Blog
:summary: A walkthrough and deployment use cases of the itertools standard library 
:thumbnail: https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg
:tags: wild python, functional programming, tutorials

About this series
-----------------

This blog post is the first of a new series I’m starting called “Wild
Python,” aka use cases of selected python libraries in deployment. Posts
of this series will generally consist of a breakdown of the library and
intended use cases, followed by several examples of how it is used in
the context of several popular GitHub repositories. This series will be
continually ongoing, partially to act as a personal refresher course.

What is *itertools*?
--------------------

Itertools is Python implementation of a common design pattern to stream
data in `functional
programming <https://www.dataquest.io/blog/introduction-functional-programming-python/>`__.
Effectively, this allows a way to take an iterable
(``list, tuple, dict, string`` etc.) and apply a very succinct method to
lazily iterate through them based on several commonly used pieces of
logic. Let’s take a toy example, one of the `most overused interview
questions <https://www.tomdalling.com/blog/software-design/fizzbuzz-in-too-much-detail/>`__:

.. code:: python

   from itertools import cycle, count, islice

   fizzes = cycle(['', '', 'fizz'])
   buzzes = cycle(['', '', '', '', 'buzz'])
   numbers = count(1)
   fizzbuzz = (f'{fizz}{buzz}' or n 
               for  fizz, buzz, n in zip(fizzes, buzzes, numbers))
   for result in islice(fizzbuzz, 16):
       print(result)

::

   1
   2
   fizz
   4
   buzz
   fizz
   7
   8
   fizz
   buzz
   11
   fizz
   13
   14
   fizzbuzz
   16

Let’s break this down: ``itertools.cycle`` consumes an iterator, then
loops back over it from the beginning infinitely, or until a stop
condition is reached. As the name implies, this is very useful for
cyclic or periodic data. ``count`` is another infinite iterator, that
accepts a “start” and “step” argument, similar to ``range()`` Finally,
we have ``islice``, another piece of syntactic sugar that is equivalent
to ``for i in range(number): do_something(iterable[i])``

However, in addition to being more readable, this has the advantage of
speed and memory efficiency. The ``for`` loop above using ``range``
would most likely be used with a previously existing iterable, which is
stored in RAM. This is opposed to the ``islice`` implementation, which
doesn’t store any values, only using RAM in the case that it is called.
Note that an equivalent alternative to the islice implementation above
is to say ``for i in range(16): print(next(fizzbuzz))`` Next is an
important method to keep in mind when working with generators.

Let’s do another example with another favorite interview question, the
`Knapsack Problem <https://en.wikipedia.org/wiki/Knapsack_problem>`__,
approximated using a brute-force approach:

.. code:: python

   from collections import namedtuple
   from itertools import combinations  

   item = namedtuple('Item', 'name value mass')
   pants = item('pants', 40, 5)
   shirt = item('shirt', 10, 2)
   shoes = item('shoes', 50, 4)
   stove = item('stove', 30, 6)
   socks = item('socks', 50, 1)
   water = item('water', 70, 7)
   tent = item('tent', 20, 6)
   hammock = item('hammock', 40, 1)
   headlamp = item('headlamp', 50, 3)
   possibilities = [pants, shirt, shoes, stove, socks, 
                    water, tent, hammock, headlamp]

   #assuming a knapsack that can carry 10kg:
   max_weight = dict()
   for n in range(1, len(possibilities)+1):
       for combination in combinations(possibilities, n):
           if sum([thing.mass for thing in combination]) == 10:
               answer = '+'.join([thing.name for thing in combination])
       error output required property nbconvert        max_weight[answer] = sum([thing.value for thing in combination])
               
   print(sorted(max_weight.items(), key=lambda d: d[1], reverse=True))

::

   [('pants+socks+hammock+headlamp', 180), ('shirt+shoes+socks+headlamp', 160), ('shirt+shoes+hammock+headlamp', 150), ('pants+shoes+socks', 140), ('pants+shoes+hammock', 130), ('shirt+socks+water', 130), ('stove+socks+headlamp', 130), ('shirt+stove+socks+hammock', 130), ('water+headlamp', 120), ('shirt+water+hammock', 120), ('stove+hammock+headlamp', 120), ('socks+tent+headlamp', 120), ('shirt+socks+tent+hammock', 120), ('tent+hammock+headlamp', 110), ('pants+shirt+headlamp', 100), ('shoes+stove', 80), ('shoes+tent', 70)]

*Note: This is neither*\ `the most efficient
solution <http://www.es.ele.tue.nl/education/5MC10/Solutions/knapsack.pdf>`__\ *,
nor is it recommended to go out into the wilderness without a shirt or
shoes.*

Let’s break this down: we have several items with a cost and weight
associated with them. There are many data structures that can represent
this, but I decided to go with named tuples for clarity’s sake (this
will probably warrant another Wild Python article). We then iterate
through all possible combinations of items by finding combinations of
different length within a nested for loop. We add them to a dictionary
if it maxes out the knapsack carrying capacity. Finally, we see what the
highest value combination is by ordering the resulting dictionary by
values rather than keys, then reversing it. We now have a very fast and
memory-efficient brute force solution! ### Chain chain chain One method
that deserves some additional explanation is ``chain``
vs. ``chain_from_iterable``. Chain takes two or more iterables as
arguments, and chains them together, consuming them in the order passed.
From_iterable takes a *single* iterator as an argument, effectively
flattening it (think smushing a matrix into an array)

Production use cases
--------------------

`Keras <https://www.tensorflow.org/guide/keras>`__ utilizes
``itertools.compress`` to check whether all functions have been properly
documented:

.. code:: python

   from itertools import compress
   def assert_args_presence(args, doc, member, name):
       args_not_in_doc = [arg not in doc for arg in args]
       if any(args_not_in_doc):
           raise ValueError(
               "{} {} arguments are not present in documentation ".format(name, list(
                   compress(args, args_not_in_doc))), member.__module__)

Compress is usually used to map an iterable to the “truthiness” of
individual components of that iterable. The list comprehension above
contains booleans based on list membership, which is then mapped back
onto the function arguments during the string formatting. This tells
anyone submitting a pull request exactly what function arguments need to
be documented.

`Numba <https://numba.pydata.org/>`__, a just-in-time compiler for
scientific computing with Python, uses itertools extensively in their
test suite:

.. code:: python

   def test_slice_passing(self):
       """
       Check passing a slice object to a Numba function.
       """
       # NOTE this also checks slice attributes
       def check(a, b, c, d, e, f):
           sl = slice(a, b, c)
           got = cfunc(sl)
           self.assertPreciseEqual(got, (d, e, f))

   cfunc = jit(nopython=True)(slice_passing)
   # Positive steps
       start_cases = [(None, 0), (42, 42), (-1, -1)]
       stop_cases = [(None, maxposint), (9, 9), (-11, -11)]
       step_cases = [(None, 1), (12, 12)]
       for (a, d), (b, e), (c, f) in itertools.product(start_cases,
                                                       stop_cases,
                                                       step_cases):
           check(a, b, c, d, e, f)

These tests ensure that the JIT variant of the function has the same
output as the python one. In order to make this test robust, they run it
on a variety of different inputs. The ``product`` is the cartesian
product of this function, effectively a nested for loop. This is an
efficient way to test a wide variety of sample cases in just a few lines
of code.

Another Numfocus library, `Dask <https://docs.dask.org/en/latest/>`__,
leads us to ``starmap``. Unlinke ``map``, which applies a function
across every item in an iterable, ``starmap``\ effectively works on
“pre-zipped” data (effectively an “iterable of iterables”). Dask wrote
their own variant of this, allowing for keyword arguments in addition to
iterables. In the code below, note that “bag (db)” just represents a
generic python object which can have multithreaded methods called on it
using method chaining.

.. code:: python

   def starmap(func, bag, **kwargs):
       return (func(*args, **kwargs) for args in bag)

   import dask.bag as db
   data = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
   b = db.from_sequence(data, npartitions=2)

   #Apply a function to each argument tuple:
   from operator import add
   b.starmap(add).compute()
   # returns [3, 7, 11, 15, 19]

   #Apply a function to each argument tuple, with additional kwargs:
   def myadd(x, y, z=0):
        return x + y + z
   b.starmap(myadd, z=10).compute()
   # returns [13, 17, 21, 25, 29]

Obviously whether to use ``map`` or ``starmap`` depends on the structure
of the iterable being fed in, but…

Considerations regarding readability
------------------------------------

You might notice that some itertools code is less “Pythonic” than a lot
of code out there. Given how clear list comprehensions can be, it’s
understandable that the traditional ``reduce`` funcitonalicty was moved
to functools rather than the global namespace. In addition, performance
gains are
`trivial <https://stackoverflow.com/questions/1247486/list-comprehension-vs-map>`__
when switching from ``map`` to a list comprehension. With this in mind,
unless you are concerned about fitting data structures in RAM, your
first-pass attempt should probably be a list comprehension rather than
reaching for the functools toolkit, as this makes for more readable and
maitainable code.

Final Thoughts
--------------

For additional use cases utilizing itertools, the `Python
documentation <https://docs.python.org/3.7/library/itertools.html#itertools-recipes>`__
has some very helpful recipes. The next time you’re trying to do some
sort of iteration on large data, or working with a heavily nested
``for`` loop, be lazy, and reach for itertools instead!

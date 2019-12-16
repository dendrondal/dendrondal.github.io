title: Making this Website
thumbnail: https://www.brandeps.com/logo-download/F/Flask-01.png
tags: [Flask, AWS, Swagger, SQLite, SQAlchemy, Swagger, REST]

#Making of...this website!

I wanted to share some of the process used in creating this website. I'm certainly not a frontend developer by any stretch of the imagination, so this was a fully new experience for me. Yes, I had the option of spinning up a squarespace or wordpress site, but where's the fun in that? I decided to build and deploy it myself, as doing this from scratch makes for a great learning opportunity. 

As with many projects, the first iteration left a lot of room for improvement. The first version (stack listed below) was great, but overkill for my use case. However, it still provided a learning experience and managed to get me a functional website, so no regrets! The second attempt is far more streamlined, scalable, and efficient.

##Stack (First attempt)
-**Flask** Flask is my framework of choice for most projects, just because of [its usefulness in creating RESTful APIs](http://dalwilliams.info/localvore). Django is a bit better for creating full websites just because of the batteries-included approach and strong opinionation of the "right way" to do things. This means quicker iteration times for larger projects. I don't expect this website to get too large, and it's helpful to build the components individually for a deeper understanding of each.

-**Frontend** There are several examples of open-source responsive templates. I chose [HTML5up](https://html5up.net/), as I really liked the aesthetics of several of their templates. This saves a lot of overhead on my part, as the HTML/CSS/JS/SASS are already defined, and I just had to tweak them to my liking.

### Deprecated Portions
These were in the first version of the website before the static refactor.

-**SQLite/SQLAlchemy** Comes included with python, and I shouldn't have to deal with too much data or a large amount of concurrency. [It's more than just a starter database](https://pythonbytes.fm/episodes/show/60/don-t-dismiss-sqlite-as-just-a-starter-db). Granted that this is being exposed to the web, it's a good idea to sanitize data going into my app to prevent injection attacks. That's where SQLAlchemy comes in, which also requires less boilerplate for queries. Yes, all SQL writes are behind authentication, but better safe than sorry!

-**Swagger/Connexion** Incredibly useful tool for creating REST APIs. You can define every endpoint with expected schema, security level, and status codes in a .yaml file before you write a single line of code.

-**ElasticBeanstalk** After playing around with a few other options, I realized pretty quickly why AWS is the industry standard. Only a few commands to spin up a website without having to manually install Nginx/Apache/etc. Also has straightforward DNS and SSL certification, on top of being quite a bit cheaper than the competition.

##Lessons Learned
This is absolutely a viable way to deploy a dynamic, responsive website. However, I realized after a month or two of deployment that several of my tech choices were overkill for the desired application, not to mention pushing me out of the AWS free tier. I realized that a portfolio website can be served using entirely static content, similar to Jekyll. Flask actually has a phenomenal workflow to generate a static blog/portfolio site: FlatPages + Freeze. That brings me to the new stack:

## Stack (Second Attempt)
-**Frozen Flask** Allows for a normal Flask development workflow, followed by running a command line tool to build the entire web app to a folder structure ideal for serving as a static site. 

-**FlatPages** Pairs well with Freeze for blog hosting, assuming you use markdown to write your posts. Just lead off your blog post with a short yaml description of post metadata. This can be read directly into Jinja for formatting, just have this in your post:

    title: Generative Models
    description: A meetup presentation I gave over the history and state-of-the-art of generative models
    thumbnail: https://upload.wikimedia.org/wikipedia/commons/1/18/Bayes%27_Theorem_MMB_01.jpg
    tags: ML, Teaching, GANs, Bayes' Theorem, VAEs, Spam Filtering, Chemistry

Assuming you have a pages directory in your application root, the flask app can be as simple as this:

    app = Flask(__name__)
    app.config.from_pyfile('settings.cfg')
    pages = FlatPages(app)
    freezer = Freezer(app)
    
    @app.route('/')
    def main_page():
        return render_template('index.html', pages=pages)
    
    @app.route('/<path:path>/')
    def render_post(path):
        page = pages.get_or_404(path)
        return render_template('post.html', page=page)

with the following Jinja to render the content. Note that the yaml notations in the markdown can be used as attributes within Jinja:

    {%  for page in pages %}
        <a href={{ url_for("render_post", path=page.path) }}>
            <div class="post">
                <div class="thumbnail">
                    <img style="width:150px; height:150px; margin-left: 5%; margin-top: 5%; margin-bottom: 5%;" src={{ page.thumbnail }} alt>
                 </div>
             <h3 style="margin-top:0; font-size:95%; alignment: center">{{ page.title }}</h3>
            <h4 style=font-size:60%>{{ page.description }}</h4>
            </div>
        </a>
    {%  endfor %}

And that's it! The markdown is rendered to HTML, with the option of adding  extensions, and compiled to a neat folder with all your assets and pages. Full credit to [John Yang](https://blog-byjohnyang.herokuapp.com/flask-website/) for his tutorial on the subject. Once I had that structure, it's back to AWS:

-**Amazon S3** A static website can be directly hosted using two S3 buckets: one for the content itself, and one for redirects. As per usual, with the help of Route 53, you can then link it to your domain name. There is a very [helpful guide](https://docs.aws.amazon.com/AmazonS3/latest/dev/website-hosting-custom-domain-walkthrough.html) for doing so readily available. 

##Conclusions
This project both provided a phenomenal learning experience, and cemented the fact that I don't want to do frontend development as a full time job (that is until WebAssembly becomes mainstream, but that's a whole different article). I'd never written a single line of CSS, had no experience with Jinja, and had never deployed an app on a cloud service before. It took a lot of trial-and-error, refactoring, and  design decisions, the latter of which is both a blessing and curse of Flask. Overall, I'm quite happy with the result, and I know I learned quite a few transferable skills in the process.

You can find the full source for this website [on Bitbucket](https://bitbucket.org/dendrondal/portfolio/)
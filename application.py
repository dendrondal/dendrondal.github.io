from flask import render_template, send_file
from flask_frozen import Freezer
from flask import Flask
from flask_flatpages import FlatPages
import sys

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')
pages = FlatPages(app)


@app.route('/')
def main_page():
    return render_template('index.html', pages=pages)


@app.route('/<path:path>/')
def render_post(path):
    page = pages.get_or_404(path)
    return render_template('post.html', page=page)


# @freezer.register_generator
# def download_resume():
#     return send_file('Williams_Resume.pdf',
#                      as_attachment=True,
#                      attachment_filename='Williams_Resume.pdf')


if __name__ == '__main__':
    from elsa import cli
    cli(app, base_url='https://dalwilliams.info')

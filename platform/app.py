from flask import Flask, render_template, request, session, redirect, url_for
from flask.ext.elasticsearch import FlaskElasticsearch

app = Flask(__name__)
es = FlaskElasticsearch(app)

@app.route('/')
def index():
    return 'Data Detective App'


if __name__ == '__main__':
    app.run(debug=True)

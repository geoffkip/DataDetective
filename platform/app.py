from flask import Flask, render_template, request, session, redirect, url_for
from flask.ext.elasticsearch import FlaskElasticsearch

app = Flask(__name__)
es = FlaskElasticsearch(app)

@app.route('/')
def index():
    return 'Data Detective App'

@app.route('/elasticsearch')
def get():
    res = requests.get('http://localhost:9200')
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    s = Search(using=es)
    res = es.search(index="paindex", body={"query": {"match_all": {}}})
    print(res)


if __name__ == '__main__':
    app.run(debug=True)

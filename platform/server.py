from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('views/index.html')

if __name__ == '__main__':
    app.run_server(debug=True)

from flask import Flask, render_template
from user.upload import *
from jump import jump_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = "BIXING IS HANDSOME"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/map")
def map():
    return render_template("map.html")


app.register_blueprint(user_upload_bp, url_prefix="/message")
app.register_blueprint(jump_bp, url_prefix="/jump")


if __name__ == '__main__':
    print(app.url_map)
    app.run(host='0.0.0.0', port=5000)
    #app.run()

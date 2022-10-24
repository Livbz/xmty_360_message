from flask import Flask
import time
app = Flask(__name__)


@app.route("/")
def test():
    print("s")
    for i in range(10):
        time.sleep(1)
        print(i)
    return "S"


app.run(threaded = True)

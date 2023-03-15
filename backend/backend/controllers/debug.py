from backend import app


@app.route("/ping")
def ping():
    return "pong!"

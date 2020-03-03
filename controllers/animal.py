from settings import app


@app.route('/hello')
def index():
    return "Hello, World!"

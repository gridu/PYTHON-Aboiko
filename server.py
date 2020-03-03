# Local modules
import config

app = config.app

if __name__ == "__main__":
    app.run(debug=True)


@app.route('/index')
def index():
    return "Hello, World!"

# app.run(port=5000)

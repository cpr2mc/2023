from app import app
from flask import render_template

@app.route('/')
def indext():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)


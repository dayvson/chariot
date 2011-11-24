from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template

app = Flask(__name__)

@app.route("/")
def direction():
    return "Hello world!"

if __name__ == '__main__':
    app.run()

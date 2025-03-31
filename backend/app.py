from flask import Flask

app = Flask(__name__)

counter = 0

@app.route('/')
def hello_world():  # put application's code here
    global counter
    counter = counter + 1
    return 'Hello World! ' + str(counter)

@app.route('/hello')
def hello_world1():  # put application's code here
    return 'Hello World 2!'

if __name__ == '__main__':
    app.run()

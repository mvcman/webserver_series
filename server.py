from flask import Flask

app = Flask('flaskapp')

@app.route('/')
def main():
    return "Hello World"

if __name__ == '__main__':
    print('name of the app {0}'.format(__name__))
    app.run('localhost', 8000)
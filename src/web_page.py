# go to http://localhost:8080/hello after execution Ctr-C

from bottle import route, run

@route('/hello')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
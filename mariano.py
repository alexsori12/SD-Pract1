from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World"
@app.route('/<name>')
def openFile(name):
    #return("Trying {}!".format(name))
    try:
        f = open("{}".format(name),'r') 
        lines=f.read()
        f.close
        return(lines)
    except Exception:
        print("F")
app.run(port=8000)
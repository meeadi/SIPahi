from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "SIPahi Flask Server is running."

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask
app=Flask(__name__)

@app.route("/routetanpaslash")
def tanpaslash():
    return '<h1>Route tanpa slash</h1>'

@app.route("/routeslash/")
def pakeslash():
    return '<h1>Route dengan slash</h1>'

#set debugging
if __name__ == "__main__":
    app.run(debug=True)
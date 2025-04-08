from flask import Flask
app=Flask(__name__)

#penerapan html escape
from markupsafe import escape
#from flask import escape --- ini ternyata udah gabisa

@app.route("/htmlescape/<code>")
def htmlescape(code):
    return escape(code)

#mendeklarasikan sebuah string, apakah bisa dihandle oleh escape
@app.route("/escape/<code>")
def process_escape(code):
    mystring="%@^&@*(#(918282))"
    return escape(mystring)

#set debugging
if __name__ == "__main__":
    app.run(debug=True)

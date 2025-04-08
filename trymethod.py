from flask import Flask, request

#import modul request
from flask import request

app=Flask(__name__)

@app.route("/cobarequest", methods=['GET', 'POST'])
def cobarequest():
    if request.method == 'GET':
        #return '<h1>coba GET</h1>'
        #coba get pake parameter yakni name dan value bitus
        return request.args.get("nama") + request.args.get("alamat")
    elif request.method == 'POST':
        #return '<h1>coba GET</h1>'
        #mendapatkan argumen dari method post, key=nama
        return request.form["alamat"] + request.form["nama"]
        
#set debugging
if __name__ == "__main__":
    app.run(debug=True)
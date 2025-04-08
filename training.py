from flask import Flask
from flask import render_template

#inisialisasi 
app = Flask(__name__)

#route mengarahkan ke halaman yang kita bikin
@app.route('/coba')

#function bernama hello_world
def hello_world():
    return 'Hello Worlddddd'

#percobaan lain
@app.route('/coba/<username>')
def coba(username):
    return '<h1>Hello %s!</h1>' % username

#jika tdk diberi ket, maka lgsg dianggap string
@app.route('/tipedata/<int:nilai>')
def tipedata(nilai):
    nilai = nilai
    return '<h1>Hello %s!</h1>' % nilai


#versi, beda route tapi satu fungsi
#karna diinisliasi integer maka setting default
@app.route('/tipe',defaults={'nilai':'0'})
@app.route('/tipe/<int:nilai>')
def tipe_data(nilai):
    nilai = nilai
    return '<h1>Hello %s!</h1>' % nilai

#sama kayak atas, tapi ini ver untuk mengetahui posisi routing
@app.route('/tipee',defaults={'_route':"home",'nilai':'0'})
@app.route('/tipee/<int:nilai>',defaults={'_route':"tipe"})
def tipe(nilai, _route):
    if _route=='home':
        return '<h1>hello !</h1>'
    elif _route=='tipe':
        nilai = nilai+50
        return '<h1>Hello %s!</h1>' % nilai
    
#menggunakan render html
@app.route('/')
def tryrender():
    #membuat variabel 
    mytype = ["Jungkook", "Taehyung", "Mohan"]
    
    #membuat dalam bentuk dictionary
    mydictionary = {"nama":"Nabilatus", "alamat":"Jakarta", "usia":"22"}
    
    #coba parsing data 
    return render_template('index.html', nama="Nabilatus", umur=22, types=mytype, dics=mydictionary)


#set debugging
if __name__ == "__main__":
    app.run(debug=True)






#from flask import Flask
#inisialisasi 
#hello = Flask(__name__)

#route mengarahkan ke halaman yang kita bikin
#@hello.route('/')

#function bernama hello_world
#def hello_world():
#    return 'Hello Worlddddd'

#set debugging
#if __name__ == "__main__":
#   hello.run(debug=True)
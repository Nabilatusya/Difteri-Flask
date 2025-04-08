# Menggunakan modul 'requests' yang benar
import requests  

# Data yang akan dikirim
mydata = {"alamat": "SIDARJOOO", "nama": "NABILATUSSSS"}

# Menggunakan method POST untuk mengirim data
req = requests.post("http://127.0.0.1:5000/cobarequest", data=mydata)

# Menampilkan response dari server
print(req.text)

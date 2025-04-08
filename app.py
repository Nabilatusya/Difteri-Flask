from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Untuk memungkinkan akses dari frontend (Laravel)
from models import db, DataDifteri, Tahun  # Import models
from clustering import perform_clustering  # Import fungsi clustering

# Inisialisasi Flask App
app = Flask(__name__)
app.config.from_object('config.Config')  # Load konfigurasi dari config.py

# Inisialisasi database dengan Flask App
db.init_app(app)

# Aktifkan CORS agar bisa diakses oleh frontend (misalnya Laravel)
CORS(app)

# Membuat tabel saat aplikasi pertama kali dijalankan
def create_tables():
    with app.app_context():
        db.create_all()
        print("Tabel berhasil dibuat atau sudah ada.")

# ✅ Perbaikan pada `/cluster_all`
@app.route('/cluster_all', methods=['GET'])
def cluster_all():
    try:
        db.session.expire_all()  # 🔄 Pastikan data terbaru diambil

        # Ambil semua tahun yang ada di database
        years = Tahun.query.with_entities(Tahun.tahun_kejadian).distinct().all()
        years = [int(y[0]) for y in years]  # Pastikan dalam bentuk integer
        
        print(f"Debug - List Tahun dari DB: {years}")

        # ✅ Definisikan dictionary sebelum digunakan
        clustering_data = {}

        # Untuk setiap tahun, panggil fungsi perform_clustering
        for year in years:
            print(f"Debug - Kirim Tahun ke perform_clustering: {year}")
            clustering_data[year] = perform_clustering(year)  # Panggil fungsi clustering

        return jsonify(clustering_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Jalankan aplikasi jika file ini dieksekusi langsung
if __name__ == '__main__':
    create_tables()  # Pastikan tabel dibuat sebelum server dijalankan
    app.run(debug=True, host='0.0.0.0', port=5000)  # Bisa diakses secara lokal dan jaringan

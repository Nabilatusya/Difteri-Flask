import numpy as np
from sklearn_extra.cluster import KMedoids
from sklearn.preprocessing import MinMaxScaler
from models import db, DataDifteri, Tahun  # Import model Tahun

def perform_clustering(year):
    try:
        year = int(year)  # 🔄 Pastikan year dalam bentuk integer
        print(f"Debug - Diterima year di perform_clustering: {year} ({type(year)})")

        # Pastikan year ada di database
        tahun = Tahun.query.filter_by(tahun_kejadian=year).first()
        print(f"Debug - Cek Tahun: {tahun}")  # Debugging untuk melihat tahun
        
        if not tahun:
            return {"message": f"Tahun {year} tidak ditemukan di database"}
        
        # 2. Ambil data berdasarkan id_tahun
        data = DataDifteri.query.filter_by(id_tahun=tahun.id_tahun).all()
        print(f"Debug - ID Tahun ditemukan: {tahun.id_tahun}")
        print(f"Debug - Jumlah DataDifteri ditemukan: {len(data)}")
        
        if not data:
            return {"message": f"Data tidak ditemukan untuk tahun {year}"}

        # 3. Ambil fitur yang akan digunakan untuk clustering
        X = np.array([[d.jml_kepadatan, d.jml_rumah_tidak_sehat, d.jml_vaksinasi_dpt, d.jml_kasus_difteri] for d in data])

        # 4. Cek apakah ada variasi dalam data sebelum normalisasi
        if np.all(X == X[0]):
            return {"error": "Data untuk clustering tidak memiliki variasi"}

        # 5. Normalisasi data
        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)

        # 6. Pastikan jumlah data cukup untuk clustering
        if X_scaled.shape[0] < 3:
            return {"error": "Data tidak cukup untuk clustering (minimal 3 data)"}

        try:
            # 7. Clustering dengan K-Medoids
            kmedoids = KMedoids(n_clusters=3, metric="euclidean", random_state=42)
            labels = kmedoids.fit_predict(X_scaled)
            medoids = kmedoids.medoid_indices_

            # 8. Urutkan cluster berdasarkan nilai rata-rata medoid
            sorted_clusters = np.argsort([np.mean(X_scaled[idx].tolist()) for idx in medoids])

            # 9. Mapping cluster ke kategori risiko
            cluster_mapping = {
                sorted_clusters[0]: "Kerawanan Rendah",
                sorted_clusters[1]: "Kerawanan Sedang",
                sorted_clusters[2]: "Kerawanan Tinggi"
            }

            # 10. Simpan hasil clustering ke database
            for i, d in enumerate(data):
                d.cluster = cluster_mapping[labels[i]]

            db.session.commit()

            return [{"nama_kecamatan": d.kecamatan.nama_kecamatan, "cluster": d.cluster} for d in data]
        
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}

    except ValueError:
        return {"error": "Tahun harus berupa angka"}
    except Exception as e:
        return {"error": str(e)}

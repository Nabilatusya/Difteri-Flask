import numpy as np
from sklearn_extra.cluster import KMedoids
from sklearn.preprocessing import MinMaxScaler
from models import db, DataDifteri, Tahun

def perform_clustering(year):
    try:
        year = int(year)
        print(f"Debug - Diterima year di perform_clustering: {year} ({type(year)})")

        tahun = Tahun.query.filter_by(tahun_kejadian=year).first()
        print(f"Debug - Cek Tahun: {tahun}")

        if not tahun:
            return {"message": f"Tahun {year} tidak ditemukan di database"}

        data = DataDifteri.query.filter_by(id_tahun=tahun.id_tahun).all()
        print(f"Debug - ID Tahun ditemukan: {tahun.id_tahun}")
        print(f"Debug - Jumlah DataDifteri ditemukan: {len(data)}")

        if not data:
            return {"message": f"Data tidak ditemukan untuk tahun {year}"}

        # Ambil fitur yang akan digunakan untuk clustering
        X = np.array([
            [d.jml_kepadatan, d.jml_rumah_tidak_sehat, d.jml_vaksinasi_dpt, d.jml_kasus_difteri]
            for d in data
        ], dtype=float)

        if np.all(X == X[0]):
            return {"error": "Data untuk clustering tidak memiliki variasi"}

        # Normalisasi dengan logika SAW (Benefit = semakin besar semakin rawan, Cost = semakin besar semakin baik)
        cost_idx = [2]  # jml_vaksinasi_dpt
        benefit_idx = [0, 1, 3]  # lainnya

        X_saw = np.zeros_like(X, dtype=float)

        for i in range(X.shape[1]):
            col = X[:, i]
            if i in benefit_idx:
                X_saw[:, i] = col / np.max(col) if np.max(col) != 0 else 0
            elif i in cost_idx:
                X_saw[:, i] = np.min(col) / col
                X_saw[:, i][~np.isfinite(X_saw[:, i])] = 0  # handle NaN & inf

        # Normalisasi MinMaxScaler
        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X_saw)

        if X_scaled.shape[0] < 3:
            return {"error": "Data tidak cukup untuk clustering (minimal 3 data)"}

        try:
            kmedoids = KMedoids(n_clusters=3, metric="euclidean", random_state=42)
            labels = kmedoids.fit_predict(X_scaled)
            medoids = kmedoids.medoid_indices_

            sorted_clusters = np.argsort([np.mean(X_scaled[idx].tolist()) for idx in medoids])

            cluster_mapping = {
                sorted_clusters[0]: "Kerawanan Rendah",
                sorted_clusters[1]: "Kerawanan Sedang",
                sorted_clusters[2]: "Kerawanan Tinggi"
            }

            for i, d in enumerate(data):
                d.cluster = cluster_mapping[labels[i]]

            db.session.commit()

            return [{
                "nama_kecamatan": d.kecamatan.nama_kecamatan,
                "cluster": d.cluster
            } for d in data]

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}

    except ValueError:
        return {"error": "Tahun harus berupa angka"}
    except Exception as e:
        return {"error": str(e)}

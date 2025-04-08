from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Kelas Tahun
class Tahun(db.Model):
    __tablename__ = 'tahuns'
    id_tahun = db.Column(db.Integer, primary_key=True)
    tahun_kejadian = db.Column(db.Integer)

    # Relasi ke DataDifteri
    data_difteri = db.relationship('DataDifteri', backref='tahun', lazy=True)

# Kelas Kecamatan
class Kecamatan(db.Model):
    __tablename__ = 'kecamatans'
    id_kecamatan = db.Column(db.Integer, primary_key=True)
    nama_kecamatan = db.Column(db.String(255))

    # Relasi ke DataDifteri
    data_difteri = db.relationship('DataDifteri', backref='kecamatan', lazy=True)

# Kelas DataDifteri
class DataDifteri(db.Model):
    __tablename__ = 'data_difteri'
    id_data = db.Column(db.Integer, primary_key=True)
    id_tahun = db.Column(db.Integer, db.ForeignKey('tahuns.id_tahun'), nullable=False)
    id_kecamatan = db.Column(db.Integer, db.ForeignKey('kecamatans.id_kecamatan'), nullable=False)
    jml_kepadatan = db.Column(db.Integer)
    jml_rumah_tidak_sehat = db.Column(db.Integer)
    jml_vaksinasi_dpt = db.Column(db.Integer)
    jml_kasus_difteri = db.Column(db.Integer)
    cluster = db.Column(db.String(255))

    # Hapus ini karena `Kecamatan` sudah punya backref
    # kecamatan = db.relationship('Kecamatan', backref='data_difteri', lazy=True)


from sqlalchemy import Column, Integer, String, Date, Float, Boolean, ForeignKey, Enum, CheckConstraint
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app import db, app
import enum

class LoaiNguoiDung(enum.Enum):
    ADMIN = 1
    NHANVIEN = 2
    GIAOVIEN = 3

class NguoiDung(db.Model, UserMixin):
    __tablename__ = 'nguoidung'

    manguoidung = Column(Integer, primary_key=True, autoincrement=True)
    tennguoidung = Column(String(50), nullable=False)
    gioitinh = Column(String(10), nullable=False)
    email = Column(String(50), nullable=False)
    sodienthoai = Column(String(20), nullable=False)
    taikhoan = Column(String(50), nullable=False, unique=True)
    matkhau = Column(String(50), nullable=False)
    loainguoidung = Column(Enum(LoaiNguoiDung), nullable=False)

    giaoviens = relationship('GiaoVien', backref='nguoidung', lazy=False)
    nhanviens = relationship('NhanVien', backref='nguoidung', lazy=False)
    quantriviens = relationship('QuanTriVien', backref='nguoidung', lazy=False)

    def get_id(self):
        return self.manguoidung

    def __str__(self):
        return self.tennguoidung

class QuanTriVien(db.Model):
    __tablename__ = 'quantrivien'

    maquantrivien = Column(String(50), primary_key=True)
    manguoidung = Column(Integer, ForeignKey('nguoidung.manguoidung'), nullable=False)

class NhanVien(db.Model):
    __tablename__ = 'nhannvien'

    manhanvien = Column(String(50), primary_key=True)
    manguoidung = Column(Integer, ForeignKey('nguoidung.manguoidung'), nullable=False)

class GiaoVien(db.Model):
    __tablename__ = 'giaovien'

    magiaovien = Column(String(50), primary_key=True)
    mamonhoc = Column(String(50), ForeignKey('monhoc.mamonhoc'), nullable=False)
    manguoidung = Column(Integer, ForeignKey('nguoidung.manguoidung'), nullable=False)

    phancongs = relationship('PhanCong', backref='giaovien', lazy=False)

    def __str__(self):
        return self.magiaovien

class QuyDinh(db.Model):
    __tablename__ = 'quydinh'

    maquydinh = Column(String(50), primary_key=True)
    tenquydinh = Column(String(50), nullable=False)
    giatri = Column(Integer, nullable=False)

    def __str__(self):
        return self.tenquydinh

class HocSinh(db.Model):
    __tablename__ = 'hocsinh'

    mahocsinh = Column(String(50), primary_key=True)
    tenhocsinh = Column(String(50), nullable=False)
    ngaysinh = Column(Date, nullable=False)
    gioitinh = Column(String(10), nullable=False)
    email = Column(String(50), nullable=False)
    sodienthoai = Column(String(20), nullable=False)
    diachi = Column(String(100), nullable=False)

    phanlops = relationship('PhanLop', backref='hocsinh', lazy=False)

    def __str__(self):
        return self.tenhocsinh

class KhoiLop(db.Model):
    __tablename__ = 'khoilop'

    makhoilop = Column(String(50), primary_key=True)
    tenkhoilop = Column(String(50), nullable=False)

    lops = relationship('Lop', backref='khoilop', lazy=False)

    def __str__(self):
        return self.tenkhoilop

class NamHoc(db.Model):
    __tablename__ = 'namhoc'
    manamhoc = Column(String(50), primary_key=True)
    tennamhoc = Column(String(20), nullable=False)

    lops = relationship('Lop', backref='namhoc', lazy=False)
    phanloplops = relationship('PhanLop', backref='namhoc', lazy=False)

    def __str__(self):
        return self.tennamhoc

class HocKy(db.Model):
    __tablename__ = 'hocky'

    mahocky = Column(String(50), primary_key=True)
    tenhocky = Column(String(20), nullable=False)

    diems = relationship('Diem', backref='hocky', lazy=False)

    def __str__(self):
        return self.tenhocky

class MonHoc(db.Model):
    __tablename__ = 'monhoc'

    mamonhoc = Column(String(50), primary_key=True)
    tenmonhoc = Column(String(50), nullable=False)

    diems = relationship('Diem', backref='monhoc', lazy=False)
    giaoviens = relationship('GiaoVien', backref='monhoc', lazy=False)

    def __str__(self):
        return self.tenmonhoc

class Lop(db.Model):
    __tablename__ = 'lop'

    malop = Column(String(50), primary_key=True)
    tenlop = Column(String(50), nullable=False)
    siso = Column(Integer, default=0)
    manamhoc = Column(String(50), ForeignKey('namhoc.manamhoc'), nullable=False)
    makhoilop = Column(String(50), ForeignKey('khoilop.makhoilop'), nullable=False)
    magiaovien = Column(String(50), ForeignKey('giaovien.magiaovien'), nullable=False)

    phanlops = relationship('PhanLop', backref='lop', lazy=False)
    phancongs = relationship('PhanCong', backref='lop', lazy=False)

    def __str__(self):
        return self.malop

class PhanLop(db.Model):
    __tablename__ = 'phanlop'

    maphanlop = Column(Integer, primary_key=True, autoincrement=True)
    malop = Column(String(50), ForeignKey('lop.malop'), nullable=False)
    mahocsinh = Column(String(50), ForeignKey('hocsinh.mahocsinh'), nullable=False)
    manamhoc = Column(String(50), ForeignKey('namhoc.manamhoc'), nullable=False)

class PhanCong(db.Model):
    __tablename__ = 'phancong'

    maphancong = Column(Integer, primary_key=True, autoincrement=True)
    malop = Column(String(50), ForeignKey('lop.malop'), nullable=False)
    magiaovien = Column(String(50), ForeignKey('giaovien.magiaovien'), nullable=False)

class LoaiDiem(db.Model):
    __tablename__ = 'loaidiem'

    maloaidiem = Column(Integer, primary_key=True, autoincrement=True)
    tenloaidiem = Column(String(50), nullable=False)

    diems = relationship('Diem', backref='loaidiem', lazy=False)

    def __str__(self):
        return self.tenloaidiem

class Diem(db.Model):
    __tablename__ = 'diem'

    madiem = Column(Integer, primary_key=True, autoincrement=True)
    maphanlop = Column(Integer, ForeignKey('phanlop.maphanlop'), nullable=False)
    mamonhoc = Column(String(50), ForeignKey('monhoc.mamonhoc'), nullable=False)
    mahocky = Column(String(50), ForeignKey('hocky.mahocky'), nullable=False)
    maloaidiem = Column(Integer, ForeignKey('loaidiem.maloaidiem'), nullable=False)
    diem = Column(Float, CheckConstraint('diem >= 0 AND diem <= 10'), nullable=False)

class BangDiemMon(db.Model):
    __tablename__ = 'bangdiemmon'

    stt = Column(Integer, primary_key=True)
    hoten = Column(String(50))
    lop = Column(String(50))
    monhoc = Column(String(50))
    hocky = Column(String(50))
    namhoc = Column(String(50))
    diem15p = Column(String(50))
    diem1t = Column(String(50))
    diemthi = Column(String(50))
    diemtrungbinh = Column(Float)
    ketqua = Column(Boolean)

class BangDiemTrungBinh(db.Model):
    __tablename__ = 'bangdiemtrungbinh'

    stt = Column(Integer, primary_key=True)
    hoten = Column(String(50))
    lop = Column(String(50))
    monhoc = Column(String(50))
    namhoc = Column(String(50))
    diemtbhk1 = Column(Float)
    diemtbhk2 = Column(Float)
    diemtbcn = Column(Float)

class BangDiemLop(db.Model):
    __tablename__ = 'bangdiemlop'

    stt = Column(Integer, primary_key=True)
    hoten = Column(String(50))
    lop = Column(String(50))
    namhoc = Column(String(50))
    diemtbhk1 = Column(Float)
    diemtbhk2 = Column(Float)
    diemtbcn = Column(Float)

class TongKetMonHoc(db.Model):
    __tablename__ = 'tongketmonhoc'

    stt = Column(Integer, primary_key=True)
    lop = Column(String(50))
    monhoc = Column(String(50))
    hocky = Column(String(50))
    namhoc = Column(String(50))
    siso = Column(Integer)
    soluongdat = Column(Integer)
    tyle = Column(Float)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # import hashlib
        #
        # u1 = NguoiDung(tennguoidung='Quản trị viên', email='admin@example.com', gioitinh='Nam',
        #                sodienthoai='0123456789', taikhoan='admin', matkhau=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #                loainguoidung=LoaiNguoiDung.ADMIN)
        # u2 = NguoiDung(tennguoidung='Nhân viên', email='nhanvien@example.com', gioitinh='Nữ',
        #                sodienthoai='0987654321', taikhoan='nhanvien', matkhau=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #                loainguoidung=LoaiNguoiDung.NHANVIEN)
        # u3 = NguoiDung(tennguoidung='Giáo viên', email='giaovien@example.com', gioitinh='Nữ',
        #                sodienthoai='0765432198', taikhoan='giaovien', matkhau=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #                loainguoidung=LoaiNguoiDung.GIAOVIEN)
        # u4 = NguoiDung(tennguoidung='Nguyễn Văn L', email='nguyen.l@example.com', gioitinh='Nam',
        #                sodienthoai='0789456321', taikhoan='giaovien1', matkhau=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #                loainguoidung=LoaiNguoiDung.GIAOVIEN)
        # u5 = NguoiDung(tennguoidung='Phan Thị M', email='phan.m@example.com', gioitinh='Nữ',
        #                sodienthoai='0111222333', taikhoan='giaovien2', matkhau=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #                loainguoidung=LoaiNguoiDung.GIAOVIEN)
        # u6 = NguoiDung(tennguoidung='Trần Thị A', email='tran.a@example.com', gioitinh='Nữ',
        #                sodienthoai='0999888777', taikhoan='giaovien3', matkhau=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #                loainguoidung=LoaiNguoiDung.GIAOVIEN)
        # db.session.add(u1)
        # db.session.add(u2)
        # db.session.add(u3)
        # db.session.add(u4)
        # db.session.add(u5)
        # db.session.add(u6)
        # db.session.commit()
        #
        # qtv = QuanTriVien(maquantrivien='QTV01', manguoidung='1')
        # db.session.add(qtv)
        # db.session.commit()
        #
        # nv = NhanVien(manhanvien='NV01', manguoidung='2')
        # db.session.add(nv)
        # db.session.commit()
        #
        # qd1 = QuyDinh(maquydinh='QD01', tenquydinh='Số tuổi tối thiểu khi tiếp nhận học sinh', giatri='15')
        # qd2 = QuyDinh(maquydinh='QD02', tenquydinh='Số tuổi tối đa khi tiếp nhận học sinh', giatri='20')
        # qd3 = QuyDinh(maquydinh='QD03', tenquydinh='Sĩ số tối đa của lớp học', giatri='40')
        # db.session.add(qd1)
        # db.session.add(qd2)
        # db.session.add(qd3)
        # db.session.commit()
        #
        # hk1 = HocKy(mahocky='HK01', tenhocky='Học kỳ 1')
        # hk2 = HocKy(mahocky='HK02', tenhocky='Học kỳ 2')
        # db.session.add(hk1)
        # db.session.add(hk2)
        # db.session.commit()
        #
        # nh1 = NamHoc(manamhoc='NH2122', tennamhoc='2021-2022')
        # nh2 = NamHoc(manamhoc='NH2223', tennamhoc='2022-2023')
        # db.session.add(nh1)
        # db.session.add(nh2)
        # db.session.commit()
        #
        # kl1 = KhoiLop(makhoilop='K10', tenkhoilop='Khối 10')
        # kl2 = KhoiLop(makhoilop='K11', tenkhoilop='Khối 11')
        # kl3 = KhoiLop(makhoilop='K12', tenkhoilop='Khối 12')
        # db.session.add(kl1)
        # db.session.add(kl2)
        # db.session.add(kl3)
        # db.session.commit()
        #
        # mh1 = MonHoc(mamonhoc='MH01', tenmonhoc='Ngữ Văn')
        # mh2 = MonHoc(mamonhoc='MH02', tenmonhoc='Toán')
        # mh3 = MonHoc(mamonhoc='MH03', tenmonhoc='Ngoại ngữ')
        # mh4 = MonHoc(mamonhoc='MH04', tenmonhoc='Lịch sử')
        # mh5 = MonHoc(mamonhoc='MH05', tenmonhoc='Địa lí')
        # mh6 = MonHoc(mamonhoc='MH06', tenmonhoc='Vật lí')
        # mh7 = MonHoc(mamonhoc='MH07', tenmonhoc='Hóa học')
        # mh8 = MonHoc(mamonhoc='MH08', tenmonhoc='Sinh học')
        # mh9 = MonHoc(mamonhoc='MH09', tenmonhoc='Giáo dục công dân')
        # db.session.add_all([mh1, mh2, mh3, mh4, mh5, mh6, mh7, mh8, mh9])
        # db.session.commit()
        #
        # gv1 = GiaoVien(magiaovien='GV01', mamonhoc='MH01', manguoidung='4')
        # gv2 = GiaoVien(magiaovien='GV02', mamonhoc='MH02', manguoidung='5')
        # gv3 = GiaoVien(magiaovien='GV03', mamonhoc='MH03', manguoidung='6')
        # gv4 = GiaoVien(magiaovien='GV04', mamonhoc='MH04', manguoidung='3')
        # gv5 = GiaoVien(magiaovien='GV05', mamonhoc='MH05', manguoidung='3')
        # gv6 = GiaoVien(magiaovien='GV06', mamonhoc='MH06', manguoidung='3')
        # gv7 = GiaoVien(magiaovien='GV07', mamonhoc='MH07', manguoidung='3')
        # gv8 = GiaoVien(magiaovien='GV08', mamonhoc='MH08', manguoidung='3')
        # gv9 = GiaoVien(magiaovien='GV09', mamonhoc='MH09', manguoidung='3')
        # db.session.add_all([gv1, gv2, gv3, gv4, gv5, gv6, gv7, gv8, gv9])
        # db.session.commit()
        #
        # lh1 = Lop(malop='A1012122', tenlop='10A1', makhoilop='K10', manamhoc='NH2122', magiaovien='GV01')
        # lh2 = Lop(malop='A1112122', tenlop='11A1', makhoilop='K11', manamhoc='NH2122', magiaovien='GV02')
        # lh3 = Lop(malop='A1212122', tenlop='12A1', makhoilop='K12', manamhoc='NH2122', magiaovien='GV03')
        # lh4 = Lop(malop='A1022122', tenlop='10A2', makhoilop='K10', manamhoc='NH2122', magiaovien='GV04')
        # lh5 = Lop(malop='A1122122', tenlop='11A2', makhoilop='K11', manamhoc='NH2122', magiaovien='GV05')
        # lh6 = Lop(malop='A1222122', tenlop='12A2', makhoilop='K12', manamhoc='NH2122', magiaovien='GV06')
        # lh7 = Lop(malop='A1012223', tenlop='10A1', makhoilop='K10', manamhoc='NH2223', magiaovien='GV07')
        # lh8 = Lop(malop='A1112223', tenlop='11A1', makhoilop='K11', manamhoc='NH2223', magiaovien='GV08')
        # lh9 = Lop(malop='A1212223', tenlop='12A1', makhoilop='K12', manamhoc='NH2223', magiaovien='GV09')
        # db.session.add_all([lh1, lh2, lh3, lh4, lh5, lh6, lh7, lh8, lh9])
        # db.session.commit()
        #
        # ld1 = LoaiDiem(tenloaidiem='15 phút')
        # ld2 = LoaiDiem(tenloaidiem='1 tiết')
        # ld3 = LoaiDiem(tenloaidiem='Thi')
        # db.session.add(ld1)
        # db.session.add(ld2)
        # db.session.add(ld3)
        # db.session.commit()

        hs1 = HocSinh(mahocsinh='HS001', tenhocsinh='Nguyễn Văn A', ngaysinh='2005-05-02', gioitinh='Nam',
                      email='van.a@example.com', sodienthoai='0987654321', diachi='23 Đường ABC, Quận 1, TP.HCM')
        hs2 = HocSinh(mahocsinh='HS002', tenhocsinh='Trần Thị B', ngaysinh='2005-08-10', gioitinh='Nữ',
                      email='thi.b@example.com', sodienthoai='0901234567', diachi='456 Đường XYZ, Quận 2, TP.HCM')
        hs3 = HocSinh(mahocsinh='HS003', tenhocsinh='Lê Minh C', ngaysinh='2005-04-15', gioitinh='Nam',
                      email='minh.c@example.com', sodienthoai='0978123456', diachi='789 Đường PQR, Quận 3, TP.HCM')
        hs4 = HocSinh(mahocsinh='HS004', tenhocsinh='Phạm Thị D', ngaysinh='2005-12-20', gioitinh='Nữ',
                      email='thi.d@example.com', sodienthoai='0912345678', diachi='101 Đường LMN, Quận 4, TP.HCM')
        hs5 = HocSinh(mahocsinh='HS005', tenhocsinh='Võ Văn E', ngaysinh='2005-06-25', gioitinh='Nam',
                      email='van.e@example.com', sodienthoai='0999888777', diachi='202 Đường UVW, Quận 5, TP.HCM')
        hs6 = HocSinh(mahocsinh='HS006', tenhocsinh='Mai Thị F', ngaysinh='2006-09-03', gioitinh='Nữ',
                      email='thi.f@example.com', sodienthoai='0888777666', diachi='303 Đường XYZ, Quận 6, TP.HCM')
        hs7 = HocSinh(mahocsinh='HS007', tenhocsinh='Hoàng Văn G', ngaysinh='2006-01-14', gioitinh='Nam',
                      email='van.g@example.com', sodienthoai='0777666555', diachi='404 Đường ABC, Quận 7, TP.HCM')
        hs8 = HocSinh(mahocsinh='HS008', tenhocsinh='Nguyễn Thị H', ngaysinh='2006-05-30', gioitinh='Nữ',
                      email='thi.h@example.com', sodienthoai='0666555444', diachi='505 Đường PQR, Quận 8, TP.HCM')
        hs9 = HocSinh(mahocsinh='HS009', tenhocsinh='Trần Văn I', ngaysinh='2006-11-12', gioitinh='Nam',
                      email='van.i@example.com', sodienthoai='0555444333', diachi='606 Đường LMN, Quận 9, TP.HCM')
        hs10 = HocSinh(mahocsinh='HS010', tenhocsinh='Lê Thị K', ngaysinh='2006-07-08', gioitinh='Nữ',
                       email='thi.k@example.com', sodienthoai='0444333222', diachi='707 Đường UVW, Quận 10, TP.HCM')
        db.session.add_all([hs1, hs2, hs3, hs4, hs5, hs6, hs7, hs8, hs9, hs10])
        db.session.commit()

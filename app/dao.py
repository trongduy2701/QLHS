from sqlalchemy import func, case, and_
from app.models import NguoiDung, LoaiNguoiDung, HocSinh, QuyDinh, Lop, NamHoc, HocKy, PhanLop, KhoiLop, MonHoc, Diem, \
    LoaiDiem, BangDiemMon, BangDiemLop, TongKetMonHoc, BangDiemTrungBinh
from app import db
import hashlib

def get_user_by_id(user_id):
    return NguoiDung.query.get(user_id)

def authenticate_user(taikhoan, matkhau, loainguoidung=None):
    matkhau = hash_password(matkhau)

    if loainguoidung == LoaiNguoiDung.ADMIN:
        return NguoiDung.query.filter(NguoiDung.taikhoan == taikhoan, NguoiDung.matkhau == matkhau, NguoiDung.loainguoidung == loainguoidung).first()
    else:
        return NguoiDung.query.filter(NguoiDung.taikhoan == taikhoan, NguoiDung.matkhau == matkhau).first()

def update_password(user, new_password):
    user.matkhau = hash_password(new_password)
    db.session.commit()

def hash_password(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()

def verify_password(stored_password, provided_password):
    return stored_password == hash_password(provided_password)

def get_quydinh(maquydinh):
    return QuyDinh.query.get(maquydinh)

def update_quydinh(quydinh):
    db.session.commit()

def get_all_quydinhs():
    return QuyDinh.query.all()

def get_monhoc(mamonhoc):
    return MonHoc.query.get(mamonhoc)

def add_monhoc(monhoc):
    db.session.add(monhoc)
    db.session.commit()

def update_monhoc(monhoc):
    db.session.commit()

def delete_monhoc(monhoc):
    db.session.delete(monhoc)
    db.session.commit()

def get_paginated_monhoc(page, per_page):
    return MonHoc.query.paginate(page=page, per_page=per_page, error_out=False)

def get_all_hocsinhs():
    return HocSinh.query.all()

def get_hocsinh_chua_phanlop():
    hocsinhs = db.session.query(HocSinh).\
        outerjoin(PhanLop, HocSinh.mahocsinh == PhanLop.mahocsinh).\
        filter(PhanLop.mahocsinh.is_(None)).all()
    return hocsinhs

def get_hocsinh(mahocsinh):
    return HocSinh.query.get(mahocsinh)

def add_hocsinh(hocsinh):
    db.session.add(hocsinh)
    db.session.commit()

def update_hocsinh(hocsinh):
    db.session.commit()

def delete_hocsinh(hocsinh):
    db.session.delete(hocsinh)
    db.session.commit()

def get_check_class(mahocsinh):
    check_class = (db.session.query(HocSinh.mahocsinh, PhanLop.maphanlop)
                   .join(PhanLop)
                   .filter(HocSinh.mahocsinh == mahocsinh)
                   .first())
    return check_class
def get_paginated_hocsinh(page, per_page):
    return HocSinh.query.paginate(page=page, per_page=per_page, error_out=False)

def get_all_namhocs():
    return NamHoc.query.all()

def get_all_khoilops():
    return KhoiLop.query.all()

def get_all_monhocs():
    return MonHoc.query.all()

def get_all_hockys():
    return HocKy.query.all()

def get_all_loaidiems():
    return LoaiDiem.query.all()

def get_all_lops():
    return Lop.query.all()

def get_lop_namhoc_khoi(namhoc, khoilop):
    return db.session.query(Lop).filter(Lop.manamhoc == namhoc, Lop.makhoilop == khoilop).all()

def get_danh_sach_lop(lop):
    students = db.session.query(HocSinh).join(PhanLop).filter(PhanLop.malop == lop).all()
    return students

def update_siso():
    classes = db.session.query(Lop).all()
    for lop in classes:
        siso = db.session.query(PhanLop).filter(PhanLop.malop == lop.malop).count()
        lop.siso = siso
    db.session.commit()

def get_ten_lop(malop):
    class_name = db.session.query(Lop).filter(Lop.malop == malop).first()
    return class_name

def get_all_phanlops():
    return PhanLop.query.all()

def get_paginated_phanlop(page, per_page):
    return PhanLop.query.paginate(page=page, per_page=per_page, error_out=False)

def get_phanlop(maphanlop):
    return PhanLop.query.get(maphanlop)

def add_phanlop(phanlop):
    db.session.add(phanlop)
    db.session.commit()

def update_phanlop(phanlop):
    db.session.commit()

def delete_phanlop(phanlop):
    db.session.delete(phanlop)
    db.session.commit()

def get_existing_class(hocsinh, namhoc):
    existing_class = (db.session.query(PhanLop).filter(
        PhanLop.mahocsinh == hocsinh,
        PhanLop.manamhoc == namhoc,
    ).first())
    return existing_class

def get_diem(stt):
    return Diem.query.get(stt)

def add_diem(diem):
    db.session.add(diem)
    db.session.commit()

def update_diem(diem):
    db.session.commit()

def delete_diem(diem):
    db.session.delete(diem)
    db.session.commit()

def get_paginated_diem(page, per_page):
    return Diem.query.paginate(page=page, per_page=per_page, error_out=False)

def count_so_cot_diem(maphanlop, mamonhoc, mahocky, maloaidiem):
    so_cot_diem = db.session.query(
        func.count(Diem.maloaidiem).label('giatri')
    ).filter(
        Diem.maphanlop == maphanlop,
        Diem.mamonhoc == mamonhoc,
        Diem.mahocky == mahocky,
        Diem.maloaidiem == maloaidiem
    ).scalar()
    return so_cot_diem

def update_bang_diem_mon():
    query = (
        db.session.query(
            HocSinh.tenhocsinh,
            Lop.tenlop,
            NamHoc.tennamhoc,
            HocKy.tenhocky,
            MonHoc.tenmonhoc,
            func.group_concat(case((Diem.maloaidiem == 1, Diem.diem))).label('diem15p'),
            func.group_concat(case((Diem.maloaidiem == 2, Diem.diem))).label('diem1t'),
            func.group_concat(case((Diem.maloaidiem == 3, Diem.diem))).label('diemthi'),
            func.round((func.avg(case((Diem.maloaidiem == 1, Diem.diem))) + (func.avg(case((Diem.maloaidiem == 2, Diem.diem)))*2) + (func.avg(case((Diem.maloaidiem == 3, Diem.diem))))*3)/6, 2).label('diemtrungbinh')
        )
        .join(PhanLop, HocSinh.mahocsinh == PhanLop.mahocsinh)
        .join(Lop, PhanLop.malop == Lop.malop)
        .join(NamHoc, NamHoc.manamhoc == Lop.manamhoc)
        .join(Diem, PhanLop.maphanlop == Diem.maphanlop)
        .join(MonHoc, MonHoc.mamonhoc == Diem.mamonhoc)
        .join(HocKy, HocKy.mahocky == Diem.mahocky)
        .group_by(
            Diem.maphanlop,
            Diem.mamonhoc,
            Diem.mahocky
        )
    )

    for result in query:
        hoten, tenlop, tennamhoc, tenhocky, tenmonhoc, diem15p, diem1t, diemthi, diemtrungbinh = result

        diem15p_formatted = ', '.join(str(x) for x in diem15p.split(',')) if diem15p else None
        diem1t_formatted = ', '.join(str(x) for x in diem1t.split(',')) if diem1t else None
        diemthi_formatted = ', '.join(str(x) for x in diemthi.split(',')) if diemthi else None

        existing_record = (
            db.session.query(BangDiemMon)
            .filter(
                BangDiemMon.hoten == hoten,
                BangDiemMon.lop == tenlop,
                BangDiemMon.namhoc == tennamhoc,
                BangDiemMon.hocky == tenhocky,
                BangDiemMon.monhoc == tenmonhoc
            )
            .first()
        )

        if existing_record:
            existing_record.diem15p = diem15p_formatted
            existing_record.diem1t = diem1t_formatted
            existing_record.diemthi = diemthi_formatted
            existing_record.diemtrungbinh = diemtrungbinh
        else:
            new_bangdiem = BangDiemMon(
                hoten=hoten,
                lop=tenlop,
                namhoc=tennamhoc,
                hocky=tenhocky,
                monhoc=tenmonhoc,
                diem15p=diem15p_formatted,
                diem1t=diem1t_formatted,
                diemthi=diemthi_formatted,
                diemtrungbinh=diemtrungbinh
            )
            db.session.add(new_bangdiem)
    db.session.commit()

def get_bang_diem_mon(lop, namhoc, hocky, monhoc):
    results = db.session.query(BangDiemMon).filter(
        BangDiemMon.lop == lop,
        BangDiemMon.namhoc == namhoc,
        BangDiemMon.hocky == hocky,
        BangDiemMon.monhoc == monhoc
    ).all()
    return results

def get_lop_bang_diem_mon():
    return db.session.query(BangDiemMon.lop).distinct().all()

def get_namhoc_bang_diem_mon():
    return db.session.query(BangDiemMon.namhoc).distinct().all()

def get_hocky_bang_diem_mon():
    return db.session.query(BangDiemMon.hocky).distinct().all()

def get_monhoc_bang_diem_mon():
    return db.session.query(BangDiemMon.monhoc).distinct().all()

def tinh_ket_qua():
    bang_diem_list = db.session.query(BangDiemMon).all()
    for bang_diem in bang_diem_list:
        if bang_diem.diemtrungbinh is not None:
            bang_diem.ketqua = bang_diem.diemtrungbinh >= 5
        else:
            bang_diem.ketqua = False
    db.session.commit()

def update_bang_diem_trung_binh():
    query = (
        db.session.query(
            BangDiemMon.hoten,
            BangDiemMon.lop,
            BangDiemMon.namhoc,
            BangDiemMon.monhoc,
            func.max(case((BangDiemMon.hocky == 'Học kỳ 1', BangDiemMon.diemtrungbinh))).label('diemtbhk1'),
            func.max(case((BangDiemMon.hocky == 'Học kỳ 2', BangDiemMon.diemtrungbinh))).label('diemtbhk2'),
            func.round((func.max(case((BangDiemMon.hocky == 'Học kỳ 1', BangDiemMon.diemtrungbinh))) + func.max(case((BangDiemMon.hocky == 'Học kỳ 2', BangDiemMon.diemtrungbinh))))/2, 2).label('diemtbcn')
        )
        .group_by(
            BangDiemMon.hoten,
            BangDiemMon.monhoc,
            BangDiemMon.lop,
            BangDiemMon.namhoc
        )
    )

    for result in query:
        hoten, lop, namhoc, monhoc, diemtbhk1, diemtbhk2, diemtbcn = result

        existing_record = (
            db.session.query(BangDiemTrungBinh)
            .filter(
                BangDiemTrungBinh.hoten == hoten,
                BangDiemTrungBinh.lop == lop,
                BangDiemTrungBinh.namhoc == namhoc,
                BangDiemTrungBinh.monhoc == monhoc
            )
            .first()
        )

        if existing_record:
            existing_record.diemtbhk1 = diemtbhk1
            existing_record.diemtbhk2 = diemtbhk2
            existing_record.diemtbcn = diemtbcn
        else:
            new_bangdiem = BangDiemTrungBinh(
                hoten=hoten,
                lop=lop,
                namhoc=namhoc,
                monhoc=monhoc,
                diemtbhk1=diemtbhk1,
                diemtbhk2=diemtbhk2,
                diemtbcn=diemtbcn
            )
            db.session.add(new_bangdiem)
    db.session.commit()

def get_bang_diem_trung_binh(lop, namhoc, monhoc):
    results = db.session.query(BangDiemTrungBinh).filter(
        BangDiemTrungBinh.lop == lop,
        BangDiemTrungBinh.namhoc == namhoc,
        BangDiemTrungBinh.monhoc == monhoc
    ).all()
    return results

def get_lop_bang_diem_trung_binh():
    return db.session.query(BangDiemTrungBinh.lop).distinct().all()

def get_namhoc_bang_diem_trung_binh():
    return db.session.query(BangDiemTrungBinh.namhoc).distinct().all()

def get_monhoc_bang_diem_trung_binh():
    return db.session.query(BangDiemTrungBinh.monhoc).distinct().all()

def update_bang_diem_lop():
    query = (
        db.session.query(
            BangDiemMon.hoten,
            BangDiemMon.lop,
            BangDiemMon.namhoc,
            func.round(func.avg(BangDiemTrungBinh.diemtbhk1).label('diemtbhk1'), 2),
            func.round(func.avg(BangDiemTrungBinh.diemtbhk2).label('diemtbhk2'), 2),
            func.round((func.avg(BangDiemTrungBinh.diemtbhk1).label('diemtbhk1') + func.avg(BangDiemTrungBinh.diemtbhk2).label('diemtbhk2')) / 2, 2).label('diemtbcn')
        )
        .join(
            BangDiemTrungBinh,
            and_(
                BangDiemTrungBinh.hoten == BangDiemMon.hoten,
                BangDiemTrungBinh.lop == BangDiemMon.lop,
                BangDiemTrungBinh.namhoc == BangDiemMon.namhoc
            )
        )
        .group_by(
            BangDiemMon.hoten,
            BangDiemMon.lop,
            BangDiemMon.namhoc
        )
    )

    for result in query:
        hoten, lop, namhoc, diemtbhk1, diemtbhk2, diemtbcn = result

        existing_record = (
            db.session.query(BangDiemLop)
            .filter(
                BangDiemLop.hoten == hoten,
                BangDiemLop.lop == lop,
                BangDiemLop.namhoc == namhoc,
            )
            .first()
        )

        if existing_record:
            existing_record.diemtbhk1 = diemtbhk1
            existing_record.diemtbhk2 = diemtbhk2
            existing_record.diemtbcn = diemtbcn
        else:
            new_bangdiem = BangDiemLop(
                hoten=hoten,
                lop=lop,
                namhoc=namhoc,
                diemtbhk1=diemtbhk1,
                diemtbhk2=diemtbhk2,
                diemtbcn=diemtbcn
            )
            db.session.add(new_bangdiem)
    db.session.commit()

def get_bang_diem_lop(lop, namhoc):
    results = db.session.query(BangDiemLop).filter(
        BangDiemLop.lop == lop,
        BangDiemLop.namhoc == namhoc,
    ).all()
    return results

def get_lop_bang_diem_lop():
    return db.session.query(BangDiemLop.lop).distinct().all()

def get_namhoc_bang_diem_lop():
    return db.session.query(BangDiemLop.namhoc).distinct().all()

def update_tong_ket_mon_hoc():
    query = (
        db.session.query(
            BangDiemMon.lop,
            BangDiemMon.monhoc,
            BangDiemMon.namhoc,
            BangDiemMon.hocky,
            func.sum(case(((BangDiemMon.ketqua == True, 1))).label('soluongdat'))
        )
        .group_by(BangDiemMon.lop, BangDiemMon.monhoc, BangDiemMon.namhoc, BangDiemMon.hocky)
    )

    for result in query.all():
        lop, monhoc, namhoc, hocky, soluongdat = result

        siso = (
            db.session.query(Lop.siso)
            .join(NamHoc, Lop.manamhoc == NamHoc.manamhoc)
            .filter(Lop.tenlop == lop, NamHoc.tennamhoc == namhoc)
            .scalar()
        )

        tyle = (soluongdat / siso) * 100 if siso != 0 and (soluongdat is not None and soluongdat != 0) else 0

        existing_record = (
            db.session.query(TongKetMonHoc)
            .filter(
                TongKetMonHoc.lop == lop,
                TongKetMonHoc.monhoc == monhoc,
                TongKetMonHoc.namhoc == namhoc,
                TongKetMonHoc.hocky == hocky)
            .first()
        )

        if existing_record:
            existing_record.soluongdat = soluongdat
            existing_record.siso = siso
            existing_record.tyle = tyle
        else:
            new_record = TongKetMonHoc(
                lop=lop, monhoc=monhoc, namhoc=namhoc, hocky=hocky, soluongdat=soluongdat, siso=siso, tyle=tyle
            )
            db.session.add(new_record)
    db.session.commit()

def get_baocao(namhoc, hocky, monhoc):
    results = db.session.query(TongKetMonHoc).filter(
        TongKetMonHoc.namhoc == namhoc,
        TongKetMonHoc.hocky == hocky,
        TongKetMonHoc.monhoc == monhoc
    ).all()
    return results

def get_namhoc_baocao():
    return db.session.query(TongKetMonHoc.namhoc).distinct().all()

def get_hocky_baocao():
    return db.session.query(TongKetMonHoc.hocky).distinct().all()

def get_monhoc_baocao():
    return db.session.query(TongKetMonHoc.monhoc).distinct().all()


def baocao_stats(monhoc=None, namhoc=None, hocky=None):
    results = db.session.query(TongKetMonHoc)
    if monhoc and namhoc and hocky:
        results = results.filter(
            TongKetMonHoc.namhoc == namhoc,
            TongKetMonHoc.hocky == hocky,
            TongKetMonHoc.monhoc == monhoc).all()
    return results
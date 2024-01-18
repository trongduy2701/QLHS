import json
from datetime import datetime
import csv
from app import app, login
import dao
from flask import render_template, redirect, request, flash, jsonify, send_file
from flask_login import login_user, logout_user, login_required, current_user
from app.models import LoaiNguoiDung, HocSinh, Diem, PhanLop, MonHoc


@app.route("/")
def home():
    dao.update_siso()
    dao.update_bang_diem_mon()
    dao.tinh_ket_qua()
    dao.update_bang_diem_trung_binh()
    dao.update_bang_diem_lop()
    dao.update_tong_ket_mon_hoc()
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        taikhoan = request.form.get('username')
        matkhau = request.form.get('password')

        nguoidung = dao.authenticate_user(taikhoan=taikhoan, matkhau=matkhau)

        if nguoidung:
            login_user(nguoidung)
            return redirect("/")
        else:
            flash('Đăng nhập thất bại. Vui lòng kiểm tra lại tài khoản và mật khẩu.', 'danger')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/admin-login', methods=['POST'])
def admin_login():
    taikhoan = request.form.get('username')
    matkhau = request.form.get('password')

    nguoidung = dao.authenticate_user(taikhoan=taikhoan, matkhau=matkhau, loainguoidung=LoaiNguoiDung.ADMIN)

    if nguoidung:
        login_user(nguoidung)
    else:
        flash('Đăng nhập thất bại. Bạn không có quyền truy cập.', 'danger')
        return redirect('/admin')
    return redirect('/admin')

@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/doi-mat-khau', methods=['GET', 'POST'])
def doi_mat_khau():
    if request.method == 'POST':
        matkhaucu = request.form.get('matkhaucu')
        matkhaumoi = request.form.get('matkhaumoi')

        if dao.verify_password(current_user.matkhau, matkhaucu):
            dao.update_password(current_user, matkhaumoi)
            logout_user()
            return redirect("/login")
        else:
            flash('Xác thực thất bại. Vui lòng kiểm tra lại mật khẩu cũ.', 'danger')
            return render_template('login.html')
    return render_template('doi-mat-khau.html')

@app.route('/profile')
@login_required
def profile():
    user_info = {
        'tennguoidung': current_user.tennguoidung,
        'gioitinh': current_user.gioitinh,
        'email': current_user.email,
        'sodienthoai': current_user.sodienthoai,
        'taikhoan': current_user.taikhoan,
    }
    return render_template('profile.html', user_info=user_info)

@app.route('/tiep-nhan', methods=['GET', 'POST'])
def tiep_nhan():
    if request.method == 'POST':
        tuoitoithieu = dao.get_quydinh('QD01')
        tuoitoida = dao.get_quydinh('QD02')

        ngaysinh = datetime.strptime(request.form['ngaysinh'], '%Y-%m-%d')
        namhientai = datetime.now().year
        tuoi = namhientai - ngaysinh.year

        if 'add' in request.form:
            if tuoitoithieu.giatri <= tuoi <= tuoitoida.giatri:
                mahocsinh = request.form.get('mahocsinh')
                tenhocsinh = request.form.get('tenhocsinh')
                ngaysinh = request.form.get('ngaysinh')
                gioitinh = request.form.get('gioitinh')
                diachi = request.form.get('diachi')
                sodienthoai = request.form.get('sodienthoai')
                email = request.form.get('email')

                hocsinh = HocSinh(mahocsinh=mahocsinh, tenhocsinh=tenhocsinh, ngaysinh=ngaysinh, gioitinh=gioitinh, diachi=diachi,
                                  sodienthoai=sodienthoai, email=email)

                dao.add_hocsinh(hocsinh)
                flash('Tiếp nhận học sinh thành công.', 'success')
            else:
                flash('Học sinh không đủ tuổi theo quy định.', 'danger')

        elif 'edit' in request.form:
            if tuoitoithieu.giatri <= tuoi <= tuoitoida.giatri:
                mahocsinh = request.form.get('mahocsinh')

                hocsinh = dao.get_hocsinh(mahocsinh)
                hocsinh.tenhocsinh = request.form.get('tenhocsinh')
                hocsinh.ngaysinh = request.form.get('ngaysinh')
                hocsinh.gioitinh = request.form.get('gioitinh')
                hocsinh.diachi = request.form.get('diachi')
                hocsinh.sodienthoai = request.form.get('sodienthoai')
                hocsinh.email = request.form.get('email')

                dao.update_hocsinh(hocsinh)
                flash('Sửa học sinh thành công.', 'success')
            else:
                flash('Học sinh không đủ tuổi theo quy định.', 'danger')

        elif 'delete' in request.form:
            mahocsinh = request.form.get('mahocsinh')
            hocsinh = dao.get_hocsinh(mahocsinh)

            check_class = dao.get_check_class(mahocsinh)
            if check_class is None:
                dao.delete_hocsinh(hocsinh)
                flash('Xóa học sinh thành công.', 'success')
            else:
                flash('Học sinh đã phân lớp.', 'success')

    page = request.args.get('page', 1, type=int)
    per_page = app.config['PAGE_SIZE']

    hocsinhs = dao.get_paginated_hocsinh(page, per_page)
    return render_template('tiep-nhan.html', hocsinhs=hocsinhs)

@app.route('/lap-danh-sach', methods=['GET', 'POST'])
def lap_danh_sach():
    if request.method == 'POST':
        lop = request.form.get('malop')
        students = dao.get_danh_sach_lop(lop)
        class_name = dao.get_ten_lop(lop)
        if 'export' in request.form:
            csv_file = f'danh_sach_{lop}.csv'
            with open(csv_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['Họ tên', 'Giới tính', 'Năm sinh', 'Địa chỉ']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for student in students:
                    writer.writerow({
                        'Họ tên': student.tenhocsinh,
                        'Giới tính': student.gioitinh,
                        'Năm sinh': student.ngaysinh.year,
                        'Địa chỉ': student.diachi
                    })
            return send_file(csv_file, as_attachment=True)
        return render_template('danh-sach-lop.html', students=students, class_name=class_name)

    namhocs = dao.get_all_namhocs()
    khoilops = dao.get_all_khoilops()
    return render_template('lap-danh-sach.html', namhocs=namhocs, khoilops=khoilops)

@app.route('/get_lop_nam_khoi', methods=['GET'])
def get_lop_nam_khoi():
    namhoc = request.args.get('manamhoc')
    khoilop = request.args.get('makhoilop')
    lops = dao.get_lop_namhoc_khoi(namhoc, khoilop)
    lops_data = [{'malop': lop.malop, 'tenlop': lop.tenlop} for lop in lops]
    return jsonify({'lops': lops_data})

@app.route('/dieu-chinh-lop', methods=['GET', 'POST'])
def dieu_chinh_lop():
    if request.method == 'POST':
        sisotoida = dao.get_quydinh('QD03')
        if 'add' in request.form:
            hocsinh = request.form.get('mahocsinh')
            lop = request.form.get('malop')
            namhoc = request.form.get('manamhoc')
            existing_class = dao.get_existing_class(hocsinh, namhoc)
            class_name = dao.get_ten_lop(lop)

            if class_name.siso <= sisotoida.giatri:
                if existing_class is None:
                    phanlop = PhanLop(mahocsinh=hocsinh, malop=lop, manamhoc=namhoc)

                    dao.add_phanlop(phanlop)
                    flash('Thêm học sinh vào lớp thành công.', 'success')
                else:
                    flash('Học sinh đã có lớp.', 'danger')
            else:
                flash('Sĩ số lớp đạt tối đa.', 'danger')

        elif 'edit' in request.form:
            maphanlop = request.form.get('maphanlop')
            phanlop = dao.get_phanlop(maphanlop)
            phanlop.mahocsinh = request.form.get('mahocsinh')
            phanlop.malop = request.form.get('malop')
            phanlop.manamhoc = request.form.get('manamhoc')
            class_name = dao.get_ten_lop(phanlop.malop)

            if class_name.siso <= sisotoida.giatri:
                dao.update_phanlop(phanlop)
                flash('Sửa lớp của học sinh thành công.', 'success')
            else:
                flash('Sĩ số lớp đạt tối đa.', 'danger')

        elif 'delete' in request.form:
            maphanlop = request.form.get('maphanlop')
            phanlop = dao.get_phanlop(maphanlop)

            dao.delete_phanlop(phanlop)
            flash('Xóa học sinh khỏi lớp thành công.', 'success')

    hocsinhs = dao.get_hocsinh_chua_phanlop()
    lops = dao.get_all_lops()
    namhocs = dao.get_all_namhocs()
    page = request.args.get('page', 1, type=int)
    per_page = app.config['PAGE_SIZE']
    phanlops = dao.get_paginated_phanlop(page, per_page)
    return render_template('dieu-chinh-lop.html', hocsinhs=hocsinhs, lops=lops, phanlops=phanlops, namhocs=namhocs)

@app.route('/nhap-diem', methods=['GET', 'POST'])
def nhap_diem():
    if request.method == 'POST':
        if 'add' in request.form:

            maphanlop = request.form.get('maphanlop')
            mamonhoc = request.form.get('mamonhoc')
            mahocky = request.form.get('mahocky')
            maloaidiem = request.form.get('maloaidiem')
            diem = request.form.get('diem')

            socotdiem = dao.count_so_cot_diem(maphanlop, mamonhoc, mahocky, maloaidiem)

            socottoida = 0
            if maloaidiem == '1':
                socottoida = 5
            elif maloaidiem == '2':
                socottoida = 3
            elif maloaidiem == '3':
                socottoida = 1
            if socotdiem < socottoida:
                diem = Diem(maphanlop=maphanlop, mamonhoc=mamonhoc, mahocky=mahocky, maloaidiem=maloaidiem, diem=diem)

                dao.add_diem(diem)
                flash('Nhập điểm thành công.', 'success')
            else:
                flash('Số cột điểm đạt tối đa.', 'danger')

        elif 'edit' in request.form:
            madiem = request.form.get('madiem')

            diem = dao.get_diem(madiem)
            diem.maphanlop = request.form.get('maphanlop')
            diem.mamonhoc = request.form.get('mamonhoc')
            diem.mahocky = request.form.get('mahocky')
            diem.maloaidiem = request.form.get('maloaidiem')
            diem.diem = request.form.get('diem')

            socotdiem = dao.count_so_cot_diem(diem.maphanlop,  diem.mamonhoc, diem.mahocky, diem.maloaidiem)

            socottoida = 0
            socottoithieu = 1
            if diem.maloaidiem == '1':
                socottoida = 5
            elif diem.maloaidiem == '2':
                diem.maloaidiem = 3
            elif diem.maloaidiem == '3':
                socottoida = 1

            if socottoithieu <= socotdiem < socottoida:
                dao.update_diem(diem)
                flash('Sửa điểm thành công.', 'success')
            elif socotdiem < socottoithieu:
                flash('Số cột điểm đạt tối thiểu.', 'danger')
            else:
                flash('Số cột điểm đạt tối đa.', 'danger')

        elif 'delete' in request.form:
            madiem = request.form.get('madiem')
            diem = dao.get_diem(madiem)
            diem.maphanlop = request.form.get('maphanlop')
            diem.mamonhoc = request.form.get('mamonhoc')
            diem.mahocky = request.form.get('mahocky')
            diem.maloaidiem = request.form.get('maloaidiem')

            socotdiem = dao.count_so_cot_diem(diem.maphanlop, diem.mamonhoc, diem.mahocky, diem.maloaidiem)
            socottoithieu = 1

            if socotdiem > socottoithieu:
                dao.delete_diem(diem)
                flash('Xóa điểm thành công.')
            else:
                flash('Số cột điểm đạt tối thiểu.')
    dao.update_bang_diem_mon()
    dao.tinh_ket_qua()
    dao.update_bang_diem_trung_binh()
    dao.update_bang_diem_lop()
    dao.update_tong_ket_mon_hoc()

    monhocs = dao.get_all_monhocs()
    hockys = dao.get_all_hockys()
    phanlops = dao.get_all_phanlops()
    loaidiems = dao.get_all_loaidiems()

    page = request.args.get('page', 1, type=int)
    per_page = app.config['PAGE_SIZE']

    diems = dao.get_paginated_diem(page, per_page)
    return render_template('nhap-diem.html', phanlops=phanlops, monhocs=monhocs, hockys=hockys, loaidiems=loaidiems, diems=diems)

@app.route('/bang-diem-mon', methods=['GET', 'POST'])
def bang_diem_mon():
    if request.method == 'POST':
        lop = request.form.get('lop')
        namhoc = request.form.get('namhoc')
        hocky = request.form.get('hocky')
        monhoc = request.form.get('monhoc')
        selected_value = {f'lop': lop, 'namhoc': namhoc, 'hocky': hocky, 'monhoc': monhoc}
        bangdiems = dao.get_bang_diem_mon(lop, namhoc, hocky, monhoc)
        if 'export' in request.form:
            csv_file = f'danh_sach_{lop}_{monhoc}_{hocky}_{namhoc}.csv'
            with open(csv_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['Họ tên', 'Điểm 15 phút', 'Điểm 1 tiết', 'Điểm thi', 'Điểm trung bình']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for bangdiem in bangdiems:
                    writer.writerow({
                        'Họ tên': bangdiem.hoten,
                        'Điểm 15 phút': bangdiem.diem15p,
                        'Điểm 1 tiết': bangdiem.diem1t,
                        'Điểm thi': bangdiem.diemthi,
                        'Điểm trung bình': bangdiem.diemtrungbinh
                    })
            return send_file(csv_file, as_attachment=True)
        return render_template('bang-diem-mon.html', bangdiems=bangdiems, selected_value=selected_value)
    lops = dao.get_lop_bang_diem_mon()
    namhocs = dao.get_namhoc_bang_diem_mon()
    hockys = dao.get_hocky_bang_diem_mon()
    monhocs = dao.get_monhoc_bang_diem_mon()
    return render_template('xem-bang-diem-mon.html', lops=lops, namhocs=namhocs, hockys=hockys, monhocs=monhocs)

@app.route('/bang-diem-trung-binh', methods=['GET', 'POST'])
def bang_diem_trung_binh():
    if request.method == 'POST':
        lop = request.form.get('lop')
        namhoc = request.form.get('namhoc')
        monhoc = request.form.get('monhoc')
        selected_value = {f'lop': lop, 'namhoc': namhoc, 'monhoc': monhoc}
        bangdiems = dao.get_bang_diem_trung_binh(lop, namhoc, monhoc)
        if 'export' in request.form:
            csv_file = f'danh_sach_{lop}_{monhoc}_{namhoc}.csv'
            with open(csv_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['Họ tên', 'Điểm TB HK1', 'Điểm TB HK2', 'Điểm TB cả năm']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for bangdiem in bangdiems:
                    writer.writerow({
                        'Họ tên': bangdiem.hoten,
                        'Điểm TB HK1': bangdiem.diemtbhk1,
                        'Điểm TB HK2': bangdiem.diemtbhk2,
                        'Điểm TB cả năm': bangdiem.diemtrungbinh
                    })
            return send_file(csv_file, as_attachment=True)
        return render_template('bang-diem-trung-binh.html', bangdiems=bangdiems, selected_value=selected_value)

    lops = dao.get_lop_bang_diem_trung_binh()
    namhocs = dao.get_namhoc_bang_diem_trung_binh()
    monhocs = dao.get_monhoc_bang_diem_trung_binh()
    return render_template('xem-bang-diem-trung-binh.html', lops=lops, namhocs=namhocs, monhocs=monhocs)

@app.route('/bang-diem-lop', methods=['GET', 'POST'])
def bang_diem_lop():
    if request.method == 'POST':
        lop = request.form.get('lop')
        namhoc = request.form.get('namhoc')
        selected_value = {f'lop': lop, 'namhoc': namhoc}
        bangdiems = dao.get_bang_diem_lop(lop, namhoc)
        if 'export' in request.form:
            csv_file = f'danh_sach_{lop}_{namhoc}.csv'
            with open(csv_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['Họ tên', 'Điểm TB HK1', 'Điểm TB HK2', 'Điểm TB cả năm']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for bangdiem in bangdiems:
                    writer.writerow({
                        'Họ tên': bangdiem.hoten,
                        'Điểm TB HK1': bangdiem.diemtbhk1,
                        'Điểm TB HK2': bangdiem.diemtbhk2,
                        'Điểm TB cả năm': bangdiem.diemtrungbinh
                    })
            return send_file(csv_file, as_attachment=True)
        return render_template('bang-diem-lop.html', bangdiems=bangdiems, selected_value=selected_value)
    lops = dao.get_lop_bang_diem_lop()
    namhocs = dao.get_namhoc_bang_diem_lop()
    return render_template('xem-bang-diem-lop.html', lops=lops, namhocs=namhocs)

@app.route('/thay-doi-quy-dinh', methods=['GET', 'POST'])
def thay_doi_quy_dinh():
    if request.method == 'POST':
        if 'edit' in request.form:
            maquydinh = request.form.get('maquydinh')
            quydinh = dao.get_quydinh(maquydinh)
            quydinh.tenquydinh = request.form.get('tenquydinh')
            quydinh.giatri = request.form.get('giatri')
            dao.update_quydinh(quydinh)

            flash('Thay đổi quy định thành công.', 'success')

    quydinhs = dao.get_all_quydinhs()
    return render_template('thay-doi-quy-dinh.html', quydinhs=quydinhs)

@app.route('/quan-ly-mon-hoc', methods=['GET', 'POST'])
def quan_ly_mon_hoc():
    if request.method == 'POST':
        if 'add' in request.form:
            mamonhoc = request.form.get('mamonhoc')
            tenmonhoc = request.form.get('tenmonhoc')

            monhoc = MonHoc(mamonhoc=mamonhoc, tenmonhoc=tenmonhoc)

            dao.add_monhoc(monhoc)
            flash('Thêm môn học thành công.', 'success')

        elif 'edit' in request.form:
            mamonhoc = request.form.get('mamonhoc')

            monhoc = dao.get_monhoc(mamonhoc)
            monhoc.tenmonhoc = request.form.get('tenmonhoc')

            dao.update_monhoc(monhoc)
            flash('Sửa môn học thành công.', 'success')

        elif 'delete' in request.form:
            mamonhoc = request.form.get('mamonhoc')
            monhoc = dao.get_monhoc(mamonhoc)
            dao.delete_monhoc(monhoc)
            flash('Xóa môn học thành công.', 'success')

    page = request.args.get('page', 1, type=int)
    per_page = app.config['PAGE_SIZE']

    monhocs = dao.get_paginated_monhoc(page, per_page)
    return render_template('quan-ly-mon-hoc.html', monhocs=monhocs)

@app.route('/thong-ke-bao-cao', methods=['GET', 'POST'])
def thong_ke_bao_cao():
    if request.method == 'POST':
        namhoc = request.form.get('namhoc')
        hocky = request.form.get('hocky')
        monhoc = request.form.get('monhoc')
        selected_value = {f'namhoc': namhoc,'hocky': hocky, 'monhoc': monhoc}
        baocaos = dao.get_baocao(namhoc, hocky, monhoc)
        if 'export' in request.form:
            csv_file = f'danh_sach_{monhoc}_{hocky}_{namhoc}.csv'
            with open(csv_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['Lớp', 'Sĩ số', 'Số lượng đạt', 'Tỷ lệ']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for baocao in baocaos:
                    writer.writerow({
                        'Lớp': baocao.lop,
                        'Sĩ số': baocao.siso,
                        'Số lượng đạt': baocao.soluongdat,
                        'Tỷ lệ': baocao.tyle
                    })
            return send_file(csv_file, as_attachment=True)
        baocaos_json = json.dumps([{'lop': baocao.lop, 'tyle': baocao.tyle} for baocao in baocaos])
        return render_template('bao-cao.html', baocaos=baocaos, selected_value=selected_value, baocaos_json=baocaos_json)
    namhocs = dao.get_namhoc_baocao()
    hockys = dao.get_hocky_baocao()
    monhocs = dao.get_monhoc_baocao()
    return render_template('thong-ke.html', namhocs=namhocs, hockys=hockys, monhocs=monhocs)

if __name__ == '__main__':
    from app import admin
    app.run(debug=True)

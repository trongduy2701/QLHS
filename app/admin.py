from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app.models import (NguoiDung, HocSinh, GiaoVien, QuyDinh, NamHoc, HocKy, MonHoc, KhoiLop, Lop, PhanLop, PhanCong, \
                        LoaiDiem, Diem, LoaiNguoiDung, NhanVien, QuanTriVien, BangDiemMon, BangDiemLop,
                        TongKetMonHoc, BangDiemTrungBinh)
from app import app, db
from flask_login import logout_user, current_user
from flask import redirect

admin = Admin(app=app, name='QUẢN LÝ HỌC SINH', template_mode='bootstrap4')

class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.loainguoidung == LoaiNguoiDung.ADMIN

class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class LogoutView(AuthenticatedUser):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

class QuyDinhView(AuthenticatedAdmin):
    column_list = ['maquydinh', 'tenquydinh', 'giatri']
    column_searchable_list = ['tenquydinh']
    column_labels = {
        'maquydinh': 'Mã quy định',
        'tenquydinh': 'Tên quy định',
        'giatri': ''
    }
    column_display_pk = True
    can_view_details = True
    can_export = True

class NamHocView(AuthenticatedAdmin):
    column_list = ['manamhoc', 'tennamhoc', 'lops', 'phanlops']
    column_searchable_list = ['tennamhoc']
    column_exclude_list = ['lops', 'phanlops']
    column_labels = {
        'manamhoc': 'Mã năm học',
        'tennamhoc': 'Tên năm học',
    }
    column_display_pk = True
    can_view_details = True
    can_export = True

class KhoiLopView(AuthenticatedAdmin):
    column_list = ['makhoilop', 'tenkhoilop', 'lops']
    column_searchable_list = ['tenkhoilop']
    column_exclude_list = ['lops']
    column_labels = {
        'makhoilop': 'Mã khối lớp',
        'tenkhoilop': 'Tên khối lớp',
    }
    column_display_pk = True
    can_view_details = True
    can_export = True

class HocKyView(AuthenticatedAdmin):
    column_list = ['mahocky', 'tenhocky', 'diems']
    column_searchable_list = ['tenhocky']
    column_exclude_list = ['diems']
    column_labels = {
        'mahocky': 'Mã học kỳ',
        'tenhocky': 'Tên học kỳ',
    }
    column_display_pk = True
    can_view_details = True
    can_export = True

class MonHocView(AuthenticatedAdmin):
    column_list = ['mamonhoc', 'tenmonhoc', 'diems', 'giaoviens']
    column_searchable_list = ['tenmonhoc']
    column_filters = ['tenmonhoc']
    column_exclude_list = ['diems', 'giaoviens']
    column_labels = {
        'mamonhoc': 'Mã môn học',
        'tenmonhoc': 'Tên môn học',
    }
    column_display_pk = True
    can_view_details = True
    can_export = True

class NguoiDungView(AuthenticatedAdmin):
    column_list = ['tennguoidung', 'taikhoan', 'loainguoidung', 'gioitinh', 'email', 'sodienthoai', 'giaoviens', 'nhanviens', 'quantriviens']
    column_searchable_list = ['tennguoidung']
    column_filters = ['loainguoidung']
    column_exclude_list = ['giaoviens', 'nhanviens', 'quantriviens']
    column_labels = {
        'manguoidung': 'Mã người dùng',
        'tennguoidung': 'Tên người dùng',
        'gioitinh': 'Giới tính',
        'email': 'Email',
        'sodienthoai': 'Số điện thoại',
        'taikhoan': 'Tài khoản',
        'matkhau': 'Mật khẩu',
        'loainguoidung': 'Loại người dùng'
    }
    column_display_pk = True
    can_view_details = True
    can_export = True

class HocSinhView(AuthenticatedAdmin):
    column_list = ['mahocsinh', 'tenhocsinh', 'ngaysinh','gioitinh', 'email', 'sodienthoai', 'diachi', 'phanlops']
    column_searchable_list = ['mahocsinh', 'tenhocsinh']
    column_filters = ['mahocsinh']
    column_exclude_list = ['phanlops']
    column_labels = {
        'mahocsinh': 'Mã học sinh',
        'tenhocsinh': 'Họ tên',
        'ngaysinh': 'Ngày sinh',
        'gioitinh': 'Giới tính',
        'email': 'Email',
        'sodienthoai': 'Số điện thoại',
        'diachi': 'Địa chỉ',
    }
    column_display_pk = True
    can_view_details = True
    can_export = True

class NhanvienView(AuthenticatedAdmin):
    column_list = ['manhanvien', 'manguoidung']
    column_searchable_list = ['manhanvien']
    column_filters = ['manhanvien']
    column_labels = {
        'manhanvien': 'Mã nhân viên',
        'manguoidung': 'Mã người dùng'
    }
    column_display_pk = True
    can_view_details = True
    can_export = True

class QuanTriVienView(AuthenticatedAdmin):
    column_list = ['maquantrivien', 'manguoidung']
    column_searchable_list = ['maquantrivien']
    column_filters = ['maquantrivien']
    column_labels = {
        'maquantrivien': 'Mã quản trị viên',
        'manguoidung': 'Mã người dùng'
    }
    column_display_pk = True
    can_view_details = True
    can_export = True

class GiaoVienView(AuthenticatedAdmin):
    column_list = ['magiaovien', 'manguoidung', 'mamonhoc', 'phancongs']
    column_searchable_list = ['magiaovien']
    column_filters = ['magiaovien']
    column_exclude_list = ['phancongs']
    column_labels = {
        'magiaovien': 'Mã giáo viên',
        'manguoidung': 'Mã người dùng',
        'mamonhoc': 'Mã Môn học',
    }
    column_display_pk = True
    can_view_details = True
    can_export = True

class LopView(AuthenticatedAdmin):
    column_list = ['malop', 'tenlop', 'siso', 'manamhoc', 'makhoilop', 'magiaovien', 'phanlops', 'phancongs', 'diems']
    column_searchable_list = ['malop', 'tenlop']
    column_filters = ['malop', 'tenlop']
    column_exclude_list = ['phanlops', 'phancongs', 'diems']
    column_labels = {
        'malop': 'Mã lớp',
        'tenlop': 'Tên lớp',
        'siso': 'Sỉ số',
        'manamhoc': 'Mã năm học',
        'makhoilop': 'Mã khối lớp',
        'magiaovien': 'Mã giáo viên',
    }
    column_display_pk = True
    can_view_details = True
    can_export = True

class PhanLopView(AuthenticatedAdmin):
    column_searchable_list = ['maphanlop', 'mahocsinh', 'malop', 'manamhoc']
    column_filters = ['maphanlop', 'mahocsinh', 'malop', 'manamhoc']
    column_labels = {
        'maphanlop': 'Mã phân lớp',
        'hocsinh': 'Mã học sinh',
        'lop': 'Mã lớp',
        'namhoc': 'Mã năm học'
    }
    column_display_pk = True
    can_view_details = True
    can_export = True

class PhanCongView(AuthenticatedAdmin):
    column_searchable_list = ['maphancong', 'magiaovien', 'malop']
    column_filters = ['maphancong', 'magiaovien', 'malop']
    column_labels = {
        'maphancong': 'Mã phân công',
        'giaovien': 'Mã giáo viên',
        'lop': 'Mã lớp'
    }
    column_display_pk = True
    can_view_details = True
    can_export = True

class LoaiDiemView(AuthenticatedAdmin):
    column_list = ['maloaidiem', 'tenloaidiem', 'diems']
    column_searchable_list = ['tenloaidiem']
    column_filters = ['tenloaidiem']
    column_exclude_list = ['diems']
    column_labels = {
        'maloaidiem': 'Mã loại điểm',
        'tenloaidiem': 'Tên loại điểm',
    }
    column_display_pk = True
    can_view_details = True
    can_export = True

class DiemView(AuthenticatedAdmin):
    column_list = ['madiem', 'maphanlop', 'mamonhoc', 'mahocky', 'maloaidiem', 'diem']
    column_searchable_list = ['madiem', 'maphanlop', 'mamonhoc', 'mahocky', 'maloaidiem']
    column_filters = ['madiem', 'maphanlop', 'mamonhoc', 'mahocky', 'maloaidiem']
    column_labels = {
        'madiem': 'Mã điểm',
        'maphanlop': 'Mã phân lớp',
        'mamonhoc': 'Mã môn học',
        'mahocky': 'Mã học kỳ',
        'maloaidiem': 'Mã loại điểm',
        'diem': 'Điểm',
    }
    column_display_pk = True
    can_view_details = True
    can_export = True

class BangDiemMonView(AuthenticatedAdmin):
    column_list = ['hoten', 'lop', 'monhoc', 'hocky', 'namhoc', 'diem15p', 'diem1t', 'diemthi', 'diemtrungbinh', 'ketqua']
    column_searchable_list = ['hoten', 'lop', 'monhoc', 'hocky', 'namhoc']
    column_filters = ['lop', 'monhoc', 'hocky', 'namhoc']
    column_labels = {
        'hoten': 'Họ và tên',
        'lop': 'Lớp',
        'monhoc': 'Môn học',
        'namhoc': 'Năm học',
        'hocky': 'Học kỳ',
        'diem15p': 'Điểm 15',
        'diem1t': 'Điểm 1 tiết',
        'diemthi': 'Điểm thi',
        'diemtrungbinh': 'Điểm trung bình',
        'ketqua': 'Kết quả'
    }
    can_edit = False
    can_delete = False
    can_create = False
    column_display_pk = True
    can_export = True

class BangDiemTrungBinhView(AuthenticatedAdmin):
    column_list = ['hoten', 'lop', 'monhoc', 'namhoc', 'diemtbhk1', 'diemtbhk2', 'diemtbcn']
    column_searchable_list = ['hoten', 'lop', 'monhoc', 'namhoc']
    column_filters = ['lop', 'monhoc', 'namhoc']
    column_labels = {
        'hoten': 'Họ và tên',
        'lop': 'Lớp',
        'monhoc': 'Môn học',
        'namhoc': 'Năm học',
        'diemtbhk1': 'Điểm TB HK1',
        'diemtbhk2': 'Điểm TB HK2',
        'diemtbcn': 'Điểm TB cả năm'
    }
    can_edit = False
    can_delete = False
    can_create = False
    column_display_pk = True
    can_export = True

class BangDiemLopView(AuthenticatedAdmin):
    column_list = ['hoten', 'lop', 'namhoc', 'diemtbhk1', 'diemtbhk2', 'diemtbcn']
    column_searchable_list = ['hoten', 'lop', 'namhoc']
    column_filters = ['lop', 'namhoc']
    column_labels = {
        'hoten': 'Họ và tên',
        'lop': 'Lớp',
        'namhoc': 'Năm học',
        'diemtbhk1': 'Điểm TB HK1',
        'diemtbhk2': 'Điểm TB HK2',
        'diemtbcn': 'Điểm TB cả năm'
    }
    can_edit = False
    can_delete = False
    can_create = False
    column_display_pk = True
    can_export = True

class TongKetMonHocView(AuthenticatedAdmin):
    column_list = ['lop', 'monhoc', 'hocky', 'namhoc', 'siso', 'soluongdat', 'tyle']
    column_searchable_list = ['lop', 'monhoc', 'hocky', 'namhoc']
    column_filters = ['lop', 'monhoc', 'hocky', 'namhoc']
    column_labels = {
        'lop': 'Lớp',
        'monhoc': 'Môn học',
        'namhoc': 'Năm học',
        'hocky': 'Học kỳ',
        'siso': 'Sĩ số',
        'soluongdat': 'Số lượng đạt',
        'tyle': 'Tỷ lệ'
    }
    can_edit = False
    can_delete = False
    can_create = False
    column_display_pk = True
    can_export = True

admin.add_view(NguoiDungView(NguoiDung, db.session, name='Người dùng', category='Quản lý hồ sơ'))
admin.add_view(GiaoVienView(GiaoVien, db.session, name='Giáo viên', category='Quản lý hồ sơ'))
admin.add_view(NhanvienView(NhanVien, db.session, name='Nhân viên', category='Quản lý hồ sơ'))
admin.add_view(QuanTriVienView(QuanTriVien, db.session, name='Quản trị viên', category='Quản lý hồ sơ'))
admin.add_view(HocSinhView(HocSinh, db.session, name='Học sinh', category='Quản lý hồ sơ'))

admin.add_view(QuyDinhView(QuyDinh, db.session, name='Quy Định', category='Quản lý danh mục'))
admin.add_view(NamHocView(NamHoc, db.session, name='Năm học', category='Quản lý danh mục'))
admin.add_view(HocKyView(HocKy, db.session, name='Học kỳ', category='Quản lý danh mục'))
admin.add_view(MonHocView(MonHoc, db.session, name='Môn học', category='Quản lý danh mục'))
admin.add_view(KhoiLopView(KhoiLop, db.session, name='Khối lớp', category='Quản lý danh mục'))
admin.add_view(LoaiDiemView(LoaiDiem, db.session, name='Loại điểm', category='Quản lý danh mục'))


admin.add_view(LopView(Lop, db.session, name='Lớp', category='Quản lý lớp'))
admin.add_view(DiemView(Diem, db.session, name='Điểm', category='Quản lý lớp'))
admin.add_view(PhanLopView(PhanLop, db.session, name='Phân lớp', category='Quản lý lớp'))
admin.add_view(PhanCongView(PhanCong, db.session, name='Phân công', category='Quản lý lớp'))


admin.add_view(BangDiemMonView(BangDiemMon, db.session, name='Bảng điểm môn', category='Thống kê báo cáo'))
admin.add_view(BangDiemTrungBinhView(BangDiemTrungBinh, db.session, name='Bảng điểm môn', category='Thống kê báo cáo'))
admin.add_view(BangDiemLopView(BangDiemLop, db.session, name='Bảng điểm lớp', category='Thống kê báo cáo'))
admin.add_view(TongKetMonHocView(TongKetMonHoc, db.session, name='Báo cáo tổng kết môn học', category='Thống kê báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))

function displayStudentDetails(mahocsinh) {
    var mahocsinh = document.querySelector(`tr[data-mahocsinh="${mahocsinh}"] td:first-child`).textContent;
    var tenhocsinh = document.querySelector(`tr[data-mahocsinh="${mahocsinh}"] td:nth-child(2)`).textContent;
    var ngaysinh = document.querySelector(`tr[data-mahocsinh="${mahocsinh}"] td:nth-child(3)`).textContent;
    var gioitinh = document.querySelector(`tr[data-mahocsinh="${mahocsinh}"] td:nth-child(4)`).textContent;
    var email = document.querySelector(`tr[data-mahocsinh="${mahocsinh}"] td:nth-child(5)`).textContent;
    var sodienthoai = document.querySelector(`tr[data-mahocsinh="${mahocsinh}"] td:nth-child(6)`).textContent;
    var diachi = document.querySelector(`tr[data-mahocsinh="${mahocsinh}"] td:nth-child(7)`).textContent;

    document.getElementById('mahocsinh').value = mahocsinh;
    document.getElementById('tenhocsinh').value = tenhocsinh;
    document.getElementById('ngaysinh').value = ngaysinh;
    document.getElementById('gioitinh').value = gioitinh;
    document.getElementById('email').value = email;
    document.getElementById('sodienthoai').value = sodienthoai;
    document.getElementById('diachi').value = diachi;
}

function setEditValues(mahocsinh, tenhocsinh, ngaysinh, gioitinh, diachi, sodienthoai, email) {
    document.getElementById('action').value = 'edit';
    document.getElementById('mahocsinh').value = mahocsinh;
    document.getElementById('tenhocsinh').value = tenhocsinh;
    document.getElementById('ngaysinh').value = ngaysinh;
    document.getElementById('gioitinh').value = gioitinh;
    document.getElementById('email').value = email;
    document.getElementById('sodienthoai').value = sodienthoai;
    document.getElementById('diachi').value = diachi;
}

function submitEditForm() {
    document.getElementById('editForm').submit();
}
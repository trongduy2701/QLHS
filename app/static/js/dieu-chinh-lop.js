function displayPhanLopDetails(maphanlop) {
    var maphanlop = document.querySelector(`tr[data-maphanlop="${maphanlop}"] td:first-child`).textContent;
    var malop = document.querySelector(`tr[data-maphanlop="${maphanlop}"] td:nth-child(2)`).textContent;
        var manamhoc = document.querySelector(`tr[data-maphanlop="${maphanlop}"] td:nth-child(3)`).textContent;
    var mahocsinh = document.querySelector(`tr[data-maphanlop="${maphanlop}"] td:nth-child(4)`).textContent;

    document.getElementById('maphanlop').value = maphanlop;
    document.getElementById('malop').value = malop;
    document.getElementById('manamhoc').value = manamhoc;
    document.getElementById('mahocsinh').value = mahocsinh;

}

function setEditValues(maphanlop, malop, manamhoc, mahocsinh) {
    document.getElementById('action').value = 'edit';
    document.getElementById('maphanlop').value = maphanlop;
    document.getElementById('malop').value = malop;
    document.getElementById('manamhoc').value = manamhoc;
    document.getElementById('mahocsinh').value = mahocsinh;
}

function submitEditForm() {
    document.getElementById('editForm').submit();
}

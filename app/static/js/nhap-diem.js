function displayDiemDetails(madiem) {
    var madiem = document.querySelector(`tr[data-madiem="${madiem}"] td:first-child`).textContent;
    var maphanlop = document.querySelector(`tr[data-madiem="${madiem}"] td:nth-child(2)`).textContent;
    var mamonhoc = document.querySelector(`tr[data-madiem="${madiem}"] td:nth-child(3)`).textContent;
    var mahocky = document.querySelector(`tr[data-madiem="${madiem}"] td:nth-child(4)`).textContent;
    var maloaidiem = document.querySelector(`tr[data-madiem="${madiem}"] td:nth-child(5)`).textContent;
    var diem = document.querySelector(`tr[data-madiem="${madiem}"] td:nth-child(6)`).textContent;

    document.getElementById('madiem').value = madiem;
    document.getElementById('maphanlop').value = maphanlop;
    document.getElementById('mamonhoc').value = mamonhoc;
    document.getElementById('mahocky').value = mahocky;
    document.getElementById('maloaidiem').value = maloaidiem;
    document.getElementById('diem').value = diem;
}

function setEditValues(madiem, maphanlop, mamonhoc, mahocky, maloaidiem, diem) {
    document.getElementById('action').value = 'edit';
    document.getElementById('madiem').value = madiem;
    document.getElementById('maphanlop').value = maphanlop;
    document.getElementById('mamonhoc').value = mamonhoc;
    document.getElementById('mahocky').value = mahocky;
    document.getElementById('maloaidiem').value = maloaidiem;
    document.getElementById('diem').value = diem;
}

function submitEditForm() {
    document.getElementById('editForm').submit();
}
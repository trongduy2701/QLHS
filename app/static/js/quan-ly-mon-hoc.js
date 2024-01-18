function displayMonHocDetails(mamonhoc) {
    var mamonhoc = document.querySelector(`tr[data-mamonhoc="${mamonhoc}"] td:first-child`).textContent;
    var tenmonhoc = document.querySelector(`tr[data-mamonhoc="${mamonhoc}"] td:nth-child(2)`).textContent;


    document.getElementById('mamonhoc').value = mamonhoc;
    document.getElementById('tenmonhoc').value = tenmonhoc;

}

function setEditValues(mamonhoc, tenmonhoc) {
    document.getElementById('action').value = 'edit';
    document.getElementById('mamonhoc').value = mamonhoc;
    document.getElementById('tenmonhoc').value = tenmonhoc;
}

function submitEditForm() {
    document.getElementById('editForm').submit();
}
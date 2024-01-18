function displayQuyDinhDetails(maquydinh) {
    var maquydinh = document.querySelector(`tr[data-maquydinh="${maquydinh}"] td:first-child`).textContent;
    var tenquydinh = document.querySelector(`tr[data-maquydinh="${maquydinh}"] td:nth-child(2)`).textContent;
    var giatri = document.querySelector(`tr[data-maquydinh="${maquydinh}"] td:nth-child(3)`).textContent;


    document.getElementById('maquydinh').value = maquydinh;
    document.getElementById('tenquydinh').value = tenquydinh;
    document.getElementById('giatri').value = giatri;
}

function setEditValues(maquydinh, tenquydinh, giatri) {
    document.getElementById('action').value = 'edit';
    document.getElementById('maquydinh').value = maquydinh;
    document.getElementById('tenquydinh').value = tenquydinh;
    document.getElementById('giatri').value = giatri;
}

function submitEditForm() {
    document.getElementById('editForm').submit();
}
function searchTimKiem() {
    var searchQuery = document.getElementById('searchQuery').value.toLowerCase();
    var rows = document.querySelectorAll('#timkiemTableBody tr');

    for (var i = 0; i < rows.length; i++) {
        var timkiemData = rows[i].innerText.toLowerCase();
        rows[i].style.display = timkiemData.includes(searchQuery) ? '' : 'none';
    }
}

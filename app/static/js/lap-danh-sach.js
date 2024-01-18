document.addEventListener("DOMContentLoaded", function () {
    function updateLops() {
        var namhoc = document.getElementById('manamhoc').value;
        var khoilop = document.getElementById('makhoilop').value;

        fetch(`/get_lop_nam_khoi?manamhoc=${namhoc}&makhoilop=${khoilop}`)
            .then(response => response.json())
            .then(data => {
                var lopSelect = document.getElementById('malop');
                lopSelect.innerHTML = "";
                data.lops.forEach(function (lop) {
                    var option = document.createElement('option');
                    option.value = lop.malop;
                    option.text = lop.tenlop;
                    lopSelect.appendChild(option);
                });
            });
    }
    document.getElementById('manamhoc').addEventListener('change', updateLops);
    document.getElementById('makhoilop').addEventListener('change', updateLops);
});
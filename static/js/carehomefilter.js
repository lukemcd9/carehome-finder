const carehomeFilter = document.querySelector('#carehome-filter');
const carehomeSort = document.querySelectorAll('.carehome-sorter');

for(let i = 0; i < carehomeSort.length; i++) {
    carehomeSort[i].addEventListener('click', event => {
        event.preventDefault()
        sortTable(i);
        let icon = carehomeSort[i].querySelector('.fas');

        if(icon.classList.contains('fa-chevron-up')) {
            icon.classList = 'fas fa-chevron-down';
        } else {
            icon.classList = 'fas fa-chevron-up';
        }
    });
}

carehomeFilter.addEventListener('input', () => {
    const tables = document.querySelector('#carehomes-table');
    const rows = tables.querySelectorAll('tr.carehome');
    for(let row of rows) {
        let text = row.textContent.toLowerCase(), val = carehomeFilter.value.toLowerCase();
        row.style.display = text.indexOf(val) === -1 ? 'none' : 'table-row';
    }
});


function sortTable(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById('carehomes-table');
    switching = true;
    dir = 'asc';
    while (switching) {
        switching = false;
        rows = table.getElementsByTagName('tr');
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName('td')[n];
            y = rows[i + 1].getElementsByTagName('td')[n];
            if (dir == 'asc') {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == 'desc') {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount++;
        } else {
            if (switchcount == 0 && dir == 'asc') {
                dir = 'desc';
                switching = true;
            }
        }
    }
}
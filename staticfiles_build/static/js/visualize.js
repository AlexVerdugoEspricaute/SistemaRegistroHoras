document.addEventListener('DOMContentLoaded', function() {
    var arrowNombres = document.getElementById('arrow-nombres');
    var arrowProyectos = document.getElementById('arrow-proyectos');
    var arrowFechas = document.getElementById('arrow-fechas'); // Nuevo
    var ordenNombres = document.getElementById('orden-nombres');
    var ordenProyectos = document.getElementById('orden-proyectos');
    var ordenFechas = document.getElementById('orden-fechas'); // Nuevo
    var ordenAscendenteNombres = true; // Por defecto, orden ascendente para nombres
    var ordenAscendenteProyectos = true; // Por defecto, orden ascendente para proyectos
    var ordenAscendenteFechas = true; // Por defecto, orden ascendente para fechas

    ordenNombres.addEventListener('click', function() {
        ordenAscendenteNombres = !ordenAscendenteNombres; // Cambia el estado de ordenación al hacer clic
        arrowNombres.textContent = ordenAscendenteNombres ? ' ▲' : ' ▼';
        sortTable('registros-table', 0, ordenAscendenteNombres ? 'asc' : 'desc');
    });

    ordenProyectos.addEventListener('click', function() {
        ordenAscendenteProyectos = !ordenAscendenteProyectos; // Cambia el estado de ordenación al hacer clic
        arrowProyectos.textContent = ordenAscendenteProyectos ? ' ▲' : ' ▼';
        sortTable('registros-table', 1, ordenAscendenteProyectos ? 'asc' : 'desc');
    });

    ordenFechas.addEventListener('click', function() {
        ordenAscendenteFechas = !ordenAscendenteFechas; // Cambia el estado de ordenación al hacer clic
        arrowFechas.textContent = ordenAscendenteFechas ? ' ▲' : ' ▼';
        sortTable('registros-table', 6, ordenAscendenteFechas ? 'asc' : 'desc'); // Cambiado a la columna de fecha (6)
    });

    function sortTable(tableId, column, order) {
        var table, rows, switching, i, x, y, shouldSwitch;
        table = document.getElementById(tableId);
        switching = true;
        while (switching) {
            switching = false;
            rows = table.getElementsByTagName('tr');
            for (i = 1; i < (rows.length - 1); i++) {
                shouldSwitch = false;
                x = rows[i].getElementsByTagName('td')[column];
                y = rows[i + 1].getElementsByTagName('td')[column];
                if (order === 'asc') {
                    if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                        shouldSwitch= true;
                        break;
                    }
                } else if (order === 'desc') {
                    if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                        shouldSwitch= true;
                        break;
                    }
                }
            }
            if (shouldSwitch) {
                rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                switching = true;
            }
        }
    }
});
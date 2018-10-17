
google.charts.load('current', { 'packages': ['timeline'] });
google.charts.setOnLoadCallback(drawChart);
function drawChart() {
    d3.json('/api/gantt/1', function (err, data) {
        console.log(data);
        create_graph(data.context);
    });

    function create_graph(rows_global) {

        console.log(rows_global);

        var container = document.getElementById('chart_div');
        var chart = new google.visualization.Timeline(container);
        var dataTable = new google.visualization.DataTable();

        dataTable.addColumn({ type: 'string', id: 'Term' });
        dataTable.addColumn({ type: 'string', id: 'Name' });
        dataTable.addColumn({ type: 'date', id: 'Start' });
        dataTable.addColumn({ type: 'date', id: 'End' });

        rows_aux = []
        rows_global.forEach(element => {
            var array = [];
            for (let index = 0; index < element.length; index++) {
                if (index == 3 || index == 4) {
                    aux = element[index].split("-");
                    array.push(
                        new Date(aux[0], aux[1], aux[2])
                    );
                } else {
                    if (element[index] != null && element[index] != 0) {
                        array.push(
                            element[index]
                        );
                    }
                }
            }
            console.log(array);
            rows_aux.push(array);
        });
        dataTable.addRows(rows_aux);

        chart.draw(dataTable);
        
        google.visualization.events.addListener(chart, 'select', myPageEventHandler);

        /**
         * Função que pega a informação do id quando clicado no gráfico
         */
        function myPageEventHandler() {

            console.log(dataTable.getValue(chart.getSelection()[0].row,0));
        }
    }
}
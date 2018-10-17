d3.json('/api/gantt/1', function (err, data) {
    console.log(data)
    create_graph(data.context)
});

function create_graph(rows) {
    google.charts.load('current', { 'packages': ['gantt'] });
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {

        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Task ID');
        data.addColumn('string', 'Task Name');
        data.addColumn('string', 'Resource');
        data.addColumn('date', 'Start Date');
        data.addColumn('date', 'End Date');
        data.addColumn('number', 'Duration');
        data.addColumn('number', 'Percent Complete');
        data.addColumn('string', 'Dependencies');

        rows_aux = []
        rows.forEach(element => {
            var array = [];
            for (let index = 0; index < element.length; index++) {
                if (index == 3 || index == 4) {
                    aux = element[index].split("-");
                    array.push(
                        new Date(aux[0], aux[1], aux[2])
                    );
                } else {
                    array.push(
                        element[index]
                    );
                }
            } 
            rows_aux.push(array);
        });
        data.addRows(rows_aux);

        var options = {
            height: 400,
            width : 1000,
            gantt: {
                trackHeight: 30
            }
        };

        var chart = new google.visualization.Gantt(document.getElementById('chart_div'));
        google.visualization.events.addListener(chart, 'select', myPageEventHandler);

        /**
         * Função que pega a informação do id quando clicado no gráfico
         */
        function myPageEventHandler() {
            console.log(data.getValue(chart.getSelection()[0].row,0));
            create_table();
        }

        chart.draw(data, options);
    }
}

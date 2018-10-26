/**
 * Gera o gráfico de gantt daquele estudante
 * Get o valor do input para buscar o id (matricura) do estudante e realiza requisição
 */
function search_informations_student() {
    d3.selectAll(".google-visualization-table-table").remove();
    var input_text = d3.select("#autocomplete-input").property("value");
    if (input_text != "") {
        var student_id = get_id_input_text(input_text);
        console.log("id:"+student_id);
        d3.json('/api/gantt/student/'+student_id, function (err, data) {
            console.log(data.context)
            create_graph(data.context)
        });
    }else{
        alert("Atenção digite o nome da Aluno!");
    }
}

function create_graph(rows) {
    google.charts.load('current', { 'packages': ['gantt']});
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
            width: '100%',
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
            create_table(data.getValue(chart.getSelection()[0].row,0));
        }

        chart.draw(data, options);
    }
}

function get_id_input_text(text){
    var text_array = text.split(" ");
    return text_array[1].replace(",","");
}
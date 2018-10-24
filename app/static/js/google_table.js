/**
 * 
 * recebe o id do nó para gerar a tabela com informação do estudante na atividade do nó
 * url: api/gantt / <int: node_id>/<int: student_id></int>
 */
function create_table(node_id) {
    console.log("create table: node id");
    console.log(node_id);
    d3.json('/api/gantt/node/'+node_id+"/student/1", function (err, data) {
        console.log("retorno das informações da atividade do nó")
        console.log(data)
        generator_table(data);
    });
}

function generator_table(params) {
    console.log("gerar tabela");
    google.charts.load('current', { 'packages': ['table'] });
    google.charts.setOnLoadCallback(drawTable);

    function drawTable() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Name');
        data.addColumn('string', 'Note');
        data.addColumn('number', 'Amount Access');
        console.log(params);
        data.addRows([
            [params.student.name, params.student_informations.notes, params.student_informations.amount_access],
        ]);

        var table = new google.visualization.Table(document.getElementById('table_div'));

        table.draw(data, { showRowNumber: true, width: '100%', height: '100%' });
    }
}
/**
 * 
 * recebe o id do nó para gerar a tabela com informação do estudante na atividade do nó
 * url: api/gantt / <int: node_id>/<int: student_id></int>
 */
function create_table(node_id) {
    console.log("create table: node id");
    console.log(node_id);
    var input_text = d3.select("#autocomplete-input").property("value");
    var student_id = get_id_input_text(input_text);
    d3.json('/api/gantt/node/'+node_id+"/student/"+student_id, function (err, data) {
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
        data.addColumn('string', 'Nome');
        data.addColumn('string', 'Nota');
        data.addColumn('number', 'Quantidade de Acesso');
        data.addColumn('number', 'Média de Acesso');
        console.log(params);
        data.addRows([
            [params.student.name, params.student_informations.notes, params.student_informations.amount_access,params.node.avg_access],
        ]);
        console.log(data);

        var table = new google.visualization.Table(document.getElementById('table_div'));

        table.draw(data, { showRowNumber: true, width: '100%', height: '100%' });
    }
}
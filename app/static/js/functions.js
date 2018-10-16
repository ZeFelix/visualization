var start_ager, end_ager, sex_m, sex_f,
    not_married, married, public, particular, params_filter = "";

/**
 * Função para capturar os valores dos campos de filtro e aplica-los
 * params_filter = variavel que carregar os valores de filtros para serem inseridos na url
 */
function set_filter_params() {

    d3.select("#sex_f").property("checked") ? sex_f = "F" : sex_f = "";
    d3.select("#sex_m").property("checked") ? sex_m = "M" : sex_m = "";
    d3.select("#not_married").property("checked") ? not_married = "S" : not_married = "";
    d3.select("#married").property("checked") ? married = "C" : married = "";
    d3.select("#public").property("checked") ? public = "PB" : public = "";
    d3.select("#particular").property("checked") ? particular = "PA" : particular = "";
    if (d3.select("#ager").property("checked")) {
        start_ager = d3.select("#start_ager").property("value");
        end_ager = d3.select("#end_ager").property("value");
    } else {
        start_ager = null;
        end_ager = null;
    }
    params_filter = "?start_ager=" + start_ager + "&" + "end_ager=" + end_ager + "&" + "sex_m=" + sex_m +
        "&" + "sex_f=" + sex_f + "&" + "not_married=" + not_married + "&" + "married=" + married + "&" + "public=" + public + "&" + "particular=" + particular

    init_get_json(params_filter);

}

/**
 * Função para ativar ou desativar os inputs de entrada de idade
 */
function ager_checked_click() {
    if (d3.select("#ager").property("checked")) {
        d3.select("#start_ager").attr("disabled", null);
        d3.select("#end_ager").attr("disabled", null);
    } else {
        d3.select("#start_ager").property("value", "").attr("disabled", true);
        d3.select("#end_ager").property("value", "").attr("disabled", true);
    }
}

function clear_filter_params() {
    set_field_default();
    init_get_json();
}

/**
 * Função para obter os parametros do filtro
 */
function get_params_filter() {
    return params_filter;
}


/**
 * Função para limpar os campos de filtro
 */
function set_field_default() {
    params_filter = "";
    d3.select("#sex_f").property("checked", true);
    d3.select("#sex_m").property("checked", true);
    d3.select("#not_married").property("checked", true);
    d3.select("#married").property("checked", true);
    d3.select("#public").property("checked", true);
    d3.select("#particular").property("checked", true);
    d3.select("#ager").property("checked", false);
    d3.select("#start_ager").property("value", "");
    d3.select("#end_ager").property("value", "");
}


/**
 * Função para gerar tabela de informações dos alunos
 */

function tabulate(data, columns) {
    var table = d3.select("body").append("table")
        .attr("style", "margin-left: 250px"),
        thead = table.append("thead"),
        tbody = table.append("tbody");

    // append the header row
    thead.append("tr")
        .selectAll("th")
        .data(columns)
        .enter()
        .append("th")
        .text(function (column) { return column; });

    // create a row for each object in the data
    var rows = tbody.selectAll("tr")
        .data(data)
        .enter()
        .append("tr");

    // create a cell in each row for each column
    var cells = rows.selectAll("td")
        .data(function (row) {
            return columns.map(function (column) {
                return { column: column, value: row[column] };
            });
        })
        .enter()
        .append("td")
        .attr("style", "font-family: Courier")
        .html(function (d) { return d.value; });

    return table;
}

/**
 * Função para gerar tooltip com tabela de informações
 */
function tooltip_tablle(data) {
    var obj = {};
    obj.header = data.name;
    obj.rows = [];
    obj.rows.push({
        "label": "Name",
        "value": "Notas"
    });
    data.students.forEach(function (student) {
        data.student_informations.forEach(element => {
            if (element.student == student.pk) {
                obj.rows.push({
                    "label": student.name,
                    "value": element.notes
                });
            }
        });
    });
    var svg = d3.select("svg")[0][0];
    tooltip.table()
        .width(180)
        .call(svg, obj);
};
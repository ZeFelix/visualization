var color_blind, start_ager, end_ager, sex_m, sex_f,
    not_married, married, public, particular, params_filter = "";

/**
 * Função para capturar os valores dos campos de filtro e aplica-los
 * params_filter = variavel que carregar os valores de filtros para serem inseridos na url
 */
function set_filter_params() {
    color_blind = d3.select("#color_blind").property("checked");
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
    params_filter = "?color_blind=" + color_blind + "&" + "start_ager=" + start_ager + "&" + "end_ager=" + end_ager + "&" + "sex_m=" + sex_m +
        "&" + "sex_f=" + sex_f + "&" + "not_married=" + not_married + "&" + "married=" + married + "&" + "public=" + public + "&" + "particular=" + particular

    init_get_json(params_filter);

}

function clear_filter_params() {
    set_field_default();
    init_get_json();
}

function get_params_filter() {
    return params_filter;
}

/**
 * Função para limpar os campos de filtro
 */
function set_field_default() {
    params_filter = "";
    d3.select("#color_blind").property("checked", false);
    d3.select("#sex_f").property("checked", true);
    d3.select("#sex_m").property("checked", true);
    d3.select("#not_married").property("checked", true);
    d3.select("#married").property("checked", true);
    d3.select("#public").property("checked", true);
    d3.select("#particular").property("checked", true);
    d3.select("#ager").property("checked", false);
    d3.select("#start_ager").property("value","");
    d3.select("#end_ager").property("value","");
}

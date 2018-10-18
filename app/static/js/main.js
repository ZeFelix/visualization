// ************** Generate the tree diagram	 *****************
var margin = { top: 20, right: 120, bottom: 20, left: 100 },
    width = 5000 - margin.right - margin.left,
    height = 500 - margin.top - margin.bottom;

var i = 0,
    duration = 750,
    root;

var tree = d3.layout.tree()
    .size([height, width]);

var diagonal = d3.svg.diagonal()
    .projection(function (d) { return [d.y, d.x]; });

// Colors as an array
// https://github.com/mbostock/d3/wiki/Ordinal-Scales#category20
// cores tag = [nó fim - caminho sem alunos(filtro) - nota 0 - nota 5 - nota 10]
// sequencia das cores = [roxo, cinza, vermelho, amarelo, verde]
var colors = d3.scale.linear().domain([-2, -1, 0, 5, 10]).range(["#7E57C2", "#BDBDBD", "#DD2C00", "#FFD600", "#1B5E20"]);
// sequencia das cores daltonico = [roxo, cinza, vermelho(daltonico), amarelo(daltonico), verde(daltonico)]
var color_blind = d3.scale.linear().domain([-2, -1, 0, 5, 10]).range(["#7E57C2", "#BDBDBD", "#fc8d59", "#ffffbf", "#91cf60"]);

var svg = d3.select("#container_visualization").append("svg")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

function init_get_json(params_filter = "") {
    d3.json("/api/all" + params_filter, function (data) {
        root = {
            "name": "Inicio",
            "root": true,
            "parent": null,
            "children": data
        };
        root.x0 = height / 2;
        root.y0 = 0;

        root.children.forEach(expand);
    });

}


function update(source) {

    // Compute the new tree layout.
    var nodes = tree.nodes(root);
    links = tree.links(nodes);

    // Normalize for fixed-depth.
    nodes.forEach(function (d) { d.y = d.depth * 180; });

    // Update the nodes…
    var node = svg.selectAll("g.node")
        .data(nodes, function (d) { return d.id || (d.id = ++i); });

    // Enter any new nodes at the parent's previous position.
    var nodeEnter = node.enter().append("g")
        .attr("class", "node")
        .attr("transform", function (d) { return "translate(" + source.y0 + "," + source.x0 + ")"; });

    nodeEnter.append("circle")
        .attr("r", 1e-6)
        .style("fill", function (d) { return d._children ? "lightsteelblue" : "#fff"; })
        .on("click", click);


    nodeEnter.append("text")
        .attr("x", function (d) { return d.children || d._children ? -13 : -100; })
        .attr("y", function (d) { return d.children || d._children ? -13 : -20; })
        .attr("text-anchor", function (d) { return d.children || d._children ? "end" : "start"; })
        .text(function (d) { return d.name; })
        .style("fill-opacity", 1e-6);

    // Transition nodes to their new position.
    var nodeUpdate = node.transition()
        .duration(duration)
        .attr("transform", function (d) { return "translate(" + d.y + "," + d.x + ")"; });

    //atualiza a cor do nó de acordo com a nota ou se for um nó fim
    nodeUpdate.select("circle")
        .attr("r", 20)
        .style("fill", function (d) {
            if (d.node_evaluated == false) {
                /**
                 * se o nó não for avaliado a cor do nó fica branca e a sua média permanece a do nó pai
                 * ou seja, a média da turma permanece
                 */
                d.node_avg = d.parent.node_avg;
                return "white";
            }
            if (d.node_avg == null) {
                return "blue";
            }
            var tag_color_blind = d3.select("#color_blind").property("checked");

            if (tag_color_blind) {
                return color_blind(d.node_avg)
            }
            return colors(d.node_avg);
        });

    nodeUpdate.select("text")
        .style("fill-opacity", 1);

    // Transition exiting nodes to the parent's new position.
    var nodeExit = node.exit().transition()
        .duration(duration)
        .attr("transform", function (d) { return "translate(" + source.y + "," + source.x + ")"; })
        .remove();

    nodeExit.select("circle")
        .attr("r", 1e-6);

    nodeExit.select("text")
        .style("fill-opacity", 1e-6);

    // Update the links…
    var link = svg.selectAll("path.link")
        .data(links, function (d) { return d.target.id; });


    // Enter any new links at the parent's previous position.
    // set as cores do link de acordo com a média das notas dos alunos
    link.enter().insert("path", "g")
        .attr("class", "link")
        .attr("d", function (d) {
            var o = { x: source.x0, y: source.y0 };
            return diagonal({ source: o, target: o });
        })
        .style("stroke", function (d, i) {
            var avg;
            if (d.target.node_evaluated == false) {
                /**
                 * se o nó não for avaliado o link é a cor do link do pai
                 * ou seja, a média da turma permanece
                 */
                avg = d.target.parent.node_avg;
            }
            if (d.target.node_avg == null) {
                return "blue";
            }
            if (d.target.node_end) {
                /**
                 * Se for um nó fim, o link permanece com a cor do pai seu pai
                 */
                return avg = d.target.parent.node_avg;
            }
            avg = d.target.node_avg;
            
            var tag_color_blind = d3.select("#color_blind").property("checked");

            if (tag_color_blind) {
                return color_blind(avg)
            }
            return colors(avg);
        });

    // Transition links to their new position.
    link.transition()
        .duration(duration)
        .attr("d", diagonal);

    // Transition exiting nodes to the parent's new position.
    link.exit().transition()
        .duration(duration)
        .attr("d", function (d) {
            var o = { x: source.x, y: source.y };
            return diagonal({ source: o, target: o });
        })
        .remove();

    // Stash the old positions for transition.
    nodes.forEach(function (d) {
        d.x0 = d.x;
        d.y0 = d.y;
    });
}

// Toggle children on click.
function click(d) {
    if (d.classe_id || d.root) {
        if (d.children) {
            d._children = d.children;
            d.children = null;
        } else {
            if (d._children != null) {
                d.children = d._children;
                d._children = null;
                d.children.forEach(expand);
            }
        }
        update(d);
    } else {
        //código para mostrar os gráficos
        tooltip_tablle(d);
    }
}

/**
 * 
 * expandir todos os nós 
 */
function expand(d) {
    if (d.classe_id || d.root) {
        if (d.children) {
            d._children = d.children;
            d.children = null;
        } else {
            if (d._children != null) {
                d.children = d._children;
                d._children = null;
                d.children.forEach(expand);
            }
        }
        update(d);
    } else {
        var params_filter = get_params_filter()
        d3.json("/api/node/" + d.node_id + params_filter, function (data) {
            d.children = data;
            d._children = null;
            d.children.forEach(expand);
            update(d);
        });
    }
}

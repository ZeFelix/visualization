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
var colors = d3.scale.linear().domain([0, 5, 10]).range(["#DD2C00", "#FFD600", "#1B5E20"]);

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


d3.json("/api/all", function (data) {
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

//div tooltip
var div = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

// d3.select(self.frameElement).style("height", "500px");

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
        .attr("transform", function (d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
        .on("click", click)
        .on("mouseover", function (d) {
            var info_students;
            if (d.classe_id) {
                info_students = "A turma possui: " + d.students_quantity + " Alunos. <br/>";
            } else {
                if (d.students) {
                    info_students = "Estudantes presentes na fase:<br/> ";
                    d.students.forEach(function (student) {
                        info_students = info_students.concat(student.name).concat("<br/>");
                    });
                }
            }
            div.transition()
                .duration(200)
                .style("opacity", .9);
            div.html(info_students)
                .style("left", (d3.event.pageX - 70) + "px")
                .style("top", (d3.event.pageY - 60) + "px");
        }).on("mouseout", function (d) {
            div.transition()
                .duration(500)
                .style("opacity", 0);
        });

    nodeEnter.append("circle")
        .attr("r", 1e-6)
        .style("fill", function (d) { return d._children ? "lightsteelblue" : "#fff"; });


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

    nodeUpdate.select("circle")
        .attr("r", 20)
        .style("fill", function (d) {
            if (d.node_avg == null) {
                return "blue";
            }
            return colors(d.node_avg)
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
    link.enter().insert("path", "g")
        .attr("class", "link")
        .attr("d", function (d) {
            var o = { x: source.x0, y: source.y0 };
            return diagonal({ source: o, target: o });
        })
        .style("stroke", function (d, i) {
            if (d.target.node_avg == null) {
                return "blue";
            }
            return colors(d.target.node_avg);
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
        console.log("treta")
    }
}

// expandir todos os nós
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
        d3.json("/api/node/" + d.node_id, function (data) {
            d.children = data;
            d._children = null;
            d.children.forEach(expand);
            update(d);
        });
    }
}



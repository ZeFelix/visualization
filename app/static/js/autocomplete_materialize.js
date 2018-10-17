/**
 * node_id e student_id
 */
d3.json('/api/gantt/1/1', function (err, data) {
    console.log(data)
    create_graph(data.context)
});

function generator_autocomplete(data) {
    $('input.autocomplete').autocomplete({
        data : data,
        // data: {
        //     "Apple": null,
        //     "Microsoft": null,
        //     "Google": 'https://placehold.it/250x250'
        // },
    });
}

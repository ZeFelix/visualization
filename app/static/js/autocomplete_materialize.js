/**
 * user_teacher_id
 */
d3.json('/api/gantt/teacher/'+ d3.select("#user_teacher_id").attr("value"), function (err, data) {
    console.log(data);
    generator_autocomplete(data.students)
});

function generator_autocomplete(data) {
    console.log(data)
    var dict = {};
    data.forEach(element => {
        dict["Matrucula: "+element.pk + ", "+element.name] = null
    });
    $('input.autocomplete').autocomplete({
        data : dict,
    });
}

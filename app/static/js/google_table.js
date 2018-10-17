function create_table() {
    google.charts.load('current', { 'packages': ['table'] });
    google.charts.setOnLoadCallback(drawTable);

    function drawTable() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Name');
        data.addColumn('number', 'Salary');
        data.addColumn('boolean', 'Full Time Employee');
        data.addColumn('boolean', 'Full Time Employee');
        data.addRows([
            ['Mike', { v: 10000, f: '$10,000' }, true,true],
            ['Jim', { v: 8000, f: '$8,000' }, false,true],
            ['Alice', { v: 12500, f: '$12,500' }, true,false],
            ['Bob', { v: 7000, f: '$7,000' }, true,true],
            ['Mike', { v: 10000, f: '$10,000' }, true,false],
        ]);

        var table = new google.visualization.Table(document.getElementById('table_div'));

        table.draw(data, { showRowNumber: true, width: '100%', height: '100%' });
    }
}

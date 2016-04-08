

$(document).ready(function() {
	chart = document.getElementById('chart');
	google.setOnLoadCallback(drawVisualization);
})


function drawVisualization() {
    var data_matrix = []

    for (i=0; i < dataSeconds.length; i++) {
        var dataCol = [dataTimestamps[i], dataSeconds[i]];
        data_matrix.push(dataCol)
    }

    renderGraph(data_matrix, "Seconds")
}

function updateCharts(e) {
	var isChecked = $(e).is(":checked");

	var data_matrix = []
	var vLegend = "";
	if (isChecked) {
	    for (i=0; i < dataSeconds.length; i++) {
	        var dataCol = [dataTimestamps[i], (dataSeconds[i]/60)];
	        data_matrix.push(dataCol)
	    }
	    vLegend = "Minutes"
	} else {
		for (i=0; i < dataSeconds.length; i++) {
	        var dataCol = [dataTimestamps[i], (dataSeconds[i])];
	        data_matrix.push(dataCol)
	    }
	    vLegend = "Seconds"
	}
    renderGraph(data_matrix, vLegend)
}

function renderGraph(data_matrix, vLegend) {
	var data = new google.visualization.DataTable();
	data.addColumn('timeofday', 'Time of Day');
    data.addColumn('number', 'Respond time');

    data.addRows(data_matrix)

    var options = {
		title: 'Push notifications recieved throught the day',
		hAxis: {
			title: "Time of day",
            viewWindow: {
	            min: [0, 0, 0],
	            max: [24, 0, 0]
          	},
          	maxValue:[24,59,59]

        },
        vAxis: {
        	title: vLegend,
        	format: '0'
        },
		height: 450,
		trendlines: { 0: {} }    // Draw a trendline for data series 0.
	};
	if( $(chart).is(':empty')) {
		chart = new google.visualization.ScatterChart(chart);
	}
	//chart = new google.visualization.ScatterChart(document.getElementById("chart"));
  	chart.draw(data, options);
}
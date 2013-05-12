var selectedSeverityLevel = 5;
var colors = {};
colors[0] = "#000000";
colors[1] = "#000000";
colors[2] = "#000000";
colors[3] = "#000000";
colors[4] = "#000000";
colors[5] = "#0000FF";
colors[6] = "#000000";
colors[7] = "#000000";

var data = {};
var totalPoints = 300;
var latest_timestamp;
var host;
var timeout;

function initializeGraph(){
    latest_timestamp = 0
    data[0] = [];
    data[1] = [];
    data[2] = [];
    data[3] = [];
    data[4] = [];
    data[5] = [];
    data[6] = [];
    data[7] = [];
}

function getLogData() {
    
    for(var severity_level in data){
        if (data[severity_level].length == 0){
            while( data[severity_level].length < totalPoints){
                data[severity_level].push(0);
            }
        }else if (data[severity_level].length == totalPoints){
            data[severity_level] = data[severity_level].slice(1);
        }
    }
    
    $.get("/events/gettotalseverity/", {latest_timestamp:latest_timestamp, host:host}, function(severity){
        latest_timestamp = severity['latest_timestamp'];
        for (var i = 0; i < 8; ++i){
            if (severity[host]){
                data[i].push(severity[host][i]);
            }else{
                data[i].push(0);
            }
        }
    });    

    // Zip the generated y values with the x values

    var res = {};
    for (var severity_level in data){
        res[severity_level] = [];
        for (var i = 0; i < data[severity_level].length; ++i) {
            res[severity_level].push([i, data[severity_level][i]]);
        }
    }
    return res;
}


var updateInterval = 1000;

function update() {
    graphData = getLogData();
    var plot = $.plot("#graph", [{data:graphData[selectedSeverityLevel], color:colors[selectedSeverityLevel], fill:true, show:true}], {
        series: {
            shadowSize: 0
        },
        xaxis: {
            show: false
        },
        legend: {
            show: true
        }
    });
    timeout = setTimeout(update, updateInterval);
}




$(document).ready(function(){
    $("#severityLevel").change(function(){
        selectedSeverityLevel = parseInt($(this).val());
    });
    $(function() {
        $( "#selectable" ).selectable({
            selected: function(event, ui){
                var selectedHost = ui.selected.innerHTML;
                if  (host != selectedHost){
                    host = selectedHost
                    clearTimeout(timeout)
                    initializeGraph();
                    update();
                }
            }
        });
    });
    $(".hosts:first").addClass("ui-selected");
    host = $(".hosts:first").text();

    initializeGraph();
    update();
});

var selectedSeverityLevel = 5;
$(function() {
        // We use an inline data source in the example, usually data would
        // be fetched from a server

        var data = {};
        var totalPoints = 300;
        var latest_timestamp = 0
        var host = "127.0.0.1";

        data[0] = [];
        data[1] = [];
        data[2] = [];
        data[3] = [];
        data[4] = [];
        data[5] = [];
        data[6] = [];
        data[7] = [];

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
                data[0].push((severity[host]) ? severity[host][0] : 0);
                data[1].push((severity[host]) ? severity[host][1] : 0);
                data[2].push((severity[host]) ? severity[host][2] : 0);
                data[3].push((severity[host]) ? severity[host][3] : 0);
                data[4].push((severity[host]) ? severity[host][4] : 0);
                data[5].push((severity[host]) ? severity[host][5] : 0);
                data[6].push((severity[host]) ? severity[host][6] : 0);
                data[7].push((severity[host]) ? severity[host][7] : 0);
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
            var plot = $.plot("#graph", [graphData[selectedSeverityLevel]], {
                series: {
                    shadowSize: 0
                },
                xaxis: {
                    show: false
                }
            });
            setTimeout(update, updateInterval);
        }

        update();

});

$(document).ready(function(){
    $("#severityLevel").change(function(){
        selectedSeverityLevel = parseInt($(this).val());
    });
});

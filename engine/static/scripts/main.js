//        'https://cdn.rawgit.com/highcharts/highcharts/v6.0.5/samples/data/usdeur.json',
var host = "http://localhost:5000"

$(document).ready(function () {

    $.getJSON(
        host+"/api/graph1",
        function (data) {
    
            Highcharts.chart('graph1', {
                legend: {
                    enabled: true
                },

                chart: {
                    zoomType: 'x'
                },
                title: {
                    text: 'News Articles Sentiment'
                },
                subtitle: {
                    text: document.ontouchstart === undefined ?
                            'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                },
                xAxis: {
                    type: 'datetime'
                },
                yAxis: {
                    title: {
                        text: 'Number of News Articles'
                    }
                },
                legend: {
                    enabled: false
                },
                series: [
                {
                    type: 'area',
                    name: 'Very Negative News',
                    data: data.vneg,
                    color: '#FF0000',
                    fillOpacity: 0.6
                },
                {
                    type: 'area',
                    name: 'Negative News',
                    data: data.neg,
                    color:'#ff7474',
                     fillOpacity: 0.5
                },
                    {
                    type: 'area',
                    name: 'Positive News',
                    data: data.pos,
                    color: '#00d4ff',
                     fillOpacity: 0.3
                },
                {
                    type: 'area',
                    name: 'Very Positive News',
                    data: data.vpos,
                    color:'#0000FF',
                     fillOpacity: 0.3
                }
                
                ]
            });
        }
);
   
});
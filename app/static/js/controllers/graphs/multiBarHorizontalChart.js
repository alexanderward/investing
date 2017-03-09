//http://krispo.github.io/angular-nvd3/#/
app.controller('multiBarHorizontalChart', function($scope){

    $scope.options = {
        title: {
                enable: true,
                text: 'Title for Line Chart'
            },
            subtitle: {
                enable: true,
                text: 'Subtitle for simple line chart. Lorem ipsum dolor sit amet, at eam blandit sadipscing, vim adhuc sanctus disputando ex, cu usu affert alienum urbanitas.',
                css: {
                    'text-align': 'center',
                    'margin': '10px 13px 0px 7px'
                }
            },
            caption: {
                enable: true,
                html: '<b>Figure 1.</b> Lorem ipsum dolor sit amet, at eam blandit sadipscing, <span style="text-decoration: underline;">vim adhuc sanctus disputando ex</span>, cu usu affert alienum urbanitas. <i>Cum in purto erat, mea ne nominavi persecuti reformidans.</i> Docendi blandit abhorreant ea has, minim tantas alterum pro eu. <span style="color: darkred;">Exerci graeci ad vix, elit tacimates ea duo</span>. Id mel eruditi fuisset. Stet vidit patrioque in pro, eum ex veri verterem abhorreant, id unum oportere intellegam nec<sup>[1, <a href="https://github.com/krispo/angular-nvd3" target="_blank">2</a>, 3]</sup>.',
                css: {
                    'text-align': 'justify',
                    'margin': '10px 13px 0px 7px'
                }
            },
            chart: {
                type: 'multiBarHorizontalChart',
                height: 450,
                x: function(d){return d.label;},
                y: function(d){return d.value;},
                showControls: true,
                showValues: true,
                duration: 500,
                xAxis: {
                    showMaxMin: false
                },
                yAxis: {
                    axisLabel: 'Symbol Last Close | Growth Rate',
                    tickFormat: function(d){
                        return d3.format(',.2f')(d);
                    }
                }
            }
        };

    $scope.data = [
        {
            "key": "Series1",
            "color": "#d62728",
            "values": [
                {
                    "label" : "Group A" ,
                    "value" : -1.8746444827653
                } ,
                {
                    "label" : "Group B" ,
                    "value" : -8.0961543492239
                } ,
                {
                    "label" : "Group C" ,
                    "value" : -0.57072943117674
                } ,
                {
                    "label" : "Group D" ,
                    "value" : -2.4174010336624
                } ,
                {
                    "label" : "Group E" ,
                    "value" : -0.72009071426284
                } ,
                {
                    "label" : "Group F" ,
                    "value" : -0.77154485523777
                } ,
                {
                    "label" : "Group G" ,
                    "value" : -0.90152097798131
                } ,
                {
                    "label" : "Group H" ,
                    "value" : -0.91445417330854
                } ,
                {
                    "label" : "Group I" ,
                    "value" : -0.055746319141851
                }
            ]
        },
        {
            "key": "Series2",
            "color": "#1f77b4",
            "values": [
                {
                    "label" : "Group A" ,
                    "value" : 25.307646510375
                } ,
                {
                    "label" : "Group B" ,
                    "value" : 16.756779544553
                } ,
                {
                    "label" : "Group C" ,
                    "value" : 18.451534877007
                } ,
                {
                    "label" : "Group D" ,
                    "value" : 8.6142352811805
                } ,
                {
                    "label" : "Group E" ,
                    "value" : 7.8082472075876
                } ,
                {
                    "label" : "Group F" ,
                    "value" : 5.259101026956
                } ,
                {
                    "label" : "Group G" ,
                    "value" : 0.30947953487127
                } ,
                {
                    "label" : "Group H" ,
                    "value" : 0
                } ,
                {
                    "label" : "Group I" ,
                    "value" : 0
                }
            ]
        }
    ]

});
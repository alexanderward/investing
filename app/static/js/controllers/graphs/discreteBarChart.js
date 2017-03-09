//http://krispo.github.io/angular-nvd3/#/
app.controller('discreteBarChart', function($scope, SymbolsService){
    var topNumber = 10;
    var title = 'Top ' + topNumber + ' Stocks - Growth Rate ';
    $scope.data = [{key: title, values: []}];

    $scope.options = {
        title: {
                enable: true,
                text: title
            },
        subtitle: {
            enable: true,
            text: '',
            css: {
                'text-align': 'center',
                'margin': '10px 13px 0px 7px'
            }
        },
        chart: {
            type: 'discreteBarChart',
            height: 450,
            margin : {
                top: 20,
                right: 20,
                bottom: 50,
                left: 55
            },
            x: function(d){return d.label;},
            y: function(d){return d.value + (1e-10);},
            showValues: true,
            valueFormat: function(d){
                return d3.format(',.4f')(d);
            },
            duration: 500,
            xAxis: {
                axisLabel: 'Stocks'
            },
            yAxis: {
                axisLabel: 'Growth Rate',
                axisLabelDistance: -10
            }
        }
        };


    function fetchData() {
        SymbolsService.getTopGrowthRate(topNumber)
            .then(function (data) {
                $scope.symbols = data;
                var graphResults = [];
                $.each(data, function (index, symbol_object) {
                    graphResults.push({label: symbol_object.symbol, 'value': symbol_object.growth_rate});
                });

                $scope.data[0].values = graphResults;

            }, function (error) {
                console.log(error)
            });

    }
    fetchData();


});
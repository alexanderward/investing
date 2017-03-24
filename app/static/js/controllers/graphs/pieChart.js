//http://krispo.github.io/angular-nvd3/#/
app.controller('pieBarChart', function($scope, DashboardService){

    $scope.init = function(title)
        {
        $scope.title = title;
        $scope.data = [
            {
                key: "One",
                y: 5
            },
            {
                key: "Two",
                y: 2
            },
            {
                key: "Three",
                y: 9
            },
            {
                key: "Four",
                y: 7
            },
            {
                key: "Five",
                y: 4
            },
            {
                key: "Six",
                y: 3
            },
            {
                key: "Seven",
                y: .5
            }
        ];
        };
    // $scope.data = [{key: title, values: []}];

    $scope.options = {
        title: {
                enable: true,
                text: $scope.title
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
            type: 'pieChart',
                height: 500,
                x: function(d){return d.key;},
                y: function(d){return d.y;},
                showLabels: true,
                duration: 500,
                labelThreshold: 0.01,
                labelSunbeamLayout: true,
                legendPosition: 'bottom',
                legend: {
                    margin: {
                        top: 5,
                        right: 35,
                        bottom: 5,
                        left: 0
                    }
                }
            }
        };




    // function fetchData() {
    //     SymbolsService.getTopGrowthRate(topNumber)
    //         .then(function (data) {
    //             $scope.symbols = data;
    //             var graphResults = [];
    //             $.each(data, function (index, symbol_object) {
    //                 graphResults.push({label: symbol_object.symbol, 'value': symbol_object.growth_rate});
    //             });
    //
    //             $scope.data[0].values = graphResults;
    //
    //         }, function (error) {
    //             console.log(error)
    //         });
    //
    // }
    // fetchData();


});
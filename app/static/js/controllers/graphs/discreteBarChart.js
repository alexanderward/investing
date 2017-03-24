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
app.controller('DemoController', [
    '$scope',
    function ($scope) {

        $scope.player = {
            gold: 100
        };

        $scope.items = [
            { name: 'Small Health Potion', cost: 4 },
            { name: 'Small Mana Potion', cost: 5 },
            { name: 'Iron Short Sword', cost: 12 }
        ];

        $scope.menuOptions = [
            ['Buy', function ($itemScope) {
                $scope.player.gold -= $itemScope.item.cost;
            }],
            null,
            ['Sell', function ($itemScope) {
                $scope.player.gold += $itemScope.item.cost;
            }, function ($itemScope) {
                return $itemScope.item.name.match(/Iron/) == null;
            }],
            null,
            ['More...', [
                ['Alert Cost', function ($itemScope) {
                    alert($itemScope.item.cost);
                }],
                ['Alert Player Gold', function ($itemScope) {
                    alert($scope.player.gold);
                }]
            ]]
        ];

        $scope.otherMenuOptions = [
            ['Favorite Color', function ($itemScope, event, modelValue, text, $li) {
                alert(modelValue);
                console.info($itemScope);
                console.info(event);
                console.info(modelValue);
                console.info(text);
                console.info($li);
            }]
        ];

        var customHtml = '<div style="cursor: pointer; background-color: pink"><i class="glyphicon glyphicon-ok-sign"></i> Testing Custom </div>';
        var customItem = {
            html: customHtml, click: function ($itemScope, event, modelValue, text, $li) {
                alert("custom html");
                console.info($itemScope);
                console.info(event);
                console.info(modelValue);
                console.info(text);
                console.info($li);
            }
        };

        var customDisabledItem = {
            html: "I'm Disabled",
            click: function ($itemScope, $event, value) {
                console.log("expect to never get here!");
            },
            enabled: function ($itemScope, $event, value) {
                console.log("can't click");
                return false;
            }
        };

        $scope.customHTMLOptions = [customItem, customDisabledItem,
            ['Example 1', function ($itemScope, $event, value) {
                alert("Example 1");
            }]
        ];

    }
]);
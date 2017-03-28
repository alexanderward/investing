//http://krispo.github.io/angular-nvd3/#/

app.directive('tableGraph', function(SymbolsService, NgTableParams, $filter){
    function has(object, key) {
      return object ? hasOwnProperty.call(object, key) : false;
   }
    var graphTableMap = {
        growthRate: {
            ordering: '-growth_rate',
            promise: function(ordering, filters, paginationCount, pageNumber){
                return SymbolsService.list(ordering, filters, paginationCount, pageNumber)
            },
            table:{
                    columns : [
                        // http://plnkr.co/edit/lO8FhO?p=preview  Also allows subfield for nested objects
                        { title: 'Symbol', field: 'symbol', visible: true, filterType: 'string'},
                        { title: 'Company', field: 'company', visible: true, filterType: 'string'},
                        { title: 'Sector', field: 'sector', visible: true, filterType: 'string'},
                        { title: 'Industry', field: 'industry', visible: true, filterType: 'string'},
                        { title: 'Growth Rate', field: 'growth_rate', visible: true, filterType: 'number'},
                        { title: 'Market Cap', field: 'market_cap', visible: true, filterType: 'number'}
                    ]
            },
            graphs: {
                pie: {
                    options: function(caption){
                        return {
                            caption: {
                                enable: true,
                                text: caption,
                                css: {
                                    width: null,
                                    textAlign: 'center'
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
                        }
                    },
                    dataConversion:function(data){
                        var graphResults = [];
                        $.each(data, function (index, symbol_object) {
                            graphResults.push({key: symbol_object.symbol, 'y': symbol_object.growth_rate});
                        });
                        return graphResults
                    },
                    faIcon: 'fa-pie-chart'
                },
                discreteBar: {
                    options: function(caption){
                return {
                    caption: {
                        enable: true,
                        text: caption,
                        css: {
                            width: null,
                            textAlign: 'center'
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
                }
            },
                    dataConversion: function(data){
                    var graphResults = [];
                    $.each(data, function (index, symbol_object) {
                        graphResults.push({label: symbol_object.symbol, 'value': symbol_object.growth_rate});
                    });
                    return [{key: '', values: graphResults}]
                },
                    faIcon: 'fa-bar-chart'
                }
            }
        }
    };

    return {
        restrict: 'E', //E = element, A = attribute, C = class, M = comment
        replace : true,
        controller: function($scope, $element, $attrs){
            $scope.reset = function () {
                $scope.tableParams.parameters({sorting:[]});
                $scope.tableParams.reload();
                $scope.tableParams.page(1);
            };
            $scope.isActiveGraph = function(item) {
                return $scope.activeGraph === item;
            };
            $scope.toggleColumns = function (item) {
                item.visible = !item.visible;
                return item.visible;
            };
            $scope.filterColumn = function(){
                var filters = [];
                $.each($scope.columns, function(index, column){
                     if (column.filter != null && column.filter)
                         if (column.filterType == 'string')
                             filters.push(column.field+'='+column.filter);
                         else if (column.filterType == 'number'){
                             if (column.filter.min)
                                filters.push('min_'+column.field+'='+column.filter.min);
                             if (column.filter.max)
                                filters.push('max_'+column.field+'='+column.filter.max);
                         }
                });
                $scope.filters = filters.join("&");
                $scope.tableParams.reload();
                $scope.tableParams.page(1);
            };

            $scope.removeFilters = function(){
                $.each($scope.columns, function(index, column){
                     column.filter = null;
                });
                $scope.filters = null;
                $scope.tableParams.reload();
                $scope.tableParams.page(1);
            };

            $scope.changeGraph = function(graph){
                $scope.graphType = graph.type;
                $scope.activeGraph = graph.type;
                var dataSource = graphTableMap[$scope.source];
                $scope.graphDetails = dataSource.graphs[$scope.graphType];
                $scope.reset();
            }

        },
        controllerAs: 'vm',
        link: function($scope, $element, $attrs, $ctrl) {
            $scope.source = $attrs.source;
            $scope.title = $attrs.title;
            var caption = $attrs.caption;

            if (! has(graphTableMap, $scope.source)){
                throw new TypeError("Must include valid graph source.  Valid options: " + Object.keys(graphTableMap).join(","));
            }
            if (typeof $attrs.default == 'undefined'){
                $scope.graphType = Object.keys(graphTableMap)[0];
            }else{
                $scope.graphType = $attrs.default;
            }

            var dataSource = graphTableMap[$scope.source];
            $scope.graphDetails = dataSource.graphs[$scope.graphType];

            if (typeof $scope.graphDetails == 'undefined') {
                throw new TypeError("Must include valid default type.  Valid options: " + Object.keys(dataSource.graphs).join(","));
            }

            var graphButtons = [];
            $scope.activeGraph = $scope.graphType;
            $.each(dataSource.graphs, function (graphName, graphDetails) {
                graphButtons.push({type: graphName, icon: graphDetails.faIcon});
            });

            $scope.graphs = graphButtons;

            $scope.columns = dataSource.table.columns;

            $scope.tableParams = new NgTableParams(
                {},
                {
                // total: 0, // length of data
                getData: function(params) {
                    $scope.graphData = [];
                    var orderBy;
                    if (params.orderBy().length == 0){
                        orderBy = dataSource.ordering;
                    }else{
                        orderBy = params.orderBy();
                    }
                    var pageNumber = params.page();

                    return dataSource.promise(orderBy, $scope.filters, params.count(), pageNumber).then(function (data) {
                        params.total(data.count);
                        $scope.graphData = data.results;
                        $scope.options = $scope.graphDetails.options(caption);
                        if (typeof $scope.graphDetails.dataConversion != 'undefined')
                            $scope.graphData = $scope.graphDetails.dataConversion($scope.graphData);

                        return data.results;

                    }, function (error) {
                        console.log(error)
                    });
                }
            });


        },
        scope: true,
        templateUrl: '/partials/directives/graph-table.html'
    }
});
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

// <article class="col-sm-12 col-md-12 col-lg-4 sortable-grid ui-sortable">
//                 <!-- new widget -->
//                 <div class="jarviswidget" id="wid-id-0" data-widget-togglebutton="false" data-widget-editbutton="false" data-widget-fullscreenbutton="false" data-widget-colorbutton="false" data-widget-deletebutton="false">
//
//                     <header>
//                         <span class="widget-icon"> <i class="glyphicon glyphicon-stats txt-color-darken"></i> </span>
//                         <h2>Top Growth </h2>
//                     </header>
//
//                     <!-- widget div-->
//                     <div class="no-padding">
//                         <!-- widget edit box -->
//                         <div class="jarviswidget-editbox">
//
//                             test
//                         </div>
//                         <!-- end widget edit box -->
//
//                         <div class="widget-body">
//                             <div ng-controller="discreteBarChart" api="api" config="{refreshDataOnly: true, deepWatchData: true}">
//                                 <nvd3 options="options" data="data"></nvd3>
//                             </div>
//                         </div>
//
//                     </div>
//                     <!-- end widget div -->
//                 </div>
//                 <!-- end widget -->
//
//             </article>
// <article class="col-sm-12 col-md-12 col-lg-4 sortable-grid ui-sortable">
//     <!-- new widget -->
//     <div class="jarviswidget" id="wid-id-0" data-widget-togglebutton="false" data-widget-editbutton="false" data-widget-fullscreenbutton="false" data-widget-colorbutton="false" data-widget-deletebutton="false">
//
//         <header>
//             <span class="widget-icon"> <i class="glyphicon glyphicon-stats txt-color-darken"></i> </span>
//             <h2>Sector Diversification</h2>
//         </header>
//
//         <!-- widget div-->
//         <div class="no-padding">
//             <!-- widget edit box -->
//             <div class="jarviswidget-editbox">
//
//                 test
//             </div>
//             <!-- end widget edit box -->
//
//             <div class="widget-body">
//                 <div ng-controller="pieBarChart" api="api" config="{refreshDataOnly: true, deepWatchData: true}" ng-init="init('Diversification')">
//                     <nvd3 options="options" data="data"></nvd3>
//                 </div>
//             </div>
//
//         </div>
//         <!-- end widget div -->
//     </div>
//     <!-- end widget -->
//
// </article>
// <article class="col-sm-12 col-md-12 col-lg-4 sortable-grid ui-sortable">
//     <!-- new widget -->
//     <div class="jarviswidget" id="wid-id-0" data-widget-togglebutton="false" data-widget-editbutton="false" data-widget-fullscreenbutton="false" data-widget-colorbutton="false" data-widget-deletebutton="false">
//
//         <header>
//             <span class="widget-icon"> <i class="glyphicon glyphicon-stats txt-color-darken"></i> </span>
//             <h2>Top Growth </h2>
//         </header>
//
//         <!-- widget div-->
//         <div class="no-padding">
//             <!-- widget edit box -->
//             <div class="jarviswidget-editbox">
//
//                 test
//             </div>
//             <!-- end widget edit box -->
//
//             <div class="widget-body">
//                 <div ng-controller="discreteBarChart" api="api" config="{refreshDataOnly: true, deepWatchData: true}">
//                     <nvd3 options="options" data="data"></nvd3>
//                 </div>
//             </div>
//
//         </div>
//         <!-- end widget div -->
//     </div>
//     <!-- end widget -->
//
// </article>
//
// <article class="col-sm-12">
//     <!-- new widget -->
//     <div class="jarviswidget" id="wid-id-0" data-widget-togglebutton="false" data-widget-editbutton="false" data-widget-fullscreenbutton="false" data-widget-colorbutton="false" data-widget-deletebutton="false">
//
//         <header>
//             <span class="widget-icon"> <i class="glyphicon glyphicon-stats txt-color-darken"></i> </span>
//             <h2>Top Growth </h2>
//         </header>
//
//         <!-- widget div-->
//         <div class="no-padding">
//             <!-- widget edit box -->
//             <div class="jarviswidget-editbox">
//
//                 test
//             </div>
//             <!-- end widget edit box -->
//
//             <div class="widget-body">
//                 <div ng-controller="discreteBarChart" api="api" config="{refreshDataOnly: true, deepWatchData: true}">
//                     <nvd3 options="options" data="data"></nvd3>
//                 </div>
//             </div>
//
//         </div>
//         <!-- end widget div -->
//     </div>
//     <!-- end widget -->
//
// </article>
//
// <article class="col-sm-12">
//     <!-- new widget -->
//     <div class="jarviswidget" id="wid-id-0" data-widget-togglebutton="false" data-widget-editbutton="false" data-widget-fullscreenbutton="false" data-widget-colorbutton="false" data-widget-deletebutton="false">
//
//         <header>
//             <span class="widget-icon"> <i class="glyphicon glyphicon-stats txt-color-darken"></i> </span>
//             <h2>Top Growth </h2>
//         </header>
//
//         <!-- widget div-->
//         <div class="no-padding">
//             <!-- widget edit box -->
//             <div class="jarviswidget-editbox">
//
//                 test
//             </div>
//             <!-- end widget edit box -->
//
//             <div class="widget-body">
//                 <div ng-app="app" ng-controller="DemoController">
//                     <div>
//                         <strong>Gold: </strong>
//                         {{player.gold}}
//                     </div>
//                     <div class="list-group">
//                         <a href="#"
//                            class="list-group-item"
//                            ng-repeat="item in items"
//                            context-menu="menuOptions">
//                             <span class="badge">{{item.cost}}</span>
//                             {{item.name}}
//                         </a>
//                     </div>
//                     <button class="btn btn-default"
//                             context-menu="otherMenuOptions"
//                             model="'Red'">Right Click</button>
//
//                     <br/>
//                     <br/>
//                     <button class="btn btn-default"
//                             context-menu="otherMenuOptions"
//                             allow-event-propagation="true"
//                             model="'Blue'">Right Click allow event propagation</button>
//
//                     <br/>
//                     <br/>
//                     <button class="btn btn-default"
//                             context-menu="otherMenuOptions"
//                             context-menu-on="click"
//                             model="'Red'">Left Click</button>
//
//                     <br/>
//                     <br/>
//                     <button class="btn btn-default"
//                             context-menu="customHTMLOptions"
//                             >Custom HTML</button>
//
//                 </div>
//             </div>
//
//         </div>
//         <!-- end widget div -->
//     </div>
//     <!-- end widget -->
//
// </article>
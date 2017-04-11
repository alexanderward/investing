app.controller('LookupCtrl', function($scope, $stateParams, $state, NgTableParams){

    $scope.autoCompleteCallback = function(result){
        $scope.symbol = result;
        $scope.symbol.portfolio = {
            net:-50,
            absNet: 50.03,
            equity: 10.00,
            transactions: [
                {
                    type: 'buy',
                    text: 'limit buy',
                    average_price: 2.20,
                    quantity: 985,
                    timestamp: "2017-04-05T17:16:02.582898Z",
                    total: 985 * 2.20
                },
                {
                    type: 'sell',
                    text: 'limit sell',
                    average_price: 2.20,
                    quantity: 985,
                    timestamp: "2017-04-05T17:16:02.582898Z",
                    total: 985 * 2.20
                },
                {
                    type: 'buy',
                    text: 'limit buy',
                    average_price: 2.20,
                    quantity: 985,
                    timestamp: "2017-04-05T17:16:02.582898Z",
                    total: 985 * 2.20
                },
                {
                    type: 'sell',
                    text: 'limit sell',
                    average_price: 2.20,
                    quantity: 985,
                    timestamp: "2017-04-05T17:16:02.582898Z",
                    total: 985 * 2.20
                },
                {
                    type: 'buy',
                    text: 'limit buy',
                    average_price: 2.20,
                    quantity: 985,
                    timestamp: "2017-04-05T17:16:02.582898Z",
                    total: 985 * 2.20
                },
                {
                    type: 'sell',
                    text: 'limit sell',
                    average_price: 2.20,
                    quantity: 985,
                    timestamp: "2017-04-05T17:16:02.582898Z",
                    total: 985 * 2.20
                },
                {
                    type: 'buy',
                    text: 'limit buy',
                    average_price: 2.20,
                    quantity: 985,
                    timestamp: "2017-04-05T17:16:02.582898Z",
                    total: 985 * 2.20
                },
                {
                    type: 'sell',
                    text: 'limit sell',
                    average_price: 2.20,
                    quantity: 985,
                    timestamp: "2017-04-05T17:16:02.582898Z",
                    total: 985 * 2.20
                },
                {
                    type: 'buy',
                    text: 'limit buy',
                    average_price: 2.20,
                    quantity: 985,
                    timestamp: "2017-04-05T17:16:02.582898Z",
                    total: 985 * 2.20
                },
                {
                    type: 'sell',
                    text: 'limit sell',
                    average_price: 2.20,
                    quantity: 985,
                    timestamp: "2017-04-05T17:16:02.582898Z",
                    total: 985 * 2.20
                },
                {
                    type: 'buy',
                    text: 'limit buy',
                    average_price: 2.20,
                    quantity: 985,
                    timestamp: "2017-04-05T17:16:02.582898Z",
                    total: 985 * 2.20
                },
                {
                    type: 'sell',
                    text: 'limit sell',
                    average_price: 2.20,
                    quantity: 985,
                    timestamp: "2017-04-05T17:16:02.582898Z",
                    total: 985 * 2.20
                }
            ]
        };
    };

});
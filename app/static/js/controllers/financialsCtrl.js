app.controller('FinancialsCtrl', function($scope, $location, FinancialsService) {
    $scope.currentFinancials = {
        portfolio_value: null,
        available_funds: null,
        funds_held_for_orders: null
    };
    $scope.dailyChange = null;
    $scope.totalChange = null;
    FinancialsService.getCurrentFinancials()
        .then(function(data) {
                $scope.currentFinancials = data;
        }, function(error) {
               console.log(error)
    });


});
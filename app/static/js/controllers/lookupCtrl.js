app.controller('LookupCtrl', function($scope, $stateParams, $state){
    $scope.autoCompleteCallback = function(result){
        $scope.symbol = result.symbol;
    };


});
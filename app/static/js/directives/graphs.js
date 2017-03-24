//http://krispo.github.io/angular-nvd3/#/
app.controller('scratchController', function($scope){
    $scope.data = ['test', '1'];
});

app.directive('graph', function() {
    return function(scope, element, attrs){
        var data = scope[attrs['graph']];
        console.log(data);
    }

});

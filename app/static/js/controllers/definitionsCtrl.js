
app.controller('DefinitionsCtrl', function($scope, $stateParams, $state, DefinitionService){
    runAllCharts();
    pageSetUp();
    DefinitionService.getDefinitions()
        .then(function(data) {
                $scope.definitions = data;
        }, function(error) {
               console.log(error)
    });
});
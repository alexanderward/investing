app.controller('BreadcrumbCtrl', function($scope, $location) {
    var lookupTable = {
        '/': 'Dashboard',
        '/profile': 'Profile',
        '/analysis': 'Analysis',
        '/research': 'Research',
        '/dictionary': 'Dictionary',
        '/notes': 'Notes',
        '/links': 'Links'
    };

    $scope.breadcrumb = lookupTable[$location.path()];

    $scope.$on('$stateChangeSuccess', function() {
        $scope.breadcrumb = lookupTable[$location.path()];
    });
});
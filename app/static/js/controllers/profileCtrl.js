
app.controller('ProfileCtrl', function($scope, $stateParams, $state, ProfileService){

	ProfileService.getProfile()
        .then(function(data) {
                $scope.profile = data;
                console.log($scope.profile);
        }, function(error) {
               console.log(error)
    });

	$scope.updateProfile = function() {
        ProfileService.updateProfile($scope.profile)
        .then(function(data) {
            notificationPopup("Profile", 'Successfully updated profile', 'success', "fa fa-check");

        }, function(error) {
            notificationPopup("Profile", error, 'error', "fa fa-exclamation-circle");
        });
    };

});
app.factory('DefinitionService', function ($http, $q) {
        var base_url = '/api/definitions/';
        return {
            getDefinitions: function() {
                // the $http API is based on the deferred/promise APIs exposed by the $q service
                // so it returns a promise for us by default
                return $http.get(base_url)
                    .then(function(response) {
                        if (typeof response.data === 'object') {
                            return response.data;
                        } else {
                            // invalid response
                            return $q.reject(response.data);
                        }

                    }, function(response) {
                        // something went wrong
                        return $q.reject(response.data);
                    });
            }
        };
    });

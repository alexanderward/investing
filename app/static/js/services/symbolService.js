app.factory('SymbolsService', function ($http, $q) {
        var base_url = '/api/symbols/';
        return {
            list: function(ordering, paginationCount, pageNumber) {
                console.log(ordering);
                // the $http API is based on the deferred/promise APIs exposed by the $q service
                // so it returns a promise for us by default
                if (typeof paginationCount === 'undefined'){
                    paginationCount = 20;
                }
                if (typeof pageNumber === 'undefined'){
                    pageNumber = 1;
                }

                return $http.get(base_url + '?ordering=' + ordering + '&count=' + paginationCount + '&page=' + pageNumber)
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
            },
        };
    });

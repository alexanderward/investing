'use strict';
var app = angular.module('app', ['ngWebsocket', 'ngRoute', 'ui.router', 'ui.bootstrap', 'nvd3', 'ui.bootstrap.contextMenu'])
    .config(['$urlRouterProvider','$stateProvider', function($urlRouterProvider, $stateProvider) {
        $urlRouterProvider.otherwise('/');
        $stateProvider
            .state('profile', {
                url: '/profile',
                templateUrl: '/partials/profile.html',
                controller: 'ProfileCtrl',
                params: {
                    notification: null
                }
            })
            .state('dashboardOverview', {
                url: '/',
                templateUrl: '/partials/dashboard-overview.html',
                controller: 'DashboardCtrl',
                params: {
                    notification: null
                }
            })
            .state('analysis', {
                url: '/analysis',
                templateUrl: '/partials/analysis.html',
                controller: 'AnalysisCtrl',
                params: {
                    notification: null
                }
            })
            .state('research', {
                url: '/research',
                templateUrl: '/partials/research.html',
                controller: 'ResearchCtrl',
                params: {
                    notification: null
                }
            })
            .state('dictionary', {
                url: '/dictionary',
                templateUrl: '/partials/dictionary.html',
                controller: 'DefinitionsCtrl',
                params: {
                    notification: null
                }
            })
            .state('notes', {
                url: '/notes',
                templateUrl: '/partials/notes.html',
                controller: 'NotesCtrl',
                params: {
                    notification: null
                }
            })
            .state('links', {
                url: '/links',
                templateUrl: '/partials/links.html',
                controller: 'LinksCtrl',
                params: {
                    notification: null
                }
            })

        ;
    }]);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);
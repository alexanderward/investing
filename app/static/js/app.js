'use strict';
var app = angular.module('app', ['ngWebsocket', 'ngRoute', 'ui.router', 'ui.bootstrap'])
    .config(['$urlRouterProvider','$stateProvider', function($urlRouterProvider, $stateProvider) {
        $urlRouterProvider.otherwise('/');
        $stateProvider
            .state('dashboardOverview', {
                url: '/',
                templateUrl: '/partials/dashboard-overview.html',
                controller: 'DashboardCtrl',
                params: {
                    notification: null
                }
            })
            .state('dashboardTransactions', {
                
                templateUrl: '/partials/dashboard-transactions.html',
                controller: 'DashboardTransactionsCtrl',
                params: {
                    notification: null
                }
            })
            .state('analyticsStrategy1', {
                
                templateUrl: '/partials/analytics-strategy1.html',
                controller: 'DashboardTransactionsCtrl',
                params: {
                    notification: null
                }
            })
            .state('analyticsStrategy2', {
                
                templateUrl: '/partials/analytics-strategy1.html',
                controller: 'DashboardTransactionsCtrl',
                params: {
                    notification: null
                }
            })
            .state('analyticsStrategy3', {
                
                templateUrl: '/partials/analytics-strategy1.html',
                controller: 'DashboardTransactionsCtrl',
                params: {
                    notification: null
                }
            })
            .state('reportMethod1', {
                
                templateUrl: '/partials/research-method1.html',
                controller: 'DashboardTransactionsCtrl',
                params: {
                    notification: null
                }
            })
            .state('reportMethod2', {
                
                templateUrl: '/partials/research-method1.html',
                controller: 'DashboardTransactionsCtrl',
                params: {
                    notification: null
                }
            })
            .state('reportMethod3', {

                templateUrl: '/partials/research-method1.html',
                controller: 'DashboardTransactionsCtrl',
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
            });
    }]);
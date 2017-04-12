var InformationApp=angular.module("InformationApp", [
                    'ngSanitize',
                    'ui.bootstrap',
                   'App.course',
                   'App.modal',
                   'App.student',
                   'App.class',
                   'App.qa',
                    'App.grade',
                   ]);


  InformationApp.directive('loadContent', function($http, $compile) {
        return {
            link: function ($scope, element, attrs) {

                $scope.loadContentpanel = function($event) {
                    console.log($event)
                    var url = $event;
                    console.log(url)
                    if (url != '/summary/information') {
                        url = ($("#"+$event.currentTarget.id).attr('realvalue'));
                        console.log(url)

                    };
                     $http.get(url).success(function (response) {
                        $compile($('.contentpanel').html(response))($scope);

                });

            }
        }
        }
    });
   InformationApp.controller('HomeCtrl',['$scope',function($scope){
        $scope.showSubMenu = '';
        $scope.openSubMenu = function($event) {
        value=$event.currentTarget.id
          if ($event.currentTarget.id == $scope.showSubMenu) {
            $scope.showSubMenu = null;
          return;
          }
          $scope.showSubMenu = $event.currentTarget.id;

        }
   }]);
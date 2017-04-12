var RegisterModel=angular.module('Register',[]);
 RegisterModel.controller('StudentCtrl', ['$scope' , function($scope) {
              $scope.ok = function() {
                 register_student();
              };

 }]);
 RegisterModel.controller('TeacherCtrl', ['$scope', function($scope) {
              $scope.create = function() {
                 register_teacher();
              };

 }]);
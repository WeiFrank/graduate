var CourseModalDemo = angular.module('App.course', []);
   CourseModalDemo.controller('CourseModalCtrl', ['$scope','$modal', '$http', function($scope, $modal, $http) {
      var modalInstance;
    $scope.templateData = '';
    $scope.open = function(url) {
        $scope.item = {};
        $http.get(url).success(function(data){
            $scope.templateData = data;
            modalInstance = $modal.open({
                template : $scope.templateData,
                controller : CourseModalInstanceCtrl,
                backdrop:'static',
                keyboard: false,
                resolve : {
                    item : function() {
                        return $scope.item;
                    }
                }
            });
            modalInstance.opened.then(function() {
            });
            modalInstance.result.then(function(result) {
            }, function(reason) {
            });
        });
    };

    $scope.close = function() {
        modalInstance.dismiss('cancel');
    }
}]);
var CourseModalInstanceCtrl = function($scope, $modalInstance, item) {
    $scope.item = item;
    $scope.selected = {
        item : $scope.item
    };
    $scope.ok = function() {
        submit_course_create();
    };
     $scope.grade = function() {
        submit_grade_input();
    };
    $scope.update = function() {
        submit_course_update();
    };
    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    };

};


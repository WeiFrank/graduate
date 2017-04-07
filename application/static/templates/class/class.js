var ClassModalDemo = angular.module('App.class', []);
   ClassModalDemo.controller('ClassModalCtrl', ['$scope','$modal', '$http', function($scope, $modal, $http) {
      var modalInstance;
    $scope.templateData = '';
    $scope.open = function(url) {
        $scope.item = {};
        $http.get(url).success(function(data){
            $scope.templateData = data;
            modalInstance = $modal.open({
                template : $scope.templateData,
                controller : ClassModalInstanceCtrl,
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
var ClassModalInstanceCtrl = function($scope, $modalInstance, item) {
    $scope.item = item;
    $scope.selected = {
        item : $scope.item
    };
    $scope.ok = function() {
        submit_class_create();
    };
    $scope.update = function() {
        submit_class_update();
    };
    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    };
};


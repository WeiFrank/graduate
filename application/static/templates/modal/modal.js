var SelfConfirmModal = angular.module('App.modal', []);
SelfConfirmModal.controller('SelfConfirmModalCtrl', ['$scope', '$modal', '$sce', function ($scope, $modal, $sce) {
    $scope.item = {}
    $scope.open = function (msg, callback, params, title, isShowOK, is_redirect, is_show_close) {
        $scope.item = {
            'callback': callback,
            'params': params,
            'msg': $sce.trustAsHtml(msg),
            'title': title,
            'isShowOK': isShowOK,
            'is_redirect': is_redirect,
            'is_show_close': is_show_close
        };
        var modalInstance = $modal.open({
            templateUrl: "/confirm_modal",
            controller: SelfConfirmModalInstanceCtrl,
            backdrop: 'static',
            keyboard: false,
            resolve: {
                item: function () {
                    return $scope.item;
                }
            }
        });
    };
    $scope.callback = function () {
        return $scope.item.callback($scope.item.params)
    };
}]);
var SelfConfirmModalInstanceCtrl = function ($scope, $modalInstance, item) {
    $scope.item = item;
    $scope.selected = {
        item: $scope.item
    };
    $scope.ok = function () {
        var callback_res = angular.element('#global_confirm_modal').scope().callback();
        //if checker is fail, not close modal
        $modalInstance.dismiss('cancel');
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
};
//    $scope.redirect = function () {
//        $modalInstance.dismiss('cancel');
//        setTimeout(function () {
//            angular.element('#logo_mail').trigger('click');
//        }, 0);
//    };



//SelfConfirmModal.controller('GridDetailModalCtrl', ['$scope', '$modal', '$sce', function ($scope, $modal, $sce) {
//    $scope.item = {}
//    $scope.open = function (html) {
//        $scope.item = {};
//        $("#selectAll").die()
//        html = '<div class="modal-header"><button type="button" ng-click="cancel()" class="close">&times;</button><h3>详细信息</h3></div>'
//            + '<div  class="modal-body">'
//            + html
//            + "</div>"
//            + '<div class="modal-footer"><button class="btn btn-white" ng-click="cancel()">' +
//            "[[ 'label close'|translate ]]" + '</button></div>'
//
//        var modalInstance = $modal.open({
//            template: html,
//            backdrop: 'static',
//            keyboard: false,
//            controller: GridDetailModalInstanceCtrl,
//            resolve: {
//                item: function () {
//                    return $scope.item;
//                }
//            }
//        });
//    };
//    $scope.callback = function () {
//        return $scope.item.callback($scope.item.params)
//    };
//}]);
//
//var GridDetailModalInstanceCtrl = function ($scope, $modalInstance, item) {
//    $scope.item = item;
//    $scope.selected = {
//        item: $scope.item
//    };
//    $scope.ok = function () {
//        $modalInstance.dismiss('cancel');
//    };
//    $scope.cancel = function () {
//        $modalInstance.dismiss('cancel');
//    };
//};

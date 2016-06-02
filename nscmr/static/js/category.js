angular.module('angularApp').controller("CartController", ["$scope","$http", function($scope, $http) {
  $scope.addToCart = function(variantId) {
    $http({
      method: 'POST',
      url: addToCartUri,
      data: { 'variant_id': variantId },
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/json;utf-8"
      }
    }).then(function successCallback(response) {
      console.log(response);
    }, function errorCallback(response) {
      console.log(response);
    });
    return false;
  };
}]);


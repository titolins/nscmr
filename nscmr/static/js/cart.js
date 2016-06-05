angular.module('angularApp', [])
.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}]).controller("CartController", ["$scope","$http", function($scope, $http) {
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
      getCart();
    }, function errorCallback(response) {
      console.log(response);
    });
  };

  $scope.parse = function(number) {
    return parseInt(number);
  };
  function getCart() {
    $http({
      url: getCartUri,
    }).then(function successCallback(response) {
      $scope.cart = response.data;
    }, function errorCallback(response) {
      console.log(response);
    });
  };
  getCart();

}]);


angular.module('angularApp', [])
.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}]).controller("CartController", ["$scope","$http", function($scope, $http) {
  getCart();
  $scope.addToWishlist = function(variantId) {
    var data = { 'variant_id': variantId };
    $http({
      method: 'POST',
      url: addToWishlistUri,
      data: data,
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/json;utf-8"
      }
    }).then(function successCallback(response) {
      console.log(response);
      alert(response.data);
    }, function errorCallback(response) {
      alert(response.data);
      console.log(response);
    });
  }

  $scope.addToCart = function(variantId) {
    var data = { 'variant_id': variantId };
    $http({
      method: 'POST',
      url: addToCartUri,
      data: data,
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/json;utf-8"
      }
    }).then(function successCallback(response) {
      console.log(response);
      alert(response.data);
      getCart();
    }, function errorCallback(response) {
      alert(response.data);
      console.log(response);
    });
  }

  function getCart() {
    $http({
      url: getCartUri,
    }).then(function successCallback(response) {
      console.log(response.data);
      $scope.initialCart = response.data;
      $scope.cart = angular.copy($scope.initialCart);
    }, function errorCallback(response) {
      console.log(response);
    });
  };
}]);


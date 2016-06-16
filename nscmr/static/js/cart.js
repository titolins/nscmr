angular.module('angularApp', ['ui.mask'])
.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}]).controller("CartController", ["$scope","$http","cartService", function($scope, $http, cartService) {
  $scope.cartService = cartService;
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

}]);


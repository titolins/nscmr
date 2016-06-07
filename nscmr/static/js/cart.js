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
      alert(response.data);
      getCart();
      /*
      $scope.initialCart = response.data['cart'];
      $scope.cart = angular.copy($scope.initialCart);
      */
    }, function errorCallback(response) {
      alert(response.data);
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
      console.log(response.data);
      $scope.initialCart = response.data;
      $scope.cart = angular.copy($scope.initialCart);
    }, function errorCallback(response) {
      console.log(response);
    });
  };
  getCart();

  $scope.toggleEdit = function($event) {
    var target = $event.currentTarget;
    var targetClass = target.classList.contains('fa-edit') ? 'field' : 'input';
    if (targetClass == 'input') $scope.cart = angular.copy($scope.initialCart);
    else {
      var field = target.parentNode;
      while (!field.classList.contains(targetClass)) field = field.parentNode;
      field.classList.toggle('hidden');
      var toggle = document.getElementById(target.dataset['toggle']);
      toggle.classList.toggle('hidden');
    }
  }

  $scope.removeItem = function(var_id) {
    data = {
      'id': var_id,
      'quantity': 0
    }
    edit(data);
  };

  $scope.confirmEdit = function($event, var_id) {
    var targetParent = $event.currentTarget.parentNode;
    while (!targetParent.classList.contains('input')) targetParent = targetParent.parentNode;
    var data = {
      'id': var_id,
      'quantity': targetParent.getElementsByTagName('input')[0].value
    }
    edit(data);
  };

  function edit(data) {
    console.log(data);
    $http({
      method: 'POST',
      url: editCartUri,
      data: data,
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/json;utf-8"
      }
    }).then(function successCallback(response) {
      console.log(response);
      alert(response.data);
      getCart();
      /*
      $scope.initialCart = response.data['cart'];
      $scope.cart = angular.copy($scope.initialCart);
      */
    }, function errorCallback(response) {
      alert(response.data);
      console.log(response);
    });
  };

}]);


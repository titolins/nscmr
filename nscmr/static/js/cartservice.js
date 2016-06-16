angular.module('angularApp')
.service('cartService', ["$http", function($http) {
  var self = this;
  this.initialCart = [];
  this.cart = [];

  this.update = function() {
    $http({
      url: getCartUri,
    }).then(function successCallback(response) {
      console.log(response.data);
      self.initialCart = response.data;
      self.cart = angular.copy(self.initialCart);
    }, function errorCallback(response) {
      console.log(response);
    });
  };
  this.addToCart = function(variantId) {
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
      self.update();
    }, function errorCallback(response) {
      alert(response.data);
      console.log(response);
    });
  };
  this.reset = function() {
    self.cart = angular.copy(self.initialCart);
  };
  var editCart = function(data) {
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
      self.update();
    }, function errorCallback(response) {
      alert(response.data);
      console.log(response);
    });
  };
  this.removeItem = function(var_id) {
    data = {
      'id': var_id,
      'quantity': 0
    }
    editCart(data);
  };

  this.confirmEdit = function(item) {
    var data = {
      'id': item['_id'],
      'quantity': item['quantity']
    }
    editCart(data);
  };


  this.update();

}]);

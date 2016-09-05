angular.module('angularApp')
.service('cartService', ["$http", function($http) {
  var self = this;
  this.initialCart = {
    totalItems: 0,
    subTotal: 0,
    total: 0,
    items: [],
  };
  this.cart = angular.copy(self.initialCart);
  this.shippingOpts = [];

  this.update = function() {
    $http({
      url: getCartUri,
    }).then(function successCallback(response) {
      console.log(response.data);
      self.initialCart.items = response.data.items;
      self.initialCart.totalItems = self.getTotalItems(response.data.items);
      self.initialCart.subTotal = self.getSubtotal(response.data.items);
      self.initialCart.total = self.getTotal(self.initialCart);
      self.cart = angular.copy(self.initialCart);
      self.shippingOpts = [];
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

  this.getTotalItems = function(cartItems) {
    var sum = 0;
    cartItems.forEach(function(item) {
      sum += item.quantity;
    });
    return sum;
  };

  this.getSubtotal = function(cartItems) {
    var sum = 0.0;
    cartItems.forEach(function(item) {
      sum += (item.quantity*item.price);
    });
    return sum;
  };

  this.getTotal = function(cart) {
    console.log('getTotal');
    if(cart.shipping === undefined) {
      return cart.subTotal;
    } else {
      return (cart.shipping.cost + cart.subTotal);
    }
  };

  this.toggleEditCart = function($event) {
    var target = $event.currentTarget;
    // if we are cancelling the edit, we simply reset the cart (redrawing the
    // template)
    if (target.classList.contains('cancel-cart')) self.reset();
    var field = target.parentNode;
    while (!field.classList.contains('field')) field = field.parentNode;
    field.getElementsByClassName('field-value')[0].classList.toggle('hidden');
    field.getElementsByClassName('field-input')[0].classList.toggle('hidden');
  }

}]);

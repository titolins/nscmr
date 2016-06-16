angular.module('angularApp')
.filter('totalPrice', function() {
  return function(items) {
    var total = 0, i = 0;
    for (; i < items.length; i++) total += (items[i].price * items[i].quantity);
    return total;
  }
})
.controller("CheckoutController", ["$scope","$http","addressesService", "cartService", function($scope, $http, addressesService, cartService) {
  $scope.addressesService = addressesService;
  $scope.addressesService.update(getAddressesUri);
  $scope.cartService = cartService;
  $scope.selectedAddress = null;
  $scope.card = {};

  $scope.selectAddress = function($event, address) {
    var target = $event.target;
    var parentNode = target.parentNode;
    while (!parentNode.classList.contains('address-panel')) parentNode = parentNode.parentNode;
    if (parentNode.classList.contains('selected')) { parentNode.classList.toggle('selected'); $scope.selectedAddress = null; }
    else {
      var selectedPanel = document.getElementsByClassName('address-panel selected')[0];
      if (selectedPanel !== undefined) selectedPanel.classList.remove('selected');
      parentNode.classList.toggle('selected');
      $scope.selectedAddress = address;
    }
  };

  $scope.toggleCheckoutOption = function($event) {
    $event.preventDefault();
    var removeOption = document.getElementById('checkout-options').getElementsByClassName('selected')[0];
    var targetOption = $event.target;
    removeOption.classList.remove('selected');
    targetOption.classList.add('selected');
    var removeDiv = document.getElementById(removeOption.dataset.target);
    var targetDiv = document.getElementById(targetOption.dataset.target);
    removeDiv.classList.add('hidden');
    targetDiv.classList.remove('hidden');
  };

  $scope.moveOptions = function(direction) {
    var currentOption = document.getElementById('checkout-options').getElementsByClassName('selected')[0];
    var target;
    if (direction === 'next') {
      target = currentOption.nextSibling.nextSibling;
    } else if (direction === 'prev') {
      target = currentOption.previousSibling.previousSibling;
    }
    if (target === null) return;
    currentOption.classList.remove('selected');
    target.classList.add('selected');
    document.getElementById(currentOption.dataset.target).classList.add('hidden');
    document.getElementById(target.dataset.target).classList.remove('hidden');
  };

  $scope.toggleEdit = function($event) {
    var target = $event.currentTarget;
    // if we are cancelling the edit, we simply reset the cart (redrawing the
    // template)
    if (target.classList.contains('cancel-cart')) $scope.cartService.reset();
    var field = target.parentNode;
    while (!field.classList.contains('field')) field = field.parentNode;
    field.getElementsByClassName('field-value')[0].classList.toggle('hidden');
    field.getElementsByClassName('field-input')[0].classList.toggle('hidden');
  }

  $scope.toggleCardBrand = function($event) {
    $event.preventDefault();
    var target = $event.target;
    var selectedBrand = document.getElementsByClassName('card-brand selected')[0];
    if (selectedBrand !== undefined) selectedBrand.classList.remove('selected');
    while (!target.classList.contains('card-brand')) target = target.parentNode;
    target.classList.add('selected');
    var brandName = target.id.split('-')[0];
    document.querySelector('input[name=brand]').value = brandName;
    $scope.card['brand'] = brandName;
  };

  $scope.getCartTotal = function() {
    var total = 0;
    for (var i = 0; i < $scope.cartService.cart; i++) total += $scope.cartService.cart[i].price;
    return total;
  };
}]);

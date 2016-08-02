angular.module('angularApp')
.controller("CheckoutController", ["$scope","$http","addressesService", "cartService", function($scope, $http, addressesService, cartService) {
  $scope.addressesService = addressesService;
  $scope.addressesService.update(getAddressesUri);
  $scope.cartService = cartService;
  $scope.selectedAddress = null;
  $scope.initialCard = {
    'brand': '',
    'number': '',
    'holderName': '',
    'securityCode': '',
    'expMonth': '',
    'expYear': ''
  };
  $scope.card = angular.copy($scope.initialCard);

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

  $scope.confirmBuy = function() {
    var data = {
      'cart': $scope.cartService.cart,
      'address': $scope.selectedAddress,
      'card': $scope.card,
    };
    // hide checkout and toggle spinner
    document.getElementById('checkout').classList.add('hidden');
    document.getElementById('checkout-conclusion').classList.remove('hidden');
    console.log(data);
    $http({
      method: 'POST',
      url: confirmUri,
      data: data,
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/json;utf-8"
      }
    }).then(function success(response) {
      console.log(response);
      document.getElementById('checkout-spinner').classList.add('hidden');
      document.getElementById('checkout-result').innerHTML = response.data;
    }, function error(response) {
      console.log(response);
      document.getElementById('checkout-spinner').classList.add('hidden');
      document.getElementById('checkout-result').innerHTML = response.data;
    });
  };

  $scope.getShipping = function() {
    document.getElementById('frete-btn').classList.add('hidden');
    document.getElementById('load-frete').classList.remove('hidden');
    $scope.cartService.shippingOpts = [];
    $scope.cartService.cart.shipping = undefined;
    $scope.cartService.correiosErrorMsg = undefined;
    $http({
      method: 'POST',
      url: shippingUri,
      data: {'zipCode': cartService.cart.zipCode },
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/json;utf-8"
      }
    }).then(function success(response) {
      console.log(response);
      response.data.forEach(function(service) {
        if(service.Erro == "-3") $scope.cartService.correiosErrorMsg = service.MsgErro;
      });
      if($scope.cartService.correiosErrorMsg == undefined) $scope.cartService.shippingOpts = response.data;
      document.getElementById('frete-btn').classList.remove('hidden');
      document.getElementById('load-frete').classList.add('hidden');
    }, function error(response) {
      console.log(response);
      document.getElementById('frete-btn').classList.remove('hidden');
      document.getElementById('load-frete').classList.add('hidden');
    });
  };

  $scope.selectShipping = function(event) {
    window.target = event.target;
    target.checked = true;
    var shippingMethods = document.querySelectorAll('input[type=checkbox]');
    shippingMethods.forEach(function(item) {
      if(item.id === target.id) return;
      item.checked = false;
    });
    $scope.cartService.shippingOpts.forEach(function(shipping) {
      if(shipping.Codigo == target.id) {
        $scope.cartService.cart.shipping = shipping.Valor;
        $scope.cartService.cart.total = $scope.cartService.getTotal($scope.cartService.cart);
      }
    });
  };

  $scope.chooseAddress = function(e, address) {
    if(e.target.parentNode.classList.contains('options-btn')) return;
    var target = e.target;
    while(!target.classList.contains('select-address')) target = target.parentNode;
    if(target.classList.contains('selected')) $scope.selectedAddress = null;
    else {
      var curSelection = document.querySelector('.select-address.selected');
      if(curSelection != null) curSelection.classList.remove('selected');
      $scope.selectedAddress = address;
    }
    target.classList.toggle('selected');
  };

}]);

//angular.module('angularApp').requires.push('credit-cards');
angular.module('angularApp')
.controller("CheckoutController", ["$scope","$http","addressesService", "cartService", "paymentService", function($scope, $http, addressesService, cartService, paymentService) {
  $scope.paymentService = paymentService;
  $scope.addressesService = addressesService;
  $scope.addressesService.update(getAddressesUri);
  $scope.cartService = cartService;
  $scope.selectedAddress = null;
  $scope.selectedCard = null;
  /*
  window.setTimeout(function() {
    $scope.$apply(function () {
      $scope.selectedAddress = $scope.addressesService.addresses[0];
    });
  }, 10000);
  */

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
    var currentOption = document.getElementsByClassName('checkout-tab selected')[0];
    var target;
    if (direction === 'next') {
      target = currentOption.nextSibling.nextSibling;
    } else if (direction === 'prev') {
      target = currentOption.previousSibling.previousSibling;
    }
    if (target != null) {
      currentOption.classList.remove('selected');
      currentOption.classList.add('hidden');
      target.classList.remove('hidden');
      target.classList.add('selected');
    }
  };

  $scope.confirmBuy = function() {
    //$scope.selectedCard.installments = $scope.installments;
    var data = {
      'cart': $scope.cartService.cart,
      'address': $scope.selectedAddress,
      'card': $scope.selectedCard,
      'senderHash': PagSeguroDirectPayment.getSenderHash(),
    };
    /* hide checkout and toggle spinner
    */
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
      document.getElementById('checkout-result').innerHTML = response.data.msg;
    }, function error(response) {
      console.log(response);
      document.getElementById('checkout-spinner').classList.add('hidden');
      document.getElementById('checkout-result').innerHTML = response.data.errors;
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
        $scope.cartService.cart.shipping = {
          cost: shipping.Valor,
          type: shipping.Tipo,
          code: shipping.Codigo,
        };
        $scope.cartService.cart.total = $scope.cartService.getTotal($scope.cartService.cart);
      }
    });
  };

  $scope.chooseAddress = function(e, address) {
    if(e.target.parentNode.classList.contains('options-btn')) return;
    var target = e.target;
    while(!target.classList.contains('card-panel')) target = target.parentNode;
    if(target.classList.contains('selected')) $scope.selectedAddress = null;
    else {
      var curSelection = document.querySelector('.card-panel.selected');
      if(curSelection != null) curSelection.classList.remove('selected');
      $scope.selectedAddress = address;
      if(address['zip_code'] != $scope.cartService.cart.zipCode) {
        $scope.selectedAddress['valid'] = false;
      } else {
        $scope.selectedAddress['valid'] = true;
      }
      console.log($scope.selectedAddress);
    }
    target.classList.toggle('selected');
  };

  $scope.confirmCard = function() {
    // get card token, then get installments and move on to confirmation page
    PagSeguroDirectPayment.createCardToken({
      cardNumber: $scope.paymentService.card.number,
      brand: $scope.paymentService.card.brandInfo.name,
      cvv: $scope.paymentService.card.cvv,
      expirationMonth: $scope.paymentService.card.expMonth,
      expirationYear: "20" + $scope.paymentService.card.expYear,
      success: function(response) {
        $scope.$apply(function() {
          $scope.selectedCard = $scope.paymentService.card;
          $scope.selectedCard.token = response.card.token;
        });
        $scope.moveOptions('next');
      },
      error: function(response) {
        console.log("[ERROR] confirmCard");
      },
      complete: function(response) {
        console.log(response);
      },
    });
  }

  

}]);

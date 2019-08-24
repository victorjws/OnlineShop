let subtotal = 0;
let total = 0;
function setTotal() {
    $("#subtotal").html("");
    $("#delivery").html("");
    $("#discount").html("");
    $("#total").html("");
    $("#subtotal").html(subtotal.format() + " 원");
    $("#delivery").html("0 원");
    $("#discount").html("0 원");
    $("#total").html(subtotal.format() + " 원");
    total = subtotal;
};
function putCartData(result) {
    let cart
    $("#cart-table").html("");
    $.each(result, function (index, data) {
        let total_price;
        cart = '<tr class="text-center">'
            + '<td class="product-remove">'
            +    '<a href="#"><span class="ion-ios-close"></span></a></td>'
            + '<td class="image-prod">'
            +    '<div class="img" style="background-image:url(' + data.product.picture + ');"></div>'
            + '</td>'
            + '<td class="product-name">'
            +    '<h3>' + data.product.name + '</h3>'
            + '</td>'
            + '<td class="price">';
            if(data.product.is_discount){
                cart += data.product.discount_price.format();
                total_price = data.product.discount_price * data.quantity;
            } else {
                cart += data.product.price.format();
                total_price = data.product.price * data.quantity;
            }
            cart += '원</td>'
            + '<td class="quantity">'
            +    '<div class="input-group mb-3">'
            +        '<span class="input-group-btn mr-2">'
	        +            '<button type="button" class="quantity-left-minus btn" data-type="minus" data-field="">'
	        +                '<i class="ion-ios-remove"></i>'
	        +            '</button>'
	        +        '</span>'
            +        '<input id="quantity-' + data.product.id + '" type="text" name="quantity"'
            +           'class="quantity form-control input-number" value="' + data.quantity + '" min="1" max="99999">'
            +        '<span class="input-group-btn ml-2">'
	        +            '<button type="button" class="quantity-right-plus btn" data-type="plus" data-field="">'
            +                '<i class="ion-ios-add"></i>'
	        +            '</button>'
	        +     	 '</span>'
            +    '</div>'
            + '</td>'
            + '<td class="total">' + total_price.format() + '원</td>'
            + '</tr>';
        $("#cart-table").append(cart);
        subtotal += total_price;
    });
    setTotal();
};
function setIamport(total){
    $('#order').click(function(e){
        let stored_token = Cookies.get('token');
        let decoded = jwt_decode(stored_token);
        IMP.request_pay({
            pg : 'kakaopay',
            pay_method : 'card',
            merchant_uid : 'merchant_' + new Date().getTime(),
            name : 'OnlineShop 결제',
            amount : total,
            buyer_email : decoded.email,
        }, function(rsp) {
            if ( rsp.success ) {
                $.ajax({
                    url: "/order/payments-complete/",
                    method: "POST",
                    dataType: 'json',
                    contentType:"application/json",
                    data: JSON.stringify({
                        imp_uid: rsp.imp_uid
                    }),
                    beforeSend: function(xhr) {
                        xhr.setRequestHeader("Authorization", "Bearer " + Cookies.get('token'));
                    },
                }).success(function (data) {
                    if(data.status==='success'){
                        var msg = '결제가 완료되었습니다.';
                        msg += '\n고유ID : ' + rsp.imp_uid;
                        msg += '\n상점 거래ID : ' + rsp.merchant_uid;
                        msg += '\n결제 금액 : ' + rsp.paid_amount;
                        msg += '\n카드 승인번호 : ' + rsp.apply_num;
                    }
                    console.log(data);
                    alert(msg);
                    console.log(msg);
                }).fail(function (data) {
                    console.log(data);
                });
            } else {
                var msg = '결제에 실패하였습니다.';
                msg += '에러내용 : ' + rsp.error_msg;
                alert(msg);
                console.log(msg);
            }
        });
    });
};
function getCartData() {
    $.ajax({
        method: 'GET',
        url: "/order/cart-api/",
        beforeSend: function(xhr) {
            xhr.setRequestHeader("Authorization", "Bearer " + Cookies.get('token'));
        },
        success: function (result){
            putCartData(result);
        },
        complete: function (result){
            setPlusMinusButtonEvent();
            setIamport(total);
        }
    });
};
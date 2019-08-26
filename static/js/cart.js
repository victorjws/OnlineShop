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
    total = subtotal;
    $("#total").html(total.format() + " 원");

};
function putCartData(result) {
    let cart
    $("#cart-table").html("");
    $.each(result, function (index, data) {
        let total_price;
        let cur_price;
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
                cur_price = data.product.discount_price;
                cart += data.product.discount_price.format();
                total_price = data.product.discount_price * data.quantity;
            } else {
                cur_price = data.product.price;
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
            +           'class="quantity form-control input-number numbersOnly" value="' + data.quantity + '"'
            +           'min="1" max="99999" price="' + cur_price + '">'
            +        '<span class="input-group-btn ml-2">'
	        +            '<button type="button" class="quantity-right-plus btn" data-type="plus" data-field="">'
            +                '<i class="ion-ios-add"></i>'
	        +            '</button>'
	        +     	 '</span>'
            +    '</div>'
            + '</td>'
            + '<td class="total" total="' + total_price + '">' + total_price.format() + '원</td>'
            + '</tr>';
        $("#cart-table").append(cart);
        subtotal += total_price;
    });
    setTotal();
};
function setIamport(total){
    $('#order').click(function(e){
        updateServerQuantity();
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
                    var msg = "";
                    if(data.status==='success'){
                        msg = '결제가 완료되었습니다.';
                        msg += '\n고유ID : ' + rsp.imp_uid;
                        msg += '\n상점 거래ID : ' + rsp.merchant_uid;
                        msg += '\n결제 금액 : ' + rsp.paid_amount;
                        msg += '\n카드 승인번호 : ' + rsp.apply_num;
                    }
                    alert(msg);
                    window.location = "/order/";
                }).fail(function (data) {
                    console.log(data);
                });
            } else {
                var msg = '결제에 실패하였습니다.';
                msg += '에러내용 : ' + rsp.error_msg;
                alert(msg);
            }
        });
    });
};
function changeQuantity(){
    $(".quantity").on("change", "input", function(){
        var price = $(this).attr("price");
        var total = $(this).val() * price;
        $(this).parent().parent().parent().find(".total").attr("total", total);
        $(this).parent().parent().parent().find(".total").html(total.format() + "원");
        updateTotal();
    });
}
function numbersOnly(){
    $('.numbersOnly').keyup(function () {
        if (this.value != this.value.replace(/[^0-9\.]/g, '')) {
           this.value = this.value.replace(/[^0-9\.]/g, '');
        }
    });
}
function updateTotal(){
    subtotal = 0;
    total = 0;
    $(".total").each(function(){
        var product_price = Number($(this).attr("total"));
        subtotal += product_price;
    })
    setTotal();
}
function updateServerQuantity(){
    let _data = [];
    $(".quantity input").each(function(){
        var id_attr = $(this).attr("id");
        var product_id = String(id_attr).split('-');
        var id = product_id[product_id.length-1];
        item = {};
        item['product_id'] = Number(id);
        item['quantity'] = Number($(this).val());
        _data.push(item);
    })
    $.ajax({
        method: 'PATCH',
        url: "/order/cart-api/",
        data: JSON.stringify(_data),
        contentType: "Application/json",
        beforeSend: function(xhr) {
            xhr.setRequestHeader("Authorization", "Bearer " + Cookies.get('token'));
        },
        success: function (result){
            console.log(result);
        },
        error: function (result){
            console.log(result);
        }
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
            changeQuantity();
            numbersOnly();
            setIamport(total);
        },
        error: function (result){
            if (result.status === 401){
                alert("로그인이 필요한 서비스입니다.");
                window.location = "/customer/login/";
            }
        }
    });
};
function putOrderData(result) {
    let order
    $("#order-table").html("");
    $.each(result, function (index, data) {
        let total_price;
        order = '<tr class="text-center">'
            + '<td class="image-prod">'
            +    '<div class="img" style="background-image:url(' + data.product.picture + ');"></div>'
            + '</td>'
            + '<td class="product-name">'
            +    '<h3>' + data.product.name + '</h3>'
            + '</td>'
            + '<td class="price">';
            if(data.product.is_discount){
                order += data.product.discount_price.format();
                total_price = data.product.discount_price * data.quantity;
            } else {
                order += data.product.price.format();
                total_price = data.product.price * data.quantity;
            }
            order += '원</td>'
            + '<td class="quantity">'
            +    '<div class="input-group mb-3">'
            +        '<input id="quantity-' + data.product.id + '" type="text" name="quantity" readonly '
            +           'class="quantity form-control input-number" value="' + data.quantity + '" min="1" max="99999">'
            +    '</div>'
            + '</td>'
            + '<td class="total">' + total_price.format() + '원</td>'
            + '<td class="order-date">' + data.order_date + '</td>'
            + '</tr>';
        $("#order-table").append(order);
    });
};
function getOrderData() {
    $.ajax({
        method: 'GET',
        url: "/order/order-api/",
        beforeSend: function(xhr) {
            xhr.setRequestHeader("Authorization", "Bearer " + Cookies.get('token'));
        },
        success: function (result){
            putOrderData(result);
        },
        complete: function (result){
            setPlusMinusButtonEvent();
        },
        error: function (result){
            if (result.status === 401){
                alert("로그인이 필요한 서비스입니다.");
                window.location = "/customer/login/";
            }
        }
    });
};
function updateCartData() {
    $.ajax({
        method: 'POST',
        url: "/order/order-api/",
        beforeSend: function(xhr) {
            xhr.setRequestHeader("Authorization", "Bearer " + Cookies.get('token'));
        },
        success: function (result){
            putOrderData(result);
        },
    });
}
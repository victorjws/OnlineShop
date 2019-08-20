let send_data = {};
Number.prototype.format = function(){
    if(this==0) return 0;
    var reg = /(^[+-]?\d+)(\d{3})/;
    var n = (this + '');
    while (reg.test(n)) n = n.replace(reg, '$1' + ',' + '$2');
    return n;
};
//function productDetail(id) {
//    $.ajax({
//      url: "/product/detail-api/" + id + "/",
//      success: function (result) {
//        $("#product-" + id).popover({
//          html: true,
//          content: result.name + "<br/>" + result.price.format() + "원"
//        }).popover('show');
//      }
//    });
//};
function putProductDetail(data){
    let product_img;
    let product_name;
    let product_price;
    let product_description;

    product_img = '<a href="' + data.picture + '" class="image-popup prod-img-bg">'
        + '<img src="' + data.picture + '" class="img-fluid" alt="Colorlib Template"></a>';
    product_name = data.name;
    product_price = '<span>' + data.price.format() + '원</span>';
    product_description = data.description;

    $("#product-img").append(product_img);
    $("#product-name").append(product_name);
    $("#product-price").append(product_price);
    $("#product-description").append(product_description);
}
function getProductDetail(id) {
    $.ajax({
        url: "/product/detail-api/" + id + "/",
        dataType : "json",
        success: function (result) {
            putProductDetail(result);
        }
    });
};
//function productLeave(id) {
//    $("#product-" + id).popover('hide');
//};
function putProductData(result, version) {
    let product;
    let pagination;
    $("#product-table").html("");
    $("#pagination").html("");
    $.each(result.results, function (index, data) {
        switch(version){
            case 1:
                product = '<div class="col-sm-12 col-md-6 col-lg-3 ftco-animate d-flex fadeInUp ftco-animated">'
                break;
            case 2:
                product = '<div class="col-sm-12 col-md-12 col-lg-4 ftco-animate d-flex fadeInUp ftco-animated">'
                break;
        }
        product +='<div class="product d-flex flex-column">'
            + '<a href="/product/' + data.id + '/" class="img-prod">'
            + '<img class="img-fluid" src="' + data.picture + '" alt="Colorlib Template">';
        if (Boolean(data.is_discount)){
            let discount_percentage = Math.round(((data.price - data.discount_price) / data.price) * 100);
            product += '<span class="status">' + discount_percentage + '% Off</span>';
        }
        product += '<div class="overlay"></div></a>'
            + '<div class="text py-3 pb-4 px-3">'
            + '<div class="d-flex">'
            + '<div class="cat"><span>';
        $.each(data.categories, function (catindex, catdata) {
            product += '\#' + catdata.name + ' ';
        });
        product += '</span></div></div>'
            + '<h3><a href="/product/' + data.id + '/">'
//            + 'onmouseenter="productDetail(' + data.id + ');"'
//            + 'onmouseleave="productLeave(' + data.id + ');">'
            + data.name + '</a></h3><div class="pricing"><p class="price">';
        if (Boolean(data.is_discount)){
            product += '<span class="mr-2 price-dc">' + data.price.format()
                + '원</span><span class="price-sale">' + data.discount_price.format() + '원</span></p>';
        } else {
            product += '<span>' + data.price.format() + '원</span>';
        }
        product += '</div><p class="bottom-area d-flex px-3">'
            + '<a href="javascript:clickAddCartButton(' + data.id + ', 1);" class="add-to-cart text-center py-2 mr-1">'
            + '<span>장바구니 담기<i class="ion-ios-add ml-1"></i></span></a>'
            + '<a href="' + '#' + '" class="buy-now text-center py-2">바로주문'
            + '<span><i class="ion-ios-cart ml-1"></i></span></a></p></div></div></div>';
        $("#product-table").append(product);
    });
    pagination = '<li><a href="' + result.previous + '">&lt;</a></li>';
    $.each(result.page_links, function (index, data) {
        if (data[2]){
            pagination += '<li class="active"><span>' + data[1] + '</span></li>';
        } else if (data[3]){
            pagination += '<li class="disabled"><span aria-hidden="true">&hellip;</span></li>';
        } else {
            pagination += '<li><a href="javascript:getProductData(\'' + data[0] + '\', 2);">' + data[1] + '</a></li>';
        }
    });
    pagination +='<li><a href="' + result.next + '">&gt;</a></li>';
    $("#pagination").html(pagination);
};

function getProductData(url, version) {
    $.ajax({
        method: 'GET',
        url: url,
        data: send_data,
        dataType : "json",
        contentType:"application/json",
        success: function (result){
            putProductData(result, version);
        }
    });
};
function putCategoryData(result, url){
    send_data = {};
    let category;
    $("#category-table").html("");
    $.each(result, function (index, data) {
        category = '<li id="' + data.id + '">'
        + '<a href="#">' + data.name + '</a></li>'
        $("#category-table").append(category);
    });
    $("#category-table").on("click", "li", function(){
        send_data['category'] = $(this).attr("id");
        getProductData("/product/list-api/", 2);
    });
};
function getCategoryData(url){
    $.ajax({
        url: url,
        dataType : "json",
        contentType:"application/json",
        success: function (result){
            putCategoryData(result, url);
        },
        error: function (response){
            console.log(response);
        }
    });
};
function createCart(send_data){
    $.ajax({
        method: 'POST',
        url: "/order/cart-api/",
        data: JSON.stringify(send_data),
        dataType : "json",
        contentType:"application/json",
        beforeSend: function(xhr) {
            xhr.setRequestHeader("Authorization", "Bearer " + Cookies.get('token'));
        },
        success: function (result){
            alert("장바구니에 성공적으로 담았습니다.");
        },
        error: function (result){
            alert("에러가 발생했습니다.");
        }
    });
};
//function updateCart(send_data){
//    $.ajax({
//        method: 'PUT',
//        url: "/order/cart-api/",
//        data: JSON.stringify(send_data),
//        dataType : "json",
//        contentType:"application/json",
//        beforeSend: function(xhr) {
//            xhr.setRequestHeader("Authorization", "Bearer " + Cookies.get('token'));
//        },
//        success: function (result){
//            alert("장바구니에 성공적으로 담았습니다.");
//        },
//        error: function (result){
//            alert("에러가 발생했습니다.");
//        }
//    });
//};
function clickAddCartButton(product_id, quantity){
    send_data = {};
    send_data['product_id'] = product_id;
    send_data['quantity'] = quantity;
    if (checkAlreadyCart(product_id)){
        console.log(true);
        alert("이미 장바구니에 담았습니다.")
    }else{
        console.log(false);
        createCart(send_data);
    }
}
function checkAlreadyCart(product_id){
    send_data = {};
    send_data['product_id'] = product_id;
    let r;
    $.ajax({
        method: 'GET',
        url: "/order/exist-api/",
        data: send_data,
        dataType : "json",
        contentType:"application/json",
        async: false,
        beforeSend: function(xhr) {
            xhr.setRequestHeader("Authorization", "Bearer " + Cookies.get('token'));
        },
        success: function (result){
            if(result.result){
                r = true;
            }else{
                r = false;
            }
        },
        error: function (result){
            console.log(result);
        }
    });
    return r;
}
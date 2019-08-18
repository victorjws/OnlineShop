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
    $("#product-table").html("");
    $.each(result, function (index, data) {
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
            + '<a href="' + '#' + '" class="add-to-cart text-center py-2 mr-1">'
            + '<span>장바구니 담기<i class="ion-ios-add ml-1"></i></span></a>'
            + '<a href="' + '#' + '" class="buy-now text-center py-2">바로주문'
            + '<span><i class="ion-ios-cart ml-1"></i></span></a></p></div></div></div>';
        $("#product-table").append(product);
    });
};

function getProductData(version) {
    $.ajax({
        method: 'GET',
        url: "/product/list-api/",
        data: send_data,
        success: function (result){
            putProductData(result, version);
        }
    });
};
function putCategoryData(result){
    let category;
    $("#category-table").html("");
    $.each(result, function (index, data) {
        category = '<li id="' + data.id + '">'
        + '<a href="#">' + data.name + '</a></li>'
        $("#category-table").append(category);
    });
    $("#category-table").on("click", "li", function(){
        send_data['category'] = $(this).attr("id");
        getProductData(2);
    });
};
function getCategoryData(){
    $.ajax({
        url: "/product/category-list-api/",
        success: function (result){
            putCategoryData(result);
        },
        error: function (response){
            console.log(response);
        }
    });
};
function logout() {
    Cookies.remove('token');
};
function saveToken(data) {
    Cookies.remove('token');
    Cookies.set('token', data.token);
};
function verifyToken(token) {
    let _data = {"token": token};
    let r = false;
    $.ajax({
        method: 'POST',
        url: "/verify-token/",
        data: _data,
        async: false,
        success: function (result){
            r = true;
        },
        error: function(result) {
            logout();
            alert("토큰이 만료되었습니다.\n다시 로그인해주세요.");
        }
    });
    return r;
};
function refreshToken(token) {
    let _data = {"token": token};
    let r = false;
    $.ajax({
        method: 'POST',
        url: "/refresh-token/",
        data: _data,
        async: false,
        success: function (result){
            saveToken(result);
            r = true;
        },
        error: function(result) {
            logout();
            alert("토큰이 만료되었습니다.\n다시 로그인해주세요.");
        }
    });
    return r;
};
function checkAuthStatus() {
    let stored_token = Cookies.get('token');
    if (stored_token !== undefined){
        if (verifyToken(stored_token)){
            checkNeedRefresh();
            return true;
        } else {
            return false;
        }
    } else {
        return false;
    }
};
function renderLoginStatus() {
    $("#show-nickname").html("");
    $("#login").html("");
    let show_nickname;
    let login;
    if(checkAuthStatus()) {
        let stored_token = Cookies.get('token');
        let decoded = jwt_decode(stored_token);
        show_nickname = '<span class="text">' + decoded.nickname + '님 환영합니다!</span>';
        login = '<a href="/" onclick="logout();" class="nav-link">Logout</a>';
    }else{
        show_nickname = '<span class="text">환영합니다!</span>';
        login = '<a href="/customer/login/" class="nav-link">Login</a>';
    }
    $("#show-nickname").html(show_nickname);
    $("#login").html(login);
};
function checkNeedRefresh() {
    var stored_token = Cookies.get('token');
    var decoded = jwt_decode(stored_token);
    var now = new Date;
    var utc_timestamp = Date.UTC(now.getUTCFullYear(),now.getUTCMonth(), now.getUTCDate() ,
          now.getUTCHours(), now.getUTCMinutes(), now.getUTCSeconds(), now.getUTCMilliseconds()) / 1000;
    if ((decoded.expiration + 32400) < utc_timestamp){
        refreshToken(stored_token);
    }
};
function registerCustomer(){
    $('#register').on("click", function() {
        _data = {
            'email': $('#email').val(),
            'nickname': $('#nickname').val(),
            'password': $('#password').val(),
            'shipping_address': $('#shipping_address').val()
        };
        $.ajax({
            method: 'POST',
            url: "/customer/register/",
            data: JSON.stringify(_data),
            dataType : "json",
            contentType:"application/json",
            success: function (result){
                alert('가입을 환영합니다!');
                window.location = "/customer/login/";
            },
            error: function (result){
                alert("에러가 발생했습니다.");
            }
        });
    });
};
function logout() {
    Cookies.remove('token');
};
function verifyToken(token) {
    let _data = {"token": token}
    let r;
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
            r = false;
        }
    });
    return r;
}
function checkAuthStatus() {
    let stored_token = Cookies.get('token');
    if (stored_token !== undefined){
        if (verifyToken(stored_token)){
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
}


$(function () {

    // 点击登录按钮
    $('#login').click(function() {

        // 对密码进行md5加密
        $('#password').val( md5($('#password').val()) );


    });


    /*

     $.get('url', {'password': md5($('#password').val())}, function(){

     })

    */



});



$(function () {

    /*
    var flag1 = false;  //表示用户名是否输入合法
    var flag2 = false;  //表示密码是否输入合法
    var flag3 = false;  //表示确认密码是否输入合法
    var flag4 = false;  //表示邮箱是否输入合法

    //用户名
    $('#username').change(function () {
        var value = $(this).val();
        if (/^[a-zA-Z_]\w{5,17}$/.test(value)) {
            // console.log('输入合法')
            flag1 = true;
            $('#msg').html('用户名可用').css('color', 'green');
        }
        else {
            // console.log('输入不合法')
            flag1 = false;
            $('#msg').html('用户名输入不正确').css('color', 'red');
        }
    });

    // 密码
    $('#password').change(function () {
        var value = $(this).val();
        if (/^.{8,}$/.test(value)) {
            // console.log('密码输入合法')
            flag2 = true
        }
        else {
            // console.log('密码输入不合法')
            flag2 = false
        }
    });

    // 确认密码
    $('#repassword').change(function () {
        var passwd = $('#password').val();
        var repasswd = $(this).val();
        if (passwd == repasswd) {
            // console.log('确认密码输入合法')
            flag3 = true
        }
        else {
            // console.log('两次密码不一致')
            flag3 = false
        }
    });

    // 邮箱正则： \w+@\w+\.\w+
    //          222@qq.com
    //          222@163.com
    //          aaa@sina.com.cn
    $('#email').change(function () {
        var value = $(this).val();
        if (/^\w+@\w+(\.\w+)+$/.test(value)) {
            // console.log('邮箱输入合法')
            flag4 = true
        }
        else {
            // console.log('邮箱输入不合法')
            flag4 = false
        }
    });


    // 点击注册按钮
    $('#register').click(function() {
        console.log('注册');
        // 如果所有输入框都输入合法，则可以提交return true
        // 如果有输入框输入不合法，则不允许提交return false

        // 如果所有输入框都输入合法，则可以提交return true
        if (flag1 && flag2 && flag3 && flag4) {
            console.log('所有输入都合法');
            return true
        }
        else {
            if (!flag1) {
                console.log('用户名输入不合法');
            }
            else if (!flag2) {
                console.log('密码输入不合法')
            }
            else if (!flag3) {
                console.log('确认密码输入不合法')
            }
            else if (!flag4) {
                console.log('邮箱输入不合法')
            }

            return false
        }
    })

    */


    //用户名
    $('#username').change(function () {

        if (virifyUsername()) {
            // $('#msg').html('用户名格式正确').css('color', 'green');

            //ajax
            //如果用户名格式正确，则检查用户名是否存在
            $.get('/axf/checkusername/', {username: $('#username').val()}, function(data) {
                // console.log(data);
                if (data.status == 1) {
                    $('#msg').html('用户名可以使用').css('color', 'green');
                }
                else if (data.status == 0) {
                    $('#msg').html(data.msg).css('color', 'orange');
                }
                else {
                    $('#msg').html(data.msg).css('color', 'orange');
                }
            });

        }
        else {
            $('#msg').html('用户名格式不正确').css('color', 'red');
        }
    });

    // 验证用户名
    function virifyUsername(){
        var value = $('#username').val();
        if (/^[a-zA-Z_]\w{5,17}$/.test(value)) {
            return true
        }
        return false
    }


    // 密码
    $('#password').change(function () {

        if (virifyPassword()) {
        }
        else {
        }
    });

    // 验证密码
    function virifyPassword(){
        var value = $('#password').val();
        if (/^.{8,}$/.test(value)) {
            return true
        }
        return false
    }

    // 确认密码
    $('#repassword').change(function () {
        if (virifyRepassword()) {

        }
        else {
        }
    });

    // 验证确认密码
    function virifyRepassword(){
        var passwd = $('#password').val();
        var repasswd = $('#repassword').val();
        if (passwd == repasswd) {
            return true
        }
        return false
    }

    // 邮箱正则： \w+@\w+\.\w+
    $('#email').change(function () {
        if (virifyEmail()) {
        }
        else {
        }
    });
    // 验证邮箱
    function virifyEmail(){
        var value = $('#email').val();
        if (/^\w+@\w+(\.\w+)+$/.test(value)) {
            return true
        }
        return false
    }


    // 点击注册按钮
    $('#register').click(function() {
        console.log('注册');

        // 如果所有输入框都输入合法，则可以提交return true
        if (virifyUsername() && virifyPassword() && virifyRepassword() && virifyEmail()) {
            console.log('所有输入都合法');

            // 对密码进行md5加密
            $('#password').val( md5($('#password').val()) );


            return true
        }
        else {
            if (!virifyUsername()) {
                console.log('用户名输入不合法');
            }
            else if (!virifyPassword()) {
                console.log('密码输入不合法')
            }
            else if (!virifyRepassword()) {
                console.log('确认密码输入不合法')
            }
            else if (!virifyEmail()) {
                console.log('邮箱输入不合法')
            }

            return false
        }
    })





});
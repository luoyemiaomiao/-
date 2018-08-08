
$(function () {

    // 支付
    /*
        支付宝支付流程：
            1,先以企业为单位(企业支付宝账号)申请使用支付宝，申请成功后会给你一个商户id
            2,在支付宝创建应用(一般需要说明支付用户,卖什么东西),创建之后一般会给你一个appid,appkey
            3,点击‘支付’按钮，你需要提交信息（包括订单号,订单金额,订单名称,回调url）,
              当支付宝支付结束（可能支付成功，也可能支付失败），支付宝会自动调用回调url，并把支付
              结果通过该url告诉你的服务器端.
            4,当支付完成后，需要在自己的服务器端将支付的订单的订单状态改变.

        微信支付： 需要微信认证，一年300块
    */

    // 伪支付
    $('#pay').click(function() {

        // 支付

        // 支付完成后， 需要把订单状态改变
        $.post('/axf/orderchangestatus/',
            {orderid: $(this).attr('orderid'), status:'1'},
            function (data) {

            if (data.status == 1){
                //如果修改订单成功，则跳转到‘我的’页面
                location.href = '/axf/mine/';
            }
            else {
                console.log(data.msg);
            }

        })

    });

});







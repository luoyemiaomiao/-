$(function () {

    // 全部类型
    $('#all_type').click(function () {
        $('#all_type_container').toggle();  //切换显示隐藏
        $('#all_type_icon').toggleClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')

        // 主动触发$('#sort_rule_container')的click事件
        $('#sort_rule_container').trigger('click')
    });

    // 全部类型的半透明区域
    $('#all_type_container').click(function () {
        $(this).hide();
        $('#all_type_icon').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')
    });


    // 排序规则
    $('#sort_rule').click(function () {
        $('#sort_rule_container').toggle();  //切换显示隐藏
        $('#sort_rule_icon').toggleClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')

        // 主动触发$('#all_type_container')的click事件
        $('#all_type_container').trigger('click')
    });

    // 排序规则的半透明区域
    $('#sort_rule_container').click(function () {
        $(this).hide();
        $('#sort_rule_icon').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')
    });



    // 加入购物车
    $('.addtocart').click(function() {

        //let也是用来声明变量的关键字
        //先得到需要加入购物车的商品id
        let goodsid = $(this).attr('goodsid');

        //数量
        let num = parseInt($(this).prev().find('.num').html());

        //ajax请求
        $.get('/axf/cartadd/', {goodsid: goodsid, num: num}, function(data) {
            // console.log(data);
            // {'status': 1, 'msg': 'ok'}

            //加入购物车成功
            if (data.status == 1){
                console.log('加入购物车成功!')
            }
            //未登录
            else if (data.status == 0){
                location.href = '/axf/login/';
                // location.assign('/axf/login/')
                // window.open('')
            }
            else {
                console.log(data.msg)
            }
        });

    });


    // +
    $('.add').click(function () {
        // let index = $(this).index('.add');
        // let num = $('.num').eq(index);
        // num.html(parseInt(num.html()) + 1)
        let num = $(this).prev();
        num.html(parseInt(num.html()) + 1);
    });

    // -
    $('.reduce').click(function () {
        let num = $(this).next();
        if (num.html() > 1) {
            num.html(parseInt(num.html()) - 1);
        }
    })





});
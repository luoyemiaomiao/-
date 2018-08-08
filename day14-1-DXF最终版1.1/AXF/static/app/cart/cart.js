$(function () {

    // +
    $('.add').click(function () {

        // console.log(11);

        //1,先发送ajax请求给服务器端，让服务器修改数量
        //2,如服务器修改成功则将浏览器中的数量修改

        // 获取cartid
        let cartid = $(this).parents('li').attr('cartid');
        let that = this;
        // console.log(this);
        // console.log($(this));

        //ajax请求
        $.get('/axf/cartnumadd/', {cartid: cartid}, function (data) {
            // console.log(data);

            if (data.status == 1){
                // location.reload()  // 刷新当前页面
                $(that).prev().html(data.num)
            }

            //重新计算总价
            calculate();
        })


    });


    // -
    $('.reduce').click(function () {

        let cartid = $(this).parents('li').attr('cartid');
        let that = this;

        //ajax
        $.post('/axf/cartnumreduce/', {cartid: cartid}, function (data) {
            // console.log(data)

            if (data.status == 1){
                $(that).next().html(data.num)
            }
            else if (data.status == 0) {
                location.assign('/axf/login/')
            }
            else {
                console.log(data.msg)
            }

            //重新计算总价
            calculate();
        });

    });


    // 删除
    $('.delbtn').click(function () {

        let cartid = $(this).parents('li').attr('cartid');
        let that = this;

        //ajax
        $.post('/axf/cartdel/', {cartid: cartid}, function(data) {
            // console.log(data);

            if (data.status == 1){
                $(that).parents('li').remove();
            }
            else if (data.status == 0) {
                location.href = '/axf/login/'
            }
            else {
                console.log(data.msg)
            }

            // 重新检测是否全选
            isAllSelect();

        });


    });


    // 勾选/取消勾选
    $('.select').click(function () {
        let cartid = $(this).parents('li').attr('cartid');
        let that = this;

        //ajax
        $.post('/axf/cartselect/', {cartid: cartid}, function(data) {
            // console.log(data);

            if (data.status == 1) {
                $(that).find('span').html(data.select ? '√' : '');
            }
            else if (data.status == 0) {
                location.href = '/axf/login/'
            }
            else {
                console.log(data.msg)
            }

            // 重新检测是否全选
            isAllSelect();

        });

    });


    // 全选
    $('#allselect').click(function () {

        //先判断要‘全选‘ 还是’取消全选‘
        //1, 如果有未勾选的商品则’全选‘
        //2, 如果都勾选了则’取消全选‘

        let selects = [];  //保存勾选的商品所在购物车的cartid
        let unSelects = [];  //保存未勾选的商品所在购物车的cartid

        // 遍历购物车的所有商品节点
        $('.menuList').each(function() {
            let isSelect = $(this).find('.select').children('span').html();
            if (isSelect) {
                selects.push($(this).attr('cartid'));
            }
            else {
                unSelects.push($(this).attr('cartid'));
            }
        });

        // 去 ‘取消全选’
        if (unSelects.length == 0){
            //ajax： 异步请求
            $.post('/axf/cartallselect/', {action:true}, function(data) {
                // console.log(data);

                if (data.status == 1){
                    $('.select').find('span').html('')
                }
                else if (data.status == 0) {
                    location.href = '/axf/login/'
                }
                else {
                    console.log(data.msg)
                }

                // 重新检测是否全选
                isAllSelect();

            })

        }

        // 去 ‘全选’
        else {
            //ajax
            // $.post('/axf/cartallselect/', {action:false, unselects:unSelects.join('#')}, function(data) {
            $.post('/axf/cartallselect/', {action:false}, function(data) {
                // console.log(data);

                if (data.status == 1){
                    $('.select').find('span').html('√')
                }
                else if (data.status == 0) {
                    location.href = '/axf/login/'
                }
                else {
                    console.log(data.msg)
                }

                // 重新检测是否全选
                isAllSelect();
            })
        }

        // ajax
        //  同步： 在同一个线程中按顺序执行
        //  异步： 在不同的线程中并行执行（多线程）



    });


    // 检测是否全选
    isAllSelect();
    function isAllSelect() {

        // 遍历所有商品的选中状态
        let s = 0;
        $('.select').each(function () {
            if ($(this).find('span').html()) {
                s++
            }
        });

        // 如果全选了，则打勾
        if (s == $('.select').length) {
            $('#allselect').find('span').html('√')
        }
        // 否则不打勾
        else {
            $('#allselect').find('span').html('')
        }

        //重新计算总价
        calculate();
    }


    // 计算总价
    function calculate() {

        //计算总价
        let total = 0; //总价

        $('.menuList').each(function () {
            //如果勾选了
            if ($(this).find('.select').find('span').html()){

                let price = $(this).find('.price').html();  //单价
                let num = $(this).find('.num').html();  //数量
                total += parseFloat(price) * parseInt(num);
            }
        });

        // 显示总价
        $('#totalPrice').html(total.toFixed(2));  // 保留两位小数

    }


    // 结算
    $('#calculate').click(function () {

        //ajax: 不能跨域
        $.post('/axf/orderadd/', function (data) {
            // console.log(data);
            if (data.status == 1){
                location.href = '/axf/order/'+ data.orderid +'/';
            }
            else {
                console.log(data.msg)
            }
        });

    });

});




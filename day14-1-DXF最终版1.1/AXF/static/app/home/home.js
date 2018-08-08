$(function () {

    // 轮播
    new Swiper('#topSwiper', {
        loop: true,
        // 如果需要分页器
        pagination: '.swiper-pagination'
    });

    // 必购
    new Swiper('#swiperMenu', {
        slidesPerView: 3  // 每页显示3个
    });




});







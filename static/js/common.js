$(window).on('scroll', function () {
    const top_btn = '<a href="#" class="top-btn">TOP</a>';
    $(window).scrollTop() > 100 ? $('body').append(top_btn) : $('.top-btn').remove();
});

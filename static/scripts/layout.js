$(document).ready(function () {
    $(".open_bar").click(function () {
        $('.nav_contents').css("display", "block");
        $('.close_bar').css("display", "block");
        $('.open_bar').css("display", "none");
        $('.nav_items li').click(function () {
            $('.nav_contents').css("display", "block");
        });
    });

    $(".close_bar").click(function () {
        $('.nav_contents').css("display", "none");
        $('.close_bar').css("display", "none");
        $('.open_bar').css("display", "block");
    });

    $('nav_items li').each(function () {
        $('.nav_contents').css("display", "none");
    });
});



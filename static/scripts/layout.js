// Nav-bar hamburger for smaller screens

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

// Slide show on large screens

let homeSlide = document.querySelectorAll(".slide");
let i;

function slideNext() {
    for (i = 0; i < homeSlide.length; i++) {
        homeSlide[i].classList.toggle("active")
    };
}
setInterval(slideNext, 5000)


// Slide show on small screens

let smSlide = document.querySelectorAll(".sm-slide");
let current = 0;

function showSlide(index) {
    for (let i = 0; i < smSlide.length; i++) {
        smSlide[i].classList.remove("sm-active");
    }

    smSlide[index].classList.add("sm-active");
}

function smNext() {
    showSlide(current);

    current = (current + 1) % smSlide.length;
}

showSlide(current);
setInterval(smNext, 5000);

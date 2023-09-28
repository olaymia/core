$('.guest-lectures-carousel').owlCarousel({
    loop: true,
    margin: 10,
    nav: true,
    dots: true,
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 1
        },
        1000: {
            items: 1
        }
    }
});

$('.recommended-carousel').owlCarousel({
    loop: true,
    margin: 10,
    nav: true,
    dots: true,
    responsive: {
        0: {
            items: 2
        },
        600: {
            items: 3
        },
        1000: {
            items: 3
        }
    }
});


$(".our-culture-carousel").owlCarousel({
    loop: true,
    margin: 10,
    nav: false,
    dots: true,
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 2
        },
        1000: {
            items: 3
        }
    }
});



$('.header-res-humburger').click(function () {
    $('.bg-menu-overlay').addClass('show');
    $('.left-side-menu').addClass('show');
});

$('.bg-menu-overlay').click(function () {
    $('.bg-menu-overlay').removeClass('show');
    $('.left-side-menu').removeClass('show');
});

// notes popup

$(document).ready(function () {
    $('#savebtn').click(function () {
        $('.ans-desc').toggleClass('d-none');
    })
});
$('.notes').click(function () {
    $('.popup').addClass('d-block');
    $('.popup').removeClass('d-none');
});
$('.cancle').click(function () {
    $('.popup').removeClass('d-block');
    $('.popup').addClass('d-none');
});
// doctor recommended carousel 
$('.doctor-recommended-carousel').owlCarousel({
    loop: true,
    margin: 24,
    nav: true,
    dots: true,
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 2
        },
        1000: {
            items: 3
        }
    }
});

// footer 
// $(function () {
//     $("#footer").load("footer.html");
// });
$('.btn-lab-value').click(function () {
    if ($('.popup').show()) {
        $('.popup').hide();
    }
});


// home menu 
$('.home-responsive-header').click(function () {
    $('.home-menu-overlay').addClass('show');
    $('.home-left-side-menu').addClass('show');
});

$('.home-menu-overlay').click(function () {
    $('.home-menu-overlay').removeClass('show');
    $('.home-left-side-menu').removeClass('show');
});

// questions details page 

// left side 
$('.question-number').click(function () {
    $('.question-num-responsive').addClass('show');
    $('.number-sidebar-overlay').addClass('show');
});

$('.number-sidebar-overlay').click(function () {
    $('.number-sidebar-overlay').removeClass('show');
    $('.question-num-responsive').removeClass('show');
});



// right side 
$('.question-icon').click(function () {
    $('.questions-right-sidebar').addClass('show');
    $('.question-right-sidebar-overlay').addClass('show');
});

$('.question-right-sidebar-overlay').click(function () {
    $('.question-right-sidebar-overlay').removeClass('show');
    $('.questions-right-sidebar').removeClass('show');
});

//lab value popup

$('.btn-lab-value').click(function () {
    $('.lab-value-sidebar').addClass('show');
    $('.lab-value-overlay').addClass('show');
});

$('.lab-value-overlay').click(function () {
    $('.lab-value-overlay').removeClass('show');
    $('.lab-value-sidebar').removeClass('show');
});


$('.lab-close-ico').click(function () {
    $('.lab-value-sidebar').removeClass('show');
});


// header menu 
$('#menu-btn').on("click", () => {
    $('#body-hidden').addClass('body-menubar');
})
$('.home-menu-overlay').click(function () {
    $('#body-hidden').removeClass('body-menubar');
})
(function ($) {
    "use strict";
    $(window).on('load', function () {
        $(".preloader").fadeOut("slow");
    });
    $('.dropdown-menu a.dropdown-toggle').on('click', function (e) {
        if (!$(this).next().hasClass('show')) {
            $(this).parents('.dropdown-menu').first().find('.show').removeClass('show');
        }
        var $subMenu = $(this).next('.dropdown-menu');
        $subMenu.toggleClass('show');
        $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function (e) {
            $('.dropdown-submenu .show').removeClass('show');
        });
        return false;
    });
    $('.search-btn').on('click', function () {
        $('.search-area').toggleClass('open');
    });
    $(document).on('ready', function () {
        $("[data-background]").each(function () {
            $(this).css("background-image", "url(" + $(this).attr("data-background") + ")");
        });
    });
    new WOW().init();
    $('.hero-slider').owlCarousel({
        loop: true,
        nav: true,
        dots: true,
        margin: 0,
        autoplay: true,
        autoplayHoverPause: true,
        autoplayTimeout: 5000,
        items: 1,
        navText: ["<i class='fal fa-angle-left'></i>", "<i class='fal fa-angle-right'></i>"],
        onInitialized: function (event) {
            var $firstAnimatingElements = $('.owl-item').eq(event.item.index).find("[data-animation]");
            doAnimations($firstAnimatingElements);
        },
        onChanged: function (event) {
            var $firstAnimatingElements = $('.owl-item').eq(event.item.index).find("[data-animation]");
            doAnimations($firstAnimatingElements);
        }
    });

    function doAnimations(elements) {
        var animationEndEvents = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
        elements.each(function () {
            var $this = $(this);
            var $animationDelay = $this.data('delay');
            var $animationDuration = $this.data('duration');
            var $animationType = 'animated ' + $this.data('animation');
            $this.css({
                'animation-delay': $animationDelay,
                '-webkit-animation-delay': $animationDelay,
                'animation-duration': $animationDuration,
                '-webkit-animation-duration': $animationDuration,
            });
            $this.addClass($animationType).one(animationEndEvents, function () {
                $this.removeClass($animationType);
            });
        });
    }
    $('.hero-slider2').owlCarousel({
        loop: true,
        margin: 20,
        center: true,
        nav: true,
        dots: false,
        autoplay: false,
        navText: ["<i class='fal fa-angle-left'></i>", "<i class='fal fa-angle-right'></i>"],
        responsive: {
            0: {
                items: 1,
                margin: 0,
            },
            600: {
                items: 2
            },
            1000: {
                items: 2,
            }
        }
    });
    $('.movie-slider').owlCarousel({
        loop: true,
        margin: 20,
        nav: true,
        dots: false,
        autoplay: false,
        navText: ["<i class='far fa-angle-left'></i>", "<i class='far fa-angle-right'></i>"],
        responsive: {
            0: {
                items: 2
            },
            600: {
                items: 3
            },
            1000: {
                items: 4
            },
            1200: {
                items: 5
            }
        }
    });
    $('.movie-slider2').owlCarousel({
        loop: true,
        margin: 20,
        nav: true,
        dots: false,
        autoplay: false,
        navText: ["<i class='far fa-angle-left'></i>", "<i class='far fa-angle-right'></i>"],
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            1000: {
                items: 3
            },
            1200: {
                items: 4
            }
        }
    });
    $('.live-slider').owlCarousel({
        loop: true,
        margin: 20,
        center: true,
        nav: true,
        dots: false,
        autoplay: false,
        navText: ["<i class='far fa-angle-left'></i>", "<i class='far fa-angle-right'></i>"],
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            1000: {
                items: 4
            }
        }
    });
    $('.tv-slider').owlCarousel({
        loop: true,
        margin: 20,
        center: true,
        nav: true,
        dots: false,
        autoplay: false,
        navText: ["<i class='far fa-angle-left'></i>", "<i class='far fa-angle-right'></i>"],
        responsive: {
            0: {
                items: 2
            },
            600: {
                items: 3
            },
            1000: {
                items: 6
            }
        }
    });
    $('.testimonial-slider').owlCarousel({
        loop: true,
        margin: 10,
        nav: false,
        dots: true,
        autoplay: false,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            1000: {
                items: 3
            },
            1400: {
                items: 4
            }
        }
    });
    $('.partner-slider').owlCarousel({
        loop: true,
        margin: 18,
        nav: false,
        dots: false,
        autoplay: true,
        responsive: {
            0: {
                items: 2
            },
            600: {
                items: 3
            },
            1000: {
                items: 6
            }
        }
    });
    $('.counter').countTo();
    $('.counter-box').appear(function () {
        $('.counter').countTo();
    }, {
        accY: -100
    });
    $(".popup-gallery").magnificPopup({
        delegate: '.popup-img',
        type: 'image',
        gallery: {
            enabled: true
        },
    });
    $(".popup-youtube, .popup-vimeo, .popup-gmaps").magnificPopup({
        type: "iframe",
        mainClass: "mfp-fade",
        removalDelay: 160,
        preloader: false,
        fixedContentPos: false
    });
    $(window).scroll(function () {
        if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
            $("#scroll-top").addClass('active');
        } else {
            $("#scroll-top").removeClass('active');
        }
    });
    $("#scroll-top").on('click', function () {
        $("html, body").animate({
            scrollTop: 0
        }, 1500);
        return false;
    });
    $(window).scroll(function () {
        if ($(this).scrollTop() > 50) {
            $('.navbar').addClass("fixed-top");
        } else {
            $('.navbar').removeClass("fixed-top");
        }
    });
    $(window).on('load', function () {
        if ($(".filter-box").children().length > 0) {
            $(".filter-box").isotope({
                itemSelector: '.filter-item',
                masonry: {
                    columnWidth: 1
                },
            });
            $('.filter-btn').on('click', 'li', function () {
                var filterValue = $(this).attr('data-filter');
                $(".filter-box").isotope({
                    filter: filterValue
                });
            });
            $(".filter-btn li").each(function () {
                $(this).on("click", function () {
                    $(this).siblings("li.active").removeClass("active");
                    $(this).addClass("active");
                });
            });
        }
    });
    if ($('#countdown').length) {
        $('#countdown').countdown('2030/01/30', function (event) {
            $(this).html(event.strftime('' + '<div class="row">' + '<div class="col countdown-item">' + '<h2 class="mb-0">%-D</h2>' + '<h5 class="mb-0">روز</h5>' + '</div>' + '<div class="col countdown-item">' + '<h2 class="mb-0">%H</h2>' + '<h5 class="mb-0">ساعت</h5>' + '</div>' + '<div class="col countdown-item">' + '<h2 class="mb-0">%M</h2>' + '<h5 class="mb-0">دقیقه</h5>' + '</div>' + '<div class="col countdown-item">' + '<h2 class="mb-0">%S</h2>' + '<h5 class="mb-0">ثانیه</h5>' + '</div>' + '</div>'));
        });
    }
    if ($('.select').length) {
        $('.select').niceSelect();
    }
    if ($('#player').length) {
        const player = new Plyr('#player');
    }
    let date = new Date().getFullYear();
    $("#date").html(date);
    $(".profile-file-btn").on('click', function (e) {
        $(this).next('.profile-file-input').click();
    });
    const getMode = localStorage.getItem('theme');
    if (getMode === 'dark') {
        $('body').addClass('theme-mode-variables');
        $('.light-btn').css('display', 'none');
        $('.dark-btn').css('display', 'block');
    }
    $('.theme-mode-control').on('click', function () {
        $('body').toggleClass('theme-mode-variables')
        const checkMode = $('body').hasClass('theme-mode-variables');
        const setMode = checkMode ? 'dark' : 'light';
        localStorage.setItem('theme', setMode);
        if (checkMode) {
            $('.light-btn').css('display', 'none');
            $('.dark-btn').css('display', 'block');
        } else {
            $('.light-btn').css('display', 'block');
            $('.dark-btn').css('display', 'none');
        }
    });
    $(window).on('load', function () {
        logoMode()
    });
    $('.theme-mode-control').on('click', function () {
        logoMode()
    });

    function logoMode() {
        let dtv = document.querySelector('.theme-mode-variables');
        if (dtv) {
            $('.logo-light-mode').css('display', 'block');
            $('.logo-dark-mode').css('display', 'none');
        } else {
            $('.logo-light-mode').css('display', 'none');
            $('.logo-dark-mode').css('display', 'block');
        }
    }
})(jQuery);
$(document).ready(function() {
    
    // Same Height
    var $item = $('.carousel .carousel-item');
    var $wHeight = $(window).height();
    $item.eq(0).addClass('active');
    $item.height($wHeight);
    $item.addClass('full-screen');

    $('.carousel .carousel-item img').each(function() {
        var $src = $(this).attr('src');
        var $color = $(this).attr('data-color');
        $(this).parent().css({
            'background-image': 'url(' + $src + ')',
            'background-color': $color
        });
        $(this).remove();
    });

    $(window).on('resize', function() {
        $wHeight = $(window).height();
        $item.height($wHeight);
    });

    $('.carousel').carousel({
        interval: 6000,
        pause: "false"
    });

    //Animate
    $('.animated').css("animation-duration", "2s");

    // Contact
    $('#submit').click(function() {
        $.post("contactus.php", $(".frm").serialize(), function(response) {
            $('#success').html(response);
        });
        return false;
    });

    // Scrollspy
    $('body').scrollspy({
        target: '#navbar'
    });

    // Smoth Scroll
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();

        var target = this.hash;
        var $target = $(target);

        $('html, body').stop().animate({
            'scrollTop': $target.offset().top
        }, 900, 'swing');

        $('.navbar-collapse.collapse').removeClass("show");
    });

    //Sticky
    $(window).scroll(function() {
        if ($(window).scrollTop() > 0) {
            $('.site-navbar').addClass('sticky');
        } else {
            $('.site-navbar').removeClass('sticky');
        };
        if ($(window).scrollTop() > 50) {
            $('.scroll-to-top').addClass('affix');
        } else {
            $('.scroll-to-top').removeClass('affix');
        };

    });


    // Reveal
    window.sr = ScrollReveal();
    sr.reveal('#about h3, #about .col-md-6', {
        duration: 1500,
        reset: true
    }, 50);
    sr.reveal('#services h3, #services .col-md-4', {
        duration: 1500,
        reset: true
    }, 50);
    sr.reveal('#portfolio h3, #portfolio .box', {
        duration: 1500,
        reset: true
    }, 50);
    sr.reveal('#team .col-md-12, #team .col-md-3', {
        duration: 1500,
        reset: true
    }, 50);
});

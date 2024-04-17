
(() => {
    const swiper = new Swiper('.js-hero-slider', {
      slidesPerView: 1,
      loop: true,
      pagination: {
        el: '.js-hero-pagination',
        clickable: true,
      },
  
      a11y: {
        paginationBulletMessage: 'Перейти к слайду {{index}}'
      }
    });
  })();

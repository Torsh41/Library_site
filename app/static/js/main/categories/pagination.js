$(function() {
    $('#user_pagination_container').on('click', function(event) {
    let target = event.target;
    if (target.tagName === 'A' && target.id.includes('list_pagi')) 
    {
      let url_path = target.dataset?.url;
      $.ajax({
        method: 'get',
        url: url_path,
        dataType: 'json',
        success: function(response) {
            categories = Array.from(response);
            $('li').filter(function() {
                return this.id.match(/category_info/);
            }).remove();
            html = "";
            categories.forEach(category => {
                html += `<li class="category__elem" id="${category.id}category_info"><a href="/category/${category.name}/search" class="about__book-link"><div class="category__block">${category.name}</div></a></li>`;
            });
            document.getElementById("categories_block").innerHTML = html;
            pagi = document.getElementById('pagination');
            pagi_li = pagi.querySelector('.pagination__item_cur_page');
            if (pagi_li)
            {
              pagi_li.className = 'pagination__item active';
            }
            for (const child of pagi.children)
            {
              if (categories.length && categories[0].cur_page == child.textContent)
              {
                child.className = 'pagination__item_cur_page';
              }
            }
        },
        error: function(jqXHR, exception) {
            if (exception === 'parsererror')
            {
                window.location.href = '/auth/login';
            }
            else
            {
                console.log(exception);
            }
        }
      });
    }
  });
});
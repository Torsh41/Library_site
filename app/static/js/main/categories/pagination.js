// функция перестройки пагинации категорий для ее правильного отображения
function categories_pagination_update(pages)
{
  $('#pagination').remove();
  let html = `<ul class="pagination__list list-reset" id="pagination">
              <li class="pagination__item disabled">
                &bull;
              </li>`;
  pages.forEach(p => {
    if (p)
    {
      html += `<li class="pagination__item active">
                  <a id="${p}list_pagi" data-url="/get_categories_page/${p}">${p}</a>
                </li>`;
    }
    else
    {
      html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`
    }
   
  });
  html += `<li class="pagination__item disabled">&bull;</li></ul>`;
  div = document.getElementById("user_pagination_container");
  div.insertAdjacentHTML('afterbegin', html);    
}


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
                html += `<li class="category__elem" id="${category.id}category_info"><a href="/category/${category.name}" class="about__book-link"><div class="category__block">${category.name}</div></a></li>`;
            });
            document.getElementById("categories_block").innerHTML = html;
            // перестройка пагинации
            categories_pagination_update(categories[0].pages_count);

            // выделение текущей страницы
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
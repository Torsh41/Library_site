// функция перестройки пагинации категорий для ее правильного отображения
function categories_pagination_update(pages, username)
{
  $('#pagination').remove();
  let html = `<ul class="pagination__list list-reset" id="pagination">
              <li class="pagination__item disabled">
                &bull;
              </li>`;
  pages.forEach(p => {
    if (p)
    {
      html += `<a data-url="/user/${username}/get_categories_page_for_book_adding/${p}">${p}</a>`;
    }
    else
    {
      html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`
    }
   
  });
  html += `<li class="pagination__item disabled">&bull;</li></ul>`;
  div = document.getElementById("categories_pagination");
  div.insertAdjacentHTML('afterbegin', html);    
}


$(function() {
    $('#pagination').on('click', function(event){
        let target = event.target;
        if (target.tagName === 'A') 
        {
          let url_path = target.dataset?.url;
          $.ajax({
            method: 'get',
            url: url_path,
            dataType: 'json',
            success: function(response) {
              let categories = Array.from(response);
              $('a').filter(function() {
                return this.id.match(/categories/);
              }).remove();
              html = '';
              for (let i = 0; i < categories.length; i++)
              {
                if (i == 0)
                {
                  html += `<a class="form__genre" id="${categories[i].id}categories"><input type="radio" name="category" class="form__checkbox" value="${categories[i].name}" checked>${categories[i].name}</a>`;
                }
                else
                {
                  html += `<a class="form__genre" id="${categories[i].id}categories"><input type="radio" name="category" class="form__checkbox" value="${categories[i].name}">${categories[i].name}</a>`;
                }
              }
              div = document.getElementById('cat_container');
              div.insertAdjacentHTML('afterbegin', html);
              // перестройка пагинации
              categories_pagination_update(categories[0].pages_count, categories[0].username);

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
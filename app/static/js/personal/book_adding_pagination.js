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
              categories = Array.from(response);
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
            error: function(error) {
                console.log(error);
            }
          });
        }
    });
});
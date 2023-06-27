function get_user_search_page(url_path, pagination_id)
{
    $.ajax({
        method: 'get',
        url: url_path,
        dataType: 'json',
        success: function(response) {
            users = Array.from(response);
            $('li').filter(function() {
              return this.id.match(/user_info/);
            }).remove();
            url = url_path.split('/');
            html = "";
            users.forEach(user => {
                html += `<li class="users__item" id="${user.id}user_info">
                <span class="users__link">
                  <div class="users__set">
                    <img src="/user/${user.username}/edit-profile/edit-avatar" alt="" class="users__img"> 
                  </div>
                  ${user.username} 
                </span>
                <a class="users__btn" id="${user.id}del_user" onclick="del_user('/admin/admin_panel/user_delete/${user.id}/${url[url.length - 1]}', '${pagination_id}')">Удалить пользователя</a>
              </li>`;
            });
            document.getElementById("users_search_list").innerHTML = html;
            pagi = document.getElementById('1pagination');
            pagi_li = pagi.querySelector('.pagination__item_cur_page');
            if (pagi_li)
            {
              pagi_li.className = 'pagination__item active';
            }
            for (const child of pagi.children)
            {
              if (users.length && users[0].cur_page == child.textContent)
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

function del_user(url_path, pagination_id) 
{
  if (confirm('Подтвердите действие'))
  {
    $.ajax({
      method: 'get',
      url: url_path,
      dataType: 'json',
      success: function(response) {
        get_user_search_page(`/admin/get_user_search_page/${response.cur_page}`);
        $('ul').filter(function() {
          return this.id.match(pagination_id);
        }).remove();
        html = `<ul class="pagination__list list-reset" id="${pagination_id}"><li class="pagination__item disabled">&bull;</li>`;

        if (response.has_elems) 
        {
          for (let i = 1; i <= response.pages; i++)
          {
            if (response.pages > 1 && i == response.cur_page)
            {
              html += ` <li class="pagination__item_cur_page">
                          <a onclick="get_user_search_page('/admin/get_user_search_page/${i}', '${pagination_id}')">${i}</a>
                        </li>`;
            }
            else
            {
              html += ` <li class="pagination__item active">
                        <a onclick="get_user_search_page('/admin/get_user_search_page/${i}', '${pagination_id}')">${i}</a>
                        </li>`;
            }
          }
        }

        html += `<li class="pagination__item disabled">&bull;</li></ul>`;
        
        document.getElementById('user_pagination_container').innerHTML = html;
      },
      error: function(error) {
          console.log(error);
      }
    });
  }
}

function get_category_page(url_path, pagination_id)
{
    $.ajax({
        method: 'get',
        url: url_path,
        dataType: 'json',
        success: function(response) {
          categories = Array.from(response);
          $('li').filter(function() {
            return this.id.match(/category_info/);
          }).remove();
          url = url_path.split('/');
          html = '';
          categories.forEach(category => {
              html += `<li class="category__elem" id="${category.id}category_info">
                        <a onclick="open_book_panel('${category.username}', '${category.name}')" class="category__book-link">${category.name}</a>
                        <a onclick="del_category('/admin/${category.username}/category_delete/${category.id}/${url[url.length - 1]}', '${pagination_id}')" class="category__btn" id="${category.id}del_category">Удалить категорию</a>
                      </li>`;
          });
          document.getElementById("categories_search_list").innerHTML += html;
          form = document.getElementById("add_category_form");
          action = form.getAttribute('action');
          action = action.split('?');
          path = action[0] + `?category_page=${url[url.length - 1]}`;
          form.setAttribute('action', path);
          pagi = document.getElementById('2pagination');
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

function del_category(url_path, pagination_id) 
{
  if (confirm('Подтвердите действие'))
  {
    $.ajax({
      method: 'get',
      url: url_path,
      dataType: 'json',
      success: function(response) {
        get_category_page(`/admin/${response.username}/get_category_search_page/${response.cur_page}`, `${pagination_id}`);
        $('ul').filter(function() {
          return this.id.match(pagination_id);
        }).remove();
        html = `<ul class="pagination__list list-reset" id="${pagination_id}">`;
        html += `<li class="pagination__item disabled">&bull;</li>`;

        if (response.has_elems) 
        {
          for (let i = 1; i <= response.pages; i++)
          {
            if (response.pages > 1 && i == response.cur_page)
            {
              html += ` <li class="pagination__item_cur_page">
                          <a onclick="get_category_page('/admin/${response.username}/get_category_search_page/${i}', '${pagination_id}')">${i}</a>
                        </li>`;
            }
            else
            {
              html += ` <li class="pagination__item active">
                          <a onclick="get_category_page('/admin/${response.username}/get_category_search_page/${i}', '${pagination_id}')">${i}</a>
                        </li>`;
            }
          }
        }

        html += `<li class="pagination__item disabled">&bull;</li></ul>`;
        
        document.getElementById('category_pagination_container').innerHTML = html;
      },
      error: function(error) {
          console.log(error);
      }
    });
  }
}
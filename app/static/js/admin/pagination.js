function get_user_search_page(url_path)
{
    $.ajax({
        method: 'get',
        url: url_path,
        dataType: 'json',
        success: function(response) {
            users = Array.from(response);
            html = "";
            users.forEach(user => {
                html += `<li class="users__item">
                <span class="users__link">
                  <div class="users__set">
                    <img src="/user/${user.username}/edit-profile/edit-avatar" alt="" class="users__img"> 
                  </div>
                  ${user.username} 
                </span>
                <a class="users__btn" id="${user.id}del_user" onclick="">Удалить пользователя</a>
              </li>`;
            });
            document.getElementById("users_search_list").innerHTML = html;
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function get_category_page(url_path)
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
        html = '';
        categories.forEach(category => {
            html += `<li class="category__elem" id="${category.id}category_info"><a class="category__book-link">${ category.name }</a>
            <a href="/admin/<username>/admin_panel/category_delete/<category_id>", username=current_user.username, category_id=category.id)}}", class="category__btn" id="${category.id}del_category">Удалить категорию</a>
          </li>`;
        });
          document.getElementById("categories_search_list").innerHTML += html;
      },
      error: function(error) {
          console.log(error);
      }
  });
}
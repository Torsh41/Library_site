$(document).ready(function () {
    $('#search_users_form').submit(function(event) {
        search_users_on_forum();
        event.preventDefault();
    });
  });

function search_users_on_forum()
{
    if (document.getElementById('username_field').value.trim() && document.getElementById('username_field').value.trim().length <= 62)
    {
        $.ajax({
            method: 'post',
            url: $("#search_users_form").attr('action'),
            dataType: 'json',
            data: $('#search_users_form').serialize(),
            success: function(response) {
            users = Array.from(response);
            div = document.getElementById("main_users_container");
            if (users.length && users[0].result)
            {
                $('ul').filter(function() {
                    return this.id.match("users_search_list");
                }).remove();
                $('h2').filter(function() {
                    return this.id.match("nothing_found");
                }).remove();
                html = `<ul class="users__list list-reset" id="users_search_list">`;
                users.forEach(user => {
                    html += `<li class="users__item" id="${user.id}user_info">
                    <span class="users__link">
                    <div class="users__set">
                        <img src="/user/${user.username}/edit-profile/edit-avatar" alt="" class="users__img"> 
                    </div>
                    ${user.username} 
                    </span>
                    <a class="users__btn" id="${user.id}del_user" onclick="del_user('/admin/admin_panel/user_delete/${user.id}/${user.page}', '1pagination')">Удалить пользователя</a>
                </li>`;
                });
                html += `</ul>`;
                div.insertAdjacentHTML("beforeend", html);

                // Собираем пагинацию 
                $('ul').filter(function() {
                    return this.id.match('1pagination');
                }).remove();
                html = `<div class="list__pagination pagination" id="user_pagination_container">
                        <ul class="pagination__list list-reset" id="1pagination"><li class="pagination__item disabled">&bull;</li>`;
        
                for (let i = 1; i <= users[0].page; i++)
                {
                    if (users[0].page > 1 && i == users[0].cur_page)
                    {
                        html += `<li class="pagination__item_cur_page">
                                <a onclick="get_user_search_page('/admin/get_user_search_page/${i}', '1pagination')">${i}</a>
                                </li>`;
                    }
                    else
                    {
                        html += `<li class="pagination__item active">
                                <a onclick="get_user_search_page('/admin/get_user_search_page/${i}', '1pagination')">${i}</a>
                                </li>`;
                    }
                }
                html += `<li class="pagination__item disabled">&bull;</li></ul></div>`;
                div.insertAdjacentHTML("beforeend", html);
                document.getElementById('username_field').value = '';
            }
            else
            {
                $('h2').filter(function() {
                    return this.id.match("nothing_found");
                }).remove();
                html = `<h2 class="list__title title" id="nothing_found">Ничего не найдено</h2>`;
                div.insertAdjacentHTML("beforeend", html);
                document.getElementById('username_field').value = '';
            }
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
    else if (document.getElementById('username_field').value.trim().length > 62)
    {
        alert('Слишком длинное имя пользователя');
    }
    else
    {
        alert('Заполните поле');
        document.getElementById('username_field').value = '';
    }
}
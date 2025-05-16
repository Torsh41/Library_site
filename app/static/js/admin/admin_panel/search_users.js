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
                    html += `
                    <li id="${user.id}user_info">
                        <a class="users__item__header users__btn" id="user_header_${user.id}" href="javascript:usersItemDetailOpen('${user.id}');" style="width: 100%;">
                            <div class="users__set">
                                <img src="/user/${user.username}/edit-profile/edit-avatar" alt="" class="users__img"> 
                            </div>
                                <span>${user.username}</span>
                            <span>${user.email}</span>
                        </a>
                        <div class="users__item__detail" id="user_detail_${user.id}" style="display: none;">
                            <div><span>Имя: ${user.username}</span></div>
                            <div><span>Почта: ${user.email}</span></div>
                            <div><span>Роль: ${user.role}</span></div>
                            <!--
                            <a class="users__btn" id="${user.id}del_user" data-url='/admin/admin_panel/user_delete/${user.id}/${user.page}' data-pagid='1pagination'>
                                Удалить пользователя
                            </a>
                            -->
                        </div>
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
                
                users[0].pages_count.forEach((page) => {
                    if (page)
                    {
                        if (page == users[0].cur_page)
                        {
                        html += `<li class="pagination__item_cur_page">
                                    <a id='${page}users_p' data-url='/admin/get_user_search_page/${page}' data-pagid='1pagination'>${page}</a>
                                </li>`;
                        }
                        else
                        {
                        html +=  `<li class="pagination__item active">
                                    <a id='${page}users_p' data-url='/admin/get_user_search_page/${page}' data-pagid='1pagination'>${page}</a>
                                </li>`;
                        }
                    }
                    else
                    {
                        html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`;
                    }
                });
                
                html += `<li class="pagination__item disabled">&bull;</li></ul></div>`;
                div.insertAdjacentHTML("beforeend", html);
                document.getElementById('username_field').value = '';
            }
            else
            {
                $('h2').filter(function() {
                    return this.id.match("nothing_found");
                }).remove();
                $('ul').filter(function() {
                    return this.id.match("users_search_list");
                }).remove();
                $('div').filter(function() {
                    return this.id.match("user_pagination_container");
                }).remove();
               
                html = `<h2 class="list__title title" id="nothing_found">Ничего не найдено</h2>`;
                div.insertAdjacentHTML("beforeend", html);
                document.getElementById('username_field').value = '';
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

function usersItemDetailOpen(itemId) {
    document.getElementById("user_header_" + itemId).href = "javascript:usersItemDetailClose('" + itemId + "');";
    document.getElementById("user_detail_" + itemId).style.display = "block";
}

function usersItemDetailClose(itemId) {
    document.getElementById("user_header_" + itemId).href = "javascript:usersItemDetailOpen('" + itemId + "');";
    document.getElementById("user_detail_" + itemId).style.display = "none";
}

$(function() {
    $('#search_users_form').submit(function(event) {
        search_users_on_forum();
        event.preventDefault();
    });

    $('#get_users').click(function(event) {
        search_users_on_forum();
    });
});


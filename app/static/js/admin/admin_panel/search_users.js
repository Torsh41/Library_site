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
                    <a class="users__btn" id="${user.id}del_user" data-url='/admin/admin_panel/user_delete/${user.id}/${user.page}' data-pagid='1pagination'>Удалить пользователя</a>
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
                
                // for (let i = 1; i <= users[0].page; i++)
                // {
                //     if (users[0].page > 1 && i == users[0].cur_page)
                //     {
                //         html += `<li class="pagination__item_cur_page">
                //                     <a id='${i}users_p' data-url='/admin/get_user_search_page/${i}' data-pagid='1pagination'>${i}</a>
                //                 </li>`;
                //     }
                //     else
                //     {
                //         html += `<li class="pagination__item active">
                //                     <a id='${i}users_p' data-url='/admin/get_user_search_page/${i}' data-pagid='1pagination'>${i}</a>
                //                 </li>`;
                //     }
                // }
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

$(function() {
    $('#search_users_form').submit(function(event) {
        search_users_on_forum();
        event.preventDefault();
    });

    $('#get_users').click(function(event) {
        search_users_on_forum();
    });
});


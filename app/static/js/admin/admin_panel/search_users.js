// Global variable, defined later
roles = {};

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
                        <a class="users__item__header users__btn" id="user_header_${user.id}" href="javascript:usersItemDetailOpen('${user.id}');">
                            <div class="users__set">
                                <img src="/user/${user.username}/edit-profile/edit-avatar" alt="" class="users__img"> 
                            </div>
                                <span>${user.username}</span>
                            <span>${user.email}</span>
                        </a>
                        <div class="users__item__detail" id="user_detail_${user.id}" style="display: none;">
                            <div><span>Имя:</span><span>${user.username}</span></div>
                            <div><span>Почта:</span><span>${user.email}</span></div>
                            <div><span>Роль:</span><span id="user_role_${user.id}">${roles[user.role]}</span></div>
                            <div>
                                <select name="user_role" id="role_select_${user.id}">
                                    <option value="">-- Выберите роль --</option>`;
                    for (const [role_id, role_name] of Object.entries(roles)) {
                        html += `   <option value="${role_id}">${role_name}</option>`;
                    }
                    html += `   </select>
                                <a class="users__btn" id="set_user_role_${user.id}" href="javascript:setUserRole('${user.id}');" data-pagid="1pagination">
                                    Изменить роль
                                </a>
                            </div>
                            <div>
                                <div></div>
                                <a class="users__btn" id="${user.id}del_user" data-url='/admin/admin_panel/user_delete/${user.id}/${user.page}' data-pagid='1pagination'>
                                    Удалить пользователя
                                </a>
                            </div>
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

function setUserRole(userId) {
    roleId = document.getElementById("role_select_" + userId).value;
    if (roleId === "") {
        alert("Выберите роль")
    } else {
        fetch("/admin/admin_panel/set_user_role/" + userId + "/" + roleId)
            .then(response => {
                if (response.ok) {
                    document.getElementById("user_role_" + userId).textContent = roles[roleId];
                } else {
                    alert("Что-то пошло не так...");
                }
            })
            .catch(error => console.error('Error:', error));
    }
}


// Кусок говна. Лучше бы его здесь не было.
const promise = fetch( "/get_role_name_list")
    .then(response => response.json())
    .catch(error => console.error('Error:', error));

$(function() {
    Promise.all([promise])
        .then(results => {
            roles = results[0];
            $('#search_users_form').submit(function(event) {
                search_users_on_forum();
                event.preventDefault();
            });

            $('#get_users').click(function(event) {
                search_users_on_forum();
            });
        })
        .catch(err => console.log(err))
});


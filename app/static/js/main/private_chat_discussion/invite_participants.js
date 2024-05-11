// функция перестройки пагинации пользователей для ее правильного отображения
function users_pagination_update(pages_count, chat_id)
{
    $('#pagination').remove();
    let html = `<ul class="pagination__list list-reset" id="pagination">
                <li class="pagination__item disabled">
                    &bull;
                </li>`;
    pages_count.forEach(p => {
        if (p)
        {
            html += `<li class="pagination__item active">
                        <a id="${p}users_p" data-url="/forum/private_chat/${chat_id}/get_users_page_to_invite/${p}">${p}</a>
                    </li>`;
        }
        else
        {
            html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`
        }
    });
    html += `<li class="pagination__item disabled">&bull;</li></ul>`;
    div = document.getElementById("close_invite_form");
    div.insertAdjacentHTML('beforebegin', html);    
}


function get_users_page(chat_id, url_path=`/forum/private_chat/${chat_id}/get_users_page_to_invite/1`)
{
    $.ajax({
        method: 'get',
        url: url_path,
        dataType: 'json',
        success: function (response) {
            users = Array.from(response); let html = "";
            $('#invite_participant_sec').find('div').filter(function() {
                return this.id.match(/user/) || this.id.match('not_found');
            }).remove();

            if (users[0].result)
            {
                users.forEach(user => {
                    html +=`<div class="form__book" id="${user.id}user">
                                <div class="form__info form__book-link">
                                    <span class="form__span-info">Имя пользователя</span>
                                    <span class="form__span-info">${user.username}</span>
                                </div>
                                <input class="comments__command" id="${user.id}send_invite" formmethod="post" type="submit" value="Отправить приглашение">
                            </div>`;
                });
                let title = document.getElementById('invite_title');
                title.insertAdjacentHTML('afterend', html);
                // перестройка пагинации
                users_pagination_update(users[0].pages_count, users[0].chat_id);
                // выделение текущей страницы
                pagi = document.getElementById('pagination');
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
            }
            else
            {
                $('#pagination').remove();
                html +=`<div class="container list__container" id="not_found">
                            <div class="list__wrap">
                                <h2 class="list__title title">Нет доступных пользователей для приглашения</h2>
                            </div>
                        </div>`;
                let title = document.getElementById('invite_title');
                title.insertAdjacentHTML('afterend', html);
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


let invite_socket = io('/private_chat'); 
$(function() {
    let chat_id = $("#write_msg").data('username').split(';')[2];
    $('#invite_participant').on('click', function(event) {
        $('#invite_participant_sec').css('display', 'block');
        get_users_page(chat_id);
      
    });

    $('#close_invite_form').on('click', function(event) {
        $('#invite_participant_sec').css('display', 'none');
    });

    $("#invite_participant_sec").on("click", function(event) {
        let target = event.target;
        if (target.tagName === "INPUT" && target.id.includes('send_invite'))
        {
            let user_id = target.id.split('send_invite')[0];
            invite_socket.emit("get invite", {
                user_id: user_id,
                chat_id: chat_id
            });
        }
    });

    socket.on("invitation", function (response) {
        if (response.result)
        {
             $('#invite_participant_sec').css('display', 'none');
             alert('К нам присоединился пользователь с именем ' + response.new_user_name + '!');
             let participants_count = Number(document.getElementById('participants_count').textContent.split(' ')[1]);
             document.getElementById('participants_count').textContent = 'Участников: ' + (participants_count + 1);
        }
        else
        {
            $('#invite_participant_sec').css('display', 'none');
            alert('Участников чата может быть не более 30!');
        }
    });

    let callback = function() {
        $('#pagination').off();
        $('#pagination').on('click', function(event) {
            let target = event.target;
            if (target.tagName === 'A' && target.id.includes('users_p'))
            {
                let url_path = target.dataset?.url;
                get_users_page(chat_id, url_path);
            }
        });
    };

    let observer = new MutationObserver(callback);

    // наблюдать за всем
    observer.observe(document, {
        childList: true, // наблюдать за непосредственными детьми
        subtree: true, // и более глубокими потомками
        attributes: true,
        characterData: true
    });
});
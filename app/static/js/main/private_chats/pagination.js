// функция перестройки пагинации чатов для ее правильного отображения
function chats_pagination_update(pages)
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
                        <a id="${p}chats_pagi" data-url="/forum/get_chats_page/${p}">${p}</a>
                    </li>`;
        }
        else
        {
            html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`;
        }
    
    });
    html += `<li class="pagination__item disabled">&bull;</li></ul>`;
    let div = document.getElementById("chats_pagination_container");
    div.insertAdjacentHTML('afterbegin', html);    
}


$(function() {
    $('#chats_section').on('click', function(event) {
        let target = event.target;
        if (target.tagName === 'A' && target.id.includes('del_chat')) 
        {
            if (confirm('Подтвердите действие'))
            {
                let chat_id = target.dataset?.chatid;
                let page = target.dataset?.page;
                $.ajax({
                    method: 'get',
                    url: `/forum/delete_private_chat/${chat_id}/${page}`,
                    dataType: 'json',
                    success: function(response) {
                        if (response[0].has_elems)
                        {
                            $('li').filter(function() {
                                return this.id.match('chat_block');
                            }).remove();
                            chats = Array.from(response); let = html = '';
                            chats.forEach(chat => {
                                html += `<li id="${chat.id}chat_block" class="fraction__list-item">
                                            <a id="${chat.id}chat_name" href="/forum/private_chat/${chat.id}" class="fraction__topic-link">
                                                <div class="fraction__topic">
                                                    <p class="fraction__text-error">${chat.name}</p>
                                                </div>
                                            </a>`;
                                            if (chat.type == "created")
                                            {
                                                html += `<div class="fraction__wrapper-command"><a class="comments__command" id="${chat.id}del_chat" data-page="${chat.cur_page}" data-chatid="${chat.id}">Удалить чат</a></div>`;
                                            }
                                        html += `</li>`;
                            });
                            let ul = document.getElementById("chats_block");
                            ul.insertAdjacentHTML('afterbegin', html);
                            chats_pagination_update(response[0].pages_count);
    
                        }
                        else
                        {
                            $(`#${chat_id}chat_block`).remove();
                            $(`#chats_pagination_container`).remove();
                            let html = `<div class="list__wrap">
                                            <a class="title list__name" href="/forum">У вас пока нет приватных чатов, но вы можете создать их на странице форума</a>
                                        </div>`;
                            let div = document.getElementById("chats_div");
                            div.insertAdjacentHTML('afterbegin', html);
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
        }
        else if (target.tagName === 'A' && target.id.includes('chats_pagi'))
        {
            let url = target.dataset?.url;
            $.ajax({
                method: 'get',
                url: url,
                dataType: 'json',
                success: function(response) {
                    $('li').filter(function() {
                        return this.id.match('chat_block');
                    }).remove();
                   
                    chats = Array.from(response); let = html = '';
                    chats.forEach(chat => {
                        html += `<li id="${chat.id}chat_block" class="fraction__list-item">
                                        <a id="${chat.id}chat_name" href="/forum/private_chat/${chat.id}" class="fraction__topic-link">
                                            <div class="fraction__topic">
                                                <p class="fraction__text-error">${chat.name}</p>
                                            </div>
                                        </a>`;
                                    if (chat.type == "created")
                                    {
                                        html += `<div class="fraction__wrapper-command"><a class="comments__command" id="${chat.id}del_chat" data-page="${chat.cur_page}" data-chatid="${chat.id}">Удалить чат</a></div>`;
                                    }
                                html += `</li>`;
                    });
                    let ul = document.getElementById("chats_block");
                    ul.insertAdjacentHTML('afterbegin', html);
                    // перестройка пагинации
                    chats_pagination_update(response[0].pages_count);

                    // выделение текущей страницы
                    let pagi = document.getElementById('pagination');
                    let pagi_li = pagi.querySelector('.pagination__item_cur_page');
                    if (pagi_li)
                    {
                        pagi_li.className = 'pagination__item active';
                    }
                    for (const child of pagi.children)
                    {
                        if (chats.length && chats[0].cur_page == child.textContent)
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
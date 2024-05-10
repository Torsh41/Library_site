function search_books_on_category_page(category_name, list_id=undefined) 
{
    if (document.getElementById('books_find_field').value.trim() || document.getElementById('books_data_field').value.trim() || document.getElementById('description_field').value.trim())
    {
        $.ajax({
            method: 'post',
            url: `/category/${category_name}/search`,
            dataType: 'json',
            data: $('#search_form').serialize(),
            success: function(response) {
                let result = response.result;
                let html = '';
                if (result)
                {
                    let books = response.data;
                    search_result = books;
                    $('section').filter(function() {
                        return this.id.match("search_result");
                    }).remove();
                    $('section').filter(function() {
                        return this.id.match("nothing_found");
                    }).remove();
                    $('#pagination_container').remove();
                    document.getElementById("books_find_field").value = "";
                    html += `<section id="search_result" class="list">
                                <div class="container list__container">
                                    <div class="list__wrap">
                                    <h2 class="list__title title">Вот, что нашлось</h2>
                                    <span class="list__results"> Всего результатов: ${books[1][0].results_count} </span>
                                    <ul class="list__books list-reset list__booksStart" id="book_search_res_ul">`;
                    books[1].forEach(book => {
                        html += `<li class="list__book" id="${book.id}search_books_info">
                                    <a href="/book-page/${book.name}?list_id=${list_id}" class="list__book-set">
                                        <img class="list__book-set" src="/${book.name}/get-cover" alt="">
                                    </a>
                                <div class="list__book-wrap">`;

                        if (book.current_user_is_auth)
                        {
                            html += `<a href="/user/${book.username}/add-book-in-list-tmp/${book.id}?list_id=${list_id}" class="list__book-delete-btn">Добавить в список</a>`;
                        }
                        html += `<a href="/book-page/${book.name}?list_id=${list_id}" class="list__link-book">Книга: ${book.name}</a>
                                    <span class="list__link">Автор: ${book.author}</span>
                                    <div class="list__mark-star">
                                        <span class="list__mark-visible">Оценка ${book.grade}</span>
                                        <img src="/static/styles/img/star1.svg" alt="" class="list__star">
                                    </div>
                                    </div>
                                </li>`;
                    });
                    html += ` </ul></div></div></section>`;
                    
                    // собираем пагинацию
                    html += `<div id="pagination_container" class="list__pagination pagination">
                                <ul id="pagination" class="pagination__list list-reset">
                                    <li class="pagination__item disabled">
                                        &bull;
                                    </li>`;
                    for (let page = 1; page <= books[1][0].pages_count; page++)
                    {
                        if (page == 1)
                        {
                            html += `<li class="pagination__item_cur_page">
                                    <a id='${page}books_p'>${page}</a>
                                    </li>`;
                        }
                        else
                        {
                            html += `<li class="pagination__item active">
                                        <a id='${page}books_p'>${page}</a>
                                    </li>`;
                        }
                    }
                    html += `<li class="pagination__item disabled">
                                &bull;
                            </li></ul></div>`;

                    let section = document.getElementById('first_section');
                    section.insertAdjacentHTML('afterend', html);
                    section = document.getElementById('search_result');
                    document.getElementById('books_data_field').value = '';
                    document.getElementById('description_field').value = '';
                    section.scrollIntoView(); // Прокрутка до верхней границы
                }
                else
                {
                    $('section').filter(function() {
                    return this.id.match("search_result");
                    }).remove();
                    $('section').filter(function() {
                    return this.id.match("nothing_found");
                    }).remove();
                    $('#pagination_container').remove();
                    document.getElementById("books_find_field").value = "";
                    html = `<section id="nothing_found" class="list">
                                <div class="container list__container">
                                <div class="list__wrap">
                                    <h2 class="list__title title">Ничего не найдено</h2>
                                </div>
                                </div>
                            </section>`;
                    let section = document.getElementById('first_section');
                    section.insertAdjacentHTML('afterend', html);
                    document.getElementById('books_data_field').value = '';
                    document.getElementById('description_field').value = '';
                    document.getElementById('nothing_found').scrollIntoView(); // Прокрутка до верхней границы
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
    else if (!document.getElementById('books_find_field').value.trim() && !document.getElementById('books_data_field').value.trim() && !document.getElementById('description_field').value.trim())
    {
        document.getElementById('books_find_field').value = '';
        document.getElementById('books_data_field').value = '';
        document.getElementById('description_field').value = '';
        alert('Заполните хотя бы одно поле поиска');
    }
}      


function get_books_page_on_category(page, list_id=undefined)
{
    $('li').filter(function() {
        return this.id.match(/search_books_info/);
    }).remove();
    document.getElementById("books_find_field").value = "";
    let html = '';
    search_result[page].forEach(book => {
        html += `<li class="list__book" id="${book.id}search_books_info">
                    <a href="/book-page/${book.name}?list_id=${list_id}" class="list__book-set">
                        <img class="list__book-set" src="/${book.name}/get-cover" alt="">
                    </a>
                <div class="list__book-wrap">`;

        if (book.current_user_is_auth)
        {
                html += `<a href="/user/${book.username}/add-book-in-list-tmp/${book.id}?list_id=${list_id}" class="list__book-delete-btn">Добавить в список</a>`;
        }
        html += `<a href="/book-page/${book.name}?list_id=${list_id}" class="list__link-book">Книга: ${book.name}</a>
                    <span class="list__link">Автор: ${book.author}</span>
                    <div class="list__mark-star">
                        <span class="list__mark-visible">Оценка ${book.grade}</span>
                        <img src="/static/styles/img/star1.svg" alt="" class="list__star">
                    </div>
                    </div>
                </li>`;
    });
    let ul = document.getElementById('book_search_res_ul');
    ul.insertAdjacentHTML('afterbegin', html);
    // выделение текущей страницы
    pagi = document.getElementById('pagination');
    pagi_li = pagi.querySelector('.pagination__item_cur_page');
    if (pagi_li)
    {
        pagi_li.className = 'pagination__item active';
    }
    for (const child of pagi.children)
    {
        if (page == child.textContent)
        {
            child.className = 'pagination__item_cur_page';
        }
    }
}


let search_result;
$(function() {
    let category_name = document.getElementById("cat_title").dataset?.name;
    let list_id = document.getElementById("cat_title").dataset?.listid;
    let callback = function() {
        $('#pagination').off();
        $('#pagination').on('click', function(event) {
            let target = event.target;
            if (target.tagName === 'A' && target.id.includes('books_p'))
            {
                let page = Number(target.textContent);
                get_books_page_on_category(page, list_id);
            }
        });
    };
    $('#search_form').submit(function(event) {
        search_books_on_category_page(category_name, list_id);
        event.preventDefault();
    });

    $('#find_books_button').on('click', function(event) {
        search_books_on_category_page(category_name, list_id);
    });

    let observer = new MutationObserver(callback);

    // наблюдать за всем
    observer.observe(document, {
            childList: true, // наблюдать за непосредственными детьми
            subtree: true, // и более глубокими потомками
            attributes: true,
            characterData: true
        });
});
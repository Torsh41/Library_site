function show_new_data(books_info, page)
{
    $('#table_head').remove();
    let html = '<div id="table_head" class="form__maintaining">';
    books_info.forEach(book_info => {
        html += `<div class="form__book" id="${book_info.id}book">
                    <div class="form__info form__book-id">
                        <span class="form__span-title">ID</span>
                        <span class="form__span-info">${book_info.id}</span>
                    </div>
                    <div class="form__info form__book-name">
                        <span class="form__span-title">Название</span>
                        <span class="form__span-info">${book_info.name}</span>
                    </div>
                    <div class="form__info form__book-author">
                        <span class="form__span-title">Авторы</span>
                        <span class="form__span-info">${book_info.authors}</span>
                    </div>
                    <div class="form__info form__book-part">
                        <span class="form__span-title">Серии</span> 
                        <span class="form__span-info">${book_info.series}</span>
                    </div>
                    <div class="form__info form__book-category">
                        <span class="form__span-title">Категории</span>
                        <span class="form__span-info">${book_info.categories}</span>
                    </div>
                    <div class="form__info form__book-date">
                        <span class="form__span-title">Дата публикации</span>
                        <span class="form__span-info">${book_info.publishing_date}</span>
                    </div>
                    <div class="form__info form__book-countpages">
                        <span class="form__span-title">Количество страниц</span>
                        <span class="form__span-info">${book_info.pages_count}</span>
                    </div>
                    <div class="form__info form__book-isbn">
                        <span class="form__span-title">ISBN</span>
                        <span class="form__span-info">${book_info.isbn}</span>
                    </div>
                    <div class="form__info form__book-comments">
                        <span class="form__span-title">Комментарии</span>
                        <span class="form__span-info">${book_info.comments}</span>
                    </div>
                    <div class="form__info form__book-info">
                        <span class="form__span-title">Краткое содержание</span>
                        <span class="form__span-info">${book_info.summary}</span>
                    </div>
                    <div class="form__info form__book-link">
                        <span class="form__span-title">Ссылка</span>
                        <span class="form__span-info">${book_info.link}</span>
                    </div>
                    <div class="form__info form__book-count">
                        <span class="form__span-title">Количество</span>
                        <span class="form__span-info"><input class="book__count" id="${book_info.id}books_count" min="0"
                                formmethod="post" placeholder="введите наличие" required type="number"
                                value="${book_info.count}"></span>
                    </div>
                    <div class="form__book-delete">
                        <input class="form__delete-btn" id="${book_info.id}del_book" data-page="${page}" formmethod="post" type="submit"
                            value="удалить из списка">
                    </div>
                </div>`;
    })
    html += '</div>';
    let thead = document.getElementById('main_table');
    thead.insertAdjacentHTML('afterbegin', html);
    thead.scrollIntoView();
}


function build_pagination(cur_page, pages)
{
    $('#pagination').remove();
    let html = `<ul class="pagination__list list-reset" id="pagination">
                    <li class="pagination__item disabled">
                        &bull;
                    </li>`;
    
    pages.forEach(p => {
        if (p)
        {
            if (p == cur_page)
            {
                html += `<li class="pagination__item_cur_page">
                            <a id="${p}books_info_p" data-url="/books-maintaining/get-page/${p}">${p}</a>
                        </li>`;
            }
            else
            {
                html += `<li class="pagination__item active">
                            <a id="${p}books_info_p" data-url="/books-maintaining/get-page/${p}">${p}</a>
                        </li>`;
            }
        }
        else
        {
            html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`;
        }
    });
    html += `<li class="pagination__item disabled">&bull;</li></ul>`;
    let pagi_div = document.getElementById('pagination_container');
    pagi_div.insertAdjacentHTML('afterbegin', html);
}


$(function() {
    $('#search_form').submit(function(event) {
        event.preventDefault();
    });

    $('#add_info').on('click', function(event) {
        $('#add_info_sec').css('display', 'block');
        $('#sel_file').val("");
    });
    
    $('#close_form').on('click', function(event) {
        $('#add_info_sec').css('display', 'none');
        $('#sel_file').val("");
    });

    $('#new_books_info').on('click', function(event) {
        let f = new FormData(document.getElementById('new_info_form'));
        $.ajax({
            method: 'post',
            url: '/books-maintaining/add-file',
            dataType: 'json',
            contentType: false,
			processData: false,
            data: f,
            success: function(response) {
                $('section').filter(function() {
                    return this.id.match("not_found");
                }).remove();
                let books_info = Array.from(response);
                if (!books_info[0].result)
                {
                    alert('Проверьте файл на соответствие шаблону!');
                    $('#sel_file').val("");
                }
                else
                {
                    show_new_data(books_info, books_info[0].cur_page);
                    document.getElementById("add_info_sec").style.display = "none";
                    $('#sel_file').val("");

                    // перестроим пагинацию 
                    build_pagination(books_info[0].cur_page, books_info[0].pages_count_arr);
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
    });

    $('#pagination_container').on('click', function(event) {
        let target = event.target;
        if (target.tagName === 'A' && target.id.includes('books_info_p'))
        {
            let url_path = target.dataset?.url;
            $.ajax({
                method: 'get',
                url: url_path,
                dataType: 'json',
                success: function(response) {
                    let books_info = Array.from(response);
                    show_new_data(books_info, books_info[0].cur_page);

                    // перестроим пагинацию 
                    build_pagination(books_info[0].cur_page, books_info[0].pages_count_arr);

                    pagi = document.getElementById('pagination');
                    pagi_li = pagi.querySelector('.pagination__item_cur_page');
                    if (pagi_li)
                    {
                        pagi_li.className = 'pagination__item active';
                    }
                    for (const child of pagi.children)
                    {
                        if (books_info.length && books_info[0].cur_page == child.textContent)
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

    $('#find_books_button').on('click', function(event) {
        if (!document.getElementById('name_field').value.trim().length)
        {
            alert('Заполните поле');
        }
        else
        {
            let search_form = new FormData(document.getElementById('search_form'));
            $.ajax({
                method: 'post',
                url: '/books-maintaining/search',
                dataType: 'json',
                contentType: false,
                processData: false,
                data: search_form,
                success: function(response) {
                    let books_info = Array.from(response);
                    if (books_info[0].result)
                    {
                        $('section').filter(function() {
                            return this.id.match("not_found");
                        }).remove();

                        show_new_data(books_info, books_info[0].cur_page);
                        let found_elem = document.getElementById(books_info[0].id_of_found_elem + 'book');
                        found_elem.scrollIntoView();
                        $(`#${books_info[0].id_of_found_elem}book`).css("opacity", ".15").animate({ opacity: "1" }, "slow");
                        document.getElementById("name_field").value = "";

                        // перестроим пагинацию 
                        build_pagination(books_info[0].cur_page, books_info[0].pages_count_arr);

                        pagi = document.getElementById('pagination');
                        pagi_li = pagi.querySelector('.pagination__item_cur_page');
                        if (pagi_li)
                        {
                            pagi_li.className = 'pagination__item active';
                        }
                        for (const child of pagi.children)
                        {
                            if (books_info.length && books_info[0].cur_page == child.textContent)
                            {
                                child.className = 'pagination__item_cur_page';
                            }
                        }
                    }
                    else
                    {
                        $('#table_head').remove();
                        $('section').filter(function() {
                            return this.id.match("not_found");
                        }).remove();
                        $('#pagination').remove();

                        let html = `<section class="list" id="not_found">
                                        <div class="container list__container">
                                            <div class="list__wrap">
                                                <h2 class="list__title title">Ничего не найдено</h2>
                                            </div>
                                        </div>
                                    </section>`;
                        let table = document.getElementById('main_table');
                        table.insertAdjacentHTML('afterbegin', html);
                        document.getElementById("name_field").value = "";
                        table.scrollIntoView();
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

    $("#main_table").on("keyup click", function(event) {
        let target = event.target;
        if (target.tagName === "INPUT" && target.id.includes('books_count') && event.which == 13)
        {
            let data = new FormData();
            data.append("id", target.id.split('books_count')[0]); data.append("new_count", target.value);
            $.ajax({
                method: 'post',
                url: '/books-maintaining/change-count',
                dataType: 'json',
                contentType: false,
                processData: false,
                data: data,
                success: function(response) {
                    alert("Количество успешно изменено");
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }
        else if (target.tagName === "INPUT" && target.id.includes('del_book') && (event.which == 13 || event.which == 1))
        {
            if (confirm("Подтвердите действие")) 
            {
                let data = new FormData();
                data.append("id", target.id.split('del_book')[0]); data.append("page", target.dataset?.page);
                $.ajax({
                    method: 'post',
                    url: '/books-maintaining/del-book',
                    dataType: 'json',
                    contentType: false,
                    processData: false,
                    data: data,
                    success: function(response) {
                        if (response.result)
                        {
                            $(`#${data.get('id')}book`).remove();

                            // перестроим пагинацию 
                            build_pagination(response.cur_page, response.pages_count_arr);
                        }
                        else
                        {
                            alert('Что-то пошло не так:(');
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
    });
});
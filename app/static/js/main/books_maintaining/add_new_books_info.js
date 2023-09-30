function show_new_data(books_info)
{
    $('tbody').remove();
    let html = '<tbody>';
    books_info.forEach(book_info => {
        html += `<tr id="${book_info.id}book">
                    <td>${book_info.id}</td>
                    <td>${book_info.name}</td>
                    <td>${book_info.authors}</td>
                    <td>${book_info.series}</td>
                    <td>${book_info.categories}</td>
                    <td>${book_info.publishing_date}</td>
                    <td>${book_info.pages_count}</td>
                    <td>${book_info.isbn}</td>
                    <td>${book_info.comments}</td>
                    <td>${book_info.summary}</td>
                    <td>${book_info.link}</td>
                    <td><input id="${book_info.id}books_count" min="0" formmethod="post" placeholder="введите наличие" required type="number" value="${book_info.count}"></td>
                    <td><input id="${book_info.id}del_book" formmethod="post" type="submit" value="удалить из списка"></td>
                </tr>`;
    })
    html += '</tbody>';
  
    let thead = document.getElementById('table_head');
    thead.insertAdjacentHTML('afterend', html);
    thead.scrollIntoView();
}


function build_pagination(cur_page, pages)
{
    $('#pagination').remove();
    let html = `<ul class="pagination__list list-reset" id="pagination">
                    <li class="pagination__item disabled">
                        &bull;
                    </li>`;
    
    for (let i = 1; i <= pages; i++)
    {
        if (cur_page == i)
        {
            html += `<li class="pagination__item_cur_page">
                        <a id="${i}books_info_p" data-url="/books-maintaining/get-page/${i}">${i}</a>
                    </li>`;
        }
        else
        {
            html += `<li class="pagination__item active">
                        <a id="${i}books_info_p" data-url="/books-maintaining/get-page/${i}">${i}</a>
                    </li>`;
        }
    
    }
    html += `<li class="pagination__item disabled">
                &bull;
            </li>
            </ul>`;
    let pagi_div = document.getElementById('pagination_container');
    pagi_div.insertAdjacentHTML('afterbegin', html);
}


$(function() {
    $('#search_form').submit(function(event) {
        event.preventDefault();
    });

    $('#add_info').on('click', function(event) {
        $('#add_info_sec').css('display', 'block');
    });
    
    $('#close_form').on('click', function(event) {
        $('#add_info_sec').css('display', 'none');
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
                show_new_data(books_info);
                document.getElementById("add_info_sec").style.display = "none";
                document.getElementById("sel_file").value = "";

                // перестроим пагинацию 
                build_pagination(books_info[0].cur_page, books_info[0].pages);
            },
            error: function(error) {
                console.log(error);
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
                    show_new_data(books_info);
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
                error: function(error) {
                    console.log(error);
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

                        show_new_data(books_info);
                        let found_elem = document.getElementById(books_info[0].id_of_found_elem + 'book');
                        found_elem.scrollIntoView();
                        $(`#${books_info[0].id_of_found_elem}book`).css("opacity", ".4").animate({ opacity: "1" }, "slow");
                        document.getElementById("name_field").value = "";

                        // перестроим пагинацию 
                        build_pagination(books_info[0].cur_page, books_info[0].pages);

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
                        $('tbody').remove();
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
                        table.insertAdjacentHTML('afterend', html);
                        document.getElementById("name_field").value = "";
                        table.scrollIntoView();
                    }
                },
                error: function(error) {
                    console.log(error);
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
                data.append("id", target.id.split('del_book')[0]);
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
                        }
                        else
                        {
                            alert('Что-то пошло не так:(');
                        }
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            }
        }
    });
});
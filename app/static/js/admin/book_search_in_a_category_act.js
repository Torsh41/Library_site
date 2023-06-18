$(document).ready(function () {
    $('#category_book_search').submit(function(event) {
        search_books_on_category();
        event.preventDefault();
    });
  });

function edit_elem_state(id)
{
    if (document.getElementById(id).style.display == "block")
    {
        document.getElementById(id).style.display = "none";
        if (id == "book_categories")
          document.getElementById("book_search_in_a_category").style.display = "none";
        if (id == "users_search")
        {
            $('ul').filter(function() {
                return this.id.match("users_search_list");
            }).remove();
            $('h2').filter(function() {
                return this.id.match("nothing_found");
            }).remove();
            document.getElementById("username_field").value = "";
        }
    }
    else
    {
        document.getElementById(id).style.display = "block";
    }
}

function form_activate(form_id, title_id, data)
{
    edit_elem_state(form_id);
    if (document.getElementById(id).style.display == "block")
        document.getElementById(title_id).value += ` ${data}`;
}

function open_book_panel(username, category)
{
    document.getElementById("book_search_in_a_category").style.display = "block";
    document.getElementById('search_res_id').value = "";
    $('li').filter(function () {
        return this.id.match(/book_info/);
    }).remove();
    $('div').filter(function () {
        return this.id.match("nothing");
    }).remove();
    $('ul').filter(function () {
        return this.id.match('3pagination');
    }).remove();
    $('h2').filter(function() {
        return this.id.match("category_title");
      }).remove();
    html = `<h2 class="list__title title" id="category_title">Книги в категории "${category}"</h2>`;
    div = document.getElementById("2cont");
    div.insertAdjacentHTML("afterbegin", html);
    form = document.getElementById("category_book_search");
    form.setAttribute("action", `/admin/${username}/search_books_on_admin_panel/${category}`);
}

function search_books_on_category()
{
    if (document.getElementById('search_res_id').value.trim() && document.getElementById('search_res_id').value.trim().length <= 200)
    {
      $.ajax({
          method: 'post',
          url: $('#category_book_search').attr('action'),
          dataType: 'json',
          data: $('#category_book_search').serialize(),
          success: function (response) {
              books = Array.from(response);
              $('li').filter(function () {
                  return this.id.match(/book_info/);
              }).remove();
              $('div').filter(function () {
                return this.id.match("nothing");
              }).remove();
              $('ul').filter(function () {
                return this.id.match('3pagination');
                }).remove();

              html = "";
              if (books[0].has_books)
              {
                books.forEach(book => {
                    html += `<li class="list__book" id="${book.id}book_info">
                                <div class="list__top">
                                    
                                    <img style="width: 310px; height: 190px" src="/${book.name}/get-cover" alt=""> 
                              
                                    <ul class="book__list list-reset">
                                        <a href="/book-page/${book.name}" class="list__link"><b>Книга:</b> ${book.name}</a>
                                        <li class="book__list-element"><b>Автор:</b> ${book.author}</li>
                                        <li class="book__list-element"><b>Оценка:</b> ${book.grade}</li>
                                        <a class="book__list-element" onclick="del_book_from_site('/admin/${book.username}/del_book/${book.category}/${book.id}/${1}')">Удалить книгу</a>
                                    </ul>
                                      
                                </div>
                            </li>`;
                });
                ul = document.getElementById('list_res');
                ul.insertAdjacentHTML('beforeend', html);
                document.getElementById('search_res_id').value = "";

                // собираем пагинацию
                html = `<ul class="pagination__list list-reset" id="3pagination">
                <li class="pagination__item disabled">&bull;</li>`;
                try {
                    for (let i = 1; i <= books[0].pages; i++) {
                        if (books[0].pages > 1 && i == books[0].cur_page)
                        {
                            html += `<li class="pagination__item_cur_page">
                                        <a onclick="get_books_page_on_admin_panel('/admin/${books[0].username}/search_books_on_admin_panel/${books[0].category}?page=${i}')">${i}</a>
                                     </li>`;
                        }
                        else
                        {
                            html += `<li class="pagination__item active">
                                        <a onclick="get_books_page_on_admin_panel('/admin/${books[0].username}/search_books_on_admin_panel/${books[0].category}?page=${i}')">${i}</a>
                                    </li>`;
                        }
                    }
                }
                catch {}
                html += `<li class="pagination__item disabled">&bull;</li></ul>`;
                div = document.getElementById('books_keeper_cont');
                div.insertAdjacentHTML('beforeend', html);
            }
            else
            {
                html = `<div class="container list__container" id="nothing">
                            <div class="list__wrap">
                            <h2 class="list__title title">Ничего не найдено</h2>
                            </div>
                        </div>`;
                ul = document.getElementById('list_res');
                ul.insertAdjacentHTML('beforeend', html);  
                document.getElementById('search_res_id').value = "";
            }
          },
          error: function(error) {
              console.log(error);
        }
      });
    }
    else if (document.getElementById('search_res_id').value.trim().length > 200)
    {
        alert('Слишком длинный ввод');
    }
    else
    {
        alert('Заполните поле');
        document.getElementById('search_res_id').value = '';
    }
}

function get_books_page_on_admin_panel(url_path)
{
    $.ajax({
        method: 'get',
        url: url_path,
        dataType: 'json',
        success: function(response) {
          books = Array.from(response);
          $('li').filter(function() {
            return this.id.match(/book_info/);
          }).remove();
          if (books[0].has_books)
          {
                html = '';
                books.forEach(book => {
                        html += `<li class="list__book" id="${book.id}book_info">
                                    <div class="list__top">
                                        
                                        <img style="width: 310px; height: 190px" src="/${book.name}/get-cover" alt=""> 
                                
                                        <ul class="book__list list-reset">
                                            <a href="/book-page/${book.name}" class="list__link"><b>Книга:</b> ${book.name}</a>
                                            <li class="book__list-element"><b>Автор:</b> ${book.author}</li>
                                            <li class="book__list-element"><b>Оценка:</b> ${book.grade}</li>
                                            <a class="book__list-element" onclick="del_book_from_site('/admin/${book.username}/del_book/${book.category}/${book.id}/${book.cur_page}')">Удалить книгу</a>
                                        </ul>
                                        
                                    </div>
                                </li>`;
                    });
                    ul = document.getElementById('list_res');
                    ul.insertAdjacentHTML('beforeend', html);
                    pagi = document.getElementById('3pagination');
                    pagi_li = pagi.querySelector('.pagination__item_cur_page');
                    if (pagi_li)
                    {
                        pagi_li.className = 'pagination__item active';
                    }
                    for (const child of pagi.children)
                    {
                        if (books[0].cur_page == child.textContent)
                        {
                            child.className = 'pagination__item_cur_page';
                        }
                    }
          }
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function del_book_from_site(url_path)
{
    if (confirm('Подтвердите действие'))
    {
        $.ajax({
            method: 'get',
            url: url_path,
            dataType: 'json',
            success: function(response) {
            $('ul').filter(function() {
                    return this.id.match("3pagination");
                }).remove();
            get_books_page_on_admin_panel(`/admin/${response.username}/search_books_on_admin_panel/${response.category}?page=${response.cur_page}`);
            html = `<ul class="pagination__list list-reset" id="3pagination">`;
            html += `<li class="pagination__item disabled">&bull;</li>`;
    
            if (response.has_elems) 
            {
                for (let i = 1; i <= response.pages; i++)
                {
                    if (response.pages > 1 && i == response.cur_page)
                    {
                          
                        html += `<li class="pagination__item_cur_page">
                                    <a onclick="get_books_page_on_admin_panel('/admin/${response.username}/search_books_on_admin_panel/${response.category}?page=${i}')">${i}</a>
                                </li>`;
                    }
                    else
                    {
                        html += `<li class="pagination__item active">
                                    <a onclick="get_books_page_on_admin_panel('/admin/${response.username}/search_books_on_admin_panel/${response.category}?page=${i}')">${i}</a>
                                </li>`;
                    }
                }
            }
    
            html += `<li class="pagination__item disabled">&bull;</li></ul>`;
            ul = document.getElementById('list_res');
            ul.insertAdjacentHTML('afterend', html);  
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
}
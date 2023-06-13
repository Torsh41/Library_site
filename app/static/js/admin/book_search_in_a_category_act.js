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
    if (document.getElementById('search_res_id').value.trim() && document.getElementById('search_res_id').value.trim().length <= 64)
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
                                    
                                    <img class="list__book-set" src="/${book.name}/get-cover" alt=""> 
                                    
                                    <div class="list__book-wrap">
                                        <a href="/book-page/${book.name}" class="list__link">Книга: ${book.name}</a>
                                        <span class="list__link">Автор: ${book.author}</span>
                                        <span class="list__link">Оценка: ${book.grade}</span>
                                        <a class="list__btn">Удалить книгу</a>
                                    </div>
                                </div>
                                </li>`;
                });
                ul = document.getElementById('list_res');
                ul.insertAdjacentHTML('beforeend', html);
                document.getElementById('search_res_id').value = "";

                // собираем пагинацию
                html = `<ul class="pagination__list list-reset" id="pagination">
                <li class="pagination__item disabled">&bull;</li>`;
                try {
                    for (let i = 1; i <= books[0].pages; i++) {
                        html += `<li class="pagination__item active">
                            <a onclick="">${i}</a>
                            </li>`;
                    }
                }
                catch { }
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

           
            
            
         
            //   html = `<ul class="pagination__list list-reset" id="pagination">
            // <li class="pagination__item disabled">&bull;</li>`;
            //   try {
            //       for (let i = 1; i <= posts[0].pages; i++) {
            //           html += `<li class="pagination__item active">
            //               <a onclick="get_posts_page('/get_posts_page/${posts[0].topic_id}/${i}')">${i}</a>
            //               </li>`;
        //           }
        //       }
        //       catch { }
        //       html += `<li class="pagination__item disabled">&bull;</li></ul>`;
        //       document.getElementById("posts_pagination_container").innerHTML = html;
        //       document.getElementById("post_body_id").value = "";

        //       $('span').filter(function () {
        //           return this.id.match('posts_count');
        //       }).remove();
        //       html = `<span class="main__span-forum" id="posts_count">Сообщений: ${posts[0].posts_count}</span>`;
        //       div = document.getElementById("main_container");
        //       div.insertAdjacentHTML("beforeend", html);
        //   },
        //   get success() {
        //       return this._success;
        //   },
        //   set success(value) {
        //       this._success = value;
          },
          error: function(error) {
              console.log(error);
        }
      });
    }
    else if (!document.getElementById('search_res_id').value.trim())
    {
        alert('Заполните поле');
        document.getElementById('search_res_id').value = "";
    }
    else if (document.getElementById('search_res_id').value.trim().length > 64)
    {
        alert('Слишком длинный ввод');
        document.getElementById('search_res_id').value = "";
    }
}
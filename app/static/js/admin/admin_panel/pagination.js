// функция перестройки пагинации пользователей для ее правильного отображения
function users_pagination_update(pages)
{
  $('#1pagination').remove();
  let html = `<ul class="pagination__list list-reset" id="1pagination">
              <li class="pagination__item disabled">
                &bull;
              </li>`;
  pages.forEach(p => {
    if (p)
    {
      html += `<li class="pagination__item_cur_page">
                  <a id='${p}users_p' data-url='/admin/get_user_search_page/${p}' data-pagid='1pagination'>${p}</a>
              </li>`;
    }
    else
    {
      html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`;
    }
   
  });
  html += `<li class="pagination__item disabled">&bull;</li></ul>`;
  div = document.getElementById("user_pagination_container");
  div.insertAdjacentHTML('afterbegin', html);    
}

function get_user_search_page(url_path, pagination_id)
{
    $.ajax({
        method: 'get',
        url: url_path,
        dataType: 'json',
        success: function(response) {
            users = Array.from(response);
            $('li').filter(function() {
              return this.id.match(/user_info/);
            }).remove();
            url = url_path.split('/');
            html = "";
            users.forEach(user => {
                html += `<li class="users__item" id="${user.id}user_info">
                          <span class="users__link">
                            <div class="users__set">
                              <img src="/user/${user.username}/edit-profile/edit-avatar" alt="" class="users__img"> 
                            </div>
                            ${user.username} 
                          </span>
                          <a class="users__btn" id="${user.id}del_user" data-url='/admin/admin_panel/user_delete/${user.id}/${url[url.length - 1]}' data-pagid='${pagination_id}'>Удалить пользователя</a>
                        </li>`;
            });
            document.getElementById("users_search_list").innerHTML = html;

            if (users.length)
            {
              // перестройка пагинации
              users_pagination_update(users[0].pages_count);

              // выделение текущей страницы
              pagi = document.getElementById('1pagination');
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

function del_user(url_path, pagination_id) 
{
  if (confirm('Подтвердите действие'))
  {
    $.ajax({
      method: 'get',
      url: url_path,
      dataType: 'json',
      success: function(response) {
        //let url = url_path.split('/'); user_id_for_del = url[url.length - 2];
        // $('li').filter(function() {
        //   return this.id.match(user_id_for_del + "user_info");
        // }).remove();
        get_user_search_page(`/admin/get_user_search_page/${response.cur_page}`);

        $('ul').filter(function() {
          return this.id.match(pagination_id);
        }).remove();
        html = `<ul class="pagination__list list-reset" id="${pagination_id}"><li class="pagination__item disabled">&bull;</li>`;

        if (response.has_elems) 
        {
          response.pages_count.forEach((page) => {
            if (page)
            {
              if (page == response.cur_page)
              {
                html += `<li class="pagination__item_cur_page">
                            <a id="${page}users_p" data-url='/admin/get_user_search_page/${page}' data-pagid='${pagination_id}'>${page}</a>
                          </li>`;
              }
              else
              {
                html += `<li class="pagination__item active">
                            <a id="${page}users_p" data-url='/admin/get_user_search_page/${page}' data-pagid='${pagination_id}'>${page}</a>
                          </li>`;
              }
            }
            else
            {
              html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`;
            }
          
          });
        }
          // for (let i = 1; i <= response.pages; i++)
          // {
          //   if (response.pages > 1 && i == response.cur_page)
          //   {
          //     html += ` <li class="pagination__item_cur_page">
          //                 <a id="${i}users_p" data-url='/admin/get_user_search_page/${i}' data-pagid='${pagination_id}'>${i}</a>
          //               </li>`;
          //   }
          //   else
          //   {
          //     html += ` <li class="pagination__item active">
          //                 <a id="${i}users_p" data-url='/admin/get_user_search_page/${i}' data-pagid='${pagination_id}'>${i}</a>
          //               </li>`;
          //   }
          // }
        

        html += `<li class="pagination__item disabled">&bull;</li></ul>`;
        
        document.getElementById('user_pagination_container').innerHTML = html;
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

// функция перестройки пагинации категорий для ее правильного отображения
function categories_pagination_update(pages, username)
{
  $('#2pagination').remove();
  let html = `<ul class="pagination__list list-reset" id="2pagination">
              <li class="pagination__item disabled">
                &bull;
              </li>`;
  pages.forEach(p => {
    if (p)
    {
      html += `<li class="pagination__item active">
                <a id="${p}categories_p" data-url="/admin/${username}/get_category_search_page/${p}" data-pagi="2pagination">${p}</a>
              </li>`;
    }
    else
    {
      html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`;
    }
   
  });
  html += `<li class="pagination__item disabled">&bull;</li></ul>`;
  div = document.getElementById("category_pagination_container");
  div.insertAdjacentHTML('afterbegin', html);    
}

function get_category_page(url_path, pagination_id)
{
    $.ajax({
        method: 'get',
        url: url_path,
        dataType: 'json',
        success: function(response) {
          categories = Array.from(response);
          $('li').filter(function() {
            return this.id.match(/category_info/);
          }).remove();
          url = url_path.split('/');
          html = '';
          categories.forEach(category => {
              html += `<li class="category__elem" id="${category.id}category_info">
                        <a id='${category.id}show_books' data-username='${category.username}' data-catname='${category.name}' class="category__book-link">${category.name}</a>
                        <a data-url='/admin/${category.username}/category_delete/${category.id}/${url[url.length - 1]}' data-pagi='${pagination_id}' class="category__btn" id="${category.id}del_category">Удалить категорию</a>
                      </li>`;
          });
          document.getElementById("categories_search_list").innerHTML += html;
          form = document.getElementById("add_category_form");
          action = form.getAttribute('action');
          action = action.split('?');
          path = action[0] + `?category_page=${url[url.length - 1]}`;
          form.setAttribute('action', path);

          // перестройка пагинации
          categories_pagination_update(categories[0].pages_count, categories[0].username);

          // выделение текущей страницы
          pagi = document.getElementById('2pagination');
          pagi_li = pagi.querySelector('.pagination__item_cur_page');
          if (pagi_li)
          {
            pagi_li.className = 'pagination__item active';
          }
          for (const child of pagi.children)
          {
            if (categories.length && categories[0].cur_page == child.textContent)
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
            $('div').filter(function() {
              return this.id.match("user_pagination_container");
            }).remove();
            $('h2').filter(function() {
                return this.id.match("nothing_found");
            }).remove();
            
            document.getElementById("username_field").value = "";
        }
    }
    else
    {
        if (id != 'book_search_in_a_category')
        {
          document.getElementById(id).style.display = "block";
          document.getElementById(id).scrollIntoView(); // Прокрутка до верхней границы
        }
    }
}

function del_category(url_path, pagination_id) 
{
  if (confirm('Подтвердите действие'))
  {
    $.ajax({
      method: 'get',
      url: url_path,
      dataType: 'json',
      success: function(response) {
        get_category_page(`/admin/${response.username}/get_category_search_page/${response.cur_page}`, `${pagination_id}`);
    
        $('ul').filter(function() {
          return this.id.match(pagination_id);
        }).remove();

        edit_elem_state('book_search_in_a_category');
        
        let html = `<ul class="pagination__list list-reset" id="${pagination_id}">`;
        html += `<li class="pagination__item disabled">&bull;</li>`;

        if (response.has_elems) 
        {
          response.pages_count.forEach(page => {
            if (page)
            { 
              if (page == response.cur_page)
              {
                html += `<li class="pagination__item_cur_page">
                        <a id='${page}categories_p' data-url='/admin/${response.username}/get_category_search_page/${page}' data-pagi='${pagination_id}'>${page}</a>
                      </li>`;
              }
              else
              {
                html += `<li class="pagination__item active">
                    <a id='${page}categories_p' data-url='/admin/${response.username}/get_category_search_page/${page}' data-pagi='${pagination_id}'>${page}</a>
                    </li>`;
              }
            }
            else
            {
              html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`;
            }
           
          });
        }

        html += `<li class="pagination__item disabled">&bull;</li></ul>`;
        
        document.getElementById('category_pagination_container').innerHTML = html;
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

function open_book_panel(username, category)
{
    section = document.getElementById("book_search_in_a_category");
    section.style.display = "block";
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
    section.scrollIntoView(); // Прокрутка до верхней границы
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
                                
                                <a href="/book-page/${book.name}" class="list__book-set">
                                   <img class="list__book-set" src="/${book.name}/get-cover" alt=""> 
                                </a>
                                    
                                
                                <div class="list__book-wrap">
                                        <a href="/book-page/${book.name}" class="list__link-book"><u>Книга:</u> ${book.name}</a>
                                        <span class="list__link"><b>Автор:</b> ${book.author}</span>
                                        <span class="list__mark-visible"><b>Оценка:</b> ${book.grade}</span>
                                        <a id='${book.id}book_d' class="list__book-delete-btn" data-url='/admin/${book.username}/del_book/${book.category}/${book.id}/${1}'>Удалить книгу</a>
                                </div>
                            </li>`;
                });
                ul = document.getElementById('list_res');
                ul.insertAdjacentHTML('beforeend', html);
                document.getElementById('search_res_id').value = "";

                // собираем пагинацию
                html = `<div class="list__pagination pagination" id="3pagination_container">
                            <ul class="pagination__list list-reset" id="3pagination">
                        <li class="pagination__item disabled">&bull;</li>`;

                books[0].pages_count.forEach((page) => {
                  if (page)
                  {
                    if (page == books[0].cur_page)
                    {
                      html += `<li class="pagination__item_cur_page">
                                  <a id="${page}get_books_p" data-url='/admin/${books[0].username}/search_books_on_admin_panel/${books[0].category}?page=${page}'>${page}</a>
                              </li>`;
                    }
                    else
                    {
                      
                      html += `<li class="pagination__item active">
                                <a id="${page}get_books_p" data-url='/admin/${books[0].username}/search_books_on_admin_panel/${books[0].category}?page=${page}'>${page}</a>
                                </li>`;
                    }
                  }
                  else
                  {
                      html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`;
                  }
                });

                html += `<li class="pagination__item disabled">&bull;</li></ul></div>`;
                div = document.getElementById('2cont');
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


// функция перестройки пагинации книг для ее правильного отображения
function books_pagination_update(pages, username, category)
{
  $('#3pagination').remove();
  let html = `<ul class="pagination__list list-reset" id="3pagination">
              <li class="pagination__item disabled">
                &bull;
              </li>`;
  pages.forEach(p => {
    if (p)
    {
      html += `<li class="pagination__item_cur_page">
                  <a id="${p}get_books_p" data-url='/admin/${username}/search_books_on_admin_panel/${category}?page=${p}'>${p}</a>
              </li>`;
    }
    else
    {
      html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`;
    }
   
  });
  html += `<li class="pagination__item disabled">&bull;</li></ul>`;
  div = document.getElementById("3pagination_container");
  div.insertAdjacentHTML('afterbegin', html);    
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
                                     <a href="/book-page/${book.name}" class="list__book-set">
                                        <img class="list__book-set" src="/${book.name}/get-cover" alt=""> 
                                    </a>
                         
                     
                                    <div class="list__book-wrap">
                                            <a href="/book-page/${book.name}" class="list__link-book"><u>Книга:</u> ${book.name}</a>
                                            <span class="list__link"><b>Автор:</b> ${book.author}</span>
                                            <span class="list__mark-visible"><b>Оценка:</b> ${book.grade}</span>
                                            <a id='${book.id}book_d' class="list__book-delete-btn" data-url='/admin/${book.username}/del_book/${book.category}/${book.id}/${book.cur_page}'>Удалить книгу</a>
                                    </div>
                                </li>`;
                    });
                    ul = document.getElementById('list_res');
                    ul.insertAdjacentHTML('beforeend', html);
                    // перестройка пагинации
                    books_pagination_update(books[0].pages_count, books[0].username, books[0].category);

                    // выделение текущей страницы
                    pagi = document.getElementById('3pagination');
                    pagi_li = pagi.querySelector('.pagination__item_cur_page');
                    if (pagi_li)
                    {
                        pagi_li.className = 'pagination__item active';
                    }
                    for (const child of pagi.children)
                    {
                        if (books.length && books[0].cur_page == child.textContent)
                        {
                            child.className = 'pagination__item_cur_page';
                        }
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
            html = `<div class="list__pagination pagination" id="3pagination_container">
                        <ul class="pagination__list list-reset" id="3pagination">`;
            html += `<li class="pagination__item disabled">&bull;</li>`;
    
            if (response.has_elems) 
            {
              response.pages_count.forEach(page => {
                if (page)
                {
                  if (page == response.cur_page)
                  {
                      html += `<li class="pagination__item_cur_page">
                                  <a id='${page}get_books_p' data-url='/admin/${response.username}/search_books_on_admin_panel/${response.category}?page=${page}'>${page}</a>
                              </li>`;
                  }
                  else
                  {
                      html += `<li class="pagination__item active">
                                  <a id='${page}get_books_p' data-url='/admin/${response.username}/search_books_on_admin_panel/${response.category}?page=${page}'>${page}</a>
                              </li>`;
                  }
                }
                else
                {
                  html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`;
                }
              });
            }
              
            html += `<li class="pagination__item disabled">&bull;</li></ul></div>`;
            ul = document.getElementById('list_res');
            ul.insertAdjacentHTML('afterend', html);  
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

let callback = function() {
  $('#user_pagination_container').off();
  $('#user_pagination_container').on('click', function(event) {
    let target = event.target;
    if (target.tagName === 'A' && target.id.includes('users_p'))
    {
      let url_path = target.dataset?.url;
      let pagination_id = target.dataset?.pagid;
      get_user_search_page(url_path, pagination_id);
    }
  });
  $('#users_search_list').off();
  $('#users_search_list').on('click', function(event) {
    let target = event.target;
    if (target.tagName === 'A' && target.id.includes('del_user'))
    {
      let url_path = target.dataset?.url;
      let pagination_id = target.dataset?.pagid;
      del_user(url_path, pagination_id);
    }
  });
  $('#category_pagination_container').off();
  $('#category_pagination_container').on('click', function(event) {
    let target = event.target;
    if (target.tagName === 'A' && target.id.includes('categories_p'))
    {
      let url_path = target.dataset?.url;
      let pagination_id = target.dataset?.pagi;
      get_category_page(url_path, pagination_id);
    }
  })
  $('#category_book_search').off();
  $('#category_book_search').submit(function(event) {
    search_books_on_category();
    event.preventDefault();
  });
  $('#users_list').off();
  $('#users_list').on('click', function(event) {
      let id = event.target.dataset?.info;
      edit_elem_state(id);
  });
  $('#categories_list').off();
  $('#categories_list').on('click', function(event) {
      let id = event.target.dataset?.info;
      edit_elem_state(id);
  });
  $('#book_categories').off();
  $('#book_categories').on('click', function(event) {
      let target = event.target;
      if (target.tagName === 'svg' || target.tagName === 'g' || target.tagName === 'rect')
      {
        document.getElementById("popupCategoryForm").style.display = "block";
      }
      else if (target.tagName === 'A' && target.id.includes('show_books'))
      {
        let username = target.dataset?.username;
        let category = target.dataset?.catname;
        open_book_panel(username, category);
      }
      else if (target.tagName === 'A' && target.id.includes('del_category'))
      {
        let url_path = target.dataset?.url;
        let pagination_id = target.dataset?.pagi;
        del_category(url_path, pagination_id);
      }
  });
  $('#find_book').off();
  $('#find_book').on('click', function(event) {
      search_books_on_category();
  });
  $('#3pagination_container').off();
  $('#3pagination_container').on('click', function(event) {
      let target = event.target;
      if (target.tagName === 'A' && target.id.includes('get_books_p'))
      {
          let url_path = target.dataset?.url;
          get_books_page_on_admin_panel(url_path);
      }
  });
  $('#list_res').off();
  $('#list_res').on('click', function(event) {
      let target = event.target;
      if (target.tagName === 'A' && target.id.includes('book_d'))
      {
          let url_path = target.dataset?.url;
          del_book_from_site(url_path);
      }
  });

  $('#close_cat_form').off();
  $('#close_cat_form').on('click', function(event) {
    document.getElementById("popupCategoryForm").style.display = "none";
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









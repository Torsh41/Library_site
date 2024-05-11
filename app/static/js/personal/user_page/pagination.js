// функция перестройки пагинации списков пользователей для ее правильного отображения
function lists_pagination_update(pages, username)
{
  $('#pagination').remove();
  let html = `<ul class="pagination__list list-reset" id="pagination">
              <li class="pagination__item disabled">
                &bull;
              </li>`;
  pages.forEach(p => {
    if (p)
    {
      html += `<li class="pagination__item_cur_page">
                  <a data-url='/user/${username}/get_lists_page/${p}'>${p}</a>
              </li>`;
    }
    else
    {
      html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`;
    }
   
  });
  html += `<li class="pagination__item disabled">&bull;</li></ul>`;
  let div = document.getElementById("pagination_container");
  div.insertAdjacentHTML('afterbegin', html);    
}


// функция перестройки пагинации элементов списка пользователя для ее правильного отображения
function items_pagination_update(pages, username, cataloge_id)
{
  $("#" + cataloge_id + "books_pagination").remove();
  let html = `<ul class="pagination__list list-reset" id="${cataloge_id}books_pagination">
              <li class="pagination__item disabled">
                &bull;
              </li>`;
  pages.forEach(p => {
    if (p)
    {
      html += `<li class="pagination__item_cur_page">
                <a data-url='/user/${username}/get_books_page/${cataloge_id}/${p}' id='${cataloge_id}books_page'>${p}</a>
              </li>`;
    }
    else
    {
      html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`;
    }
   
  });
  html += `<li class="pagination__item disabled">&bull;</li></ul>`;
  div = document.getElementById(cataloge_id + "books_pagination_container");
  div.insertAdjacentHTML('afterbegin', html);    
}


function get_lists_page(url_path)
{
    $.ajax({
      method: 'get',
      url: url_path,
      dataType: 'json',
      success: function(response) {
        let cataloges = Array.from(response);
        $('section').filter(function() {
          return this.id.match(/cataloge_info/);
        }).remove();
        let url = url_path.split('/');
        let html = '';
        cataloges.forEach(cataloge => {
          html += `<section class="list" id="${cataloge.id}cataloge_info">
          <div class="container list__container">
            <div class="list__wrap">
              <h2 class="list__title title">${cataloge.name}</h2>
              <!--Название списка, которое ввел пользователь-->

              <ul class="list__books list-reset" id="${cataloge.id}books_info_container">
                <!--Добавление книги в список - перебрасывает в рааздел категорий книг-->
                <li class="list__book list__add">
                  <a href="/categories?list_id=${cataloge.id}" class="list__link">
                    <div class="list__block-add">
                      <svg class="list__svg2" width="78" height="78" viewBox="0 0 78 78" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <g clip-path="url(#clip0_139_2)">
                          <rect x="35" width="8" height="78" fill="#cec8bd" />
                          <rect x="78" y="35" width="8" height="78" transform="rotate(90 78 35)" fill="#cec8bd" />
                        </g>
                        <defs>
                          <clipPath id="clip0_139_2">
                            <rect width="78" height="78" fill="white" />
                          </clipPath>
                        </defs>
                      </svg>
                    </div>
                  </a>
                </li>`;
                let items = Array.from(cataloge.items);
                items.forEach(item => {
                  html += `<li class="list__book" id="${cataloge.id}book_info">
                            <a href="/book-page/${item.id}" class="list__book-set">
                              <img class="list__book-set" src="/${item.id}/get-cover" alt="">
                            </a>
                          
                            <div class="list__book-wrap">
                              <a href="/book-page/${item.id}" class="list__link-book"><u>Книга:</u> ${item.name}</a>`;
                  html += `<select name="read_state" class="book__select" id="${cataloge.id}${item.id}state" data-itemid="${item.id}">`;
                            if (item.read_state == "Планирую")
                              html += `<option class="book__state book__plan" value="Планирую" selected>Планирую</option>  
                                        <option class="book__state book__read" value="Читаю">Читаю</option>
                                        <option class="book__state book__fuck" value="Заброшено">Заброшено</option>
                                        <option class="book__state book__done" value="Прочитано">Прочитано</option>`;
                            else if (item.read_state == "Читаю")
                              html += `<option class="book__state book__plan" value="Планирую">Палнирую</option>
                                        <option class="book__state book__read" value="Читаю" selected>Читаю</option>
                                        <option class="book__state book__fuck" value="Заброшено">Заброшено</option>
                                        <option class="book__state book__done" value="Прочитано">Прочитано</option>`;
                            else if (item.read_state == "Заброшено")
                              html += `<option class="book__state book__plan" value="Планирую">Планирую</option>
                                        <option class="book__state book__read" value="Читаю">Читаю</option>
                                        <option class="book__state book__fuck" value="Заброшено" selected>Заброшено</option>
                                        <option class="book__state book__done" value="Прочитано">Прочитано</option>`;
                            else if (item.read_state == "Прочитано")
                              html += `<option class="book__state book__plan" value="Планирую">Планирую</option>
                                        <option class="book__state book__read" value="Читаю">Читаю</option>
                                        <option class="book__state book__fuck" value="Заброшено">Заброшено</option>
                                        <option class="book__state book__done" value="Прочитано" selected>Прочитано</option>`;
                  html += `</select>`;            
                  html += `<a class="list__book-delete-btn" data-url='/user/${cataloge.username}/delete-item/${cataloge.id}/${item.id}/${1}' id='${cataloge.id}del_book'>Удалить книгу из списка</a>
                          </div>
                        </li>`;
                });
                html += `</ul>`;

                // собираем пагинацию книг каждого списка
                html += `<div class="list__pagination pagination" id="${cataloge.id}books_pagination_container">
                            <ul class="pagination__list list-reset" id="${cataloge.id}books_pagination">
                              <li class="pagination__item disabled">&bull;</li>`;
                if (items.length != 0)
                {
                  items[0].pages_count.forEach(p => {
                      if (p)
                      {
                        if (p == 1)
                        {
                          html += `<li class="pagination__item_cur_page">
                                    <a data-url='/user/${cataloge.username}/get_books_page/${cataloge.id}/${p}' id='${cataloge.id}books_page'>${p}</a>
                                  </li>`;
                        }
                        else
                        {
                          html += `<li class="pagination__item active">
                                      <a data-url='/user/${cataloge.username}/get_books_page/${cataloge.id}/${p}' id='${cataloge.id}books_page'>${p}</a>
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
                html += `<div class="list__end">
                          <a class="list__delete-btn" id="${cataloge.id}del_list" data-url="/user/${cataloge.username}/delete-list/${cataloge.id}/${url[url.length - 1]}">Удалить список
                          </a></div></div></div></section>`;
        }); 
        let div = document.getElementById('lists_container');
        div.insertAdjacentHTML('afterbegin', html);
        if (cataloges.length)
        {
          // перестройка пагинации
          lists_pagination_update(cataloges[0].pages_count, cataloges[0].username);

          // выделение текущей страницы
          pagi = document.getElementById('pagination');
          pagi_li = pagi.querySelector('.pagination__item_cur_page');
          if (pagi_li)
          {
            pagi_li.className = 'pagination__item active';
          }
          for (const child of pagi.children)
          {
            if (cataloges.length && cataloges[0].cur_page == child.textContent)
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

function get_books_page(url_path, cataloge_id)
{
  $.ajax({
    method: 'get',
    url: url_path,
    dataType: 'json',
    success: function(response) {
      books = Array.from(response);
      $('li').filter(function() {
        return this.id.match(cataloge_id + 'book_info');
      }).remove();
      url = url_path.split('/');
      let html = '';
      books.forEach(book => {
        html += `<li class="list__book" id="${cataloge_id}book_info">
                    <a href="/book-page/${book.id}" class="list__book-set">
                      <img class="list__book-set" src="/${book.id}/get-cover" alt="">
                    </a>
                    
                    <div class="list__book-wrap">
                      <a href="/book-page/${book.id}" class="list__link-book"><u>Книга:</u> ${book.name}</a>
                      <select name="read_state" class="book__select" id="${cataloge_id}${book.id}state" data-itemid="${book.id}">`;
                        if (book.read_state == "Планирую")
                          html += `<option class="book__state book__plan" value="Планирую" selected>Планирую</option>  
                                    <option class="book__state book__read" value="Читаю">Читаю</option>
                                    <option class="book__state book__fuck" value="Заброшено">Заброшено</option>
                                    <option class="book__state book__done" value="Прочитано">Прочитано</option>`;
                        else if (book.read_state == "Читаю")
                          html += `<option class="book__state book__plan" value="Планирую">Планирую</option>
                                    <option class="book__state book__read" value="Читаю" selected>Читаю</option>
                                    <option class="book__state book__fuck" value="Заброшено">Заброшено</option>
                                    <option class="book__state book__done" value="Прочитано">Прочитано</option>`;
                        else if (book.read_state == "Заброшено")
                          html += `<option class="book__state book__plan" value="Планирую">Планирую</option>
                                    <option class="book__state book__read" value="Читаю">Читаю</option>
                                    <option class="book__state book__fuck" value="Заброшено" selected>Заброшено</option>
                                    <option class="book__state book__done" value="Прочитано">Прочитано</option>`;
                        else if (book.read_state == "Прочитано")
                          html += `<option class="book__state book__plan" value="Планирую">Планирую</option>
                                    <option class="book__state book__read" value="Читаю">Читаю</option>
                                    <option class="book__state book__fuck" value="Заброшено">Заброшено</option>
                                    <option class="book__state book__done" value="Прочитано" selected>Прочитано</option>`;
                        html += `</select>`;
                      
        html += `<a class="list__book-delete-btn" data-url='/user/${book.username_of_cur_user}/delete-item/${cataloge_id}/${book.id}/${url[url.length - 1]}' id='${cataloge_id}del_book'>Удалить книгу из списка</a>
                  </div>
                </li>`;
      });
      document.getElementById(cataloge_id + 'books_info_container').innerHTML += html;
      // перестройка пагинации
      items_pagination_update(books[0].pages_count, books[0].username_of_cur_user, cataloge_id);

      // выделение текущей страницы
      pagi = document.getElementById(cataloge_id + 'books_pagination');
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


$(function() {
  $('#pagination_container').on('click', function(event){
    let target = event.target;
    if (target.tagName === 'A') 
    {
      let url_path = target.dataset?.url;
      get_lists_page(url_path);
    }
  });

  $('#lists_container').on('click', function(event){
    let target = event.target;
    if (target.tagName === 'A' && target.id.includes('del_list')) 
    {
      let url_path = target.dataset?.url;
      if (confirm('Подтвердите действие'))
      {
        $.ajax({
          method: 'get',
          url: url_path,
          dataType: 'json',
          success: function(response) {
            get_lists_page(`/user/${response.username}/get_lists_page/${response.cur_page}`);
            $('ul').filter(function() {
              return this.id.match('pagination');
            }).remove();
            html = `<ul class="pagination__list list-reset" id="pagination">
                      <li class="pagination__item disabled">&bull;</li>`;

            if (response.has_elems) 
            {
              response.pages_count.forEach(page => {
                if (page)
                {
                  if (page == response.cur_page)
                  {
                    html += `<li class="pagination__item_cur_page">
                              <a data-url="/user/${response.username}/get_lists_page/${page}">${page}</a>
                            </li>`;
                  }
                  else
                  {
                    html += `<li class="pagination__item active">
                              <a data-url="/user/${response.username}/get_lists_page/${page}">${page}</a>
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
            document.getElementById('pagination_container').innerHTML = html;
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
    else if (target.tagName === 'A' && target.id.includes('books_page'))
    {
      let url_path = target.dataset?.url;
      let cataloge_id = url_path.split('/')[4];
      get_books_page(url_path, cataloge_id);
      
    }
    else if (target.tagName === 'A' && target.id.includes('del_book'))
    {
      let url_path = target.dataset?.url;
      let cataloge_id = url_path.split('/')[4];
      if (confirm('Подтвердите действие'))
      {
        $.ajax({
          method: 'get',
          url: url_path,
          dataType: 'json',
          success: function(response) {
            get_books_page(`/user/${response.username}/get_books_page/${cataloge_id}/${response.cur_page}`, cataloge_id);
            $('ul').filter(function() {
              return this.id.match(cataloge_id + 'books_pagination');
            }).remove();
            let html = `<ul class="pagination__list list-reset" id="${cataloge_id}books_pagination"><li class="pagination__item disabled">&bull;</li>`;
            
            if (response.has_elems) 
            {
              response.pages_count.forEach(page => {
                if (page)
                {
                  if (page == response.cur_page)
                  {
                    html += `<li class="pagination__item_cur_page">
                              <a data-url='/user/${response.username}/get_books_page/${cataloge_id}/${page}' id='${cataloge_id}books_page'>${page}</a>
                            </li>`;
                  }
                  else
                  {
                    html += `<li class="pagination__item active">
                              <a data-url='/user/${response.username}/get_books_page/${cataloge_id}/${page}' id='${cataloge_id}books_page'>${page}</a>
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
            
            document.getElementById(cataloge_id + 'books_pagination_container').innerHTML = html;
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

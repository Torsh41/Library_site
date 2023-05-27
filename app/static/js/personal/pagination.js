function get_lists_page(url_path)
{
  $.ajax({
      method: 'get',
      url: url_path,
      dataType: 'json',
      success: function(response) {
        cataloges = Array.from(response);
        $('section').filter(function() {
          return this.id.match(/cataloge_info/);
        }).remove();
        url = url_path.split('/');
        html = '';
        cataloges.forEach(cataloge => {
          html += `<section class="list" id="${cataloge.id}cataloge_info">
          <div class="container list__container">
            <div class="list__wrap">
              <h2 class="list__title title">${ cataloge.name }</h2>
              <!--Название списка, которое ввел пользователь-->
  
              <ul class="list__books list-reset" id="${cataloge.id}books_info_container">
                <!--Добавление книги в список - перебрасывает в рааздел категорий книг-->
                <li class="list__book list__add"><a href="/categories?list_id=${cataloge.id}" class="list__link">
                    <svg width="78" height="78" viewBox="0 0 78 78" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <g clip-path="url(#clip0_139_2)">
                        <rect x="35" width="8" height="78" fill="#D9D9D9" />
                        <rect x="78" y="35" width="8" height="78" transform="rotate(90 78 35)" fill="#D9D9D9" />
                      </g>
                      <defs>
                        <clipPath id="clip0_139_2">
                          <rect width="78" height="78" fill="white" />
                        </clipPath>
                      </defs>
                    </svg>
                  </a>
                </li>`;
                items = Array.from(cataloge.items);
                items.forEach(item => {
                html += `<li class="list__book" id="${cataloge.id}book_info">
                        <a href="/book-page/${item.name}" class="list__book-set">
                          <img class="list__book-set" src="/${item.name}/get-cover" alt="">
                        </a>
                        
                        <div class="list__book-wrap">
                          <a href="/book-page/${item.name}" class="list__link-book">Книга: ${ item.name
                          }</a>
                        <a href="#" class="list__link">Состояние чтения: ${ item.read_state }</a>
        
                        <a class="list__book-delete-btn" onclick="del_book_from_list('/user/${cataloge.username}/delete-item/${cataloge.id}/${item.id}/${1}', '${cataloge.id}')">Удалить
                          книгу из списка</a>
                        </div>
                      </li>`;
                });
                html += `</ul>`;

                // собираем пагинацию книг каждого списка
                html += `<div class="list__pagination pagination">
                          <ul class="pagination__list list-reset" id="${cataloge.id}books_pagination">
                          <li class="pagination__item disabled">
                              <a onclick="" id="lists_back">
                                  &laquo;
                              </a>
                              <script>scroll('lists_back')</script>
                          </li>`;
                try
                {
                  for (let i = 1; i <= items[0].pages; i++)
                  {
                      html += `<li class="pagination__item active">
                                <a onclick="get_books_page('/user/${cataloge.username}/get_books_page/${cataloge.id}/${i}', '${cataloge.id}')">${i}</a>
                                </li>
                                <script>scroll(${ i } + 'list_pagination')</script>`;
                  }
                    
                  if (items[0].pages > items[0].cur_page)
                  {
                    html += `<li>  
                              <a onclick="get_books_page('/user/${cataloge.username}/get_books_page/${cataloge.id}/${items[0].cur_page + 1}', '${cataloge.id}')" id="lists_up">
                              &raquo;
                              </a>`;     
                  }   
                  else
                  {
                    html += `<li class="pagination__item disabled">  
                              <a onclick="" id="lists_up">
                              &raquo;
                              </a>`;    
                  }
                }   
                catch
                {
                  html += `<li class="pagination__item disabled">  
                  <a onclick="" id="lists_up">
                  &raquo;
                  </a>`;    
                }
                html += `<script>scroll('lists_up')</script>
                          </li>
                          </ul>
                          </div>`;
                // 

                html += `<a class="list__delete-btn" id="${cataloge.id}del_list" onclick="del_list('/user/${cataloge.username}/delete-list/${cataloge.id}/${url[url.length - 1]}')">
                          <svg width="461" height="1" viewBox="0 0 461 1" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <line y1="0.5" x2="461" y2="0.5" stroke="black" />
                          </svg>
                          Удалить список
                          <svg width="461" height="1" viewBox="0 0 461 1" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <line y1="0.5" x2="461" y2="0.5" stroke="black" />
                          </svg>
                          </a><script>scroll(${cataloge.id} + 'del_list')</script></div></div></section>`;
        });
          
        document.getElementById("user_page_main_container").innerHTML += html;
      },
      error: function(error) {
          console.log(error);
      }
  });
}

function del_list(url_path) 
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
        html = `<ul class="pagination__list list-reset" id="pagination">`;
        if (response.cur_page == 1)
        {
          html += `<li class="pagination__item disabled"> 
          <a onclick="" id="lists_back">`;
        }
        else
        {
          html += `<li> <a onclick="get_lists_page('/user/${response.username}/get_lists_page/${response.cur_page - 1}')" id="lists_back">`;
        }
        html += `&laquo;</a><script>scroll('lists_back')</script></li>`;
        if (response.has_elems) 
        {
          for (let i = 1; i <= response.pages; i++)
          {
              html += `<li class="pagination__item active">
                        <a onclick="get_lists_page('/user/${response.username}/get_lists_page/${i}')">${i}</a>
                        </li>
                        <script>scroll(${ i } + 'list_pagination')</script>`;
          }
        }

        if (response.cur_page == response.pages)
        {
          html += `<li class="pagination__item disabled">
          <a onclick="" id="lists_up">`;
        }
        else
        {
          html += `<li> <a onclick="get_lists_page('/user/${response.username}/get_lists_page/${response.cur_page + 1}')" id="lists_up">`;
        }
        html += `&raquo;</a><script>scroll('lists_up')</script></li></ul>`;
        
        document.getElementById('pagination_container').innerHTML = html;
      },
      error: function(error) {
          console.log(error);
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
      html = '';
      books.forEach(book => {
                    html += `<li class="list__book" id="${cataloge_id}book_info">
                    <a href="/book-page/${book.name}" class="list__book-set">
                      <img class="list__book-set" src="/${book.name}/get-cover" alt="">
                    </a>
                    
                    <div class="list__book-wrap">
                      <a href="/book-page/${book.name}" class="list__link-book">Книга: ${book.name}</a>
                    <a href="#" class="list__link">Состояние чтения: ${ book.read_state }</a>

                    <a class="list__book-delete-btn" onclick="del_book_from_list('/user/${book.username_of_cur_user}/delete-item/${cataloge_id}/${book.id}/${url[url.length - 1]}', '${cataloge_id}')">Удалить
                    книгу из списка</a>
                    </div>
                  </li>`;
      });
      document.getElementById(cataloge_id + 'books_info_container').innerHTML += html;
    },
    error: function(error) {
        console.log(error);
    }
});
}

function del_book_from_list(url_path, cataloge_id) 
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

        html = `<ul class="pagination__list list-reset" id="pagination">`;
        if (response.cur_page == 1)
        {
          html += `<li class="pagination__item disabled"> 
          <a onclick="" id="lists_back">`;
        }
        else
        {
          html += `<li> <a onclick="get_books_page('/user/${response.username}/get_books_page/${response.cur_page - 1}', '${cataloge_id}')" id="lists_back">`;
        }
        html += `&laquo;</a><script>scroll('lists_back')</script></li>`;
        if (response.has_elems) 
        {
          for (let i = 1; i <= response.pages; i++)
          {
              html += ` <li class="pagination__item active">
                        <a onclick="get_books_page('/user/${response.username}/get_books_page/${i}', '${cataloge_id}')">${i}</a>
                        </li>
                        <script>scroll(${ i } + 'list_pagination')</script>`;
          }
        }

        if (response.cur_page == response.pages)
        {
          html += `<li class="pagination__item disabled">
          <a onclick="" id="lists_up">`;
        }
        else
        {
          html += `<li> <a onclick="get_books_page('/user/${response.username}/get_books_page/${response.cur_page + 1}', '${cataloge_id}')" id="lists_up">`;
        }
        html += `&raquo;</a><script>scroll('lists_up')</script></li></ul>`;
        
        document.getElementById(cataloge_id + 'books_pagination_container').innerHTML = html;
      },
      error: function(error) {
          console.log(error);
      }
    });
}
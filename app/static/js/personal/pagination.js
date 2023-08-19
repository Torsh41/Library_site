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
                items = Array.from(cataloge.items);
                items.forEach(item => {
                html += `<li class="list__book" id="${cataloge.id}book_info">
                          <a href="/book-page/${item.name}" class="list__book-set">
                            <img class="list__book-set" src="/${item.name}/get-cover" alt="">
                          </a>
                        
                          <div class="list__book-wrap">
                            <a href="/book-page/${item.name}" class="list__link-book"><u>Книга:</u> ${item.name}</a>
                            <a href="/book-page/${item.name}" class="list__link-plan"><u>Состояние чтения:</u> ${ item.read_state }</a>
                            <a class="list__book-delete-btn" data-url='/user/${cataloge.username}/delete-item/${cataloge.id}/${item.id}/${1}' id='${cataloge.id}del_book'>Удалить книгу из списка</a>
                          </div>
                        </li>`;
                });
                html += `</ul>`;

                // собираем пагинацию книг каждого списка
                html += `<div class="list__pagination pagination" id="${cataloge.id}books_pagination_container">
                          <ul class="pagination__list list-reset" id="${cataloge.id}books_pagination">
                            <li class="pagination__item disabled">&bull;</li>`;
                try
                {
                    for (let i = 1; i <= items[0].pages; i++)
                    {
                      if (items[0].pages > 1 && i == 1)
                      {
                          html += `<li class="pagination__item_cur_page">
                                    <a data-url='/user/${cataloge.username}/get_books_page/${cataloge.id}/${i}' id='${cataloge.id}books_page'>${i}</a>
                                  </li>`;
                      }
                      else
                      {
                        html += `<li class="pagination__item active">
                                  <a data-url='/user/${cataloge.username}/get_books_page/${cataloge.id}/${i}' id='${cataloge.id}books_page'>${i}</a>
                                </li>`;
                      }
                    }
                }
                catch
                {}
                html += `<li class="pagination__item disabled">&bull;</li></ul></div>`;    
                // 

                html += `<div class="list__end">
                          <a class="list__delete-btn" id="${cataloge.id}del_list" data-url="/user/${cataloge.username}/delete-list/${cataloge.id}/${url[url.length - 1]}">Удалить список
                          </a></div></div></div></section>`;
        }); 
        document.getElementById('lists_container').innerHTML = html;
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
                      <a href="/book-page/${book.name}" class="list__link-book"><u>Книга:</u> ${book.name}</a>
                      <a href="/book-page/${book.name}" class="list__link-plan"><u>Состояние чтения:</u> ${book.read_state}</a>
                      <a class="list__book-delete-btn" data-url='/user/${book.username_of_cur_user}/delete-item/${cataloge_id}/${book.id}/${url[url.length - 1]}' id='${cataloge_id}del_book'>Удалить книгу из списка</a>
                    </div>
                  </li>`;
      });
      document.getElementById(cataloge_id + 'books_info_container').innerHTML += html;
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
    error: function(error) {
        console.log(error);
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
              for (let i = 1; i <= response.pages; i++)
              {
                if (response.pages > 1 && i == response.cur_page)
                {
                  html += `<li class="pagination__item_cur_page">
                            <a data-url="/user/${response.username}/get_lists_page/${i}">${i}</a>
                          </li>`;
                }
                else
                {
                  html += `<li class="pagination__item active">
                            <a data-url="/user/${response.username}/get_lists_page/${i}">${i}</a>
                           </li>`;
                }
              }
            }
            html += `<li class="pagination__item disabled">&bull;</li></ul>`;
            document.getElementById('pagination_container').innerHTML = html;
          },
          error: function(error) {
              console.log(error);
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
            html = `<ul class="pagination__list list-reset" id="${cataloge_id}books_pagination"><li class="pagination__item disabled">&bull;</li>`;
            
            if (response.has_elems) 
            {
              for (let i = 1; i <= response.pages; i++)
              {
                if (response.pages > 1 && i == response.cur_page)
                {
                  html += `<li class="pagination__item_cur_page">
                              <a data-url='/user/${response.username}/get_books_page/${cataloge_id}/${i}' id='${cataloge_id}books_page'>${i}</a>
                            </li>`;
                }
                else
                {
                  html += `<li class="pagination__item active">
                              <a data-url='/user/${response.username}/get_books_page/${cataloge_id}/${i}' id='${cataloge_id}books_page'>${i}</a>
                            </li>`;
                }
              }
            }

            html += `<li class="pagination__item disabled">&bull;</li></ul>`;
            
            document.getElementById(cataloge_id + 'books_pagination_container').innerHTML = html;
          },
          error: function(error) {
              console.log(error);
          }
        });
      }
    }
  });
});

// let observer = new MutationObserver(callback);

// // наблюдать за всем, кроме атрибутов
// observer.observe(document, {
//   childList: true, // наблюдать за непосредственными детьми
//   subtree: true, // и более глубокими потомками
//   attributes: true,
//   characterData: true
// });

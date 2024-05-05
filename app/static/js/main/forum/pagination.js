// функция перестройки пагинации тем конкретной категории для ее правильного отображения
function topics_pagination_update(pages, category_id)
{
  $("#" + category_id + "topics_pagi").remove();
  let html = `<ul class="pagination__list list-reset" id="${category_id}topics_pagi">
              <li class="pagination__item disabled">
                &bull;
              </li>`;
  pages.forEach(p => {
    if (p)
    {
      html += `<li class="pagination__item active">
                <a id="${p}topics_p" data-url="/get_topics_page_on_forum/${category_id}/${p}" data-catid="${category_id}">${p}</a>
              </li>`;
    }
    else
    {
      html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`;
    }
   
  });
  html += `<li class="pagination__item disabled">&bull;</li></ul>`;
  div = document.getElementById(category_id + "topics_pagi_container");
  div.insertAdjacentHTML('afterbegin', html);    
}


// функция перестройки пагинации категорий для ее правильного отображения
function categories_pagination_update(pages)
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
                <a id="${p}category_p" data-url="/get_categories_page_on_forum/${p}">${p}</a>
              </li>`;
    }
    else
    {
      html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`;
    }
   
  });
  html += `<li class="pagination__item disabled">&bull;</li></ul>`;
  div = document.getElementById("pagination_container");
  div.insertAdjacentHTML('afterbegin', html);    
}


function get_topics_page_on_forum(url_path, category_id)
{
  $.ajax({
    method: 'get',
    url: url_path,
    dataType: 'json',
    success: function(response) {
      topics = Array.from(response);
      $('li').filter(function() {
        return this.id.match(category_id + 'topic_info');
      }).remove();
      url = url_path.split('/');
      html = '';
      topics.forEach(topic => {
          html += `<li class="fraction__list-item" id="${category_id}topic_info">
                      <a href="/forum/${topic.id}" class="fraction__topic-link">
                        <div class="fraction__topic" id="${category_id}${topic.id}topic_name_div">
                          <p class="fraction__text-error" id="${category_id}${topic.id}top_name">
                            ${topic.name}
                          </p> 
                        </div>
                      </a>`;
                    if (topic.cur_user_is_admin)
                    {
                      html += `<a class="comments__command" id="${category_id}${topic.id}admin_mark">Админ</a>
                              <a id="${category_id}${topic.id}change_topic_name" class="comments__command" data-url="/change-topic-name/${category_id}/${topic.id}" data-name="${topic.name}">Редактировать</a>
                              <a id='${category_id}${topic.id}topic_d' class="comments__command" data-url='/delete-topic/${category_id}/${topic.id}/${topic.cur_page}' data-catid='${category_id}'>Удалить</a>`;
                    }
        html += `</li>`;
      });
      div = document.getElementById(category_id + "grid_container");
      div.insertAdjacentHTML('beforeend', html);

      // перестройка пагинации
      if (topics.length)
      {
        topics_pagination_update(topics[0].pages_count, category_id);
      }

      // выделение текущей страницы
      pagi = document.getElementById(category_id + 'topics_pagi');
      pagi_li = pagi.querySelector('.pagination__item_cur_page');
      if (pagi_li)
      {
        pagi_li.className = 'pagination__item active';
      }
      for (const child of pagi.children)
      {
        if (topics.length && topics[0].cur_page == child.textContent)
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


function change_topic_name()
{
  if (document.getElementById('changed_topic_name_field').value.trim() && document.getElementById('changed_topic_name_field').value.trim().length <= 100)
  {
      $.ajax({
          method: 'post',
          url: $("#change_topic_name_form").attr('action'),
          dataType: 'json',
          data: $('#change_topic_name_form').serialize(),
          success: function(response) {
            $('p').filter(function() {
              return this.id.match(response.category_id + response.topic_id + "top_name");
            }).remove();
            $('a').filter(function() {
              return this.id.match(response.category_id + response.topic_id + "change_topic_name");
            }).remove();
          
            let html = `<p class="fraction__text-error" id="${response.category_id}${response.topic_id}top_name"> ${response.name}</p>`;
            let div = document.getElementById(response.category_id + response.topic_id + 'topic_name_div');
            div.insertAdjacentHTML('afterbegin', html)
            html = `<a id="${response.category_id}${response.topic_id}change_topic_name" class="comments__command" data-url="/change-topic-name/${response.category_id}/${response.topic_id}" data-name="${response.name}">Редактировать</a>`;
            let a = document.getElementById(response.category_id + response.topic_id + 'admin_mark');
            a.insertAdjacentHTML('afterend', html);
            document.getElementById("changed_topic_name_field").value = "";
            document.getElementById("change_topic_name_form").setAttribute("action", "");
            document.getElementById("change_topic_name_sec").style.display = "none";
            document.getElementById(response.category_id + "topic_info").scrollIntoView(); // прокрутка до верхней границы
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
  else if (document.getElementById('changed_topic_name_field').value.trim().length > 200)
  {
    alert('Слишком длинное название темы!');
  }
  else
  {
    alert('Заполните поле!');
    document.getElementById('changed_topic_name_field').value = '';
  }
}


$(function() {
    $('#pagination_container').on('click', function(event) {
        let target = event.target;
        if (target.tagName === 'A' && target.id.includes('category_p')) 
        {
          let url_path = target.dataset?.url;
          $.ajax({
            method: 'get',
            url: url_path,
            dataType: 'json',
            success: function(response) {
                categories = Array.from(response);
                $('section').filter(function() {
                    return this.id.match(/category_info/);
                }).remove();
                $('section').filter(function() {
                  return this.id.match("not_found");
                }).remove();
                document.getElementById("category_name_id").value = "";
                html = "";
                url = url_path.split('/');
                categories.forEach(category => {
                    html +=  `<section id="${category.id}category_info" class="fraction">
                    <div class="fraction__container container">
                      <div class="fraction__wrap">
                        <h2 class="fraction__title title" id="${category.id + 'category_title'}">${category.name}</h2> 
                        <span class="fraction__results" id="${category.id + 'topics_count'}"> Всего тем: ${category.topics_count}</span>`;
                        html += `<ul class="fraction__topic-list list-reset" id="${category.id + 'grid_container'}">`;
                        if (category.username_of_cur_user)
                        {
                            html += `<li class="fraction__list-item">
                                          <div class="fraction__topic" data-user='${category.username_of_cur_user}' data-category='${category.id}' data-pagi='${url[url.length - 1]}'>
                                            <svg width="78" height="78" viewBox="0 0 78 78" fill="none" xmlns="http://www.w3.org/2000/svg" data-user='${category.username_of_cur_user}' data-category='${category.id}' data-pagi='${url[url.length - 1]}'>
                                              <g clip-path="url(#clip0_139_2)" data-user='${category.username_of_cur_user}' data-category='${category.id}' data-pagi='${url[url.length - 1]}'>
                                                <rect x="35" width="8" height="78" fill="#F5F5DC" data-user='${category.username_of_cur_user}' data-category='${category.id}' data-pagi='${url[url.length - 1]}' />
                                                <rect x="78" y="35" width="8" height="78" transform="rotate(90 78 35)" fill="#F5F5DC" data-user='${category.username_of_cur_user}' data-category='${category.id}' data-pagi='${url[url.length - 1]}' />
                                              </g>
                                            </svg>
                                          </div>
                                      </li>`;
                        }
                        else
                        {
                            html += `<li class="fraction__list-item">
                                        <a class="fraction__topic-link"> 
                                        <div class="fraction__topic">
                                          <p class="fraction__text-error">
                                            Создавать темы могут только авторизованные пользователи.
                                          </p>
                                        </div>
                                        </a>
                                      </li>`;
                        }
                        topics = Array.from(category.topics);
                        topics.forEach(topic => {
                            html += `<li class="fraction__list-item" id="${category.id + 'topic_info'}">
                                        <a href="/forum/${topic.id}" class="fraction__topic-link">
                                          <div class="fraction__topic" id="${category.id}${topic.id}topic_name_div">
                                            <p class="fraction__text-error" id="${category.id}${topic.id}top_name">
                                              ${topic.name}
                                            </p>
                                          </div>
                                        </a>`;
                            if (category.cur_user_is_admin)
                            {
                              html += `<a class="comments__command" id="${category.id}${topic.id}admin_mark">Админ</a>
                                      <a id="${category.id}${topic.id}change_topic_name" class="comments__command" data-url="/change-topic-name/${category.id}/${topic.id}" data-name="${topic.name}">Редактировать</a>
                                      <a id='${category.id}${topic.id}topic_d' class="comments__command" data-url='/delete-topic/${category.id}/${topic.id}/${1}' data-catid='${category.id}'>Удалить</a>`;      
                            }
                            html += `</li>`;
                        });
                      html += `</ul>
                              <div class="list__pagination pagination" id="${category.id}topics_pagi_container">
                                <ul class="pagination__list list-reset" id="${category.id}topics_pagi">
                                <li class="pagination__item disabled">
                                  &bull;
                                </li>`;
                  
                      if (topics[0])
                      {
                        topics[0].topic_pages.forEach(page => {
                          if (page)
                          {
                            html +=`<li class="pagination__item active">
                                    <a id='${page}topics_p' data-url='/get_topics_page_on_forum/${category.id}/${page}' data-catid='${category.id}'>${page}</a>
                                  </li>`;
                          }
                          else
                          {
                            html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`;
                          }
                        });
                      }
        
                    html += `<li class="pagination__item disabled">
                                &bull;
                              </li>
                              </ul></div></div></section>`;
                });
                section = document.getElementById('categories_container');
                section.insertAdjacentHTML('afterbegin', html);

                // перестройка пагинации
                categories_pagination_update(categories[0].pages_count);

                // выделение текущей страницы
                pagi = document.getElementById('pagination');
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
    });
    
    $('#categories_container').on('click', function(event) {
        let target = event.target;
        if (target.tagName === 'div' || target.tagName === 'svg' || target.tagName === 'g' || target.tagName === 'rect') 
        {
          let username = target.dataset?.user;
          let category_id = target.dataset?.category;
          let page = target.dataset?.pagi;
          document.getElementById("popupForm").style.display = "block";
          form = document.getElementById("add_topic_form");
          form.setAttribute("action", `/${username}/${category_id}/add_topic?page=${page}`);
        }
        else if (target.tagName === 'A' && target.id.includes('topic_d'))
        {
            let url_path = target.dataset?.url;
            let category_id = target.dataset?.catid;
            if (confirm('Подтвердите действие'))
            {
                $.ajax({
                    method: 'get',
                    url: url_path,
                    dataType: 'json',
                    success: function(response) {
                        get_topics_page_on_forum(`/get_topics_page_on_forum/${category_id}/${response.cur_page}`, `${category_id}`);
                        $('div').filter(function() {
                        return this.id.match(category_id + 'topics_pagi_container');
                        }).remove();

                        html = `<div class="list__pagination pagination" id="${category_id}topics_pagi_container">
                                <ul class="pagination__list list-reset" id="${category_id}topics_pagi"><li class="pagination__item disabled"> &bull;</li>`;                            
                        if (response.has_elems) 
                        {
                          response.pages_count.forEach(page => {
                            if (page)
                            {
                              if (page == response.cur_page)
                              {
                                html +=`<li class="pagination__item_cur_page">
                                          <a id='${page}topics_p' data-url='/get_topics_page_on_forum/${category_id}/${page}' data-catid='${category_id}'>${page}</a>
                                        </li>`;
                              }
                              else
                              {
                                html +=`<li class="pagination__item active">
                                          <a id='${page}topics_p' data-url='/get_topics_page_on_forum/${category_id}/${page}' data-catid='${category_id}'>${page}</a>
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
                        div = document.getElementById(category_id + 'grid_container');
                        div.insertAdjacentHTML('afterend', html);
                        document.getElementById(category_id + 'topics_count').textContent = `Всего тем: ${response.topics_count}`;
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
        else if (target.tagName === 'A' && target.id.includes('change_topic_name'))
        {
          let url_path = target.dataset?.url;
          let cur_topic_name = target.dataset?.name;
          document.getElementById("changed_topic_name_field").value = cur_topic_name;
          document.getElementById("change_topic_name_form").setAttribute("action", url_path);
          document.getElementById("change_topic_name_sec").style.display = "block";
        }
        else if (target.tagName === 'A' && target.id.includes('topics_p')) 
        {
          let url_path = target.dataset?.url;
          let category_id = target.dataset?.catid;
          get_topics_page_on_forum(url_path, category_id);
        }
    });
    
    $('#cl_form').on('click', function(event) {
        document.getElementById("popupForm").style.display = "none";
    });

    $('#cl_change_topic_name_form').on('click', function(event) {
      document.getElementById("change_topic_name_sec").style.display = "none";
    });

    $('#change_topic_name_button').on('click', function(event) {
        change_topic_name();
    });
    
    $('#change_topic_name_button').submit(function(event) {
      change_topic_name();
      event.preventDefault();
    });

    $('#add_topic_button').on('click', function(event) {
        if (document.getElementById('topic_name_id_form').value.trim() && document.getElementById('topic_name_id_form').value.trim().length <= 200)
        {
          $.ajax({
            method: 'post',
            url: $("#add_topic_form").attr('action'),
            dataType: 'json',
            data: $('#add_topic_form').serialize(),
            success: function(response) {
              topics_for_cur_category = Array.from(response)
              if (topics_for_cur_category[0].result)
              {
                $('li').filter(function() {
                  return this.id.match(topics_for_cur_category[0].category_id + 'topic_info');
                }).remove();
                $('span').filter(function() {
                  return this.id.match(topics_for_cur_category[0].category_id + 'topics_count');
                }).remove();
                $('ul').filter(function() {
                  return this.id.match(topics_for_cur_category[0].category_id + 'topics_pagi');
                }).remove();
                html = '';
                topics_for_cur_category.forEach(topic => {
                    html += `<li class="fraction__list-item" id="${topic.category_id + 'topic_info'}">
                                <a href="/forum/${topic.topic_id}" class="fraction__topic-link">
                                  <div class="fraction__topic" id="${topic.category_id}${topic.topic_id}topic_name_div">
                                    <p class="fraction__text-error" id="${topic.category_id}${topic.topic_id}top_name">
                                      ${topic.name}
                                    </p>
                                  </div>
                                </a>`;
                    if (topic.cur_user_is_admin)
                    {
                      html += `<a class="comments__command" id="${topic.category_id}${topic.topic_id}admin_mark">Админ</a>
                              <a id="${topic.category_id}${topic.topic_id}change_topic_name" class="comments__command" data-url="/change-topic-name/${topic.category_id}/${topic.topic_id}" data-name="${topic.name}">Редактировать</a>
                              <a id='${topic.category_id}${topic.topic_id}topic_d' class="comments__command" data-url='/delete-topic/${topic.category_id}/${topic.topic_id}/${topic.topic_pages}' data-catid='${topic.category_id}'>Удалить</a>`;      
                    }
                    html += `</li>`;
                });
                div_outer = document.getElementById(topics_for_cur_category[0].category_id + 'category_title');
                div_outer.insertAdjacentHTML('afterend', `<span class="fraction__results" id="${topics_for_cur_category[0].category_id + 'topics_count'}">Всего тем: ${topics_for_cur_category[0].topics_count}</span>`);
                div = document.getElementById(topics_for_cur_category[0].category_id + 'grid_container');
                div.insertAdjacentHTML('beforeend', html);
                document.getElementById("topic_name_id_form").value = "";
                document.getElementById("popupForm").style.display = "none";
      
                // собираем пагинацию
                html = `<div class="list__pagination pagination" id="${topics_for_cur_category[0].category_id}topics_pagi_container">
                        <ul class="pagination__list list-reset" id="${topics_for_cur_category[0].category_id}topics_pagi">
                          <li class="pagination__item disabled">&bull;</li>`;
                if (topics_for_cur_category[0])
                {
                  topics_for_cur_category[0].pages_count.forEach(page => {
                    if (page)
                    {
                      if (topics_for_cur_category[0].topic_pages > 1 && page == topics_for_cur_category[0].topic_pages)
                      {
                          html +=`<li class="pagination__item_cur_page">
                          <a id='${page}topics_p' data-url='/get_topics_page_on_forum/${topics_for_cur_category[0].category_id}/${page}' data-catid='${topics_for_cur_category[0].category_id}'>${page}</a>
                          </li>`;
                      }
                      else
                      {
                          html +=`<li class="pagination__item active">
                                <a id='${page}topics_p' data-url='/get_topics_page_on_forum/${topics_for_cur_category[0].category_id}/${page}' data-catid='${topics_for_cur_category[0].category_id}'>${page}</a>
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
                div.insertAdjacentHTML('afterend', html);
                alert(`Тема успешно создана`);
              }
              else
              {
                document.getElementById("topic_name_id_form").value = "";
                alert(`Такая тема уже имеется в данном разделе`);
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
        else if (document.getElementById('topic_name_id_form').value.trim().length > 200)
        {
          alert('Слишком длинное название темы');
        }
        else
        {
          alert('Заполните поле');
          document.getElementById('topic_name_id_form').value = '';
        }
    });
});
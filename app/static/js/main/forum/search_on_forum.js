function search_category_on_forum() 
{
  if (document.getElementById('category_name_id').value.trim() && document.getElementById('category_name_id').value.trim().length <= 200)
  {
    $.ajax({
        method: 'post',
        url: '/search_category_on_forum',
        dataType: 'json',
        data: $('#search_form').serialize(),
        success: function(response) {
          categories = Array.from(response);
          if (categories[0].result)
          {
                $('section').filter(function() {
                    return this.id.match(/category_info/);
                }).remove();
                $('section').filter(function() {
                  return this.id.match("not_found");
                }).remove();
                document.getElementById("category_name_id").value = "";
                html = '';
                categories.forEach(category => {
                    html += `<section id="${category.id}category_info" class="fraction">
                    <div class="fraction__container container">
                      <div class="fraction__wrap">
                        <h2 class="fraction__title title" id="${category.id + 'category_title'}">${category.name}</h2> 
                        <span class="fraction__results" id="${category.id + 'topics_count'}"> Всего тем: ${category.topics_count}</span>`;
                        html += `<ul class="fraction__topic-list list-reset" id="${category.id + 'grid_container'}">`;
                        if (category.username_of_cur_user)
                        {
                            html += `<li class="fraction__list-item">
                                          <div class="fraction__topic" data-user="${category.username_of_cur_user}" data-category="${category.id}" data-pagi="${category.cur_page}">
                                            <svg width="78" height="78" viewBox="0 0 78 78" fill="none" xmlns="http://www.w3.org/2000/svg" data-user="${category.username_of_cur_user}" data-category="${category.id}" data-pagi="${category.cur_page}">
                                              <g clip-path="url(#clip0_139_2)" data-user="${category.username_of_cur_user}" data-category="${category.id}" data-pagi="${category.cur_page}">
                                                <rect x="35" width="8" height="78" fill="#F5F5DC" data-user="${category.username_of_cur_user}" data-category="${category.id}" data-pagi="${category.cur_page}" />
                                                <rect x="78" y="35" width="8" height="78" transform="rotate(90 78 35)" fill="#F5F5DC" data-user="${category.username_of_cur_user}" data-category="${category.id}" data-pagi="${category.cur_page}" />
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
          
                          html += `<li class="fraction__list-item" id="${category.id}topic_info">
                                    <a href="/forum/${topic.id}" class="fraction__topic-link" id="${category.id + 'topic_info'}">
                                      <div class="fraction__topic" id="${category.id}${topic.id}topic_name_div">
                                        <p class="fraction__text-error" id="${category.id}${topic.id}top_name">${topic.name}</p>
                                      </div>
                                    </a>`;
                                    if (category.cur_user_is_admin)
                                    {
                                      html += `<div class="fraction__wrapper-command"><a class="comments__command" id="${category.id}${topic.id}admin_mark">Админ</a>
                                              <a id="${category.id}${topic.id}change_topic_name" class="comments__command" data-url="/change-topic-name/${category.id}/${topic.id}" data-name="${topic.name}">Редактировать</a>
                                              <a id='${category.id}${topic.id}topic_d' class="comments__command" data-url='/delete-topic/${category.id}/${topic.id}/${1}' data-catid='${category.id}'>Удалить</a></div>`;      
                                    }
                                 html+= `</li>`;                    
                        });

                    html += `</ul>`;
                    // собираем пагинацию для топиков каждой категории
                    html += `<div class="list__pagination pagination" id="${category.id}topics_pagi_container">
                                <ul class="pagination__list list-reset" id="${category.id}topics_pagi">
                                  <li class="pagination__item disabled">
                                    &bull;
                                  </li>`;
                    if (topics[0])
                    {
                      topics[0].pages_count.forEach(page =>{
                        if (page)
                        {
                          if (topics[0].pages > 1 && page == topics[0].cur_page)
                          {
                            html += `<li class="pagination__item_cur_page">
                                        <a id='${page}topics_p' data-url='/get_topics_page_on_forum/${category.id}/${page}' data-catid='${category.id}'>${page}</a>
                                      </li>`;
                          }
                          else
                          {
                            html += `<li class="pagination__item active">
                                      <a id='${page}topics_p' data-url='/get_topics_page_on_forum/${category.id}/${page}' data-catid='${category.id}'>${page}</a>
                                    </li>`;
                          }
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
                              </ul></div>`;
                    html += `</div></div></section>`;
              });
                section = document.getElementById('categories_container');
                section.insertAdjacentHTML('afterbegin', html);
                section = document.getElementById(categories[0].id_of_found_elem + 'category_info');
                section.scrollIntoView(); // Прокрутка до верхней границы
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
          }
          else
          {
            $('section').filter(function() {
              return this.id.match(/category_info/);
            }).remove();
            $('section').filter(function() {
              return this.id.match("not_found");
            }).remove();
            document.getElementById("category_name_id").value = "";
            html = `<section class="list" id="not_found">
                      <div class="container list__container">
                        <div class="list__wrap">
                          <h2 class="list__title title">Ничего не найдено</h2>
                        </div>
                      </div>
                    </section>`;
            section = document.getElementById('first_section');
            section.insertAdjacentHTML('afterend', html);
            document.getElementById('not_found').scrollIntoView(); // Прокрутка до верхней границы
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
  else if (document.getElementById('category_name_id').value.trim().length > 200)
  {
    alert('Слишком длинное название категории');
  }
  else
  {
    alert('Заполните поле');
    document.getElementById('category_name_id').value = '';
  }
}      

$(function() {
  $('#search_form').submit(function(event) {
    search_category_on_forum();
    event.preventDefault();
  });

  $('#found_category').click(function(event) {
    search_category_on_forum();
  });
});


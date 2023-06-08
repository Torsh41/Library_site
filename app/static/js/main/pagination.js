function get_categories_page(url_path)
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
            html = "";
            categories.forEach(category => {
                html += `<li class="about__cat-elem" id="${category.id}category_info"><a href="/category/${category.name}/search" class="about__book-link">${category.name}</a></li>`;
            });
            document.getElementById("categories_block").innerHTML = html;
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function get_comments_page(url_path)
{
    $.ajax({
        method: 'get',
        url: url_path,
        dataType: 'json',
        success: function(response) {
            comments = Array.from(response);
            $('li').filter(function() {
                return this.id.match(/comment_info/);
            }).remove();
            url = url_path.split('/');
            html = "";
            comments.forEach(comment => {
                html += `<li class="comments__comment">
                        <div class="comments__top">
                        <div class="comments__image">
                        <img class="comments__image-set" src="/user/${comment.username}/edit-profile/edit-avatar">
                        </div>`;
                if (comment.username == comment.name_of_current_user && comment.current_user_is_authenticated)
                {
                    html += `<a href="/user/${comment.name_of_current_user}" class="comments__link">${comment.username}</a></div>`;
                }
                else
                {
                    html += `<a class="comments__link">${comment.username}</a></div>`;
                }
                html += `<p class="comments__link">${comment.day + " " + comment.month + " " + comment.year}</p>`;
                html += `<p class="comments__text">${comment.body}</p>`;
                html += ` <div class="comments__commands">`;
                if (comment.username == comment.name_of_current_user)
                {
                    html += `  
                        <section class="loginPopup" id="${comment.id}" style="display: none">
                        <div class="formPopup">
                            <h2 class="comments__title title">Редактирование комментария</h2>
                            <form class="formContainer"
                            action="/${comment.name_of_current_user}/${comment.book_name}/edit-comment/${comment.id}?page=${url[url.length - 1]}" method="post">

                            <label class="comments__label">
                                <span class="comments__span">Ваш комментарий</span>
                                <textarea type="text" class="comments__textarea" id="${comment.id}field" rows="5"
                                name="newComment" placeholder="введите новый комментарий..." required></textarea>
                            </label>

                            <button class="comments__btn btn" id="${comment.id}edit_comment">Изменить</button>
                            <button type="button" class="btn cancel"
                                onclick="closeEditCommentForm('${comment.id}')">Отменить</button>
                            </form>
                        </div>
                        </section>
                        <script>scroll(${comment.id + 'edit_comment'})</script>

                        <a onclick="edit('${comment.body}', '${comment.id}')" class="comments__command">Редактировать</a>
                        <a class="comments__command" onclick="del_comment('/${comment.name_of_current_user}/${comment.book_name}/delete-comment/${comment.id}/${url[url.length - 1]}')" id="${comment.id}del">Удалить</a>
                        <script>scroll(${comment.id  + 'del'})</script>`;
                }
                html += `</div></li>`;
                
            });
            document.getElementById("comments_info_container").innerHTML = html;
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function del_comment(url_path) 
{
    $.ajax({
        method: 'get',
        url: url_path,
        dataType: 'json',
        success: function(response) {
          get_comments_page(`/get_comments_page/${response.book_name}/${response.cur_page}`);
          $('ul').filter(function() {
            return this.id.match('comments_pagination');
          }).remove();
  
          html = `<ul class="pagination__list list-reset" id="pagination">`;
          if (response.cur_page == 1)
          {
            html += `<li class="pagination__item disabled"> 
            <a onclick="" id="lists_back">`;
          }
          else
          {
            html += `<li> <a onclick="get_comments_page('/get_comments_page/${response.book_name}/${response.cur_page - 1}')" id="lists_back">`;
          }
          html += `&laquo;</a><script>scroll('lists_back')</script></li>`;
          if (response.has_elems) 
          {
            for (let i = 1; i <= response.pages; i++)
            {
                html += ` <li class="pagination__item active">
                          <a onclick="get_comments_page('/get_comments_page/${response.book_name}/${i}')">${i}</a>
                          </li>
                          <script>scroll(${i} + 'list_pagination')</script>`;
            }
          }
  
          if (response.cur_page == response.pages)
          {
            html += `<li class="pagination__item disabled">
            <a onclick="" id="lists_up">`;
          }
          else
          {
            html += `<li> <a onclick="get_comments_page('/get_comments_page/${response.book_name}/${response.cur_page + 1}')" id="lists_up">`;
          }
          html += `&raquo;</a><script>scroll('lists_up')</script></li></ul>`;
          
          document.getElementById('comments_pagination_container').innerHTML = html;
        },
        error: function(error) {
            console.log(error);
        }
      });
}

function get_categories_page_on_forum(url_path)
{
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
                    html += `<div class="fraction__topic-list" id="${category.id + 'grid_container'}">`;
                    if (category.username_of_cur_user)
                    {
                        html += `<a class="fraction__topic-link" onclick="openForm('${category.username_of_cur_user}', '${category.name}', '${url[url.length - 1]}')"> <!--Add the new topic (for users)-->
                                  <div class="fraction__topic">
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
                                  </div>
                                </a>`;
                    }
                    else
                    {
                        html += ` <a class="fraction__topic-link"> 
                                  <div class="fraction__topic">
                                    Создавать темы могут только авторизованные пользователи.
                                  </div>
                                  </a>`;
                    }
                    topics = Array.from(category.topics);
                    topics.forEach(topic => {
                        html += `<a href="/forum/${topic.name}" class="fraction__topic-link" id="${category.id + 'topic_info'}">
                                <div class="fraction__topic">
                                  ${topic.name}
                                </div>
                                </a>`;
                    });
                html += `</div></div></div></section>`;
            });
            section = document.getElementById('first_section');
            section.insertAdjacentHTML('afterend', html);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function get_posts_page(url_path)
{
  $.ajax({
    method: 'get',
    url: url_path,
    dataType: 'json',
    success: function(response) {
        posts = Array.from(response);
        $('div').filter(function() {
            return this.id.match(/discussion_post/);
        }).remove();
        html = "";
        posts.forEach(post => {
        html += `<div class="discussion__message message" id="${post.id}discussion_post"> 
                      <div class="message__left">
                        <div class="message__name">
                          <a href="#" class="message__link">
                            <div class="message__set">
                              <img src="/user/${post.username}/edit-profile/edit-avatar" alt="" class="message__img"> 
                            </div>
                            ${post.username}
                          </a>
                        </div>
      
                        <div class="message__name-info">
                          <p class="message__info">Данные о пользователе</p>
                          <span class="message__span">На сайте с ${post.user_day + " " + post.user_month +
                          " " + post.user_year}</span>
                        </div>
                      </div>
    
                      <div class="message__right">
                        <p class="message__text">
                        ${post.body} <!--Сообщение пользователя-->
                        </p>`;

                  if (post.username == post.current_username)
                  {
                    html += `<div class="message__admin">
                              <a href="" class="message__admin-btn">Редактировать</a>
                              <a href="" class="message__admin-btn">Удалить</a>
                              </div>`;
                  }
                 html += `</div></div>`;
         });
         div = document.getElementById('disc_posts_container');
         div.insertAdjacentHTML('afterbegin', html);
    },
    error: function(error) {
        console.log(error);
    }
  });
}

function get_topics_page_on_forum(url_path, category_id)
{
  $.ajax({
    method: 'get',
    url: url_path,
    dataType: 'json',
    success: function(response) {
      topics = Array.from(response);
      $('a').filter(function() {
        return this.id.match(category_id + 'topic_info');
      }).remove();
      url = url_path.split('/');
      html = '';
      topics.forEach(topic => {
                    html += ` <a href="/forum/${topic.id}" id="${category_id}topic_info" class="fraction__topic-link">
                              <div class="fraction__topic">
                                ${topic.name} 
                              </div>
                              </a>`;
      });
      div = document.getElementById(category_id + "grid_container");
      div.insertAdjacentHTML('beforeend', html);
    },
    error: function(error) {
        console.log(error);
    }
  });
}



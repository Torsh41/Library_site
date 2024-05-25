// функция перестройки пагинации постов для ее правильного отображения
function posts_pagination_update(pages, chat_id)
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
                <a id="${p}posts_p" data-url="/get_posts_page_on_chat_disc/${chat_id}/${p}">${p}</a>
              </li>`;
    }
    else
    {
      html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`
    }
   
  });
  html += `<li class="pagination__item disabled">&bull;</li></ul>`;
  div = document.getElementById("posts_pagination_container");
  div.insertAdjacentHTML('afterbegin', html);    
}


$(function() {
    $('#posts_pagination_container').on('click', function(event) {
        let target = event.target;
        if (target.tagName === 'A' && target.id.includes('posts_p')) 
        {
          let url_path = target.dataset?.url;
          $.ajax({
            method: 'get',
            url: url_path,
            dataType: 'json',
            success: function(response) {
                posts = Array.from(response.posts);
                pages_count = Array.from(response.pages_count);
                $('div').filter(function() {
                    return this.id.match(/discussion_post/);
                }).remove();
                let html = "";
                posts.forEach(post => {
                html += `<div class="discussion__message message" id="${post.id}discussion_post"> 
                              <div class="message__left">
                                <div class="message__name">`;
                                if (post.username == post.current_username) 
                                {
                                  html += `<a href="/user/${post.current_username}" class="message__link">`;
                                }
                                else
                                {
                                  html += `<a class="message__link">`;
                                }
                                html += `<div class="message__set">
                                    <img src="/user/${post.username}/edit-profile/edit-avatar" alt="" class="message__img"> 
                                    </div>
                                    ${post.username}
                                  </a>
                                </div>
              
                                <div class="message__name-info" id="${post.id}user_info">
                                  <p class="message__info">  
                                  <span class="message__span">
                                    ${post.age}
                                  </span>
                                  <span class="message__span">
                                    ${post.gender}
                                  </span>
                                  <span class="message__span">
                                    ${post.city}
                                  </span>
                                  <span class="message__span">
                                    ${post.about_me}
                                  </span>
                                  </p>
                                  <span class="message__span">На сайте с ${post.user_day + " " + post.user_month +
                                  " " + post.user_year}</span>`;
                                  if (post.edited)
                                  {
                                    html += `<span class="message__span" id="${post.id}edited">изменено</span>`;
                                  }
                              html += `</div></div>`;
                              html += `<div class="message__right" id="${post.id}msg_write_id">
                                        <div class="message__wrappermain">
                                          <div class="message__dataform" id="${post.id}post_date">
                                            <span class="message__span">${post.post_day + " " + post.post_month + " " + post.post_year}</span>
                                          </div>`;
                              if (post.this_is_answer)
                              {
                                html += `<div class="message__answer" id="${post.id}base_to_answer">
                                          <span class="message__span-answer">Сообщение от ${post.username_of_post_from}</span>
                                          <p class="message__text-answer">${post.body_of_post_from}</p>
                                        </div>`;
                              }
                              html += `<p class="message__text" id="${post.id}post_body">
                              ${post.body} <!--Сообщение пользователя-->
                              </p>`;
                              if (post.file)
                              {
                                html += `<img id="${post.id}img" style="width: 80px; height: 80px" src="/${post.id}/get-post-screenshot-on-private-chat" data-postid="${post.id}"/>
                                          <div id="${post.id}modal" class="modal">
                                            <span class="close" onclick="document.getElementById('${post.id}modal').style.display='none'">&times;</span>
                                            <img class="modal-content" id="${post.id}modal_img">
                                          </div>`;
                              }
                              html += `</div>`;
                          if (post.username == post.current_username)
                          {
                            html += `<div class="message__admin" id="${post.id}personal_cont">
                                      <a class="message__admin-btn" id="${post.id}answer_on" data-chatid='${post.chat_id}' data-postid='${post.id}'>Ответить</a>
                                      <a class="message__admin-btn" id="${post.id}edit_post_a" data-chatid='${post.chat_id}' data-postid='${post.id}' data-body='${post.body}'>Редактировать</a>
                                      <a class="message__admin-btn" id="${post.id}post_d" data-chatid='${post.chat_id}' data-postid='${post.id}' data-page='${post.cur_page}'>Удалить</a>
                                      </div>`;
                          }
                          else if (post.user_is_admin)
                          {
                            html += `<div class="message__admin" id="${post.id}personal_cont">
                            <a class="comments__command">Админ</a>
                            <a class="message__admin-btn" id="${post.id}answer_on" data-chatid='${post.chat_id}' data-postid='${post.id}'>Ответить</a>
                            <a class="message__admin-btn" id="${post.id}post_d" data-chatid='${post.chat_id}' data-postid='${post.id}' data-page='${post.cur_page}'>Удалить</a>
                            </div>`;
                          }
                          else if (post.current_username)
                          {
                            html += `<div class="message__admin" id="${post.id}personal_cont">
                            <a class="message__admin-btn" id="${post.id}answer_on" data-chatid='${post.chat_id}' data-postid='${post.id}'>Ответить</a>
                            </div>`;
                          }
                         html += `</div></div>`;
                 });
                 div = document.getElementById('disc_posts_container');
                 div.insertAdjacentHTML('afterbegin', html);
                 write_post_form = document.getElementById('add_post_form');
                 if (write_post_form)
                 {
                  action = write_post_form.getAttribute('action');
                  action = action.split('?')[0];
                  write_post_form.setAttribute('action', action);
                 }
                // перестройка пагинации
                posts_pagination_update(pages_count, posts[0].chat_id);

                // выделение текущей страницы
                 pagi = document.getElementById('pagination');
                 pagi_li = pagi.querySelector('.pagination__item_cur_page');
                 if (pagi_li)
                 {
                   pagi_li.className = 'pagination__item active';
                 }
                 for (const child of pagi.children)
                 {
                   if (posts.length && posts[0].cur_page == child.textContent)
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
});
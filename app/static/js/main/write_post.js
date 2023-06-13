$(document).ready(function () {
    $('#add_post_form').submit(function(event) {
        add_post_on_forum();
        event.preventDefault();
    });
  });
  
function add_post_on_forum() 
{
    if (document.getElementById('post_body_id').value.trim())
    {
     
      form = document.getElementById("add_post_form");
      var formData = new FormData(form); 
      $.ajax({
          method: 'post',
          url: $("#add_post_form").attr('action'),
          dataType: 'json',
          contentType: false,
			    processData: false,
          data: formData,
          success: function(response) {
            posts = Array.from(response);
            $('div').filter(function() {
              return this.id.match(/discussion_post/);
            }).remove();
            html = "";
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
                            if (post.file)
                            {
                              html += `<img style="width: 80px; height: 80px" onclick="this.style.width='300px'; this.style.height='300px'"
                              onmouseout="this.style.width='80px'; this.style.height='80px'" src="/${post.id}/get-post_screenshot">`;
                            }

                      if (post.username == post.current_username)
                      {
                        html += `<div class="message__admin">
                                  <a href="" class="message__admin-btn">Редактировать</a>
                                  <a class="message__admin-btn" onclick="del_post('/${post.current_username}/del_post/${post.topic_id}/${post.id}/${post.cur_page}', '${post.topic_id}')">Удалить</a>
                                  </div>`;
                      }
                     html += `</div></div>`;
            });
            div = document.getElementById('disc_posts_container');
            div.insertAdjacentHTML('afterbegin', html);

            // собираем пагинацию
            $('ul').filter(function() {
                    return this.id.match('pagination');
            }).remove();
            html = `<ul class="pagination__list list-reset" id="pagination">
            <li class="pagination__item disabled">&bull;</li>`;
            try
            {
              for (let i = 1; i <= posts[0].pages; i++)
              {
                html += `<li class="pagination__item active">
                          <a onclick="get_posts_page('/get_posts_page/${posts[0].topic_id}/${i}')">${i}</a>
                          </li>`;
              }
            }
            catch
            {}
            html += `<li class="pagination__item disabled">&bull;</li></ul>`;
            document.getElementById("posts_pagination_container").innerHTML = html;
            document.getElementById("post_body_id").value = "";

            $('span').filter(function() {
              return this.id.match('posts_count');
            }).remove();
            html = `<span class="main__span-forum" id="posts_count">Сообщений: ${posts[0].posts_count}</span>`;
            div = document.getElementById("main_container");
            div.insertAdjacentHTML("beforeend", html);
            document.getElementById("file_input_id").value = '';
          },
          error: function(error) {
              console.log(error);
          }
      });
    }
    else
    {
      alert('Заполните поле');
    }
}      
$(document).ready(function () {
    $('#add_post_form').submit(function(event) {
        add_post_on_forum();
        document.getElementById("post_body_id").setAttribute('required');
        event.preventDefault();
    });
  });
  
function add_post_on_forum() 
{
    if (document.getElementById('post_body_id').value.trim())
    {
      $.ajax({
          method: 'post',
          url: $("#add_post_form").attr('action'),
          dataType: 'json',
          data: $('#add_post_form').serialize(),
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
            document.getElementById('posts_pagination_container').innerHTML = html;
            document.getElementById("post_body_id").value = "";
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
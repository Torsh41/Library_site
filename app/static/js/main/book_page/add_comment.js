$(function() {
  $('#send_comment').on('click', function(event) {
    let target = event.target;
    let username = target.dataset?.user;
    let book_name = target.dataset?.book;
    form = document.getElementById('add_comment_form');
    form.setAttribute("action", `/${username}/${book_name}/add_comment`);
    if (document.getElementById('comment_body_id').value.trim() && document.getElementById('comment_body_id').value.trim().length <= 200)
    {
      $.ajax({
          method: 'post',
          url: $("#add_comment_form").attr('action'),
          dataType: 'json',
          data: $('#add_comment_form').serialize(),
          success: function(response) {
            comments = Array.from(response);
            $('li').filter(function() {
              return this.id.match(/comment_info/);
            }).remove();
            html = "";
            comments.forEach(comment => {
              html += ` <li class="comments__comment" id="${comment.id}comment_info">
                            <div class="comments__top">
                                <div class="comments__image">
                                <img class="comments__image-set" src="/user/${comment.username}/edit-profile/edit-avatar">
                                <!--Тут добавленная фотка пользователем-->
                                </div>`;
                                if (comment.username == comment.name_of_current_user && comment.current_user_is_authenticated)
                                {
                                    html += `<a href="/user/${comment.name_of_current_user}" class="comments__link">${comment.username}</a></div>`;
                                }
                                else 
                                {
                                    html += `<a class="comments__link">${comment.username}</a></div>`;
                                }
                               
                            
                            html += `<p class="comments__link" id="${comment.id}date">${comment.day + " " + comment.month + " " + comment.year}</p>`;
                            html += `<p class="comments__text" id="${comment.id}com_body">${comment.body}</p>`;
                            html += ` <div class="comments__commands" id="${comment.id}com_commands_cont">`;
                            if (comment.username == comment.name_of_current_user)
                            {
                              html += `<a id="${comment.id}edit_com_a" data-combody='${comment.body}' data-username='${comment.name_of_current_user}' data-bookname='${comment.book_name}' data-comid='${comment.id}' class="comments__command">Редактировать</a>
                                        <a class="comments__command" data-url='/${comment.name_of_current_user}/${comment.book_name}/delete-comment/${comment.id}/${comment.pages}' id="${comment.id}del">Удалить</a>`;
                            }
                            else if (comment.user_is_admin)
                            {
                              html += `<a class="comments__command">Админ</a>
                                        <a class="comments__command" data-url='/${comment.name_of_current_user}/${comment.book_name}/delete-comment/${comment.id}/${comment.pages}' id="${comment.id}del">Удалить</a>`;
                            }
                            html += `</div></li>`;
            });
            document.getElementById("comments_info_container").innerHTML = html;
            document.getElementById("comment_body_id").value = "";

            // собираем пагинацию
            $('ul').filter(function() {
                    return this.id.match('comments_pagination');
            }).remove();
            html = `<ul class="pagination__list list-reset" id="comments_pagination">
            <li class="pagination__item disabled">&bull;</li>`;
            comments[0].pages_count.forEach((page) => {
                if (page)
                {
                    if (page == comments[0].cur_page)
                    {
                        html += `<li class="pagination__item_cur_page">
                                    <a id='${page}comments_p' data-url='/get_comments_page/${comments[0].book_name}/${page}'>${page}</a>
                                </li>`;
                    }
                    else
                    {
                        html += `<li class="pagination__item active">
                                    <a id='${page}comments_p' data-url='/get_comments_page/${comments[0].book_name}/${page}'>${page}</a>
                                </li>`;
                    }
                }
                else
                {
                    html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`;
                }
            });
            
            html += `<li class="pagination__item disabled">&bull;</li></ul>`;
            document.getElementById('comments_pagination_container').innerHTML = html;
            li = document.getElementById(comments[0].id_of_added_comment + 'comment_info');
            li.scrollIntoView(); // Прокрутка до верхней границы
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
    else if (document.getElementById('comment_body_id').value.trim().length > 200)
    {
        alert('Слишком длинный комментарий');
    }
    else
    {
        alert('Заполните поле');
        document.getElementById('comment_body_id').value = '';
    }
  });
});

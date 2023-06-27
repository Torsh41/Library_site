function add_comment_for_book(username, book_name)
{
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
                              html += `<a id="${comment.id}edit_com_a" onclick="edit('${comment.body}', '${comment.name_of_current_user}', '${comment.book_name}', '${comment.id}')" class="comments__command">Редактировать</a>
                                        <a class="comments__command" onclick="del_comment('/${comment.name_of_current_user}/${comment.book_name}/delete-comment/${comment.id}/${comment.pages}')" id="${comment.id}del">Удалить</a>
                                        <script>scroll(${comment.id  + 'del'})</script>`;
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
            try
            {
              for (let i = 1; i <= comments[0].pages; i++)
              {
                if (comments[0].pages > 1 && i == comments[0].pages)
                {
                  html += `<li class="pagination__item_cur_page">
                              <a onclick="get_comments_page('/get_comments_page/${comments[0].book_name}/${i}')">${i}</a>
                            </li>`;
                }
                else
                {
                  html += `<li class="pagination__item active">
                            <a onclick="get_comments_page('/get_comments_page/${comments[0].book_name}/${i}')">${i}</a>
                        </li>`;
                }
              }
            }
            catch {}
            html += `<li class="pagination__item disabled">&bull;</li></ul>`;
            document.getElementById('comments_pagination_container').innerHTML = html;
            li = document.getElementById(comments[0].id_of_added_comment + 'comment_info');
            li.scrollIntoView(); // Прокрутка до верхней границы
          },
          error: function(error) {
              console.log(error);
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
}
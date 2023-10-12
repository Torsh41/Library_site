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
                html += `<li class="comments__comment" id="${comment.id}comment_info">
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
                html += `<p class="comments__link" id="${comment.id}date">${comment.day + " " + comment.month + " " + comment.year}</p>`;
                html += `<p class="comments__text" id="${comment.id}com_body">${comment.body}</p>`;
                html += ` <div class="comments__commands" id="${comment.id}com_commands_cont">`;
                if (comment.username == comment.name_of_current_user)
                {
                  html += `<a id="${comment.id}edit_com_a" data-combody="${comment.body}" data-username="${comment.username}" data-bookname="${comment.book_name}" data-comid="${comment.id}" class="comments__command">Редактировать</a>
                            <a class="comments__command" data-url='/${comment.name_of_current_user}/${comment.book_name}/delete-comment/${comment.id}/${url[url.length - 1]}' id="${comment.id}del">Удалить</a>`;
                }
                else if (comment.user_is_admin)
                {
                  html += `<a class="comments__command">Админ</a>
                           <a class="comments__command" data-url='/${comment.name_of_current_user}/${comment.book_name}/delete-comment/${comment.id}/${url[url.length - 1]}' id="${comment.id}del">Удалить</a>`;
                }
                html += `</div></li>`;
                
            });
            document.getElementById("comments_info_container").innerHTML = html;
            pagi = document.getElementById('comments_pagination');
            pagi_li = pagi.querySelector('.pagination__item_cur_page');
            if (pagi_li)
            {
              pagi_li.className = 'pagination__item active';
            }
            for (const child of pagi.children)
            {
              if (comments.length && comments[0].cur_page == child.textContent)
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

function edit_comment_ajax()
{
    if (document.getElementById('edit_comment_field').value.trim() && document.getElementById('edit_comment_field').value.trim().length <= 200)
    {
        $.ajax({
            method: 'post',
            url: $("#edit_comment_form").attr('action'),
            dataType: 'json',
            data: $('#edit_comment_form').serialize(),
            success: function(response) {
              $('p').filter(function() {
                  return this.id.match(response.id + "com_body");
                }).remove();
              $('a').filter(function() {
                  return this.id.match(response.id + "edit_com_a");
                }).remove();
              

              html = `<p class="comments__text" id="${response.id}com_body">${response.body}</p>`;
              p =  document.getElementById(response.id + 'date');
              div = document.getElementById(response.id + 'com_commands_cont');
              p.insertAdjacentHTML('afterend', html);
              html = `<a id="${response.id}edit_com_a" data-combody="${response.body}" data-username="${response.username}" data-bookname="${response.book_name}" data-comid="${response.id}" class="comments__command">Редактировать</a>`;
              div.insertAdjacentHTML('afterbegin', html)
              document.getElementById("edit_comment_field").value = "";
              document.getElementById("edit_comment_sec").style.display = "none";
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
    else if (document.getElementById('edit_comment_field').value.trim().length > 200)
    {
      alert('Слишком длинный комментарий');
    }
    else
    {
      alert('Заполните поле');
      document.getElementById('edit_comment_field').value = '';
    }
}

$(function() {
    $('#comments_info_container').on('click', function(event) {
        let target = event.target;
        if (target.tagName === 'A' && target.id.includes('del')) 
        {
          let url_path = target.dataset?.url;
          if (confirm('Подтвердите действие'))
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
          
                  html = `<ul class="pagination__list list-reset" id="comments_pagination"><li class="pagination__item disabled"> &bull;</li>`;
                  if (response.has_elems) 
                  {
                    for (let i = 1; i <= response.pages; i++)
                    {
                      if (response.pages > 1 && i == response.cur_page)
                      {
                        html += `<li class="pagination__item_cur_page">
                                  <a id="${i}comments_p" data-url='/get_comments_page/${response.book_name}/${i}'>${i}</a>
                                 </li>`;
                      }
                      else
                      {
                        html += `<li class="pagination__item active">
                                    <a id="${i}comments_p" data-url='/get_comments_page/${response.book_name}/${i}'>${i}</a>
                                 </li>`;
                      }
                    }
                  }
          
                  html += `<li class="pagination__item disabled">&bull;</li></ul>`;
                  
                  document.getElementById('comments_pagination_container').innerHTML = html;
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
        else if (target.tagName === 'A' && target.id.includes('edit_com_a')) 
        {
          let comment_id = target.dataset?.comid;
          let username = target.dataset?.username;
          let book_name = target.dataset?.bookname;
          let text = target.dataset?.combody;
          document.getElementById("edit_comment_sec").style.display = "block";
          document.getElementById("edit_comment_field").value = text;
          form = document.getElementById("edit_comment_form");
          form.setAttribute("action", `/${username}/${book_name}/edit-comment/${comment_id}`);
        }
    });
    
    $('#comments_pagination_container').on('click', function(event) {
        let target = event.target;
        if (target.tagName === 'A' && target.id.includes('comments_p'))
        {
          let url_path = target.dataset?.url;
          get_comments_page(url_path);
        }
    });

    $('#edit_comment_form').submit(function(event) {
      edit_comment_ajax();
      event.preventDefault();
    });
    
    $('#close_form').click(function(event) {
      document.getElementById("edit_comment_field").value = "";
      document.getElementById("edit_comment_sec").style.display = "none";
    });
  
    $('#edit_comment').click(function(event) {
      edit_comment_ajax();
    });
});
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
                html += `<li class="category__elem" id="${category.id}category_info"><a href="/category/${category.name}/search" class="about__book-link"><div class="category__block">${category.name}</div></a></li>`;
            });
            document.getElementById("categories_block").innerHTML = html;
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
                  html += `<a id="${comment.id}edit_com_a" onclick="edit('${comment.body}', '${comment.name_of_current_user}', '${comment.book_name}', '${comment.id}')" class="comments__command">Редактировать</a>
                            <a class="comments__command" onclick="del_comment('/${comment.name_of_current_user}/${comment.book_name}/delete-comment/${comment.id}/${url[url.length - 1]}')" id="${comment.id}del">Удалить</a>`;
                }
                else if (comment.user_is_admin)
                {
                  html += `<a class="comments__command">Админ</a>
                           <a class="comments__command" onclick="del_comment('/${comment.name_of_current_user}/${comment.book_name}/delete-comment/${comment.id}/${url[url.length - 1]}')" id="${comment.id}del">Удалить</a>`;
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
        error: function(error) {
            console.log(error);
        }
    });
}

function del_comment(url_path) 
{
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
                          <a onclick="get_comments_page('/get_comments_page/${response.book_name}/${i}')">${i}</a>
                        </li>`;
              }
              else
              {
                html += `<li class="pagination__item active">
                          <a onclick="get_comments_page('/get_comments_page/${response.book_name}/${i}')">${i}</a>
                          </li>`;
              }
            }
          }
  
          html += `<li class="pagination__item disabled">&bull;</li></ul>`;
          
          document.getElementById('comments_pagination_container').innerHTML = html;
        },
        error: function(error) {
            console.log(error);
        }
      });
  }
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
                    html += `<ul class="fraction__topic-list list-reset" id="${category.id + 'grid_container'}">`;
                    if (category.username_of_cur_user)
                    {
                        html += `<li class="fraction__list-item">
                                    <a class="fraction__topic-link" onclick="openForm('${category.username_of_cur_user}', '${category.name}', '${url[url.length - 1]}')"> <!--Add the new topic (for users)-->
                                      <div class="fraction__topic">
                                        <svg width="78" height="78" viewBox="0 0 78 78" fill="none" xmlns="http://www.w3.org/2000/svg">
                                          <g clip-path="url(#clip0_139_2)">
                                            <rect x="35" width="8" height="78" fill="#F5F5DC" />
                                            <rect x="78" y="35" width="8" height="78" transform="rotate(90 78 35)" fill="#F5F5DC" />
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
                                      <div class="fraction__topic">
                                        <p class="fraction__text-error">
                                          ${topic.name}
                                        </p>
                                      </div>
                                    </a>`;
                        if (category.cur_user_is_admin)
                        {
                          html += `<a class="comments__command">Админ</a>
                                  <a class="comments__command" onclick="del_topic('/delete-topic/${category.id}/${topic.id}/${1}', '${category.id}')">Удалить</a>`;      
                        }
                        html += `</li>`;
                    });
                html += `</ul>
                        <div class="list__pagination pagination">
                          <ul class="pagination__list list-reset" id="${category.id}topics_pagi">
                          <li class="pagination__item disabled">
                            &bull;
                          </li>`;
                try
                {
                  for (let i = 1; i <= topics[0].topic_pages; i++)
                  {
                      html +=`<li class="pagination__item active">
                                <a onclick="get_topics_page_on_forum('/get_topics_page_on_forum/${category.id}/${i}', '${category.id}')">${i}</a>
                              </li>`;
                  }
                }
                catch
                {}
                html += `<li class="pagination__item disabled">
                            &bull;
                          </li>
                          </ul></div></div></section>`;
            });
            section = document.getElementById('first_section');
            section.insertAdjacentHTML('afterend', html);
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
                          " " + post.user_year}</span>
                        </div>
                      </div>
    
                      <div class="message__right" id="${post.id}msg_write_id">`;
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
                        html += `<img style="width: 80px; height: 80px" onclick="this.style.width='300px'; this.style.height='300px'"
                        onmouseout="this.style.width='80px'; this.style.height='80px'" src="/${post.id}/get-post_screenshot">`;
                      }

                  if (post.username == post.current_username)
                  {
                    html += `<div class="message__admin" id="${post.id}personal_cont">
                              <a class="message__admin-btn" id="${post.id}answer_on" onclick="answer_on_post('${post.id}')">Ответить</a>
                              <a class="message__admin-btn" id="${post.id}edit_post_a" onclick="open_popup_form('/${post.current_username}/edit_post/${post.topic_id}/${post.id}', '${post.body}')">Редактировать</a>
                              <a class="message__admin-btn" onclick="del_post('/${post.current_username}/del_post/${post.topic_id}/${post.id}/${post.cur_page}', '${post.topic_id}')">Удалить</a>
                              </div>`;
                  }
                  else if (post.user_is_admin)
                  {
                    html += `<div class="message__admin" id="${post.id}personal_cont">
                    <a class="comments__command">Админ</a>
                    <a class="message__admin-btn" id="${post.id}answer_on" onclick="answer_on_post('${post.id}')">Ответить</a>
                    <a class="message__admin-btn" onclick="del_post('/${post.current_username}/del_post/${post.topic_id}/${post.id}/${post.cur_page}', '${post.topic_id}')">Удалить</a>
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
    error: function(error) {
        console.log(error);
    }
  });
}

function del_post(url_path, topic_id)
{
  if (confirm('Подтвердите действие'))
  {
    $.ajax({
      method: 'get',
      url: url_path,
      dataType: 'json',
      success: function(response) {
        get_posts_page(`/get_posts_page/${topic_id}/${response.cur_page}`);
        $('ul').filter(function() {
          return this.id.match('pagination');
        }).remove();

        html = `<ul class="pagination__list list-reset" id="pagination"><li class="pagination__item disabled"> &bull;</li>`;                            
        if (response.has_elems) 
        {
          for (let i = 1; i <= response.pages; i++)
          {
            if (response.pages > 1 && i == response.cur_page)
            {
              html += `<li class="pagination__item_cur_page">
                        <a onclick="get_posts_page('/get_posts_page/${topic_id}/${i}')">${i}</a>
                      </li>`;
            }
            else
            {
              html += `<li class="pagination__item active">
                        <a onclick="get_posts_page('/get_posts_page/${topic_id}/${i}')">${i}</a>
                        </li>`;
            }
          }
        }

        html += `<li class="pagination__item disabled">&bull;</li></ul>`;
        
        document.getElementById('posts_pagination_container').innerHTML = html;
        $('span').filter(function() {
          return this.id.match('posts_count');
        }).remove();
        html = `<span class="main__span-forum" id="posts_count">Сообщений: ${response.posts_count}</span>`;
        div = document.getElementById("main_container");
        div.insertAdjacentHTML("beforeend", html);
      },
      error: function(error) {
          console.log(error);
      }
    });
  }
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
                        <div class="fraction__topic">
                          <p class="fraction__text-error">
                            ${topic.name}
                          </p> 
                        </div>
                      </a>`;
                    if (topic.cur_user_is_admin)
                    {
                      html += `<a class="comments__command">Админ</a>
                                <a class="comments__command" onclick="del_topic('/delete-topic/${category_id}/${topic.id}/${topic.cur_page}', '${category_id}')">Удалить</a>`;
                           
                    }
        html += `</li>`;
      });
      div = document.getElementById(category_id + "grid_container");
      div.insertAdjacentHTML('beforeend', html);
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
    error: function(error) {
        console.log(error);
    }
  });
}

function del_topic(url_path, category_id)
{
  if (confirm('Подтвердите действие'))
  {
    $.ajax({
      method: 'get',
      url: url_path,
      dataType: 'json',
      success: function(response) {
        get_topics_page_on_forum(`/get_topics_page_on_forum/${category_id}/${response.cur_page}`, `${category_id}`);
        $('ul').filter(function() {
          return this.id.match(category_id + 'topics_pagi');
        }).remove();

        html = `<div class="list__pagination pagination">
                  <ul class="pagination__list list-reset" id="${category_id}topics_pagi"><li class="pagination__item disabled"> &bull;</li>`;                            
        if (response.has_elems) 
        {
          for (let i = 1; i <= response.pages; i++)
          {
            if (response.pages > 1 && i == response.cur_page)
            {
              html += `<li class="pagination__item_cur_page">
                        <a onclick="get_topics_page_on_forum('/get_topics_page_on_forum/${category_id}/${i}', '${category_id}')">${i}</a>
                      </li>`;
            }
            else
            {
              html += `<li class="pagination__item active">
                        <a onclick="get_topics_page_on_forum('/get_topics_page_on_forum/${category_id}/${i}', '${category_id}')">${i}</a>
                        </li>`;
            }
          }
        }
        html += `<li class="pagination__item disabled">&bull;</li></ul></div>`;
        div = document.getElementById(category_id + 'grid_container');
        div.insertAdjacentHTML('afterend', html);
        document.getElementById(category_id + 'topics_count').textContent = `Всего тем: ${response.topics_count}`;
      },
      error: function(error) {
          console.log(error);
      }
    });
  }
}

function get_lists_page_to_add_book(url_path, read_state, book_id)
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
      html = "";
      cataloges.forEach(cataloge => {
      html += `<section class="list__list" id="${cataloge.id}cataloge_info">
                    <div class="container lists__catalog">
                      <a class="title list__name" href="/user/${cataloge.username}/add-book-in-list/${cataloge.id}/${book_id}/${read_state}">${cataloge.name}</a>
                    </div>
                </section>`;
      });
      div = document.getElementById('cataloges_hat');
      div.insertAdjacentHTML('afterend', html);
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
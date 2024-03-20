function write_post_socket(topic_id, post_id_to_answer = false) 
{
  if (document.getElementById("post_body_id").value.trim() && document.getElementById("post_body_id").value.trim().length <= 200) 
  {
    form = document.getElementById("add_post_form");
    var formData = new FormData(form);
    socket.emit("send post", {
      post_body: formData.get("post_body"),
      filename: formData.get("screenshot").name,
      screenshot: formData.get("screenshot"),
      topic_id: topic_id,
      post_id_to_answer: post_id_to_answer,
    });

    // $('#add_post_button').on('click', function(event) {
    //   write_post_socket(topic_id);
    // });
    document.getElementById("add_post_button").setAttribute("onclick", `write_post_socket('${topic_id}')`);
  } 
  else if (document.getElementById("post_body_id").value.trim().length > 200) 
  {
    alert("Слишком длинный пост");
  } 
  else 
  {
    alert("Заполните поле");
    document.getElementById("post_body_id").value = "";
  }
}


function del_post_socket(topic_id, post_id, page) 
{
  if (confirm("Подтвердите действие")) 
  {
    socket.emit("del post", {
      topic_id: topic_id,
      post_id: post_id,
      page: page,
    });

    // $('#add_post_button').on('click', function(event) {
    //   write_post_socket(topic_id);
    // });
    document.getElementById("add_post_button").setAttribute("onclick", `write_post_socket('${topic_id}')`);
  }
}


function add_post_on_forum(posts) {
  posts = Array.from(posts);
  $("div")
    .filter(function () {
      return this.id.match(/discussion_post/);
    })
    .remove();
  html = "";
  posts.forEach((post) => {
    html += `<div class="discussion__message message" id="${post.id}discussion_post"> 
                          <div class="message__left">
                            <div class="message__name">`;
    if (post.username == cur_username) 
    {
      html += `<a href="/user/${cur_username}" class="message__link">`;
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
                              <span class="message__span">На сайте с ${
                                post.user_day +
                                " " +
                                post.user_month +
                                " " +
                                post.user_year
                              }</span>
                            </div>
                          </div>
        
                          <div class="message__right" id="${post.id}msg_write_id">`;
    if (post.this_is_answer) 
    {
      if (post.basic_post_exist) 
      {
        html += `<div class="message__answer" id="${post.id}base_to_answer">
                                        <span class="message__span-answer">Сообщение от ${post.username_of_post_from}</span>
                                        <p class="message__text-answer">${post.body_of_post_from}</p>
                                      </div>`;
      }
      else
      {
        html += `<div class="message__answer" id="${post.id}base_to_answer">
                                        <span class="message__span-answer">Сообщение удалено</span>
                                      </div>`;
      }
    }
    html += `<p class="message__text" id="${post.id}post_body">
                            ${post.body} <!--Сообщение пользователя-->
                            </p>`;
    if (post.file) 
    {
      html += `<img style="width: 80px; height: 80px" onclick="this.style.width='300px'; this.style.height='300px'"
                              onmouseout="this.style.width='80px'; this.style.height='80px'" src="/${post.id}/get-post_screenshot">`;
    }

    if (post.username == cur_username) 
    {
      html += `<div class="message__admin" id="${post.id}personal_cont">
                                  <a class="message__admin-btn" id="${post.id}answer_on" data-topicid='${post.topic_id}' data-postid='${post.id}'>Ответить</a>
                                  <a class="message__admin-btn" id="${post.id}edit_post_a" data-url='/${cur_username}/edit_post/${post.topic_id}/${post.id}' data-body='${post.body}'>Редактировать</a>
                                  <a class="message__admin-btn" id="${post.id}post_d" data-topicid='${post.topic_id}' data-postid='${post.id}' data-page='${post.cur_page}'>Удалить</a>
                                  </div>`;
    } else if (cur_user_is_admin) 
    {
      html += `<div class="message__admin" id="${post.id}personal_cont">
                                    <a class="comments__command">Админ</a>
                                    <a class="message__admin-btn" id="${post.id}answer_on" data-topicid='${post.topic_id}' data-postid='${post.id}'>Ответить</a>
                                    <a class="message__admin-btn" id="${post.id}post_d" data-topicid='${post.topic_id}' data-postid='${post.id}' data-page='${post.cur_page}'>Удалить</a>
                                  </div>`;
    } else if (cur_username) 
    {
      html += `<div class="message__admin" id="${post.id}personal_cont">
            <a class="message__admin-btn" id="${post.id}answer_on" data-topicid='${post.topic_id}' data-postid='${post.id}'>Ответить</a>
            </div>`;
    }
    html += `</div></div>`;
  });
  div = document.getElementById("disc_posts_container");
  div.insertAdjacentHTML("afterbegin", html);
  div.scrollIntoView(false); // Прокрутка до нижней границы

  // собираем пагинацию
  $("ul")
    .filter(function () {
      return this.id.match("pagination");
    })
    .remove();
  html = `<ul class="pagination__list list-reset" id="pagination">
            <li class="pagination__item disabled">&bull;</li>`;
  posts[0].pages_count.forEach(p => {
    if (p)
    {
      if (p == posts[0].cur_page)
      {
        html += `<li class="pagination__item_cur_page">
                    <a id="${p}posts_p" data-url='/get_posts_page/${posts[0].topic_id}/${p}'>${p}</a>
                  </li>`;
      }
      else
      {
        html += `<li class="pagination__item active">
                  <a id="${p}posts_p" data-url='/get_posts_page/${posts[0].topic_id}/${p}'>${p}</a>
                </li>`;
      }
    }
    else
    {
      html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`;
    }
  });

  html += `<li class="pagination__item disabled">&bull;</li></ul>`;
  document.getElementById("posts_pagination_container").innerHTML = html;
  if (document.getElementById("post_body_id"))
  {
    document.getElementById("post_body_id").value = "";
  }

  $("span")
    .filter(function () {
      return this.id.match("posts_count");
    })
    .remove();
  html = `<span class="main__span-forum" id="posts_count">Сообщений: ${posts[0].posts_count}</span>`;
  div = document.getElementById("main_container");
  div.insertAdjacentHTML("beforeend", html);
  if (document.getElementById("file_input_id"))
  {
    document.getElementById("file_input_id").value = "";
  }
}

function del_post(response, topic_id, post_id) 
{
  get_posts_page(`/get_posts_page/${topic_id}/${response.cur_page}`);
  
  $("#pagination").remove();

  let html = `<ul class="pagination__list list-reset" id="pagination"><li class="pagination__item disabled"> &bull;</li>`;
  if (response.has_elems) 
  {
    response.pages_count.forEach(p => {
      if (p)
      {
        if (p == response.cur_page)
        {
          html += `<li class="pagination__item_cur_page">
                      <a id='${p}posts_p' data-url='/get_posts_page/${topic_id}/${p}'>${p}</a>
                    </li>`;
        }
        else
        {
          html += `<li class="pagination__item active">
                      <a id='${p}posts_p' data-url='/get_posts_page/${topic_id}/${p}'>${p}</a>
                    </li>`;
        }
      }
      else
      {
        html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`;
      }
    });
  }
  html += `<li class="pagination__item disabled">&bull;</li></ul>`;
  document.getElementById("posts_pagination_container").innerHTML = html;
  $("span")
    .filter(function () {
      return this.id.match("posts_count");
    })
    .remove();
  html = `<span class="main__span-forum" id="posts_count">Сообщений: ${response.posts_count}</span>`;
  div = document.getElementById("main_container");
  div.insertAdjacentHTML("beforeend", html);
}

function answer_on_post(topic_id, post_id) 
{
  document.getElementById("add_post_button").setAttribute("onclick", `write_post_socket('${topic_id}', '${post_id}')`);
  // $('#add_post_button').on('click', function(event) {
  //   write_post_socket(topic_id, post_id);
  // });
  document.getElementById("add_post_form").scrollIntoView();
  $("#post_body_id").css("opacity", ".4").animate({ opacity: "1" }, "slow");
}


function get_posts_page(url_path, post_id=undefined)
{
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
                        if (post.basic_post_exist)
                        {
                          html += `<div class="message__answer" id="${post.id}base_to_answer">
                                    <span class="message__span-answer">Сообщение от ${post.username_of_post_from}</span>
                                    <p class="message__text-answer">${post.body_of_post_from}</p>
                                  </div>`;
                        }
                        else
                        {
                          html += `<div class="message__answer" id="${post.id}base_to_answer">
                                    <span class="message__span-answer">Сообщение удалено</span>
                                  </div>`;
                        }
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
                              <a class="message__admin-btn" id="${post.id}answer_on" data-topicid='${post.topic_id}' data-postid='${post.id}'>Ответить</a>
                              <a class="message__admin-btn" id="${post.id}edit_post_a" data-url='/${cur_username}/edit_post/${post.topic_id}/${post.id}' data-body='${post.body}'>Редактировать</a>
                              <a class="message__admin-btn" id="${post.id}post_d" data-topicid='${post.topic_id}' data-postid='${post.id}' data-page='${post.cur_page}'>Удалить</a>
                              </div>`;
                  }
                  else if (post.user_is_admin)
                  {
                    html += `<div class="message__admin" id="${post.id}personal_cont">
                    <a class="comments__command">Админ</a>
                    <a class="message__admin-btn" id="${post.id}answer_on" data-topicid='${post.topic_id}' data-postid='${post.id}'>Ответить</a>
                    <a class="message__admin-btn" id="${post.id}post_d" data-topicid='${post.topic_id}' data-postid='${post.id}' data-page='${post.cur_page}'>Удалить</a>
                    </div>`;
                  }
                  else if (post.current_username)
                  {
                    html += `<div class="message__admin" id="${post.id}personal_cont">
                    <a class="message__admin-btn" id="${post.id}answer_on" data-topicid='${post.topic_id}' data-postid='${post.id}'>Ответить</a>
                    </div>`;
                  }
                 html += `</div></div>`;
        });
        let div = document.getElementById('disc_posts_container');
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

let socket = io(); 
let cur_username = '';
let cur_user_is_admin;
$(function() {
  let a = $("#write_msg");
  if (a && a.length > 0) 
  {
    let topic_id = a.data('username').split(';')[2];
    let write_post_form = document.getElementById("add_post_form");
    if (write_post_form)
    {
      // $('#add_post_button').on('click', function(event) {
      //   write_post_socket(topic_id);
      // });
      document.getElementById("add_post_button").setAttribute("onclick", `write_post_socket('${topic_id}')`);
      a.on('click', function () {
        document.getElementById("add_post_button").setAttribute("onclick", `write_post_socket('${topic_id}')`);
        // $('#add_post_button').on('click', function(event) {
        //   write_post_socket(topic_id);
        // });
        write_post_form.scrollIntoView();
        $("#post_body_id").css("opacity", ".4").animate({ opacity: "1" }, "slow");
      });
    }
    let username = a.data('username').split(';')[0];
    cur_user_is_admin = Number(a.data('username').split(';')[1]);
    if (username.length > 0)
    {
      cur_username = username;
    }
  }
  socket.on("add post", function (posts) {
    add_post_on_forum(posts.data);
  });
  socket.on("del post response", function (response) {
    del_post(response.response, response.topic_id, response.post_id);
  });

  $('#disc_posts_container').on('click', function(event) {
      let target = event.target;
      if (target.tagName === 'A' && target.id.includes('post_d'))
      {
        let topic_id = target.dataset?.topicid;
        let post_id = target.dataset?.postid;
        let page = target.dataset?.page;
        del_post_socket(topic_id, post_id, page);
      }
      else if (target.tagName === 'A' && target.id.includes('answer_on'))
      {
        let topic_id = target.dataset?.topicid;
        let post_id = target.dataset?.postid;
        answer_on_post(topic_id, post_id);
      }
  });
});








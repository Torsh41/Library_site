$(document).ready(function () {
    $('#edit_post_form').submit(function(event) {
        edit_post_ajax();
        event.preventDefault();
    });
  });

function open_popup_form(url_path, post_body)
{
    document.getElementById("edit_post_sec").style.display = "block";
    document.getElementById("edit_post_field").value = post_body;
    form = document.getElementById("edit_post_form");
    form.setAttribute("action", url_path);
}

function closeEditPostForm()
{
    document.getElementById("edit_post_field").value = "";
    document.getElementById("edit_post_sec").style.display = "none";
}
function edit_post_ajax()
{
    if (document.getElementById('edit_post_field').value.trim())
    {
      $.ajax({
          method: 'post',
          url: $("#edit_post_form").attr('action'),
          dataType: 'json',
          data: $('#edit_post_form').serialize(),
          success: function(response) {
            $('p').filter(function() {
                return this.id.match(response.post_id + "post_body");
              }).remove();
            $('a').filter(function() {
                return this.id.match(response.post_id + "edit_post_a");
              }).remove();
             

            html = `  <p class="message__text" id="${response.post_id}post_body">
                        ${response.post_body} <!--Сообщение пользователя-->
                      </p>`;
            div = document.getElementById(response.post_id + 'base_to_answer');
            if (div)
            {
              div.insertAdjacentHTML('afterend', html);
            }
            else
            {
              div = document.getElementById(response.post_id + 'msg_write_id');
              div.insertAdjacentHTML('afterbegin', html);
            }
            div_ = document.getElementById(response.post_id + 'personal_cont');
            html = `<a class="message__admin-btn" id="${response.post_id}edit_post_a" onclick="open_popup_form('/${response.username}/edit_post/${response.topic_id}/${response.post_id}', '${response.post_body}')">Редактировать</a>`;
            div_.insertAdjacentHTML('afterbegin', html)
            closeEditPostForm();
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
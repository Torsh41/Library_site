$(document).ready(function () {
    $('#edit_comment_form').submit(function(event) {
        edit_comment_ajax();
        event.preventDefault();
    });
});

function edit(text, username, book_name, comment_id)
{
    document.getElementById("edit_comment_sec").style.display = "block";
    document.getElementById("edit_comment_field").value = text;
    form = document.getElementById("edit_comment_form");
    form.setAttribute("action", `/${username}/${book_name}/edit-comment/${comment_id}`);
}

function closeEditCommentForm()
{
    document.getElementById("edit_comment_field").value = "";
    document.getElementById("edit_comment_sec").style.display = "none";
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
              html = `<a id="${response.id}edit_com_a" onclick="edit('${response.body}', '${response.username}', '${response.book_name}', '${response.id}')" class="comments__command">Редактировать</a>`;
              div.insertAdjacentHTML('afterbegin', html)
              closeEditCommentForm();
            },
            error: function(error) {
                console.log(error);
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
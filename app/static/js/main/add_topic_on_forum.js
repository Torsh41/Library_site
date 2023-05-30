function openForm(username, category_name, page) 
{
  document.getElementById("popupForm").style.display = "block";
  form = document.getElementById("add_topic_form");
  form.setAttribute("action", `/${username}/${category_name}/add_topic?page=${page}`);
}

function closeForm() 
{
  document.getElementById("popupForm").style.display = "none";
}

// $(document).ready(function () {
//   $('#add_topic_form').submit(function(event) {
//     validate_topic_name();
//     event.preventDefault();
//   });
// });

function validate_topic_name()
{
  $.ajax({
    method: 'post',
    url: $("#add_topic_form").attr('action'),
    dataType: 'json',
    data: $('#add_topic_form').serialize(),
    success: function(response) {
      topics_for_cur_category = Array.from(response)
      if (topics_for_cur_category[0].result)
      {
        $('a').filter(function() {
          return this.id.match(topics_for_cur_category[0].category_id + 'topic_info');
        }).remove();
        $('span').filter(function() {
          return this.id.match(topics_for_cur_category[0].category_id + 'topics_count');
        }).remove();
        html = '';
        topics_for_cur_category.forEach(topic => {
            html += `<a href="/forum/${topic.name}" class="fraction__topic-link" id="${topic.category_id + 'topic_info'}">
                      <div class="fraction__topic">
                        ${topic.name}
                      </div>
                      </a>`;
        });
        div_outer = document.getElementById(topics_for_cur_category[0].category_id + 'category_title');
        div_outer.insertAdjacentHTML('afterend', `<span class="fraction__results" id="${topics_for_cur_category[0].category_id + 'topics_count'}">Всего тем: ${topics_for_cur_category[0].topics_count}</span>`);
        div = document.getElementById(topics_for_cur_category[0].category_id + 'grid_container');
        div.insertAdjacentHTML('beforeend', html);
        document.getElementById("topic_name_id_form").value = "";
        document.getElementById("popupForm").style.display = "none";
        alert(`Тема успешно создана`);
      }
      else
      {
        document.getElementById("topic_name_id_form").value = "";
        alert(`Такая тема уже имеется в данном разделе`);
      }
    },
    error: function(error) {
        console.log(error);
    }
  });
}
    
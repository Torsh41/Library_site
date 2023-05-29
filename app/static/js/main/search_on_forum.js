$(document).ready(function () {
  $("form").submit(function(event) {
    search_category_on_forum();
    event.preventDefault();
  });
});

function search_category_on_forum() 
{
    $.ajax({
        method: 'post',
        url: '/search_category_on_forum',
        dataType: 'json',
        data: $('form').serialize(),
        success: function(response) {
          categories = Array.from(response);
          if (categories[0].result)
          {
                $('section').filter(function() {
                    return this.id.match(/category_info/);
                }).remove();
                $('section').filter(function() {
                  return this.id.match("not_found");
                }).remove();
                document.getElementById("category_name_id").value = "";
                
                html = "";
                categories.forEach(category => {
                    html +=  `<section id="${category.id}category_info" class="fraction">
                    <div class="fraction__container container">
                      <div class="fraction__wrap">
                        <h2 class="fraction__title title">${category.name}</h2> 
                        <span class="fraction__results"> Всего тем: ${category.topics_count}</span> 
                            <a href="#" class="fraction__topic-link"> <!--Add the new topic (for users)-->
                              <div class="fraction__topic">
                                <svg width="78" height="78" viewBox="0 0 78 78" fill="none" xmlns="http://www.w3.org/2000/svg">
                                  <g clip-path="url(#clip0_139_2)">
                                    <rect x="35" width="8" height="78" fill="#D9D9D9" />
                                    <rect x="78" y="35" width="8" height="78" transform="rotate(90 78 35)" fill="#D9D9D9" />
                                  </g>
                                  <defs>
                                    <clipPath id="clip0_139_2">
                                      <rect width="78" height="78" fill="white" />
                                    </clipPath>
                                  </defs>
                                </svg>
                              </div>
                            </a>`;
                        topics = Array.from(category.topics);
                        topics.forEach(topic => {
                            html += `<div class="fraction__topic-list">
                            <a href="/forum/${topic.name}" class="fraction__topic-link">
                              <div class="fraction__topic">
                                ${topic.name}
                              </div>
                            </a>
                          </div>`;
                        });
                    html += `</div></div></section>`;
                });
                section = document.getElementById('first_section');
                section.insertAdjacentHTML('afterend', html);
                section = document.getElementById(categories[0].id_of_found_elem + 'category_info');
                section.scrollIntoView(); // Прокрутка до верхней границы
          }
          else
          {
            $('section').filter(function() {
              return this.id.match(/category_info/);
            }).remove();
            $('section').filter(function() {
              return this.id.match("not_found");
            }).remove();
            document.getElementById("category_name_id").value = "";
            html = `<section class="list" id="not_found">
                    <div class="container list__container">
                      <div class="list__wrap">
                        <h2 class="list__title title">Ничего не найдено</h2>
                      </div>
                    </div>
                    </section>`;
            section = document.getElementById('first_section');
            section.insertAdjacentHTML('afterend', html);
          }
        },
        error: function(error) {
            console.log(error);
        }
    });
}      
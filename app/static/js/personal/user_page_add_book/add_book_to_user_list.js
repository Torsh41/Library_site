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

$(function() {
    $('#comments_pagination_container').on('click', function(event) {
       let target = event.target;
       if (target.tagName === 'A' && target.id.includes('lists_p'))
       {
        let url_path = target.dataset?.url;
        let read_state = target.dataset?.readstate;
        let book_id = target.dataset?.bookid;
        get_lists_page_to_add_book(url_path, read_state, book_id);
       } 
    });
});

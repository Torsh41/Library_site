function convert(first_page, last_page, func_name, url_path, elem_for_remove_id, li_id, pagination_id)
{
    $('li').filter(function() {
        return this.id.match(elem_for_remove_id);
      }).remove();
    for (let i  = first_page; i <= last_page; i++)
    {
        html += `<li class="pagination__item active">
                    <a onclick="${func_name}('${url_path + i}', '${pagination_id}')">${i}</a>
                </li>`;
    }
    li = document.getElementById(li_id);
    li.insertAdjacentHTML("afterbegin", html);

}
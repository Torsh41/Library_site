// import the following script in the header
// <script defer src="{{ url_for('static', filename='js/common/book_search_form.js') }}"></script>

const formId = "search-form";
var form = new BookSearchForm(formId);
const sectionIdBookList = "book-list-section";
const sectionIdPagination = "pagination-section";


function renderBookTemplate(response) {
  if (response.result != true) {
    return
  }
  html = `
<div class="container list__container">
  <div class="list__wrap">
    <h2 class="list__title title">Вот, что нашлось</h2>
    <span class="list__results"> Всего результатов: ${response.book_list.length} </span>
    <ul class="list__books list-reset list__booksStart" id="book_search_res_ul">`;
  response.book_list.forEach(book => {
    if (book.name.length > 10) {
      book.name = book.name.slice(0, 10) + "...";
    }
    if (book.author.length > 10) {
      book.author = book.author.slice(0, 10) + "...";
    }
    html += `
      <li class="list__book" id="${book.id}search_books_info">
        <a href="/book-page/${book.id}" class="list__book-set">
          <img class="list__book-set" src="/${book.id}/get-cover" alt="">
        </a>
        <div class="list__book-wrap">`;
    if (response.current_user.is_authenticated) {
      html += `
          <a href="/user/${response.current_user.username}/add-book-in-list-tmp/${book.id}" class="list__book-delete-btn">Добавить в список</a>`;
    }
    html += `
          <a href="/book-page/${book.id}" class="list__link-book">Книга: ${book.name}</a>
          <span class="list__link">Автор: ${book.author}</span>
          <div class="list__mark-star">
            <span class="list__mark-visible">Оценка ${book.grade_avg}</span>
            <img src="/static/styles/img/star1.svg" alt="" class="list__star">
          </div>
        </div>
      </li>`;
  });
  html += `
    </ul>
  </div>
</div>`;

  let section = document.getElementById(sectionIdBookList);
  section.innerHTML = html;
  section.scrollIntoView();
}

function renderPaginationTemplate(response) {
  if (response.result != true) {
    return
  }
  html = `
<ul id="pagination" class="pagination__list list-reset">
  <li class="pagination__item disabled">
    &bull;
  </li>`;
  response.pagination.page_list.forEach(page => {
    if (page == response.pagination.page) {
      html += `
  <li class="pagination__item_cur_page">
    <a href="#book-list-section">${page}</a>
  </li>`;
    } else {
      html += `
  <li class="pagination__item active">
    <a href="javascript:form.submit(${page});">${page}</a>
  </li>`;
    }
  });
  html += `
  <li class="pagination__item disabled">
    &bull;
  </li>
</ul>`;

  let section = document.getElementById(sectionIdPagination);
  section.innerHTML = html;
}

form.renderBookTemplate = renderBookTemplate;
form.renderPaginationTemplate = renderPaginationTemplate;

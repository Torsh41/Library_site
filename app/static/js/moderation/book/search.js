// requires the following scripts in the header
// <script defer src="{{ url_for('static', filename='js/common/lunchbox.js') }}"></script>
// <script defer src="{{ url_for('static', filename='js/common/book_search_form.js') }}"></script>

const formId = "book_search_filters_form";
var form = new BookSearchForm(formId);
const sectionIdBookList = "book-list-section";
const sectionIdPagination = "pagination-section";
const sectionIdStatusForm = "status-form-template";

const statusFormClassName = "status-form";
const statusFormClassNameBookId = "status-form-book-id";
const statusFormClassNameComment = "status-form-comment";
const statusFormClassNameStatus = "status-form-status";


function nodeCopyAttributesTo(src, dst) {
    let attr_list = src.attributes;
    for (let attr of attr_list) {
        dst.setAttribute(attr.name, attr.value);
    }
}

function renderBookTemplate(response) {
    if (response.result != true) {
        return
    }
    html = `
<li><h2>Результаты поиска</h4></li>`;
    response.book_list.forEach(book => {
        date = new Date(book.upload_datetime);
        console.log(date);
        console.log(date.getHours());
        console.log(date.getMinutes());
        upload_datetime = "" + date.getHours() +
            ":" + date.getMinutes() +
            " " + date.getDate() +
            "." + date.getMonth() +
            "." + date.getFullYear();
        html += `
<li class="item__list__container status__lamp__parent" id="book_${book.id}">
  <a class="item__list__header book__btn" id="book_header_${book.id}" href="javascript:lunchboxOpen('book_header_${book.id}', 'book_detail_${book.id}');">
    <div>
      <!-- <img src="/user/${book.name}/edit-profile/edit-avatar" alt="" class="users__img">  -->
      <img class="moderation__book__img" src="/${book.id}/get-cover" alt="">
    </div>
    <div class="item__list__detail">
      <div><b>Книга:</b><span>${book.name}</span></div>
      <div><b>Пользователь:</b><span>${response.current_user.username}</span></div>
      <div><b>Время загрузки:</b><span>${upload_datetime}</span></div>
      <div><b>Статус заявки:</b><span id="item_header_status_${book.id}">${book.moderation_status}</span></div>
      <div><b></b><i>v раскрыть v</i></div>
    </div>
  </a>
  <div class="item__list__detail" id="book_detail_${book.id}", style="display: none;">`;
        if (book.name) {
            html += `<div><b>Название: </b><span>${book.name}</span></div>`;
        }
        if (book.author) {
            html += `<div><b>Автор: </b><span>${book.author}</span></div>`;
        }
        if (book.description) {
            html += `<div><b>Описание: </b><span>${book.description}</span></div>`;
        }
        if (book.reference_url) {
            html += `<div><b>Ссылка: </b><a href="${book.reference_url}">${book.reference_url}</a></div>`;
        }
        if (book.isbn) {
            html += `<div><b>ISBN: </b><span>${book.isbn}</span></div>`;
        }
        if (book.publishing_house) {
            html += `<div><b>Издательство: </b><span>${book.publishing_house}</span></div>`;
        }
        if (book.release_year) {
            html += `<div><b>Год выпуска: </b><span>${book.release_year}</span></div>`;
        }
        if (book.count_of_chapters) {
            html += `<div><b>Количество глав: </b><span>${book.count_of_chapters}</span></div>`;
        }
        if (book.category) {
            html += `<div><b>Категория: </b><span>${book.category}</span></div>`;
        }
        html += `
    <div>
      <b></b><a class="item__button" href="/admin/${response.current_user.username}/change_book_info/${book.id}">Изменить значения</a>
    </div>
  </div>`;
        // Insert status form placeholder
        html += `<form class="${statusFormClassName}-placeholder"
                    data-book-id="${book.id}"
                    data-moderation-status="${book.moderation_status}"
                    data-moderation-comment="${book.moderation_comment}"></form>`;
        html += `
  <div class="status__lamp" id="lamp_${book.id}" style="background-color: gray;"></div>
</li>`;
    });

    if (response.book_list.length == 0) {
      html += `<li><span>Не найдено ни одной книги</span></li>`;
    }

    let section = document.getElementById(sectionIdBookList);
    section.innerHTML = html;
    section.scrollIntoView();

    let statusFormList = document.getElementsByClassName(statusFormClassName + "-placeholder");
    while (statusFormList.length > 0) {
        let form = statusFormList[0];
        const book_id = form.dataset.bookId;
        const moderation_comment = form.dataset.moderationComment;
        const moderation_status = form.dataset.moderationStatus;
        const statusFormTemplate = document.getElementById(sectionIdStatusForm)
                                           .getElementsByTagName("form")[0];
        while(form.attributes.length > 0)
            form.removeAttribute(form.attributes[0].name);

        nodeCopyAttributesTo(statusFormTemplate, form);
        // Copy html elements from the form template
        for (const elemTemplate of statusFormTemplate.children) {
            const elem = document.createElement(elemTemplate.tagName);
            nodeCopyAttributesTo(elemTemplate, elem);
            form.appendChild(elem);
        }
        // Customize form to a corresponding book
        const inputBookId = form.getElementsByClassName(statusFormClassNameBookId)[0];
        inputBookId.value = book_id;
        const inputComment = form.getElementsByClassName(statusFormClassNameComment)[0];
        inputComment.defaultValue = moderation_comment;
        const selectStatusTemplate = statusFormTemplate.getElementsByClassName(statusFormClassNameStatus)[0];
        let selectStatus = form.getElementsByClassName(statusFormClassNameStatus)[0];
        for (const optionTemplate of selectStatusTemplate) {
            let option = document.createElement(optionTemplate.tagName);
            nodeCopyAttributesTo(optionTemplate, option);
            option.text = optionTemplate.text;
            if (option.text == moderation_status) {
                option.defaultSelected = true;
            }
            selectStatus.appendChild(option);
        }
        setStatusLampColor("lamp_" + book_id, moderation_status);
        // Set on submit event
        form.addEventListener("submit", function(event) {
            event.preventDefault();
            fetch(event.target.action, {
                method: event.target.method,
                body: new FormData(event.target)
            }).then(response => {
                if (!response.ok) {
                    throw new Error(`Something wrong with request to '${uri}'. Status code: ${response.status}.`);
                }
                return response.json();
            }).then(data => {
                console.log(data);
                if (data.result == true) {
                    // Update status
                    setStatusLampColor("lamp_" + book_id, data.status_name);
                    const statusSpan = document.getElementById("item_header_status_" + book_id);
                    statusSpan.textContent = data.status_name;
                }
            }).catch(error => {
                console.log(error);
            });
        });
    }
}

function renderPaginationTemplate(response) {
    if (response.result != true) {
        return
    }
    html = `
<ul class="pagination__list list-reset" id="pagination">
  <li class="pagination__item disabled">&bull;</li>`;
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
  <li class="pagination__item disabled">&bull;</li>
</ul>`;

    let section = document.getElementById(sectionIdPagination);
    section.innerHTML = html;
}

form.renderBookTemplate = renderBookTemplate;
form.renderPaginationTemplate = renderPaginationTemplate;
form.submit(1);

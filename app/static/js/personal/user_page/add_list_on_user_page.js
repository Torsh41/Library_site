let beauty_add_list = () => {
    const select = document.querySelector('.js-custom-select');
    const choices = new Choices(select, {
        searchEnabled: false,
        itemSelectText: '',
        classNames: {
            containerOuter: 'defselect',
            containerInner: 'defselect__inner',
            input: 'defselect__input',
            inputCloned: 'defselect__input--cloned',
            list: 'defselect__list',
            listItems: 'defselect__list--multiple',
            listSingle: 'defselect__list--single',
            listDropdown: 'defselect__list--dropdown',
            item: 'defselect__item',
            itemSelectable: 'defselect__item--selectable',
            itemDisabled: 'defselect__item--disabled',
            itemChoice: 'defselect__item--choice',
            placeholder: 'defselect__placeholder',
            group: 'defselect__group',
            groupHeading: 'defselect__heading',
            button: 'defselect__button',
            activeState: 'is-active',
            focusState: 'is-focused',
            openState: 'is-open',
            disabledState: 'is-disabled',
            highlightedState: 'is-highlighted',
            selectedState: 'is-selected',
            flippedState: 'is-flipped',
            loadingState: 'is-loading',
            noResults: 'has-no-results',
            noChoices: 'has-no-defselect'
          }
    });
};


$(function() {

    $('#open_popup_form').on('click', function(event) {
        
        document.getElementById("popupForm").style.display = "block";
    });

    $('#close_popup_form').on('click', function(event)
    {   
        
        document.getElementById("popupForm").style.display = "none";
        
        
    });

    $('#add_list').on('click', function(event) {
        
        if (document.getElementById('add_list_field').value.trim() && document.getElementById('add_list_field').value.trim().length <= 200)
        {
        $.ajax({
            method: 'post',
            url: $("#add_list_form").attr('action'),
            dataType: 'json',
            data: $("#add_list_form").serialize(),
            success: function(response) {
            let cataloges = Array.from(response);
            if (cataloges[0].result == 2)
            {
                $('section').filter(function() {
                return this.id.match(/cataloge_info/);
                }).remove();
                let html = '';
                cataloges.forEach(cataloge => {
                        html += `<section class="list" id="${cataloge.id}cataloge_info">
                                    <div class="container list__container">
                                        <div class="list__wrap">
                                            <h2 class="list__title title">${cataloge.name}</h2>
                                            <!--Название списка, которое ввел пользователь-->
            
                        <ul class="list__books list-reset" id="${cataloge.id}books_info_container">
                            <!--Добавление книги в список - перебрасывает в рааздел категорий книг-->
                            <li class="list__book list__add">
                                <a href="/categories?list_id=${cataloge.id}" class="list__link">
                                    <div class="list__block-add">
                                        <svg class="list__svg2" width="78" height="78" viewBox="0 0 78 78" fill="none" xmlns="http://www.w3.org/2000/svg">
                                            <g clip-path="url(#clip0_139_2)">
                                                <rect x="35" width="8" height="78" fill="#cec8bd" />
                                                <rect x="78" y="35" width="8" height="78" transform="rotate(90 78 35)" fill="#cec8bd" />
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
                            let items = Array.from(cataloge.items);
                            if (items.length != 0)
                            {
                                items.forEach(item => {
                                html += `<li class="list__book" id="${cataloge.id}book_info">
                                            <a href="/book-page/${item.id}" class="list__book-set">
                                                <img class="list__book-set" src="/${item.id}/get-cover" alt="">
                                            </a>
                                            
                                            <div class="list__book-wrap">
                                                <a href="/book-page/${item.id}" class="list__link-book"><u>Книга:</u> ${item.name}</a>
                                                <select name="read_state" class="book__select js-custom-select" id="${cataloge.id}${item.id}state" data-itemid="${item.id}">`;
                                                if (item.read_state == "Планирую")
                                                    html += `<option class="book__state book__plan" value="Планирую" selected>Планирую</option>  
                                                            <option class="book__state book__read" value="Читаю">Читаю</option>
                                                            <option class="book__state book__fuck" value="Заброшено">Заброшено</option>
                                                            <option class="book__state book__done" value="Прочитано">Прочитано</option>`;
                                                else if (item.read_state == "Читаю")
                                                    html += `<option class="book__state book__plan" value="Планирую">Палнирую</option>
                                                            <option class="book__state book__read" value="Читаю" selected>Читаю</option>
                                                            <option class="book__state book__fuck" value="Заброшено">Заброшено</option>
                                                            <option class="book__state book__done" value="Прочитано">Прочитано</option>`;
                                                else if (item.read_state == "Заброшено")
                                                    html += `<option class="book__state book__plan" value="Планирую">Планирую</option>
                                                            <option class="book__state book__read" value="Читаю">Читаю</option>
                                                            <option class="book__state book__fuck" value="Заброшено" selected>Заброшено</option>
                                                            <option class="book__state book__done" value="Прочитано">Прочитано</option>`;
                                                else if (item.read_state == "Прочитано")
                                                    html += `<option class="book__state book__plan" value="Планирую">Планирую</option>
                                                            <option class="book__state book__read" value="Читаю">Читаю</option>
                                                            <option class="book__state book__fuck" value="Заброшено">Заброшено</option>
                                                            <option class="book__state book__done" value="Прочитано" selected>Прочитано</option>`;
                                                html += `</select>`;
                                                html += `<a class="list__book-delete-btn" data-url='/user/${cataloge.username}/delete-item/${cataloge.id}/${item.id}/${1}' id='${cataloge.id}del_book'>Удалить книгу из списка</a>
                                            </div>
                                        </li>`;
                                });
                            }
                        html += `</ul>`;
                            
                        // собираем пагинацию книг каждого списка
                        html += `<div class="list__pagination pagination" id="${cataloge.id}books_pagination_container">
                                    <ul class="pagination__list list-reset" id="${cataloge.id}books_pagination">
                                        <li class="pagination__item disabled">&bull;</li>`;
                        if (items.length != 0)
                        {
                            items[0].pages_count.forEach(p => {
                                if (p)
                                {
                                    if (p == 1)
                                    {
                                        html += `<li class="pagination__item_cur_page">
                                                    <a data-url='/user/${cataloge.username}/get_books_page/${cataloge.id}/${p}' id='${cataloge.id}books_page'>${p}</a>
                                                </li>`;
                                    }
                                    else
                                    {
                                        html += `<li class="pagination__item active">
                                                    <a data-url='/user/${cataloge.username}/get_books_page/${cataloge.id}/${p}' id='${cataloge.id}books_page'>${p}</a>
                                                </li>`;
                                    }
                                }
                                else
                                {
                                    html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`;
                                }
                            });
                        }
                    
                        html += `<li class="pagination__item disabled">&bull;</li></ul></div>`;    
                        html += `<div class="list__end">
                                    <a class="list__delete-btn" id='${cataloge.id}del_list' data-url='/user/${cataloge.username}/delete-list/${cataloge.id}/${cataloge.last_page}'>
                                        Удалить список
                                    </a></div></div></div></section>`;
                });
                let div = document.getElementById('lists_container');
                div.insertAdjacentHTML('afterbegin', html);

                // собираем пагинацию для списков
                $('#pagination').remove();
                html = `<ul class="pagination__list list-reset" id="pagination">
                            <li class="pagination__item disabled">&bull;</li>`;

                cataloges[0].pages_count.forEach(p => {
                    if (p)
                    {
                        if (p == cataloges[0].last_page)
                        {
                            html += `<li class="pagination__item_cur_page">
                                        <a data-url='/user/${cataloges[0].username}/get_lists_page/${p}'>${p}</a>
                                    </li>`;
                        }
                        else
                        {
                            html += `<li class="pagination__item active">
                                        <a data-url='/user/${cataloges[0].username}/get_lists_page/${p}'>${p}</a>
                                    </li>`;
                        }
                    }
                    else
                    {
                        html += `<li class="pagination__item disabled"><a href="#">&hellip;</a></li>`;
                    }
                });

                html += `<li class="pagination__item disabled">&bull;</li></ul>`;
                div = document.getElementById('pagination_container');
                div.insertAdjacentHTML('afterbegin', html);

                section = document.getElementById(cataloges[cataloges.length - 1].id + 'cataloge_info');
                section.scrollIntoView(); // Прокрутка до верхней границы
                document.getElementById('add_list_field').value = '';
                document.getElementById('popupForm').style.display = "none";
                beauty_add_list();
            }
            else if (cataloges[0].result == 1)
            {
                alert('У вас уже есть список с таким названием');
                document.getElementById('add_list_field').value = '';
            }
            else 
            {
                alert('Различных списков может быть не больше 6');
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
        else if (document.getElementById('add_list_field').value.trim().length > 200)
        {
        alert('Слишком длинное название списка');
        }
        else
        {
        alert('Заполните поле');
        document.getElementById('add_list_field').value = '';
        }
        
    });
})   

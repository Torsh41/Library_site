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
            cataloges = Array.from(response);
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
                            items = Array.from(cataloge.items);
                            if (items.length != 0)
                            {
                                items.forEach(item => {
                                html += `<li class="list__book" id="${cataloge.id}book_info">
                                            <a href="/book-page/${item.name}" class="list__book-set">
                                                <img class="list__book-set" src="/${item.name}/get-cover" alt="">
                                            </a>
                                            
                                            <div class="list__book-wrap">
                                                <a href="/book-page/${item.name}" class="list__link-book"><u>Книга:</u> ${item.name}</a>
                                                <a href="/book-page/${item.name}" class="list__link-plan"><u>Состояние чтения:</u> ${item.read_state}</a>
                                                <a class="list__book-delete-btn" data-url='/user/${cataloge.username}/delete-item/${cataloge.id}/${item.id}/${1}' id='${cataloge.id}del_book'>Удалить книгу из списка</a>
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
                                for (let i = 1; i <= items[0].items_pages; i++)
                                {
                                    if (items[0].items_pages > 1 && i == 1)
                                    {
                                        html += `<li class="pagination__item_cur_page">
                                                    <a data-url='/user/${cataloge.username}/get_books_page/${cataloge.id}/${i}' id='${cataloge.id}books_page'>${i}</a>
                                                </li>`;
                                    }
                                    else
                                    {
                                        html += `<li class="pagination__item active">
                                                    <a data-url='/user/${cataloge.username}/get_books_page/${cataloge.id}/${i}' id='${cataloge.id}books_page'>${i}</a>
                                                </li>`;
                                    }
                                }
                            }
                            
                            html += `<li class="pagination__item disabled">&bull;</li></ul></div>`;    
                            // 

                            html += `<div class="list__end">
                                        <a class="list__delete-btn" id='${cataloge.id}del_list' data-url='/user/${cataloge.username}/delete-list/${cataloge.id}/${cataloge.pages}'>
                                            Удалить список
                                        </a></div></div></div></section>`;
                    });
                document.getElementById('lists_container').innerHTML = html;
                // собираем пагинацию для списков
                $('ul').filter(function() {
                return this.id.match('pagination');
                }).remove();
                html = `<ul class="pagination__list list-reset" id="pagination">
                            <li class="pagination__item disabled">&bull;</li>`;
                try
                {
                    for (let i = 1; i <= cataloges[0].pages; i++)
                    {
                        if (cataloges[0].pages > 1 && i == cataloges[0].pages)
                        {
                            html += `<li class="pagination__item_cur_page">
                                        <a data-url='/user/${cataloges[0].username}/get_lists_page/${i}'>${i}</a>
                                    </li>`;
                        }
                        else
                        {
                            html += `<li class="pagination__item active">
                                        <a data-url='/user/${cataloges[0].username}/get_lists_page/${i}'>${i}</a>
                                    </li>`;
                        }
                    }
                }
                catch {}
                html += `<li class="pagination__item disabled">&bull;</li></ul>`;
                document.getElementById('pagination_container').innerHTML = html;

                section = document.getElementById(cataloges[cataloges.length - 1].id + 'cataloge_info');
                section.scrollIntoView(); // Прокрутка до верхней границы
                document.getElementById('add_list_field').value = '';
                document.getElementById('popupForm').style.display = "none";
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

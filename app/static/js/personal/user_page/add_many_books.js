$(function() {
    $('#add_many_books_form').submit(function(event) {
        event.preventDefault();
    });

    $('#add_info').on('click', function(event) {
        $('#add_many_books_sec').css('display', 'block');
        $('#sel_file').val("");
    });
    
    $('#close_form').on('click', function(event) {
        $('#add_many_books_sec').css('display', 'none');
        $('#sel_file').val("");
    });

    $('#many_books_info').on('click', function(event) {
        let f = new FormData(document.getElementById('add_many_books_form'));
        $.ajax({
            method: 'post',
            url: '/user/add-books',
            dataType: 'json',
            contentType: false,
			processData: false,
            data: f,
            success: function(response) {
            
                if (response.result)
                {
                    alert(`Добавлено ${response.count} книг`);
                    $('#sel_file').val("");
                    document.getElementById("add_many_books_sec").style.display = "none";
                }
                else
                {
                    alert('Проверьте файл на соответствие шаблону!');
                    $('#sel_file').val("");
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
    });
});
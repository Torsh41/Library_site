function create_private_chat()
{
    if (document.getElementById('name_field').value.trim())
    {
        $.ajax({
            method: 'post',
            url: `/forum/create_private_chat`,
            dataType: 'json',
            data: $('#new_private_chat_form').serialize(),
            success: function(response) {
                if (response.result === 2)
                {
                    alert('Чат успешно создан!');
                    $('#add_info_sec').css('display', 'none');
                    $('#name_field').val("");
                }
                else if (response.result === 1)
                {
                    alert('Вы уже создавали чат с такой темой!');
                    $('#name_field').val("");
                }
                else
                {
                    alert('Можно создавать не более 10 приватных чатов для одного человека!');
                    $('#name_field').val("");
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
    else
    {
        alert('Поле не должно быть пустым!');
        $('#name_field').val("");
    }
}


$(function() {
    $('#add_private_chat').on('click', function(event) {
        $('#add_info_sec').css('display', 'block');
        $('#name_field').val("");
    });
    
    $('#close_form').on('click', function(event) {
        $('#add_info_sec').css('display', 'none');
        $('#name_field').val("");
    });

    $('#new_private_chat_form').submit(function(event) {
        create_private_chat();
        event.preventDefault();
    });

    $('#new_private_chat_but').on('click', function(event) {
        create_private_chat();
    });
});
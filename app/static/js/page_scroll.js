function scroll(button_id) 
{
    if(localStorage.getItem('scroll'))  
    {
        var body = document.body, html = document.documentElement;
        var height = Math.max(body.scrollHeight, body.offsetHeight, body.clientHeight, html.clientHeight, html.offsetHeight, html.scrollHeight);
        if (height > parseInt(localStorage.getItem('page_height')) || height < parseInt(localStorage.getItem('page_height')))
        {
            window.scrollTo(0, height);
        }
        else 
        {
            window.scrollTo(0, parseInt(localStorage.getItem('scroll')));
        }
        window.localStorage.clear();
    }

    $(`#${button_id}`).on('click', function()
    {
        localStorage.setItem('scroll', window.pageYOffset);
        var html = document.documentElement;
        var body = document.body;
        localStorage.setItem('page_height', Math.max(body.scrollHeight, body.offsetHeight, body.clientHeight, html.clientHeight, html.scrollHeight, html.offsetHeight));
    });
}
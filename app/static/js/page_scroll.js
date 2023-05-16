function scroll(button_id) 
{
    if(localStorage.getItem('scroll'))  
    {
        window.scrollTo(0, parseInt(localStorage.getItem("scroll")));
        window.localStorage.clear();
    }

    $(`#${button_id}`).on("click", function()
    {
        localStorage.setItem("scroll", window.pageYOffset);
    });
}
function edit_elem_state(id)
{
    if (document.getElementById(id).style.display == "block")
    {
        document.getElementById(id).style.display = "none";
    }
    else
    {
        document.getElementById(id).style.display = "block";
    }
}


function form_activate(form_id, title_id, data)
{
    edit_elem_state(form_id);
    if (document.getElementById(id).style.display == "block")
        document.getElementById(title_id).value += ` ${data}`;
}
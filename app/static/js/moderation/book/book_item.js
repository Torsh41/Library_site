function setStatusSelectedValue(selectId, moderation_status) {
    const selector = document.getElementById(selectId);
    for (const option of selector) {
        if (option.value == moderation_status) {
            option.defaultSelected = true;
        }
    }
}

function setStatusOnSubmit(formId) {
    const uri = "/moderation/book/set_moderation_status";
    const form = document.getElementById(formId);
    console.log(form);
    form.addEventListener("submit", e => {
        e.preventDefault();
        fetch(uri, {
            method: 'post',
            body: new FormData(e.target)
        }).then(response => {
            console.log(response);
            if (response.ok) {
            }
            return response.json;
        }).then(data => {
              console.log(data);
              // Handle response here.
          });
    });
}

function bookItemDetailOpen(itemId) {
    document.getElementById("book_header_" + itemId).href = "javascript:bookItemDetailClose('" + itemId + "');";
    document.getElementById("book_detail_" + itemId).style.display = "block";
}

function bookItemDetailClose(itemId) {
    document.getElementById("book_header_" + itemId).href = "javascript:bookItemDetailOpen('" + itemId + "');";
    document.getElementById("book_detail_" + itemId).style.display = "none";
}

$('#search_users_form').submit(function(event) {
    search_users_on_forum();
    event.preventDefault();
});

$('#get_users').click(function(event) {
    search_users_on_forum();
});

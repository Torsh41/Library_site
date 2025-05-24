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

$("#item_pagination_container").off();
$("#item_pagination_container").on("click", function(event) {
    let target = event.target;
    // check if an <a> tag was clicked
    if (target.tagName === 'A' && target.id.includes("item_p")) {
        var filters_form = document.getElementById("book_search_filters_form");
        // get url for the next page, and replace form.action with it
        filters_form.action = target.dataset?.url;
        filters_form.submit();
        console.log("Hallelujah");
    }
});

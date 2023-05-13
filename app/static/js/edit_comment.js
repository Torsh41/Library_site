function edit(text, id){
    document.getElementById(id).style.display = "block";
    document.getElementById(id + "field").value = text;
    }
function closeEditCommentForm(id){
    document.getElementById(id).style.display = "none";
    }
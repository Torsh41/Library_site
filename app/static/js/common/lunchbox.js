function lunchboxOpen(anchorId, lunchboxId) {
    document.getElementById(lunchboxId).style.display = "block";
    document.getElementById(anchorId).href =
        "javascript:lunchboxClose('" + anchorId + "', '" + lunchboxId + "');";
}

function lunchboxClose(anchorId, lunchboxId) {
    document.getElementById(lunchboxId).style.display = "none";
    document.getElementById(anchorId).href =
        "javascript:lunchboxOpen('" + anchorId + "', '" + lunchboxId + "');";
}

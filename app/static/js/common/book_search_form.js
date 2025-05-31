// HOW-TO
// 1) Redefine renderBookTemplate and renderPaginationTemplate methods.
//   The reponse is whatever a request to form.action returns.
//   Iterate over elements in response and generate html section.
//   Insert the section into the document
// 2) When doing pagination, make an anchor call form.submit(page_number)
//
// Example is available in `app/static/js/main/book/search/search.js`,
// and in `app/templates/

class BookSearchForm {
    constructor(formId) {
        this.formId = formId;
        this.formOnSubmit();
    }

    // Redefine these two methods for each class instance
    renderBookTemplate(response) { }
    renderPaginationTemplate(response) { }

    formOnSubmit() {
        $('#' + this.formId).submit((function(event) {
            event.preventDefault();
            this.submit(1);
        }).bind(this));
    }

    submit(page) {
        let form = document.getElementById(this.formId);
        form.scrollIntoView();
        $.ajax({
            method: form.method,
            url: form.action,
            dataType: 'json',
            data: $('#' + this.formId).serialize() + "&page=" + page,
            success: (function(response) {
                this.renderBookTemplate(response);
                this.renderPaginationTemplate(response);
            }).bind(this),
            error: function(jqXHR, exception) {
                console.log("ERROR");
                console.log(exception);
            }
        });
    }
}

$(function() {
    $('#lists_container').on('change', function(event){
        let target = event.target;
        if (target.tagName === 'SELECT' && target.id.includes('state'))
        {
            let state_name = target.options[target.selectedIndex].text;
            let item_id = target.dataset.itemid;
            $.ajax({
                method: 'post',
                url: '/user/change_read_state/',
                dataType: 'json',
                data: {read_state: state_name,
                       item_id: item_id},
                success: function(response) {
                    if (response.read_state)
                    {
                        $(target).val(response.read_state);
                    }
                    else
                    {
                        console.log(response);
                    }
                },
                error: function(jqXHR, exception) {
                console.log(exception);
                }
            });
        }
    });
});
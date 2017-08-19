 (function () {
 	window.item_list = {{item_list|safe}};
 })();
 $("#tags").autocomplete({
 	source: window.item_list
 })(django.jQuery);

/* (function($) {
    $(document).on('formset:added', function(event, $row, formsetName) {
        if (formsetName == 'author_set') {
            // Do something
        }
    });

    $(document).on('formset:removed', function(event, $row, formsetName) {
        // Row removed
    });
})(django.jQuery);*/
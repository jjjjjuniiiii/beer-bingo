(function($){   
    $(function(){
        $(document).ready(function() {
            $('#id_questionsSet').bind('change', question_set_change);            
            $('#id_question > option').show();
            if ($('#id_questionsSet').val() != '') {
                var question_set_id = $('#id_questionsSet').val();
                $.ajax({
                    "type"      : "GET",
                    "url"         : "/product_change/?question_set_id="+question_set_id,
                    "dataType"  : "json",
                    "cache"       : false,
                    "success"   : function(json) {
                        $('#id_question >option').remove();
                        for(var j = 0; j < json.length; j++){
                            $('#id_question').append($('<option></option>').val(json[j][0]).html(json[j][1]));
                        }
                    }           
                });
            }
        });
    });  
})(django.jQuery);

// based on the questionsSet, questions will be loaded

var $ = django.jQuery.noConflict();

function question_set_change()
{
    var question_set_id = $('#id_questionsSet').val();
    $.ajax({
        "type"      : "GET",
        "url"         : "/product_change/?question_set_id="+question_set_id,
        "dataType"  : "json",
        "cache"       : false,
        "success"   : function(json) {
            $('#id_question > option').remove();
            for(var j = 0; j < json.length; j++){
                $('#id_question').append($('<option></option>').val(json[j][0]).html(json[j][1]));
            }
        }           
    })(jQuery);
}
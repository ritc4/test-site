$(document).ready(function(){
    $("#form_ajax").find('#id_username').on("blur",function(e){
    e.preventDefault();
    csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
//    console.log($(this).serialize());
        $.ajax({
            url: '/register/',
            type: 'post',
            data: {
            'username': $('#id_username').val(),
            'csrfmiddlewaretoken': csrfToken
        },
            dataType: 'json',

            success: function(response){
                $('.alert').removeAttr('style');
                if (response.text_resp){
                    $('#error_login').addClass('alert-danger').text(response.text_resp);
                    $('#btn').attr('disabled','disabled');
                    console.log(response);
                }

                else if (response.text_resp_error){
                    $('#error_login').removeClass('alert-danger').addClass('alert-success').text(response.text_resp_error);
                    $('#btn').removeAttr('disabled');
                    console.log(response);
                }

                else if (response.text_resp_error_text){
                     $('#error_login').addClass('alert-danger').text(response.text_resp_error_text);
                     console.log(response);
                }
            },
            error: function(response){
                $('#id_username_helptext').append(response.text_resp);
            }
        });
    });
});
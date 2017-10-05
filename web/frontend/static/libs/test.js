$(document).ready(function(e){
    $('#id_name').keyup(function() {
        if ($('#id_name').val() != "") {
            $('#wait_for_upload').hide();
            $('#upload_form_group').fadeIn();
        } else {
            $('#upload_form_group').fadeOut(function() {
                $('#wait_for_upload').show();
            });
        }
    });
});

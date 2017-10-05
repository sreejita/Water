$(document).ready(function(e){
    $('#id_name').keyup(function() {
        if ($('#id_name').val() != "") {
            $('#wait_for_upload').hide();
            $('#upload_form_group').fadeIn();
            $('#upload_btn').fadeIn();
        } else {
            $('#upload_form_group').fadeOut(function() {
                $('#wait_for_upload').show();
            });
        }
    });

    var text = "Process started";

    $(':checkbox').checkboxpicker();
    $("a.my-tool-tip").tooltip();
    $('input[type="file"]').change(function () {
        $('#up-step').removeClass('disabled');
        if ($(this).val() != "") {
            var file = document.getElementById('id_docfile').files[0];
            console.log(file.name);
            if (file) {
                var fileSize = 0;
                if (file.size > 1024 * 1024)
                    fileSize = (Math.round(file.size * 100 / (1024 * 1024)) / 100).toString() + ' MB';
                else
                    fileSize = (Math.round(file.size * 100 / 1024) / 100).toString() + ' KB';

                document.getElementById('fileName').innerHTML = 'Name: ' + file.name;
                document.getElementById('fileSize').innerHTML = 'Size: ' + fileSize;
                document.getElementById('fileType').innerHTML = 'Type: ' + file.type;
            }
        } else {
            $('#label_upload').html("No file Choosen");
        }
    });

    $('#id_docfile').fileupload({
        url: '/frontend/upload_data/',
        dataType: 'json',
        add: function(e, data){
            $("#up-step").off('click').on('click', function () {
                $('#progress').fadeIn();
                data.submit();
            });
        },
        done: function (e, data) {
            text = "Uploading done!";
            $('#upload_message').html(text);
            $('#profiling').fadeIn();
            $('#profile_msg').fadeIn();
            var wf_id = data._response.result['wf_id'];
            var user = data._response.result['user'];
            sessionStorage.setItem('user', JSON.stringify(user));
            sessionStorage.setItem('wf_id', JSON.stringify(wf_id));
            var timer = setInterval(myFunction, 10000);
            function myFunction() {
                var temp_user = sessionStorage.getItem('user');
                var user_id = $.parseJSON(temp_user);
                var temp_wf_id = sessionStorage.getItem('wf_id');
                var wfid = $.parseJSON(temp_wf_id);
                $.ajax({
                    type: 'GET',
                    url: '/get_profile_status/',
                    dataType: 'json',
                    data: "wf_id=" + wfid + "&user=" + user_id,
                    success: function (e, data) {
                        console.log(data);
                        console.log(e['task_status']);
                        var task_status = e['task_status'];
                        if (task_status === "COMPLETED") {
                            clearInterval(timer);
                            $("#profile_message").html("Profiling completed.");
                            $("#profile_btn").fadeIn();
                            $('#profile_msg').hide();
                            $('#get_confirm_msg').fadeIn();
                            $('#accept-step').removeClass('disabled');
                            $('#cancel-step').removeClass('disabled');
                        }

                    }
                })
            }
        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('.progress-bar').css(
                'width',
                progress + '%'
            );
        },
        fail: function (e, data) {
            var message;
            if (typeof data.message !== 'undefined'){
                message  = 'Error - upload failed.';
            }
            else {
                message  = data.jqXHR.responseJSON.message;
            }
            var error = "<div class='alert alert-danger'><p>We encountered an error while uploading: <br /><strong>" + message + "</strong></p>";
            error += "<p>Please <a href='mailto:uwcloudmatcher@gmail.com'>contact us</a> if this error persists.</p>";
            error += "</div>";
            $('#upload_message').html(error);
            $('.progress').fadeOut();
        }
    });

});

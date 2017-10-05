$(document).ready(function () {
    $('#load').before(function(event) {

        // event.preventDefault();

        var formData = new FormData($('#load')[0]);

        $.ajax({
            xhr : function() {
                var xhr = new window.XMLHttpRequest();

                xhr.upload.addEventListener('progress', function(e) {

                    if (e.lengthComputable) {
                        var percent = Math.round((e.loaded / e.total) * 100);

                        $('#progressBar').attr('aria-valuenow', percent).css('width', percent + '%').text(percent + '%');
                    }

                });

                return xhr;
            },
            type : 'POST',
            // url  : '/frontend/job/1/upload1',
            data : formData,
            processData : false,
            contentType : false,
        });
    });
});
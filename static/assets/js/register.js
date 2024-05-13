$(document).ready(function() {
    $('#registration-form').submit(function(e) {
        e.preventDefault(); 

        var formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: formData,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function(response) {
                alert(response.message);
                window.location.href = response.redirect_url;
            },
            error: function(xhr) {
                $('.form-control').removeClass('is-invalid');
                $('.error-message').remove();

                var errors = xhr.responseJSON.errors;
                $.each(errors, function(field, message) {
                    if (field === 'password1' || field === 'password2') {
                        var input = $('#id_' + field); 
                        input.addClass('is-invalid').after('<div class="error-message text-error-2">' + message + '</div>');
                    } else {
                        var input = $('[name=' + field + ']');
                        input.addClass('is-invalid').after('<div class="error-message text-error-2">' + message + '</div>');
                    }
                });
            }
        });
    });
});

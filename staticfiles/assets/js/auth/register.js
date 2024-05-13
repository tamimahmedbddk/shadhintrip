$(document).ready(function() {


    // Submit registration form via AJAX
    $('#registration-form').submit(function(e) {
        e.preventDefault(); // Prevent the default form submission

        var formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'), // The URL to submit the data
            data: formData,
            processData: false, // Needed for FormData
            contentType: false, // Needed for FormData
            dataType: 'json', // Expect JSON response
            success: function(response) {
                alert(response.message); // Show an alert to the user
                window.location.href = response.redirect_url; // Then redirect
            },
            error: function(xhr) {
                // Clear previous errors
                $('.form-control').removeClass('is-invalid');
                $('.error-message').remove();

                // Handle and display errors
                var errors = xhr.responseJSON.errors;
                $.each(errors, function(field, message) {
                    // Special handling for password fields
                    if (field === 'password1' || field === 'password2') {
                        var input = $('#id_' + field); // Use the actual ID of the input
                        input.addClass('is-invalid').after('<div class="error-message text-danger">' + message + '</div>');
                    }
                    else {
                        // For non-captcha fields, append error after input
                        var input = $('[name=' + field + ']');
                        input.addClass('is-invalid').after('<div class="error-message text-danger">' + message + '</div>');
                    }
                });
            }
        });
    });
});

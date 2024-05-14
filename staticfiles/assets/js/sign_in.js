$(document).ready(function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('#login-form').on('submit', function(e) {
        e.preventDefault();
        var formData = $(this).serialize();
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: formData,
            dataType: 'json',
            success: function(response) {
                if (response.success) {
                    window.location.href = response.redirect_url;
                } else {
                    $(".form-check").html('<p class="text-error-2">' + response.error + '</p>');
                }
            },
            error: function(xhr, status, error) {
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    $('.form-check').html('<p class="text-error-2">' + xhr.responseJSON.error + '</p>');
                } else {
                    $('.form-check').html('<p class="text-error-2">An error occurred. Please try again.</p>');
                }
            }
        });
    });
});

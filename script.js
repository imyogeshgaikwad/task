$(document).ready(function() {
    // Load tasks
    loadTasks();

    // Registration form submission
    $('#registerForm').submit(function(event) {
        event.preventDefault();
        var regData = {
            'username': $('#reg_username').val(),
            'password': $('#reg_password').val()
        };
        $.ajax({
            type: 'POST',
            url: '/api/register',
            contentType: 'application/json',
            data: JSON.stringify(regData),
            success: function(response) {
                alert(response.msg);
                $('#reg_username').val('');
                $('#reg_password').val('');
            },
            error: function(error) {
                alert('Error: ' + error.responseJSON.error);
            }
        });
    });

    // Login form submission
    $('#loginForm').submit(function(event) {
        event.preventDefault();
        var loginData = {
            'username': $('#login_username').val(),
            'password': $('#login_password').val()
        };
        $.ajax({
            type: 'POST',
            url: '/api/login',
            contentType: 'application/json',
            data: JSON.stringify(loginData),
            success: function(response) {
                localStorage.setItem('token', response.access_token);
                alert('Login successful');
                $('#login_username').val('');
                $('#login_password').val('');
                loadTasks();
            },
            error: function(error) {
                alert('Error: ' + error.responseJSON.error);
            }
        });
    });

    // Handle task form submission
    $('#taskForm').submit(function(event) {
        event.preventDefault();
        var formData = {
            'name': $('#name').val(),
            'status': $('#status').val()
        };
        $.ajax({
            type: 'POST',
            url: '/api/tasks',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            headers: {
                Authorization: 'Bearer ' + localStorage.getItem('token')
            },
            success: function(response) {
                $('#taskList').append('<p>ID: ' + response.id + ', Name: ' + response.name + ', Status: ' + response.status + '</p>');
                $('#name').val('');
                $('#status').val('');
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    });
});

function loadTasks() {
    $.get('/api/tasks', function(data) {
        $('#taskList').empty();
        data.forEach(function(task) {
            $('#taskList').append('<p>ID: ' + task.id + ', Name: ' + task.name + ', Status: ' + task.status + '</p>');
        });
    });
}

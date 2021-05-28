
$('form.reg_user').submit(function () {
    console.log('Попытка пошла')
    fetch('/auth/registration', {
        method: "POST",
        body: JSON.stringify({
            login: $('#login_reg').val(),
            password: $('#password_reg').val(),
            name: $('#first_name_reg').val(),
            surname: $('#last_name_reg').val(),
            email: $('#email_reg').val()
        })
    }).then(function (response) {
        return(response.json())
    }).then(function (data) {
        if(data.success){
            alert('Регистрация прошла успешно!')
            window.location.href = '/'
        }else{
            alert(data.error)
        }
    })
})
$('form.auth_user').submit(function () {
    console.log('Попытка пошла')
    fetch('/auth/login', {
        method: "POST",
        body: JSON.stringify({
            login: $('#login').val(),
            password: $('#password').val(),
        })
    }).then(function (response) {
        return(response.json())
    }).then(function (data) {
        if(data.success){
            alert('Авторизация прошла успешно!')
            window.location.href = '/'
        }else{
            alert(data.error)
        }
    })
})
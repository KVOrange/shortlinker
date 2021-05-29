
function eraseCookie(name) {   
    document.cookie = name+'=; Max-Age=-99999999;';  
}
$('form.reg_user').submit(function () {
    eraseCookie('JWT')
    fetch('/api/auth/registration', {
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
            document.cookie = "JWT=Bearer "+data.token+"; path=/;"
            window.location.href = '/'
        }else{
            alert(data.error)
        }
    })
})
$('form.auth_user').submit(function () {
    eraseCookie('JWT')
    fetch('/api/auth/login', {
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
            document.cookie = "JWT=Bearer "+data.token+"; path=/;"
            window.location.href = '/'
        }else{
            alert(data.error)
        }
    })
})
$('.exit').on('click',function(){
    console.log('Выход')
    eraseCookie('JWT')
    window.location.href='/'
})
function getCookie(name) {
  var nameEQ = name + "=";
  var ca = document.cookie.split(';');
  for(var i=0;i < ca.length;i++) {
      var c = ca[i];
      while (c.charAt(0)==' ') c = c.substring(1,c.length);
      if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
  }
  return null;
}
$('form.linkcut').submit(function () {
  let result = $('.link_container').val()
  if(!result){
    $('.linkresult').append(
      `<div class="link_result_error">Невозможно преобразовать пустую строку!</div>`)
    $('.link_result_error').fadeIn();
  }
  else{
    fetch('/api/link/add', {
      method: "POST",
      headers: new Headers({
        'Authorization': getCookie('JWT')
      }), 
      body: JSON.stringify({
        url: result,
        name: $('#short_name').val(),
        type: $("input[name='group1']:checked").val(),
        description: $('#description').val()
      })
    }).then(function (response) {
      return response.json()
    }).then(function (data) {
      if (data.success) {
        console.log(window.location.protocol+'//'+window.location.host)
        $('.linkresult').append(
          `
                  <div class="white-text row link_resulter"
                  ><div class='col s6 truncate'>
                  <a href="/l/link/`+data.link_name+`">`+window.location.protocol+'//'+window.location.host+`/l/`+data.link_name+`</a>
                  </div>
                  <div class='col s4' style='display:flex; padding: 0 !important; justify-content: space-between;'>
                    <span class='truncate' style="color:#057baa;">`+ $('.link_container').val() + `</span>
                  </div>
                  <a class="waves-effect waves-light btn copy_btn">Копировать</a>
                  </div>
                  `)
        $('.link_resulter').fadeIn();
      } else {
        $('.linkresult').append(
          `
                <div class="link_result_error">Невозможно сократить эту ссылку. `+data.error+`!</div>
                `)
        $('.link_result_error').fadeIn();
      }
      console.log(data)
    })
  }
  

})
$('.open-lk').on('click', function () {
  console.log(getCookie('JWT'))
  if(getCookie('JWT')){
    window.location.href = '/lk'
  }else{
    $('.background-slide').toggle();
    $('.container-lk').animate({ width: 'toggle' }, 350);
    $('.container-lk').css('display', 'flex')
  }
  $('.background-slide').on('click', function () {
    $('.background-slide').toggle();
    $('.container-lk').animate({ width: 'toggle' }, 350);
  }
  )
  
  
  // $('.background-slide').toggle();animate({width:'toggle'}, 350);
})

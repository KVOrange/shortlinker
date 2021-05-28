$('form.linkcut').submit(function () {
  let result = $('.link_container').val()
  if(!result){
    $('.linkresult').append(
      `<div class="link_result_error">Невозможно преобразовать пустую строку!</div>`)
    $('.link_result_error').fadeIn();
  }
  else{
    fetch('/l/link/default_create', {
      method: "POST",
      body: JSON.stringify({
        url: result
      })
    }).then(function (response) {
      return response.json()
    }).then(function (data) {
      if (data.success) {
        $('.linkresult').append(
          `
                  <div class="white-text row link_resulter"
                  ><div class='col s6 truncate'>
                  `+ data.link + `
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
  $('.background-slide').toggle();
  $('.container-lk').animate({ width: 'toggle' }, 350);
  $('.container-lk').css('display', 'flex')
})
$('.background-slide').on('click', function () {
  $('.background-slide').toggle();
  $('.container-lk').animate({ width: 'toggle' }, 350);
  // $('.background-slide').toggle();animate({width:'toggle'}, 350);
})

let chart = 'NaN';
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
draw_history = function (link_chart, label, today_noize_history) {
    // if(chart != 'NaN'){
    //     chart.destroy();
    // }
    chart = new Chart(link_chart, {
        type: 'line',
        data: {
            labels: label,
            datasets: [
                {
                    label: "Посещение",
                    backgroundColor: 'rgba(255, 99, 132, 0.7)',
                    borderColor: 'rgb(255,99,132)',
                    data: today_noize_history,
                    type: 'line',
                },
            ]
        },
        options: {
            scales: {
                yAxes: [{
                    stacked: true
                }]
            }
        }
    });
    
}
var counter = 0
$('.open_info').on('click', function () {
    let temp_id = 'chart_'+$(this).attr('id')
    var ctx = document.getElementById(temp_id).getContext('2d'); // 2d context
    $(this)
        .parent()
        .parent()
        .parent()
        .children('.link_fullinfo').slideToggle()
    
   
})
$('.history_info').on('click', function(){
    temp_link_name = $(this).attr('id')
    fetch('/api/link/info/statistic', {
        method: "POST",
        headers: new Headers({
            'Authorization': getCookie('JWT')
        }),
        body: JSON.stringify({
            name: temp_link_name,
            datetime_start: $(this).parent().children('span').children('.datestart').val()+'T00:00:00',
            datetime_end: $(this).parent().children('span').children('.dateend').val()+'T00:00:00'
        }) 
    }).then(function(response){
        return response.json()
    }).then(function(data){
        if(data.success){
            let temp_id = 'chart_'+temp_link_name

            var ctx = document.getElementById(temp_id).getContext('2d'); // 2d context
            let labels = []
            let today_noize_history = []
            let history = data.info;
            for (let i = 0; i < history.length; i++){
                labels.push(history[i]['date']);
                today_noize_history.push(history[i]['count']);
            }
            draw_history(ctx,labels,today_noize_history);                        
        }
    })
})

$('.update_link').on('click',function(){
    short_link = $(this).parent().parent().children('#short_name')
    description = $(this).parent().parent().children('#description')
    link_type = $("input[name='group1']:checked")
    link_id = $(this).parent().parent().parent('.row').parent('.link_fullinfo').attr('id')
    fetch('/api/link/'+$(this).attr('id'),{
            method: "PUT",
            headers: new Headers({
                'Authorization': getCookie('JWT')
              }), 
            body: JSON.stringify({
                name: short_link.val(),
                type: link_type.val(),
                description: description.val()
            })
        }).then(function(response){
            return response.json()
        }).then(function(data){
            if(data.success){
                alert('Изменения приняты в силу')
                window.location.reload()
            }else{
                alert(data.error)
            }
        })
})
$('.delete_link').on('click',function(){
    fetch('/api/link/'+$(this).attr('id'),{
        method: "DELETE",
        headers: new Headers({
        'Authorization': getCookie('JWT')
      })
    }).then(function(response){
        return response.json()
    }).then(function(data){
        if(data.success){
            alert('Удаление прошло успешное')
            window.location.reload()
        }else{
            alert(data.error)
        }
    })
})

let chart = 'NaN';
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
    counter+=1;
    let temp_id = 'chart-'+$(this).attr('id')
    console.log(temp_id)
    var ctx = document.getElementById(temp_id).getContext('2d'); // 2d context
    $(this)
        .parent()
        .parent()
        .parent()
        .children('.link_fullinfo').slideToggle()
    draw_history(ctx,['10.02.2020 10:00:00','10.02.2020 10:00:00','10.02.2020 10:00:00'],[counter, 1, 2]);
    
    // fetch('/link/statistic',{
    //     method: "POST",
    //     body: JSON.stringify({

    //     })
    // }).then(function(response){
    //     return response.json()
    // }).then(function(data){
    //     if(data.success){
            
    //     }else{

    //     }
    // })
    
})
$('.update_link').on('click',function(){
    short_link = $(this).parent().parent().children('#short_name')
    description = $(this).parent().parent().children('#description')
    console.log(short_link.val())
    console.log(description.val())
    link_type = $("input[name='group1']:checked")
    console.log(link_type.val())
    link_id = $(this).parent().parent().parent('.row').parent('.link_fullinfo').attr('id')
    console.log(link_id)
})
$('.delete_link').on('click',function(){
    // fetch('/link/statistic',{
    //     method: "POST",
    //     body: JSON.stringify({

    //     })
    // }).then(function(response){
    //     return response.json()
    // }).then(function(data){
    //     if(data.success){
            
    //     }else{

    //     }
    // })
})

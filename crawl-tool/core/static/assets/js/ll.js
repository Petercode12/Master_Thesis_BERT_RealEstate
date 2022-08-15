const btn = document.getElementsByClassName("toggle-vis");

const index = [0, 0];

const colors = ['green','red' ];
for( let i = 0; i < btn.length; i ++){

    btn[i].addEventListener('click', function onClick() {

        btn[i].style.backgroundColor = colors[index[i]];
        btn[i].style.borderColor = colors[index[i]]
        btn[i].style.color = 'white';

        index[i] = index[i] >= colors.length - 1 ? 0 : index[i] + 1;
        }
        );
    }

function change(data){
    var btn = document.getElementsByClassName("toggle-vis")[data];

    if (btn.value == "On") {
        btn.value = "Close";
        btn.innerHTML = "Tắt";
    }
    else {
        btn.value = "On";
        btn.innerHTML = "Bật";
    }
    }

function change1(data){
        var btn = document.getElementsByClassName("toggle-vis-nhadat24h")[data];
        if (btn.value == "On") {
            btn.value = "Close";
            btn.innerHTML = "Tắt";
        }
        else {
            btn.value = "On";
            btn.innerHTML = "Bật";
        }
        }

function format(data) {
    let res = '<table cellpadding="5" cellspacing="0" boorder="0" style="padding-left:50px;">' +
        '<tr>' +
        '<td>Danh Sách:</td><td>';
    let phones = data[2].split(";");
    for (let i = 0; i < (phones.length < 10 ? phones.length : 10); i++){
        res += phones[i] + '<br>';
    };
    if (phones.length >= 10){
        res += '<a class="see-more" href="/vieclamtot-phone-user/?job=\'' + data[1].split(' ').join('%20').replace(/\//g, "%2F") + '\'" target="_blank">Xem Thêm</a>'
        }   
    return  res + '</td></tr>' + '</table>';
    
}   

function display_date(data, type){
    var x = data.replace("T", " ").replace("Z", "");
    if (type==='display'){
        return '<p class="post-time"><br>' + x + '</p>'
        // return '<p>' + data + '</p>';
        }
    return data;
}

function from_timestamp_to_date(data){
    const options = {month: 'long', day: 'numeric', hour:'numeric', minute:'numeric' };
    var time_stamp = parseInt(data);
    if (time_stamp.toString().length === 10){
        time_stamp = time_stamp * 1000;
    }
    var date = new Date(time_stamp);
    var x = date.toLocaleDateString('vi', options);
    return x;
}

function random_rgba() {
    var o = Math.round, r = Math.random, s = 200;
    return 'rgba(' + o(r()*s) + ',' + o(r()*s) + ',' + o(r()*s) + ',' + r().toFixed(1) + ')';
}

function renderChart(label, data, line_data) {
    const bar_names = ['Thợ Xây, Thợ Hồ',
                        'Bán Hàng',
                        'Tài Xế',
                        'Giúp Việc, Tạp Vụ',
                        'Nhân Viên Nhà Hàng, Khách Sạn',
                        'Nhân Viên Chăm Sóc Khách Hàng',
                        'Bảo Vệ, An Ninh, Vệ Sỹ',
                        'Thợ Điện - Điện Tử - Điện Lạnh',
                        'Thợ Dệt May - Da giày',
                        'Nhân Viên Spa, Thẫm Mỹ Viện, Làm Tóc, Nail',
                        'Nhân Viên Chế Biến, Đóng Gói Thực Phẩm',
                        'Hành Chính, Thư Ký, Trợ Lý',
                        'Thợ Sửa Chữa Ô Tô, Xe Máy, Máy Móc Các Loại',
                        'Lao Động Phổ Thông',
                        'Nhân Viên Kinh Doanh',
                        'Bất Động Sản',
                        'Công Nhân Tại Khu Công Nghiệp',
                        'Đa Ngành Nghề',
                        'PG, PB, Lễ Tân',
                        'Đầu Bếp, Pha Chế',
                        'Tài Chính, Kế Toán, Kiểm Toán',
                        'Thợ Sắt - Hàn - Cơ Khí',
                        'Thợ Mộc - Thợ Gỗ',
                        'Tài Xế Giao Nhận Hàng Xe Máy'

]
    
    const ctx = document.getElementById('myChart').getContext('2d');
    var CHART = $('#myChart');
    window.myChart = new Chart(CHART, {
        type: 'bar',
        data: {
            labels: label,
            datasets: [
            {
                lineTension: 0,
                label: "Average",
                data: line_data,
                backgroundColor: 
                    'rgba(0, 135, 255, 1)'
                ,
                borderColor: 
                    'rgba(0, 135, 255, 1)'
                ,
                borderWidth: 1,
                type:"line",
                fill: false,
                borderWidth: 5
            }
        
        ]
        },
        options: {
            title: {
                display: true,
                text: 'Biểu Đồ Cập Nhật Dữ Liệu',
                fontSize: 20,
                fontColor: 'black'
            },
            scales: {
                xAxes:[{
                    
                    ticks: {
                        min: -1,
                        max: 8,
                        stepSize: 1,
                        fixedStepSize: 1,
                        autoSkip: false
                      }
                }],
                yAxes: [{
                    display: true,
                    ticks: {
                        beginAtZero: true,
                        steps: 10,
                        stepValue: 5
                    }
                }]
            }
        }
    });


    for(let i = 0; i < 24;i ++){
        myChart.data.datasets.push(
            {
               label: bar_names[i],
               data: data[i],
               backgroundColor: random_rgba(),
               type: 'bar',
               borderColor: random_rgba(),
               borderWidth:1
               
           });
        
    }
    window.myChart.update();

  }
  
function getChartData() {
    $.ajax({
        type: 'POST',
        url: '/vieclamtot-time-chart/',
        success: function (response) {

            console.log(response)

            const notyf = new Notyf({
                position: {
                    x: 'right',
                    y: 'top',
                },
                ripple: true,
                types: [
                    {
                        type: 'success',
                        background: '#1b998b',
                        icon: {
                            className: '',
                            tagName: 'span',
                            color: '#fff'
                        },
                        dismissible: true,
                    }
                ]
            });
            
            notyf.open({
                type: 'success',
                message: 'Cập nhật biểu đồ thành công !!!'
            });
            
            let stats = response.statistic;

            let label = [];
            let data = [];
            let line_sum =[];
            let x = 0; 
            let k = 0;
            for( let i = 0; i < 24; i++){
                data[i] = [];
            }

            for( let i = 0; i < stats.length; i++){
                x = 0
                // label.push("Thời Gian: " + from_timestamp_to_date(stats[i]["crawled_at"]));
                // let num_keys = stats[i]["num_post"].split(",");
                let temp = stats[i];
                var values = Object.keys(temp).map(function(key){
                    return temp[key];
                });
                label.push("Thời Gian: " + from_timestamp_to_date(stats[i]["crawled_at"]));
                for (let j = 0; j < 24; j++){
                    k = values[j+1];
                    data[j].push(k);
                    x += k;
                }
                line_sum.push(x/24);
            }
            renderChart(label, data, line_sum);
            

        },
        error: (xhr) => {
            const notyf = new Notyf({
                position: {
                    x: 'right',
                    y: 'top',
                },
                ripple: true,
                types: [
                    {
                        type: 'error',
                        background: '#FA5151',
                        icon: {
                            className: '',
                            tagName: 'span',
                            color: '#fff'
                        },
                        dismissible: true,
                    }
                ]
            });

            notyf.open({
                type: 'error',
                message: 'Biều đồ đã có lỗi xảy ra !!!'
            });
            
        },
    });
  }

  function vieclamtot_update_chart(){
    $("#update-chart").attr("disabled", true);

    $("#update-chart").html('<i class="fas fa-sync fa-spin"></i>');

    $.ajax({
        type: 'POST',
        url: '/vieclamtot-update-chart/',
        success: function (response) {
            const notyf = new Notyf({
                position: {
                    x: 'right',
                    y: 'top',
                },
                ripple: true,
                types: [
                    {
                        type: 'success',
                        background: '#1b998b',
                        icon: {
                            className: '',
                            tagName: 'span',
                            color: '#fff'
                        },
                        dismissible: true,
                    }
                ]
            });
            notyf.open({
                type: 'success',
                message: 'Đã gửi quét thành công!'
            });
            // $('#data').DataTable().clear().draw();
            window.location.reload();
            setTimeout(function(){
                $("#update-chart").attr("disabled", false);
                $("#update-chart").html('Quét Dữ Liệu');
            }, 5000);

        },
        error: (xhr) => {
            const notyf = new Notyf({
                position: {
                    x: 'right',
                    y: 'top',
                },
                ripple: true,
                types: [
                    {
                        type: 'error',
                        background: '#FA5151',
                        icon: {
                            className: '',
                            tagName: 'span',
                            color: '#fff'
                        },
                        dismissible: true,
                    }
                ]
            });
            notyf.open({
                type: 'error',
                message: 'Lỗi ' + String(xhr.statusText) + ':' + String(xhr.responseJSON) + '<br><br>Xin vui lòng thử lại hoặc liên hệ với bên kĩ thuật'
            });
            $("#update-chart").attr("disabled", false);
            $("#update-chart").html('Update Chart');
        },
    });

        
  }

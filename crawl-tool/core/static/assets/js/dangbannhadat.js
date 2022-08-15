currentTimestamp = parseInt(moment().unix());
        theInterval = null;

        function deleteDatatableRecords(){

            id_array = [];
            const re_id = /(>[0-9:-\s]+<)/;
            $( ".odd" ).each(function( index ) {
                if ($(this).find("input[type=checkbox]").is(":checked")) { 
                    id_array.push($(this).find("td")[1].innerHTML); 
                } 
            });

            $( ".even" ).each(function( index ) {
                if ($(this).find("input[type=checkbox]").is(":checked")) { 
                    id_array.push($(this).find("td")[1].innerHTML); 
                } 
            });
            
            $.ajax({
                type: 'POST',
                url: '/dangbannhadat-delete-data/',
                data: {
                    "id_array": id_array.join(','),
                },
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
                        message: 'Đã xóa thành công !!!'
                    });
                    
                    $('#dataDangBanNhaDat').DataTable().clear().draw();
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
                        message: 'Xóa thất bại hoặc bạn chưa chọn dữ liệu để xóa !!!'
                    });
                    
                },
            });
        }

        function refreshDatatable(){
            $('.table-responsive').toggle();
        }

        function changeToClientSide(){
            $('#data').DataTable().destroy();
            $('#data').DataTable({
                serverSide: false,
                searching: false,
                paging: false,
                destroy: true,
                bSort: false,
                dom: 'Bfrtip',
                buttons:[
                    'copyHtml5',
                    'excelHtml5',
                    'csvHtml5',
                    'pdfHtml5',
                    {
                        text: "Tắt Tự Động Cập Nhật",
                        className: 'btn-danger',
                        action: function (e, dt, node, config) {
                            clearInterval(theInterval);
                            $('#data').DataTable().destroy();
                            changeToServerSide();
                        },
                    },
                ]
            });
            $('#data').DataTable().clear().draw();

            setTimeout(function(){
                $('.dt-buttons button').removeClass('dt-button').addClass('btn btn-sm');
                $('.buttons-copy').addClass('btn btn-sm btn-info');
                $('.buttons-excel').addClass('btn btn-sm btn-tertiary');
                $('.buttons-csv').addClass('btn btn-sm btn-success');
                $('.buttons-pdf').addClass('btn btn-sm btn-primary');
            }, 100);

            theInterval = setInterval(function(){ 
                
                $.ajax({
                    type: 'POST',
                    url: '/vieclamtot-auto-data/',
                    data: {
                        "timestamp": parseInt(currentTimestamp)
                    },
                    success: function (response) {

                        $('#data').DataTable().clear().draw();

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
                        
                        // notyf.open({
                        //     type: 'success',
                        //     message: 'Có dữ liệu mới !!!'
                        // });

                        for (i = 0; i < response.data.length; i++) {
                            $('#data').dataTable().fnAddData([
                                // '',
                                // response.data[i]["id"],
                                response.data[i]["updated_at"],
                                response.data[i]["search_keyword"],
                                response.data[i]["post_title"],
                                response.data[i]["job_type"],
                                response.data[i]["full_description"],
                                response.data[i]["company_name"],
                                response.data[i]["vacancies"],
                                response.data[i]["salary_with_unit"],
                                response.data[i]["min_salary"],
                                response.data[i]["max_salary"],
                                response.data[i]["salary_type"],
                                response.data[i]["contract_type"],
                                response.data[i]["min_age"],
                                response.data[i]["max_age"],
                                response.data[i]["preferred_gender"],
                                response.data[i]["preferred_education"],
                                response.data[i]["preferred_working_experience"],
                                response.data[i]["skills"],
                                response.data[i]["benefits"],
                                response.data[i]["street_number"],
                                response.data[i]["ward"],
                                response.data[i]["district"],
                                response.data[i]["city"],
                                response.data[i]["address"],
                                response.data[i]["coordinate"],
                                response.data[i]["url"],
                                response.data[i]["post_author"],
                                response.data[i]["post_time"],
                                response.data[i]["phone"]
                            ]);
                        }

                        $('#data').DataTable().order([1, 'asc']).draw();
                        $('#data').DataTable().order([0, 'asc']).draw();
                        
                        // $('#data').DataTable().clear().draw();
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
                            message: 'Kết nối thất bại !!!'
                        });
                        
                    },
                });

            }, 5000);

        };
        
        function DangBanNhaDatChangeToServerSide(){
            var table = $('#dataDangBanNhaDat').DataTable({
                lengthMenu: [[10, 20, 25, 50, 100], [10, 20, 25, 50, 100]],
                language: {
                "lengthMenu": "Hiện _MENU_ hàng mỗi trang (cũng là số dòng khi tải file về)"
                },
                responsive: true,
                serverSide: true,
                destroy: true,
                scrollX: true,
                order: [[ 2, "desc" ]],
                sAjaxSource: "/dangbannhadat-show-data/",  
                    columnDefs: [
                        // {
                        //     targets: 6,
                        //     visible: false
                        // },
                        // {
                        //     targets: 25,
                        //     visible: false
                        // },
                        // {
                        //     targets: 1,
                        //     visible: false
                            
                        // },
                        {"className": "dt-center", "targets": "_all"}
                    ],
                    columns: [
                            {
                        'data':null,
                        'defaultContent':'',
                        'checkboxes':{
        
        
                            'selectRow':true
                        }},
                        {name: "id", data: 0},
                        {name: "format_time", data: 2, render: display_date},
                        {name: "post_title", data: 3},
                        {name: "type", data: 4},
                        {name: "description", data: 5},
                        {name: "area", data: 6},
                        {name: "price_with_unit", data: 7},
                        {name: "address", data: 8},
                        {name: "url", data: 9, 
                            render: function(data, type) {
                                if (type === 'display') {
                                    return '<a class="table_link" target="_blank" href="' + data + '">' + data + '</a>';

                                }
                                return data;
                            }},
                        {name: "post_author", data: 10},
                        {name: "phone_number", data: 11}
                        
                    ],
                    dom: 'Blfrtip',
                    buttons: [
                        
                        {
                            text: "Cập Nhật",
                            className: 'btn-primary',
                            action: function (e, dt, node, config) {
                                dangbannhadat_update_chart()
                            },
                        },
                        'copyHtml5',
                        {
                            extend: 'excelHtml5',
                            text: 'Excel',
                            filename: function(){
                                return 'Thông Tin Việc Làm Tốt'
                            }
                        },
                        {
                            extend: 'csvHtml5',
                            text: 'CSV',
                            filename: function(){
                                return 'Thông Tin Việc Làm Tốt'
                            }
                        },
                        {
                            extend: 'pdfHtml5',
                            text: 'PDF',
                            filename: function(){
                                return 'Thông Tin Việc Làm Tốt'
                            }
                        },
                        {
                            text: "Xóa Dữ Liệu Đã Chọn",
                            className: 'delete-btn',
                            action: function (e, dt, node, config) {
                                if (window.confirm("Bạn có chắn chắn muốn xóa?")) {
                                    deleteDatatableRecords();
                                }
                            },
                        },
                    ],
                    
            });
            $('button.toggle-vis').on( 'click', function (e) {
                    e.preventDefault();
            
                    // Get the column API object
                    var column = table.column( $(this).attr('data-column') );
            
                    // Toggle the visibility
                    column.visible( ! column.visible() );
                } );
            setTimeout(function(){
                $('.dt-buttons button').removeClass('dt-button').addClass('btn btn-sm');
                $('.buttons-copy').addClass('btn btn-sm btn-info');
                $('.buttons-excel').addClass('btn btn-sm btn-tertiary');
                $('.buttons-csv').addClass('btn btn-sm btn-success');
                $('.buttons-pdf').addClass('btn btn-sm btn-danger');
            }, 100);

        }

    function crawlDangBanNhaDat(end_page){

        if (end_page == ''){

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
                    message: 'Vui lòng nhập đầy đủ thông số tìm kiếm !!!'
                });
                $("#trigger-button").attr("disabled", false);
                $("#trigger-button").html('Quét Dữ Liệu');

        }

        else{

            $("#trigger-button").attr("disabled", true);

            $("#trigger-button").html('<i class="fas fa-sync fa-spin"></i>');

            $.ajax({
                type: 'POST',
                url: '/dangbannhadat-get-data/',
                data: {
                    "end_page": end_page
                },
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
                        message: 'Đã gửi lệnh quét thành công!'
                    });
                    $('#dataDangBanNhaDat').DataTable().clear().draw();

                    setTimeout(function(){
                        $("#trigger-button").attr("disabled", false);
                        $("#trigger-button").html('Quét Dữ Liệu');
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
                    $("#trigger-button").attr("disabled", false);
                    $("#trigger-button").html('Quét Dữ Liệu');
                },
            });

        }

    }
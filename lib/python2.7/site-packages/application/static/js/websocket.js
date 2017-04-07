    function createSocket(http_host) {
        async_task_socket = new ReconnectingWebSocket('ws://'+http_host+':27905',null, {reconnectInterval: 2000,reconnectDecay:1,maxReconnectAttempts:20})
        async_task_socket.onerror = function(event){ console.log('async_task_socket has errr',event); };
    
        async_task_socket.onopen = function(event) { 
            async_task_socket.send('ok'); 
            async_task_socket.onmessage = function(event) { 
                //console.log('Client received a message',event); 
                if (event.data == 'ok'){
                }else if (event.data == 'reload_alert'){
                   reload_warning_num();
                } else {
                    socket_handler(event.data)
                }
            }; 
        
            async_task_socket.onclose = function(event) { 
                console.log('Client notified async_task_socket has closed',event); 
            }; 
        };
    }

    function task_complete_handler(data) {
        var success = data['success'];
        var error = data['error'];
        var tname = SelfTranslate(data.name);
        if ( success ) {
            $(".device_tip").text(tname + '完成').css({"display":"block","color":'#000'});                                                
            var title = tname + "任务成功";
            lobibox_popup('success', title);
            $('.panel-f-style table').trigger('reloadGrid');
        } else{
            var title = tname + "任务失败";
            lobibox_popup('error', title);
        }
    }

    function task_complete_grid_reload(){
        var tmptxt = $(".device_tip").text();
        if($("#disk_path_").hasClass("call_delete") || tmptxt.indexOf("删除中") >=0 ){
            //$(".device_tip").text(tname + "失败：" +error).css({"display":"block","color":'#000'});                                                
            $('#grid_disk_table').trigger("reloadGrid");                                                
            $("#disk_path_").removeClass("call_delete");
        }
        $('#grid_disk_table').trigger("reloadGrid");                                                
        $('#volume_available_tb').trigger("reloadGrid");
        $("#tb_node_mng").trigger('reloadGrid');
        $('#volume_folder_tb').trigger('reloadGrid');
    }

    function lobibox_popup(level, title){
        //level is one of [success, error, info, warning]
        Lobibox.notify(level, {
            delay: false,
            title: title,
            msg: "",
        });
    }


    function socket_handler(data_str) {
        var data = JSON.parse(data_str)
        var success = data['success']
        var error = data['error']
        task_complete_grid_reload();
        task_complete_handler(data);

        tmptxt = $(".device_tip").text()
        if($("#disk_path_").hasClass("call_stop") || tmptxt.indexOf("停止服务中")>=0){
            $(".device_tip").text(result).css({"display":"block","color":'#000'});                                                
            $('#grid_disk_table').trigger("reloadGrid");                                                    
        }
    }


    // listen login expired time and redirect to /login 
    function listen_re_login(http_host){
        websocket = new ReconnectingWebSocket('ws://'+ http_host +':27905',null, {reconnectInterval: 2000,reconnectDecay:1})
    
        websocket.onopen = function(event) { 
            websocket.send('ok'); 
            websocket.onmessage = function(event) { 
                if (event.data == 'start'){
                    window.location.href="/login";
                }
            }; 
        
            websocket.onclose = function(event) { 
                console.log('Client notified websocket has closed',event); 
            }; 
       };
    }

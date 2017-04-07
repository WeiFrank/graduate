      var plotdata=new Array();    
      var totalPoints = 10;
      var plotarr=new Array();
      var get_array_data=new Array();
      var iops_max=new Array();
      var options_plot = new Array();
      function getRandomData(id,index,item_data,targetDiv) { 
          if( typeof(plotdata[id])=="undefined")
          {
             plotdata[id]=new Array();   
             console.log(id );     	
           }
          if( typeof(plotdata[id][index])=="undefined")
          {
             plotdata[id][index]=new Array();   
             console.log(index );     	
           }
          if(plotdata[id][index].length>=totalPoints)
             {
             	  plotdata[id][index] = plotdata[id][index].slice(1); 
                 plotdata[id][index].push(item_data);
             } 
          else
           { 
             for(var i=1;i<totalPoints;i++){
                        plotdata[id][index].push("");  
                 	 	}        
             plotdata[id][index].push(item_data) 
           }  
           //获取最后一秒的数据   
           var tempbaifenbi=$("#"+targetDiv.attr("id").split("_td")[0]+"_last"+id);
               tempbaifenbi.text(plotdata[id][index][plotdata[id][index].length-1]) ;
               tempbaifenbi.parent().parent().attr("title",tempbaifenbi.parent().text());              
         // $("#"+targetDiv.attr("id").split("_td")[0]+"_last"+arg).text(plotdata[arg][plotdata[arg].length-1]) ;
          var res = new Array();
          var mark=1;
       	 for (var i = 0; i <plotdata[id][index].length; ++i)
            {
 					if(plotdata[id][index][i]!="") {
                 if(plotdata[id][index][i]<=40){mark=1}
                 else
                 if(plotdata[id][index][i]<=60){mark=2}
                 else
                 if(plotdata[id][index][i]<=80){mark=3}
                 else
                 if(plotdata[id][index][i]>80){mark=4}
               }
            	res.push([i, plotdata[id][index][i]])               
            }
        	   return new Array(res,mark);   
    	}  
    	/*iops*/
    	function get_iops_percent(o,value,max_value,b){
    		         if(max_value==0||value==0)
                	 {
                	 	 o.find(".cluster_iops_read").css("width",0);
                	    o.find(".cluster_iops_txt").text(0); 

                	    if(o.attr("id").indexOf("IOPS")>=0){                	                   	    	
                	   	  if(b)
                	    	  o.parent().attr("title",o.parent().attr("title")+" w："+0)  
                	    	  else
                	    	   o.parent().attr("title","r："+0)        
                	    }
                	    else
                	    {                 	                         	    	
                	   	  if(b)
                	    	  o.parent().attr("title",o.parent().attr("title")+" out："+0)      
                	    	  else
                	    	  o.parent().attr("title","in："+0)               	    	
                	    	}                	                   
                	 }
                	 else{ 
                	 	 o.find(".cluster_iops_read").css("width",100*value/max_value);
                	    o.find(".cluster_iops_txt").text(value);
                	    
                	     if(o.attr("id").indexOf("IOPS")>=0){                	                          	    	
                	   	  if(b)
                	    	  o.parent().attr("title",o.parent().attr("title")+" w："+value)  
                	    	  else
                	    	  o.parent().attr("title","r："+value)  
                	    }
                	    else
                	    {                 	                           	    	
                	   	  if(b)
                	    	  o.parent().attr("title",o.parent().attr("title")+" out："+value)    
                	    	  else
                	    	   o.parent().attr("title","in："+value)               	    	
                	    	}         
                	 	}
    		}
    	function update_time(o,ids,first,cluster_id,host_id) {          
          //请求服务器数据 
         var bValid=false;
        get_array_data = [];
        iops_max=[];
            
                _data = {"host_id":host_id, "hostids":ids.toString(), "cluster_id":cluster_id};
          $.ajax({
         	 url : "/host/jquery_unitflot",
                 type : "GET",  
                contentType: "application/json",
                 data: _data, 
                 dataType: "json",
         	 async : false, 
         	 success:function(data){
                   temp = data.slice(0,-2)
                   for (x in temp){
                        get_array_data.push(temp[x]);
                    }
                   gridload = data.splice(data.length-1,1)
                    if (gridload == 'true') {
                          $('#tb_node_mng').trigger("reloadGrid");
                    }
                        ldata = data.splice(data.length-1,1)
                        array_data = ldata.toString().split(',')
                        for(var i=0;i<ids.length;i++){                        	
                            temp = array_data[i];
                          $('#tb_node_mng').jqGrid('setRowData', ids[i], { service_status:temp}); 
                                     //进程颜色区分
 				     status_value=$('#tb_node_mng').find("#"+ids[i]).find(".p_values");
                 sv_value=status_value.text().split("/");
                 //sv_value[0]=0;sv_value[1]=3;
                 if(sv_value[0]==0&&$('#tb_node_mng').find("#"+ids[i]).find(".lichd").attr("src")=="/static/img/green_status.png")
                 {
                      status_value.css("color","#EA303E");
                 }
                 else
                 if(sv_value[0]==0&&$('#tb_node_mng').find("#"+ids[i]).find(".lichd").attr("src")=="/static/img/red_status.png")
                 {
                      status_value.css("color","#999999");
                 }
                 else
                 if(sv_value[1]-sv_value[0]==0)
                 {
                      status_value.css("color","#00B83F");
                 }
                 else
                 if(sv_value[1]-sv_value[0]==1)
                 {
                      status_value.css("color","#FADB03");
                 }
                 else
                 if(sv_value[1]-sv_value[0]>1)
                 {
                      status_value.css("color","#FFA03B");
                 }                         	
                        }                    
                 },
              error:function(data){
               	  clearInterval(window.time);  
               	  bValid=true;
               	}             
            })
            if(bValid){
                   return false;            	
            	}
           iops_max.push(get_array_data.pop(),get_array_data.pop(),get_array_data.pop(),get_array_data.pop());

//         get_array_data=[10,20,30,40,50,60,70,80,90]   
      	for(var i=0;i<ids.length;i++){
      		 if(first){
      		 	   get_iops_percent(o.find("#IOPS_read_"+ids[i]),get_array_data[i*6],iops_max[3]);
      		 	   get_iops_percent(o.find("#IOPS_write_"+ids[i]),get_array_data[1+i*6],iops_max[2],true);      		 	   
      		 	   get_iops_percent(o.find("#swallow_"+ids[i]),get_array_data[2+i*6],iops_max[1]);
      		 	   get_iops_percent(o.find("#spit_"+ids[i]),get_array_data[3+i*6],iops_max[0],true);      		 	         		 	         		 	 
                	            	                	               	    		 	
               	plot_show(o.find("#usage_cpu_td"+ids[i]),i+ids.length*0,ids[i],0,get_array_data[4+i*6]); 
              		plot_show(o.find("#usage_mem_td"+ids[i]),i+ids.length*1,ids[i],1,get_array_data[5+i*6]);
              }
              else
              {
                	 get_iops_percent(o.find("#IOPS_read_"+ids[i]),get_array_data[i*6],iops_max[3]);
      		 	    get_iops_percent(o.find("#IOPS_write_"+ids[i]),get_array_data[1+i*6],iops_max[2],true);      		 	   
      		 	    get_iops_percent(o.find("#swallow_"+ids[i]),get_array_data[2+i*6],iops_max[1]);
      		 	    get_iops_percent(o.find("#spit_"+ids[i]),get_array_data[3+i*6],iops_max[0],true);  
                   var arr=getRandomData(ids[i],0,get_array_data[4+i*6],o.find("#usage_cpu_td"+ids[i]))
                   if(arr[1]==1){
    				       options_plot[i+ids.length*0].lines.fillColor="#00B83F";
    				      }              
                   if(arr[1]==2){
    				       options_plot[i+ids.length*0].lines.fillColor="#FFEB58";
    				      }
    		          if(arr[1]==3){
    				       options_plot[i+ids.length*0].lines.fillColor="#FFA03B";
    				     }
    				    if(arr[1]==4){
    				       options_plot[i+ids.length*0].lines.fillColor="#EA303E";
    				    	}
                   $.plot(plotarr[0+i*2].getPlaceholder(),[arr[0]],options_plot[i+ids.length*0])
                   
                   
                   arr=getRandomData(ids[i],1,get_array_data[5+i*6],o.find("#usage_mem_td"+ids[i]))
                   if(arr[1]==1){
    				       options_plot[i+ids.length*1].lines.fillColor="#00B83F";
    				      }                   
                   if(arr[1]==2){
    				       options_plot[i+ids.length*1].lines.fillColor="#FFEB58";
    				      }
    		          if(arr[1]==3){
    				       options_plot[i+ids.length*1].lines.fillColor="#FFA03B";
    				     }
    				    if(arr[1]==4){
    				       options_plot[i+ids.length*1].lines.fillColor="#EA303E";
    				    	} 
                   $.plot(plotarr[1+i*2].getPlaceholder(),[arr[0]],options_plot[i+ids.length*1])                 
                 //  plotarr[1+i*2].setData([arr[0]]);
                 //  plotarr[1+i*2].draw();  
              	} 
      	}  
   	} 
   	function plot_show(targetDiv,i,id,index,item_data){    
   	     options_plot[i]={
   	     	   colors: ["#000", "#afd8f8", "#cb4b4b", "#4da74d", "#9440ed"],
       		 	series: { shadowSize: 0 }, 
       		 	yaxis: {show:false, min:0,max:100},
       			xaxis: { show: false,min:0,max:9 },
       			grid: { backgroundColor: "#000",borderWidth:1,borderColor:"#797979"},
       			lines: {lineWidth: 1,fill:true,fillColor: "#00B83F"}
    			};
    			var arr=getRandomData(id,index,item_data,targetDiv);
    			if(arr[1]==2){
    				options_plot[i].lines.fillColor="#FFEB58";
    				}
    			if(arr[1]==3){
    				options_plot[i].lines.fillColor="#FFA03B";
    				}	
    		   if(arr[1]==4){
    				options_plot[i].lines.fillColor="#EA303E";
    				}
         var chart= $.plot(targetDiv, [arr[0] ], options_plot[i]);
         plotarr.push(chart);            
      }  	
      function plot_show_all(o,ids,cluster_id,host_id){
      if($("#div_node_tb").hasClass("time_interval")){
         for(var i=0;i<ids.length;i++){    
   		   plotdata[ids[i]]=new Array(); 
   		   plotdata[ids[i]][0]=new Array();
  		      plotdata[ids[i]][1]=new Array();
         }    
      $("#div_node_tb").removeClass("time_interval"); 
      }  	
         update_time(o,ids,true,cluster_id,host_id)          

           window.time= window.setInterval(function(){
            if($('#interval_tip').hasClass('div_host'))
              {
              	 update_time(o,ids,false,cluster_id,host_id)
             }
            else
               clearInterval(window.time)
         	},30000)
      }
   		
   		
   		
   		
   		

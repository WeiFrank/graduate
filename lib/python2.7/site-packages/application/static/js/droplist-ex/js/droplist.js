var droplistArray=new Array();
(
	function(){
		$.extend($.fn,{
			/**
			 * 销毁下拉列表 <br />
			 * 调用方法： <br />
			 * jquery插件的机制进行开发，调用方式类似jquery其他方法<br />
			 * 举例如下：<br />
			 *		$('#dispfile2').destroyDropDown();<br />
			 *		(1)dispfile2意义为id=dispfile2的input输入框<br />
			 * @name destroyDropDown 
			 */
			destroyDropDown:function(){
				$("#rqDropDownList_"+$(this).attr("id")).remove();
			},
			/**
			 * 销毁选择样式 <br />
			 * 调用方法： <br />
			 * jquery插件的机制进行开发，调用方式类似jquery其他方法<br />
			 * 举例如下：<br />
			 *		$('#dispfile2').destroySelect();<br />
			 *		(1)dispfile2意义为id=dispfile2的input输入框<br />
			 * @name destroySelect 
			 */
			destroySelect:function(){
				$("#selectDiv_"+$(this).attr("id")).remove();
			},
			/**
			 * 展现下拉列表 <br />
			 * 调用方法： <br />
			 * jquery插件的机制进行开发，调用方式类似jquery其他方法<br />
			 * 举例如下：<br />
			 *		$('#dispfile2').rqDropDown(settings);<br />
			 *		(1)dispfile2意义为id=dispfile2的input输入框<br />
			 *      (2)参数settings ,下拉列表配置参数，json对象.举例：<br />var settings = {<br />"apppath":,//web应用根路径<br />"datatype":"local",//数据类型,如果为local，则source属性为json对象。如果为json，则source为远程数据的url<br />"source":jsonDataArr,<br />"multi":true,//是否具备多选的能力<br />"urlData"://datatype为json时，此处为source指定的url的参数对<br />};<br />
			 * @name rqDropDown
			 * @param settings 
			 */
			rqDropDown:function(settings){
				var DATALIST_DIV_HEIGHT = "auto";
				var DATA_OVER_BACKCOLOR = "#f5f5f5";
				var DATA_OUT_BACKCOLOR = "#FCFCFC";
				var down_text = "";
				var isOut=true
				settings = extendSettings(settings,$(this));
				gcResource(settings);
				changeInputStyle(settings);
				initEvents(settings);
				droplistArray.push(settings);			
				var  scrollFunc=function(e){ 
 							var target = e.target || e.srcElement;
 							//if(target.id === getSrcId(settings)) return;
 							if(target.id === ("selectDiv_"+getSrcId(settings))) return;
 							if(target.className=="rqdataDiv") return;
 							//daiwenxue-update
 							if(target.className=="rqDataFont") return;
 							if(target.className=="rqDropDownList") return;
 							if(isOut)
 							{
 								for(var i=0;i<droplistArray.length;i++)
 							   {
   						    $('#'+getSrcId(droplistArray[i])).destroyDropDown();
   					      }
   					   }   						
							};
	         if(document.addEventListener){ 
                         document.addEventListener('DOMMouseScroll',scrollFunc,false); 
            }
			   document.onmousewheel =scrollFunc;
				document.onmousedown =scrollFunc;
				/**
				 * 初始化事件
				 * 1.下拉图片的click事件，控制下拉列表的创建显示和销毁
				 * 2.输入框的数据过滤事件
				 */
				function initEvents(settings){
					//2.定义它的click事件-点击则出现数据
					$('#selectDiv_'+getSrcId(settings)).click(
						function(){
							if($('#rqDropDownList_'+getSrcId(settings)).length>0){
								$('#'+getSrcId(settings)).destroyDropDown();
							}else{
								switch(settings.datatype){
									case "json":
										showRqDropDownByJson(settings);
										break;
									case "local":
										showRqDropDownByLocal(settings);
										break;	
								}
								displayNowValue(settings);								
							}
						}
					)
					$('#'+getSrcId(settings)).click(
						function(){
							if($('#rqDropDownList_'+getSrcId(settings)).length>0){
								$('#'+getSrcId(settings)).destroyDropDown();
							}else{
								switch(settings.datatype){
									case "json":
										showRqDropDownByJson(settings);
										break;
									case "local":
										showRqDropDownByLocal(settings);
										break;	
								}
								displayNowValue(settings);								
							}
						}
					)
						
					//3.定义 事件,数据改变了则改变下拉列表的数据
					settings.inputObj.keydown(
						function(){
							down_text = $(this).val();
						}
					)
					settings.inputObj.keyup(
						function(){
							var up_text = $(this).val();
							if(down_text!=up_text){
								filterData(up_text);
							}
						}
					)
				}
				/**
				 * 改变输入框的样式
				 * 1.输入框后增加一个下拉图片。图片的大小，位置，由输入框计算而得
				 */
				function changeInputStyle(settings){
					//1.改变input的外观，
					var inputObjID = getSrcId(settings);
					var select_image = $("<span id='selectDiv_"+inputObjID+"' name='selectDiv_"+inputObjID+"' class='selectDiv'><img id='selectImg_"+inputObjID+"' name='selectImg_"+inputObjID+"' class='selectImg'></img></span>");
					$("#"+inputObjID).after(select_image);
					$('#selectImg_'+inputObjID).attr("src",settings.imageFolder+"select.png");
					if(!settings.position) {
						select_image.css("position","relative");
						select_image.css("left","-"+($('#selectImg_'+inputObjID).width()+10)+"px");
						select_image.css("top","-5px");
					}
					$('#selectImg_'+inputObjID).attr("height","6px");
					$('#selectImg_'+inputObjID).attr("width","8px");
					$('#selectImg_'+inputObjID).css("verticalAlign","-5px");
				}
				/**
				 * 回收资源，销毁之前输入框创建的下拉列表等，便于重新创建
				 * 1.销毁下拉列表DIV
				 * 2.销毁下拉图片DIV
				 */
				function gcResource(settings){
					$('#'+getSrcId(settings)).destroyDropDown();
					$('#'+getSrcId(settings)).destroySelect();
				}
				/**
				 * 初始化配置参数
				 * 将传入的覆盖到默认的对象上，
				 */
				function extendSettings(settings,inputObj){
					var defaultSettings = {
						"apppath":"rqLib",
						"datatype":"json",//json + local
						"source":null,
						"multi":false,
						"inputObj":inputObj,
						"urlData":"",
						"imageFolder":"/static/js/droplist-ex/css/images/",
						"onchange":null
					};
					settings = $.extend(true,defaultSettings,settings);
					if(settings.imageFolder==null||settings.imageFolder==""){
						if(settings.apppath!=null&&settings.apppath!=""){
							settings.imageFolder = settings.apppath+"/mis2/gezComponents/formstyle/css/images/";
						}else{
							settings.imageFolder = "";
						}
					}
					return settings; 
				}
				/**
				 * 复选的情况下，反显输入框中的值,
				 * 单选的反显没有弄,
				 */
				function displayNowValue(settings){
					var realvalue = settings.inputObj.attr("realvalue");
					if(realvalue&&realvalue!=""){
						if(settings.multi&&settings.multi==true){
							var realids = realvalue.split(",");
							var reallen = realids.length;
							for(var i=0;i<reallen;i++){
								var realid = realids[i];
								$('#rqdata_'+getSrcId(settings)+'_'+realid).attr('checked','checked');
							}
							var sumLen = $("#rqDataList_"+getSrcId(settings)).children().length;
							if(reallen<sumLen){
								afterNotAllChecked(settings);
							}else if(reallen==sumLen){
								afterAllChecked(settings);
							}
						}else{
							$('#rqdataDiv_'+getSrcId(settings)+'_'+realid).css('background-color',DATA_OVER_BACKCOLOR);
						}
					}else{
						if(settings.multi&&settings.multi==true){
							afterAllUnChecked(settings);
						}
					}
				}
				/**
				 * 获取源输入框的ID的统一方法
				 */
				function getSrcId(settings){
					return settings.inputObj.attr('id');
				}
				/**
				 * 过滤数据的核心方法
				 */
				function filterData(filter_text){
					if($('#rqDataList_'+getSrcId(settings)).length>0){
						$.each($('#rqDataList_'+getSrcId(settings)+'>div'),function(key,value){
							var text = $(value).attr('text');
							if(text.indexOf(filter_text)==-1){
								$(value).css('display','none');
							}else{
								$(value).css('display','block');
							}
						});
					}
				}
				/**
				 * 如果数据类型是远程json数据，则此方法为入口
				 */
				function showRqDropDownByJson(settings){
					$.ajax({
						type:"POST",
						url: settings.source,
						cache:false,
						data:settings.urlData,
						dataType:"json",
						success:function(data, textStatus){
							createHTMLByData(data,settings);
						},
						error:function(XMLHttpRequest, textStatus, errorThrown){
							alert(errorThrown);
						}
					});
				}
				/**
				 * 如果数据类型是本地数据，则此方法为入口
				 */
				function showRqDropDownByLocal(settings){
					var data = settings.source;
					createHTMLByData(data,settings);
				}
				/**
				 * 创建下拉列表最外层整体的DIV
				 */
				function createBorderDiv(settings){
					var inId = settings.inputObj.attr('id');
					var frameDiv = $("<div id='rqDropDownList_"+inId+"' class='rqDropDownList' onmouseover='isOut=false' onmouseoout='isOut=true'></div>");
					frameDiv.css('left',settings.inputObj.offset().left);
					frameDiv.css('top',settings.inputObj.offset().top+settings.inputObj.height()+2);
					frameDiv.width(settings.inputObj.width()+32);
					return frameDiv;
				}
				/**
				 * 把下拉列表的数据转化成html元素
				 */
				function createHTMLByData(data,settings){
					var borderDiv = createBorderDiv(settings);
					//全选复选框
					if(settings.multi&&settings.multi==true){
						var chooseAllDiv = createChooseAll(settings);
						borderDiv.append(chooseAllDiv);
					}
					//数据
					var dataDiv = createDataList(data,settings);
					borderDiv.append(dataDiv);
					
					//条目数及确定取消
					var funcDiv = createFuncDiv(data,settings);
					borderDiv.append(funcDiv);
					
					$(document.body).append(borderDiv);
				}
				/**
				 * 创建总条目数，确定取消按钮的div
				 */
				function createFuncDiv(data,settings){
					var inId = getSrcId(settings);
					var funcFont = $("<font class='rqDropDownNum'>总条目数:"+data.length+"</font><br />");
					var funcBtn1 = $("<input id='OKBtn_"+inId+"' class='OKButton' type='button' value='确定'/>");
					$(funcBtn1).click(
						function(){
							setValue2Src(settings);
							//关闭窗口
							$('#'+getSrcId(settings)).destroyDropDown();
						}
					)
					var funcBtn2 = $("<input id='CancelBtn_"+inId+"' class='CancelButton' type='button' value='取消'/>");
					$(funcBtn2).click(
						function(){
							//关闭窗口
							$('#'+getSrcId(settings)).destroyDropDown();
						}
					)
					var funcDiv = $("<div id='funcDiv_"+inId+"' class='funcDiv'></div>");
					funcDiv.append(funcFont);
					if(settings.multi&&settings.multi==true){
						funcDiv.append(funcBtn1);
						funcDiv.append(funcBtn2);
					}
					return funcDiv;
				}
				/**
				 * 工具方法，获取字符串的字节数
				 */
				function getStrByteLen(str){
					//计算字节数
					var charCount = 0;
					for(var i=0,len=str.length;i<len;i++){
						var item = str.charCodeAt(i);
						if(item>255){
							charCount+=2;
						}else{
							charCount+=1;
						}
					}
					return charCount;
				}
				/**
				 * 工具方法，获取字符串的宽度
				 */
				function getStrWidth(str){
					//计算字符串宽度
					var span = $("<span>"+str+"</span>");
					$(document.body).append(span);
					var strwidth = span.width();
					span.remove();
					return strwidth;
				}
				
				/**
				 * 给源输入框赋值的方法
				 */
				function setValue2Src(settings){
					var inId = getSrcId(settings);
					//回填值
					var idValue = "";
					var textValue = "";
					if(settings.multi&&settings.multi==true){
						$.each($('#rqDataList_'+inId+' input'),function(key,value){
							var id = $(value).attr('id');
							if(id.indexOf("rqdata_"+inId+"_")==0){
								var checkAttr = $(value).attr('checked');
								if(checkAttr){
									idValue += $(value).val();
									idValue +=",";
									textValue += $(value).attr('text');
									textValue += ","; 
								}
							}
						});
						if(idValue!=""){
							idValue = idValue.substring(0,idValue.length-1);
						}
						if(textValue!=""){
							textValue = textValue.substring(0,textValue.length-1);
						}
					}else{
						idValue = settings.radioDataDiv.attr("value");
						textValue = settings.radioDataDiv.attr("text");
					}
					if(settings.onchange){
						eval(settings.onchange+"('"+textValue+"','"+idValue+"');");
					}
					var valueArr = textValue.split(",");
					var vc = valueArr.length;
					if(vc<6){
						settings.inputObj.attr('title',textValue);
					   title_for_firefox(settings.inputObj,textValue)
					}else{
						var temp = valueArr[0]+","+valueArr[1]+","+valueArr[2]+","+valueArr[3]+","+valueArr[4]+" 等"+vc+"项";
						settings.inputObj.attr('title',temp);
					}
					$('#selectDiv_'+getSrcId(settings)).attr('title',settings.inputObj.attr('title'));
					var fontWidth = getStrWidth(textValue);
					var inputWidth = settings.inputObj.width()-$('#selectDiv_'+getSrcId(settings)).width(); 
					if(fontWidth>inputWidth){
						//截取+...
						var fontCount = getStrByteLen(textValue);
						var aa = parseInt(inputWidth/parseInt(fontWidth/fontCount));
						aa = aa-3;
						var endIndex=textValue.length-1;
						for(var i=0,len=textValue.length;i<len;i++){
							var charItem = textValue.charCodeAt(i);
							if(charItem>255){
								aa = aa-2;
							}else{
								aa = aa-1;
							}
							if(aa==0){
								endIndex = i;
								break;
							}else if(aa<0){
								endIndex = i-1;
								break;
							}
						}
						var resultStr = textValue.substring(0,endIndex+1)+"...";
						settings.inputObj.val(resultStr);
					}else{
						settings.inputObj.val(textValue);
					}
					settings.inputObj.attr('realvalue',idValue);
				}
				
				/**
				 * 当全选触发以后，其他元件的状态变化。
				 * 全选既包括全选按钮被点击的情况，也包括单选按钮全部选中的情况
				 */
				function afterAllChecked(settings){
					var inId = getSrcId(settings);
					//$('#OKBtn_'+inId).removeAttr("disabled");
					//$('#OKBtn_'+inId)[0].disabled="";
					$('#rqChooseAllImg_'+inId).attr("src",settings.imageFolder+"all_checked.png");
				}
				/**
				 * 当全不选触发以后，其他元件的状态变化。
				 * 全不选既包括全选按钮被点击的情况，也包括单选按钮全部不选中的情况
				 */
				function afterAllUnChecked(settings){
					var inId = getSrcId(settings);
					//$('#OKBtn_'+inId).attr("disabled","disabled");
					$('#rqChooseAllImg_'+inId).attr("src",settings.imageFolder+"no_checked.png");
				}
				/**
				 * 当不全选触发以后，其他元件的状态变化。
				 * 不全选既包括单选按钮不全部选中的情况
				 */
				function afterNotAllChecked(settings){
					var inId = getSrcId(settings);
					//$('#OKBtn_'+inId)[0].disabled="";//("disabled");
					$('#rqChooseAllImg_'+inId).attr("src",settings.imageFolder+"notall_checked.png");
				}
				/**
				 * 创建全选部分的DIV
				 */
				function createChooseAll(settings){
					var chooseAllImg = $("<img id='rqChooseAllImg_"+getSrcId(settings)+"' class='rqChooseAllImg'></img>");
					chooseAllImg.attr("src",settings.imageFolder+"no_checked.png");
					chooseAllImg.toggle(
						function(){
							afterAllChecked(settings);
							$.each($('#rqDataList_'+getSrcId(settings)+' input'),function(key,value){
								var id = $(value).attr('id');
								if(id.indexOf("rqdata_"+getSrcId(settings)+"_")==0){
									$(value).attr('checked','checked');
								}
							});
						},
						function(){
							afterAllUnChecked(settings);
							$.each($('#rqDataList_'+getSrcId(settings)+' input'),function(key,value){
								var id = $(value).attr('id');
								if(id.indexOf("rqdata_"+getSrcId(settings)+"_")==0){
									$(value).removeAttr('checked');
								}
							});
						}
					)
					var chooseAllFont = $("<font class='rqChooseAllFont'>(全选)</font>");
					var chooseAllDiv = $("<div id='rqChooseAllDiv_"+getSrcId(settings)+"' class='rqChooseAllDiv'></div>");
					chooseAllDiv.append(chooseAllImg);
					chooseAllDiv.append(chooseAllFont);
					return chooseAllDiv;
				}
				/**
				 * 创建数据列表部分的DIV
				 */
				function createDataList(data,settings){
					var listDiv = $("<div id='rqDataList_"+getSrcId(settings)+"' class='rqDataList'></div>");
					if(data.length>9){
						listDiv.height(DATALIST_DIV_HEIGHT);
						listDiv.css('overflow-y','hidden');	
					}
					$(settings.borderDiv).append(listDiv);
					$.each(data,function(key,value){
						var id = value[0];
						var text = value[1];
						var dataDiv = createOneData(id,text,settings);
						listDiv.append(dataDiv);
					});
					return listDiv;
				}
				/**
				 * 创建单条数据的DIV
				 */
				function createOneData(id,text,settings){
					var dataCheckBox = $("<input id='rqdata_"+getSrcId(settings)+"_"+id+"' type='checkbox' value='"+id+"' text='"+text+"' />");
					dataCheckBox.click(
						function(){
							var no_checked_num = 0;
							var checked_num = 0;
							var sum_num = 0; 
							$.each($('#rqDataList_'+getSrcId(settings)+' input'),function(key,value){
								var id = $(value).attr('id');
								if(id.indexOf("rqdata_"+getSrcId(settings)+"_")==0){
									sum_num++;
									var valuechecked = $(value).attr("checked");
									if(valuechecked){
										checked_num++;
									}else{
										no_checked_num++;
									}
								}
							});
							if(no_checked_num==0){
								afterAllChecked(settings);
							}else if(checked_num==0){
								afterAllUnChecked(settings);
							}else{
								afterNotAllChecked(settings);
							}
						}
					)
					var dataFont = $("<font class='rqDataFont'>"+text+"</font>"); 
					var dataDiv = $("<div id='rqdataDiv_"+getSrcId(settings)+"_"+id+"' class='rqdataDiv' value='"+id+"' title='"+text+"' text='"+text+"'></div>");
					dataDiv.mouseover(
						function(){
							$(this).css('background-color',DATA_OVER_BACKCOLOR);
			            var temp=$(this).attr("text");
			            $(this).attr("title",temp)
                     title_for_firefox($(this),temp)    			            
			            }
					)
					dataDiv.mouseout(
						function(){
							$(this).css('background-color',DATA_OUT_BACKCOLOR);
						}
					)
					if(!(settings.multi&&settings.multi==true)){
						dataDiv.click(
							function(){
								settings.radioDataDiv = $(this);  
								setValue2Src(settings);
								//关闭窗口
								$('#'+getSrcId(settings)).destroyDropDown();							
							}
						)
					}
					if(settings.multi&&settings.multi==true){
						dataDiv.append(dataCheckBox);
					}
					dataDiv.append(dataFont);
					return dataDiv;
				}
			}
		})
	}
)();
/**
 * 点击下拉列表以外的地方，则下拉列表关闭
 * 此方法加入，会使QTP脚本运行失败，所以暂时注掉。但是功能上是好用的
 */
/*
$(document).bind(
	"click",
	function(event){
		$.each($("div"),function(key,value){
			var curr_id = $(value).attr("id");
			if(curr_id.indexOf("rqDropDownList_")==0){
				var minX = $(value).offset().left;
				var minY = $(value).offset().top;
				var maxX = minX+$(value).width();
				var maxY = minY+$(value).height();
				
				var inDropDown =((event.pageX>=minX&&event.pageX<=maxX)&&(event.pageY>=minY&&event.pageY<=maxY)); 
				
				var inputid = curr_id.substring(curr_id.indexOf("_")+1);
				
				minX = $('#'+inputid).offset().left;
				minY = $('#'+inputid).offset().top;
				maxX = $('#selectDiv_'+inputid).offset().left+$('#selectDiv_'+inputid).width();
				maxY = minY+$('#'+inputid).height();
				var inSelect = ((event.pageX>=minX&&event.pageX<=maxX)&&(event.pageY>=minY&&event.pageY<=maxY));
				if(!(inDropDown||inSelect)){
					$('#'+inputid).destroyDropDown();
				}
			}
		});
	}
);
*/
//点其他地方，关闭div

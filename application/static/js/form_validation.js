function updateTips(t, input_obj, flag) {
    var $el = input_obj.parent();
    var top = $el[0].offsetTop;
    var left = $el[0].offsetLeft;
    var jqtip = $('.error-tip');
    jqtip.find('span').css({
        'bottom': '-30px',
        'border-top': '15px solid #fa575f',
        'border-bottom': '15px solid transparent'
    });
    jqtip.find('p').text(t);
    if (flag) {
        jqtip.css({
            'top': '-9999px',
            'left': '-9999px'
        });
        input_obj.css({
            'border': '1px solid #D8DCE5'
        });
    } else {
        jqtip.css({
            'top': (top - jqtip[0].offsetHeight) + 'px',
            'left': (left + 20) + 'px'
        });
        input_obj.css({
            'border': '1px solid #fa575f'
        });
    }
}
function updateDownTips(t, input_obj, flag) {
    var $el = input_obj.parent();
    var top = $el[0].offsetTop;
    var left = $el.width() - 300;
    var jqtip = $('.error-tip.error-tip-down');
    jqtip.find('span').css({
        'bottom': '100%',
        'border-bottom': '15px solid #fa575f',
        'border-top': '15px solid transparent'
    });
    jqtip.find('p').text(t);
    if (flag) {
        jqtip.css({
            'top': '-9999px',
            'left': '-9999px'
        });
        input_obj.css({
            'border': '1px solid #D8DCE5'
        });
    } else {
        jqtip.css({
            'top': (top + 30) + 'px',
            'left': left + 'px'
        });
        input_obj.css({
            'border': '1px solid #fa575f'
        });
    }
}
//----- 正则验证
function checkRegexp(o, regexp, n, tipDown) {
    var value = $.trim(o.val());
    if (!(regexp.test(value))) {
        if (!tipDown) {
            updateTips(n, o);
        } else {
            updateDownTips(n, o, false);
        }
        return false;
    } else {
        if (!tipDown) {
            updateTips(n, o, true);
        } else {
            updateDownTips(n, o, true);
        }
        return true;
    }
}
//-------中文姓名或者英文姓名的验证    
function checkRegexp_person(o, regexp1, regexp2, n) {
    var value = $.trim(o.val());
    if (regexp1.test(value) || regexp2.test(value)) {
        o.removeClass("ui-state-error");
        o.siblings(".error_tip").hide();
        return true;
    } else {
        o.addClass("ui-state-error");
        updateTips(n, o);
        return false;
    }
}
//不为0整数特殊验证
function checkRegexp_num(o, regexp, n) {
    var value = $.trim(o.val());
    if (!(regexp.test(value)) || value == 0) {
        updateTips(n, o);
        return false;
    } else {
        updateTips(n, o, true);
        return true; 
    }
}
function checkPort(o,n) {
    var port = parseInt(o.val());
    if(isNaN(port)) {
        updateTips('输入正确的端口号。', o);
        return false;
    } else if (port > 0 && port < 65536) {
        updateTips(n, o, true);
        return true; 
    } else {
        updateTips(n, o);
        return false;
    }
}
function checkEnableSubmit(objs) {
    var result = {};
    for (var i = 0; i < objs.length; i++) {
        var obj = objs[i];
        var $el = obj.el;
        if(!$el.val()) {
            result = obj;
            result.enableSubmit = false;
            break;
        }
        if(obj.regs) {
            result = checkRegs(obj.regs, $el);
            if(result.text) {
               break;
            }
        }
    }
    return result;
}
function checkRegs(regArr, el) {
    var result = {};
    for(var i = 0; i < regArr.length; i++) {
        var reg = regArr[i].regexp;
        if(reg instanceof Array) {
            var flag = false;
            for (var k = 0; k < reg.length; k++) {
                var flag = reg[k].test(el.val());
                if(flag) {
                    break;
                }
            }
            if(!flag) {
                result.el = el;
                result.text = regArr[i].text;
                result.enableSubmit = false;
            }
        } else {
            var flag = reg.test(el.val());
            if(!flag) {
                result.el = el;
                result.text = regArr[i].text;
                result.enableSubmit = false;
                break;
            }
        }
    }
    return result;
}
//长度验证  
function checkLength(o, n, min, max, tipDown) {
    var value = $.trim(o.val());
    if (value.length > max || value.length < min) {
        if (!tipDown) {
            updateTips(n + "的长度必须在" + min + "至" + max + "位之间。", o, false);
        } else {
            updateDownTips(n + "的长度必须在" + min + "至" + max + "位之间。", o, false);
        }
        return false;
    } else {
        if (!tipDown) {
            updateTips(n + "的长度必须在" + min + "至" + max + "位之间。", o, true);
        }
        return true;
    }
}
//固定长度验证  
function checkLengthnums(o, n, num) {
    var value = $.trim(o.val());
    if (value.length != num) {
        updateTips(n + "的长度必须是" + num + "位", o);
        return false;
    } else {
        o.removeClass("ui-state-error");
        o.siblings(".error_tip").hide();
        return true;
    }
}
//密码长度验证   
function checkLength_pwd(o, n, min, max, objs) {
    var passwd = o.val()
    if (passwd.length == 0) {
        var tips = objs + '不能为空';
        updateTips(tips, o)
        return false;
    }
    if (passwd.length > max || passwd.length < min) {
        updateTips(n, o);
        return false;
    } else {
        updateTips(n, o, true);
        return true;
    }
}
//大小验证
function checkCapacity(o, min, max, tips) {
    var value = parseInt($.trim(o.val()), 10);
    if (value > max || value < min) {
        updateTips(tips, o);
        return false;
    } else {
        updateTips(tips, o, true);
        return true;
    }
}
//============ip-range
function ipRegexp_range(ip, tips, input_tips) {
    var aa = /^([0-9]|[.])+~([0-9]|[.])*$/;
    if (aa.test(ip)) {
        if (ipRegexp(ip.split("~")[0], tips, input_tips) && ipRegexp(ip.split("~")[1], tips, input_tips)) {
            input_tips.removeClass("ui-state-error");
            input_tips.siblings(".error_tip").hide();
            return true;
        } else {
            return false;
        }
    } else {

        var n = "IP Pool Range的格式必须为“192.168.1.101~192.168.1.110”的方式指定起止范围";
        updateTips(n, tips, input_tips);
        return false
    }

}
//ip格式验证
function ipRegexp(ip, tips, input_tips) {
    var val = /([0-9]{1,3}\.){3}[0-9]{1,3}/;
    var vald = val.exec(ip);
    //alert(ip+'---'+vald);
    var n = 'IP格式有误,正确的格式例如：192.168.1.1';
    if (input_tips.attr('id') == 'ddog_hosts') {
        var n = 'IP格式有误,正确的格式例如：192.168.1.2:9500';
    }
    if (vald == null) {
        updateTips(n, tips, input_tips);
        return false;
    }
    if (vald != '') {
        if (vald[0] != ip) {
            updateTips(n, tips, input_tips);
            return false;
        }
    }
    var ip_s = ip.split('.')
    for (i = 0; i < ip_s.length; i++) {
        if (parseInt(ip_s[i]) > 255) {
            updateTips(n, tips, input_tips);
            return false;
        }
    }
    input_tips.removeClass("ui-state-error");
    input_tips.siblings(".error_tip").hide();
    return true;
}
//空格隔开多ip验证
function ipRegexp_group(ip, tips, input_tips) {
    ips = ip.split(" ");
    var boolens = true;
    for (var i = 0; i < ips.length; i++) {
        boolens = boolens && checkipRegexp_1(ips[i], input_tips, tips);
    }
    if (boolens) {
        return true
    } else {
        return false
    }
}

function checkipRegexp_1(o, input_tips, n) {
    var value = o;
    reqexp = /([0-9]{1,3}\.){3}[0-9]{1,3}/;
    var vald = reqexp.exec(value);
    if (vald == null) {
        input_tips.addClass("ui-state-error");
        updateTips(n, input_tips);
        return false;
    }
    if (vald != '') {
        if (vald[0] != value) {
            input_tips.addClass("ui-state-error");
            updateTips(n, input_tips);
            return false;
        }
    }
    var ip_s = value.split('.')
    for (i = 0; i < ip_s.length; i++) {
        if (parseInt(ip_s[i]) > 255) {
            input_tips.addClass("ui-state-error");
            updateTips(n, input_tips);
            return false;
        }
    }
    input_tips.removeClass("ui-state-error");
    input_tips.siblings(".error_tip").hide();
    return true;
}
//ip验证  
function checkipRegexp(o, regexp, n) {
    var value = $.trim(o.val());
    if (!(regexp.test(value))) {
        updateTips(n, o);
        return false;
    } else {
        var ip_s = value.split('.')
        for (i = 0; i < ip_s.length; i++) {
            if (parseInt(ip_s[i]) > 255) {
                updateTips(n, o);
                return false;
            }
        }
        updateTips(n, o, true);
        return true;
    }
}
//验证为空
function checkNull(o, n) {
    return checkValueNull(o, o.val(), n);
}

function checkValueNull(o, val, n) {
    if ($.trim(val).length <= 0) {
        updateTips(n, o, false);
        return false;
    } else {
        updateTips(n, o, true);
        return true;
    }
}

function checkClusterNull(o, n) {
    if ($.trim(o.attr('realvalue')).length <= 0) {
        o.addClass("ui-state-error");
        updateTips(n, o);
        return false;
    } else {
        o.removeClass("ui-state-error");
        o.siblings(".error_tip").hide();
        return true;
    }
}

function checkdouble(o, n, regexp, c) {
    if (!(regexp.test(n))) {
        updateTips(c, o);
        return false;
    }
    return true;
}

function check_license_file(o) {
    var value = $.trim(o.val());
    if (value == '') {
        updateTips("必须选择要上传的模板文件", o);
        o.blur();
        return false;
    }
    var strTemp = value.substr(value.lastIndexOf(".") + 1).toLowerCase();
    //var strTemp = value.split(".");
    /* if(strTemp.length<=2)
     { 
     updateTips('授权文件的格式为 *.tar.gz',o);
     o.blur();
     return false;
     }*/
    //  strTemp = strTemp[strTemp.length-2]+strTemp[strTemp.length-1];
    if (strTemp == 'tar') {
        return true;
    } else {
        updateTips('授权文件的格式应为 *.tar', o);
        o.blur();
        return false;
    }

    return true;
}

function checkPasswd(new_passwd, re_passwd, n) {
    if (new_passwd.val() != re_passwd.val()) {
        updateTips(n, re_passwd);
        return false;
    } else {
        updateTips(n, re_passwd, true);
        return true;
    }
}
/*控制键盘只能输入数字和退格键 num数字的位数*/
function input_len_keydown(o, num) {
    if (num == "" || num == "undefined") {
        num = 2;
    }
    o.keydown(function (e) {
        k = e.keyCode
        if ((k <= 57 && k >= 48) || (k <= 105 && k >= 96)) {
            if ($.trim(o.val()).length >= num) {
                return false
            }
            return true;
        } else if (k == 8 || k == 9) {
            return true;
        } else {
            return false
        }
    })
}
// 密码中间不能有空格
function string_between_null(o, n) {
    var value = $.trim(o.val()).split("");
    var s_b = true;
    for (var i = 0; i < value.length; i++) {
        if (value[i] == " ") {
            s_b = false;
            break;
        }
    }
    if (!s_b) {
        o.addClass("ui-state-error");
        updateTips(n, o);
        return false;
    } else {
        o.removeClass("ui-state-error");
        o.siblings(".error_tip").hide();
        return true;
    }
}


/*drop list js*/
/*-----------------------------------------------------------------------*/
function title_for_firefox(o, string) {
    if (navigator.userAgent.indexOf("Firefox") > 0) {
        if (string.length > 60) {
            o.attr("title", string.slice(0, 59) + " " + string.slice(60));
            if (string.slice(60).length > 60) {
                o.attr("title", string.slice(0, 59) + " " + string.slice(60, 119) + " " + string.slice(120));
                if (string.slice(120).length > 60) {
                    o.attr("title", string.slice(0, 59) + " " + string.slice(60, 119) + " " + string.slice(120, 179) + " " + string.slice(180));
                    if (string.slice(180).length > 60) {
                        o.attr("title", string.slice(0, 59) + " " + string.slice(60, 119) + " " + string.slice(120, 179) + " " + string.slice(180, 239) + " " + string.slice(240));
                    }
                }
            }
        }
    }
}
/*-----------------------------------------------------------------------*/
//iprange 验证
function checkipBool(ipval) {
    var value = $.trim(ipval);
    regexp = /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/i
    if (!(regexp.test(value))) {
        return false;
    } else {
        var ip_s = value.split('.')
        for (i = 0; i < ip_s.length; i++) {
            if (parseInt(ip_s[i]) > 254) {
                return false;
            }
        }
        return true;
    }
}

function checkiprangeTilde(ippre, ipTilde) {
    var tilde_pre = parseInt(ipTilde.split('~')[0]);
    var tilde_last = parseInt(ipTilde.split('~')[1]);
    if (isNaN(tilde_last) || isNaN(tilde_pre)) {
        return false;
    }
    if (parseInt(tilde_last) >= 255) {
        return false;
    }
    if ((parseInt(tilde_pre) - parseInt(tilde_last)) >= 0) {
        return false;
    }

    //for (tilde_i=tilde_pre; tilde_i<tilde_last; tilde_i++){
    //    console.log(tilde_i)
    //}
    return true;
}

function checkiprangeBracket(iprangeval) {
    var iprangevals = iprangeval.split('[');
    ippre = iprangevals[0];

    iprange = iprangeval.substring(iprangeval.indexOf("[") + 1, iprangeval.indexOf("]"));
    ipranges = iprange.split(',')
    for (ipindex = 0; ipindex < ipranges.length; ipindex++) {
        var iplast = ipranges[ipindex];
        if (iplast.indexOf('~') > 0) {
            result = checkiprangeTilde(ippre, iplast);
        } else {
            result = checkipBool(ippre + iplast)
        }
        if (!result) {
            return false;
        }
    }
    return true;
}

function checkIpinputRegexp(o, n) {
    var value = $.trim(o.val());
    if (value) {
        var values = value.split(';');
        for (i = 0; i < values.length; i++) {
            iprangeval = values[i];
            result = true;
            if (iprangeval.indexOf('[')) {
                result = checkiprangeBracket(iprangeval);
            } else {
                result = checkipBool(iprangeval);
            }
            if (!result) {
                updateTips(n, o);
                return false;
            }
        }
        updateTips(n, o, true);
        return true;
    } else {
        updateTips(n, o, false);
        return false;
    }
}

function checkOnlyInitator(initiator_input,ul) {
    var initiator = initiator_input.val();
    var $lis = ul.find('li');
    var initiators = initiator.split(';');
    var already_initiators = [];
    if(!checkInputOnly(initiators)) {
        updateTips('不允许输入重复的initiator。', initiator_input, false);
        return false;
    }
    for (var i = 0; i < $lis.length; i++) {
        var already_initiator = $lis[i].textContent;
        var split_already_initiator = already_initiator.split(';');
        var already_initiator_arr = getInitiator(split_already_initiator);
        already_initiators = already_initiators.concat(already_initiator_arr);
    }
    for (var i = 0; i < initiators.length; i++) {
        for (var j = 0; j < already_initiators.length; j++) {
            if(already_initiators[j] == initiators[i]) {
                updateTips('initiator不允许重复。', initiator_input, false);
                return false;
            }
        }   
    }
    updateTips('', initiator_input, true);
    return true;
}

function getInitiator(split_already_ip) {
    var result = [];
    for (var i = 0; i < split_already_ip.length; i++) {
        result.push(split_already_ip[i]);
    }
    return result;
}

function checkOnlyIp(ip_input,ul) {
    var ip = ip_input.val();
    var $lis = ul.find('li');
    var ips = ip.split(';');
    var already_ips = [];
    var input_ips = [];
    if(!checkInputOnly(ips)) {
        updateTips('不允许输入重复的ip地址。', ip_input, false);
        return false;
    }
    for (var i = 0; i < $lis.length; i++) {
        var already_ip = $lis[i].textContent;
        var split_already_ip = already_ip.split(';');
        var already_ip_arr = getIP(split_already_ip);
        already_ips = already_ips.concat(already_ip_arr);
    }
    var ip_arr = getIP(ips);
    input_ips = input_ips.concat(ip_arr);
    for (var i = 0; i < input_ips.length; i++) {
        for (var j = 0; j < already_ips.length; j++) {
            if(already_ips[j] == input_ips[i]) {
                updateTips('ip地址不允许重复。', ip_input, false);
                return false;
            }
        }   
    }
    updateTips('', ip_input, true);
    return true;
}

function getIP (split_already_ip) {
    var result = [];
    for (var i = 0; i < split_already_ip.length; i++) {
        var ind = split_already_ip[i].indexOf('~');
        if ( ind > -1) {
            var begin = parseInt(split_already_ip[i].substring( split_already_ip[i].indexOf('[') + 1,ind));
            var end = parseInt(split_already_ip[i].substring(ind + 1, split_already_ip[i].indexOf(']')));
            var last_point_index = split_already_ip[i].lastIndexOf('.');
            var pre_ip = split_already_ip[i].substring(0,last_point_index + 1);
            for (var j = begin; j < end + 1; j++) {
                result.push(pre_ip + j);
            }
        } else {
            result.push(split_already_ip[i]);
        }
    }
    return result;
}

function checkInputOnly(arr) {
    var inputs = getIP(arr).sort();
    for(var i=0;i<inputs.length;i++){ 
        if (inputs[i] == inputs[i+1]){ 
            return false;
        }
    }
    return true;
}

function checkCHAP(chap_name, chap_password) {
    var bValid = true;
    bValid = bValid && checkNull(chap_name, "CHAP用户不允许为空");
    bValid = bValid && checkLength(chap_name, "CHAP用户", 3, 32);
    bValid = bValid && checkNull(chap_password, "CHAP密码不允许为空");
    bValid = bValid && checkLength(chap_password, "CHAP密码", 12, 16);
    return bValid
}

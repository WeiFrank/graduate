//=======================================================================
$(document).ready(function () {
    $.jgrid.defaults.styleUI = "Bootstrap";
    $.jgrid.defaults.loadui = "block";
});

var mainpanelHeight = parseInt($(window).height()) - 315;

if (mainpanelHeight < 300) {
    mainpanelHeight = 300;
}

function jqgrid_resize($el) {
    if ($('.ui-jqgrid-view').length == 0) {
        return;
    }
    if($el.length == 0) {
        return;
    }
//    console.log('elele')
//    console.log($el)
    var $gridBody = $el.parent('.ui-jqgrid-view');
//    console.log('body')
//    console.log($el.parent())
    var $grid = $el;
    var height = 47 * $grid.getGridParam('rowNum') + 1 < mainpanelHeight ? mainpanelHeight : 47 * $grid.getGridParam('rowNum') + 300;
//    console.log('lllllllllllllllllllllllll')
//    console.log($grid.getGridParam('rowNum'))
    $grid.setGridHeight(height);
    var outerwidth = $gridBody.width();
//    console.log(outerwidth)
    $grid.setGridWidth(700);
}

var pre_window_height = $(window).height();

function mainpanel_resize() {
    //var jqgrid_view_id = $(".ui-jqgrid-view").attr('id');
    var mainpanelMinHeight = $(window).height();
    var mainHeight = document.body.offsetHeight
    /*if (jqgrid_view_id !=  undefined && mainpanelMinHeight < pre_window_height){
     mainpanelMinHeight = mainpanelMinHeight + 13; //jqgrid页面时，获取高度不准确,在此处加13px
     }*/
    /*mainpanelMinHeight += 'px';*/


    $(".mainpanel").css({
        "min-height": mainpanelMinHeight,
    });
}
$(document).ready(function () {
    mainpanel_resize();
});
$(window).resize(function () {
    jqgrid_resize();
});

//jqgrid page-nav
function showRowNum(list_target_page, records) {
    $("#" + list_target_page.id).jqGrid('setGridParam', {rowNum: records}).trigger("reloadGrid");
}

function jqgrid_page(el, data) {
//     console.log(el)
    var $target_page = el.parent().parent().parent().parent().parent().siblings('.grid-tools');
//    var $target_page = el.parent().parent().parent().parent().parent().siblings('#gridpager');
    console.log($target_page)
    $target_page.find('.grid-pager').remove();
    var page = el[0].p.page;
    console.log(page)
    var rowNum = el[0].p.rowNum;
    console.log(rowNum)
    var records = el[0].p.records;
    var totalPage = Math.ceil(records / rowNum);
    totalPage = totalPage == 0 ? 1 : totalPage;
    var htmlArr = ['<div class="grid-pager pull-right">', '<select class="f-select">',
        '<option ' + (rowNum == 3 ? 'selected = "selected"' : '') + ' value="3">3</option>',
        '<option ' + (rowNum == 6 ? 'selected = "selected"' : '') + ' value="6">6</option>',
        '<option ' + (rowNum == 9 ? 'selected = "selected"' : '') + 'value="9">9</option>', '</select>',
        '<div class="btn-group">', '<button type="button" class="btn btn-white">共 ' + records + ' 项 / ' + totalPage + ' 页</button>',
        '<button type="button" rid="1" class="btn btn-white ' + (page == 1 ? 'not-available" disabled' : '"') + '><i class="fa fa-angle-double-left"></i></button>',
        '<button type="button" rid="2" class="btn btn-white ' + (page == 1 ? 'not-available" disabled' : '"') + '><i class="fa fa-angle-left"></i></button>',
        '<button type="button" class="btn btn-white">' + page + '</button>',
        '<button type="button" rid="3" class="btn btn-white ' + (page == totalPage ? 'not-available" disabled' : '"') + '><i class="fa fa-angle-right"></i></button>',
        '<button type="button" rid="4" class="btn btn-white ' + (page == totalPage ? 'not-available" disabled' : '"') + '><i class="fa fa-angle-double-right"></i></button>',
        '</div>',
        '<span>跳转</span>',
        '<input type="text">',
        '<button type="button" rid="go" class="btn btn-white btn-turn">GO</button>',
        '</div>'
    ];
    var html = htmlArr.join('');
    $target_page.append(html);

    var $pager = $target_page.find('.grid-pager');
    var $pagenumList = $pager.find('select');
    var $input = $pager.find('input');
    $pagenumList.on('change', function () {
        el.jqGrid('setGridParam', {page: 1, rowNum: $(this).val()}).trigger("reloadGrid");
    });

    $pager.find('button[rid=1]').on('click', function () {
        el.jqGrid('setGridParam', {page: 1, rowNum: $pagenumList.val()}).trigger("reloadGrid");
    });

    $pager.find('button[rid=2]').on('click', function () {
        el.jqGrid('setGridParam', {page: page - 1, rowNum: $pagenumList.val()}).trigger("reloadGrid");
    });

    $pager.find('button[rid=3]').on('click', function () {
        el.jqGrid('setGridParam', {page: page + 1, rowNum: $pagenumList.val()}).trigger("reloadGrid");
    });

    $pager.find('button[rid=4]').on('click', function () {
        el.jqGrid('setGridParam', {page: totalPage, rowNum: $pagenumList.val()}).trigger("reloadGrid");
    });
    $pager.find('button[rid=go]').on('click', function () {
        var value = $input.val();
        if (isNaN(value)) {
            value = 1;
        } else {
            if (value < 1) {
                value = 1
            } else if (value > totalPage) {
                value = totalPage;
            }
        }
        el.jqGrid('setGridParam', {page: parseInt(value), rowNum: $pagenumList.val()}).trigger("reloadGrid");
    });
}

function get_event_page_info(list_target_page) {
    var re_records = list_target_page.getGridParam('records'); //获取返回的记录数
    var re_page = list_target_page.getGridParam('page'); //获取返回的当前页
    var re_rowNum = list_target_page.getGridParam('rowNum'); //获取每页数
    var re_total = list_target_page.getGridParam("lastpage");
    var re_pre = parseInt(re_page) - 1;
    var re_next = parseInt(re_page) + 1;
    if (re_next >= re_total)
        re_next = re_total;
    if (re_pre <= 1)
        re_pre = 1;
    return {"re_pre": re_pre, "re_next": re_next};
}

//错误和确认操作弹出框
$(function () {
    isArray = function (obj) {
        return Object.prototype.toString.call(obj) === '[object Array]';
    }
    SelfConfirm = function (msg, callback, params, title) {
        if (typeof(title) == "undefined") {
            title = '确认提示'
        }
        angular.element('#global_confirm_modal').scope().open(msg, callback, params, title, true);
    }
    SelfAlert = function (msg, title) {
        if (typeof(title) == "undefined") {
            title = '错误提示'
        }
        angular.element('#global_confirm_modal').scope().open(msg, '', '', title, false, false, true);
    };

    SelfRedirect= function (msg, title) {
        if (typeof(title) == "undefined"){
            title = '跳转提示'
        }
        angular.element('#global_confirm_modal').scope().open(msg, '', '', title, false, true);
    };  

    SelfTranslate = function (key) {
        return angular.element('#global_confirm_modal').scope().translate(key);
    }
});

function set_tables() {
    var trs = $(".modal-body").find("tr");
    for (var i = 0; i < trs.length; i++) {
        if (i % 2 == 0) {
            trs[i].style.background = "#f5fafa";
        } else {
            trs[i].style.background = "#fff";
        }
    }
};

function _multi_checkbox_get_ids(selector) {
    var pd_ids = ''
    selector.each(function () {
        if ($(this).attr('checked') == true || $(this).attr('checked') == "checked") {
            pd_ids += $(this).val() + ",";
        }
    });
    return pd_ids
}


function get_repnums() {
    var repnums = new Array();
    var repnum_range = 4;
    for (repnum = 2; repnum <= repnum_range; repnum++) {
        var values = new Array();
        values[0] = repnum;
        values[1] = repnum;
        repnums.push(values);
    }
    return repnums
}

function get_tiers() {
    var tiers = new Array();

    var show = new Array();
    show[0] = '高速层'
    show[1] = '低速层'
    show[-1] = '自动分层'

    var tier_range = 2;
    for (tier = -1; tier < tier_range; tier++) {
        var values = new Array();
        values[0] = tier;
        values[1] = show[tier];
        tiers.push(values);
    }
    return tiers
}

function get_periods() {
    var periods = new Array();
    var show = new Array();
    show[0] = 'seconds'
    show[1] = 'minites'
    show[2] = 'hours'
    show[3] = 'days'
    show[4] = 'months'
    show[5] = 'years'
    var period_range = 6;
    for (p = 0; p < period_range; p++) {
        var values = new Array();
        values[0] = p;
        values[1] = show[p];
        periods.push(values);
    }
    return periods
}

function isContains(str, substr) {
    return new RegExp(substr).test(str);
}
//user login timeout 
function resetLoginTime() {
    $.ajax({
        type: "get",
        url: "/is_login",
        async: false,
        success: function (data) {
            if (data == 'False') {
                window.location.href = "/login";
            }
        },
        error: function (XHR) {
            if (XHR.status == 0) {
                window.location.href = "/login";
            }
        }
    })
    clearTimeout(myTime);
    myTime = setTimeout('LoginTimeout()', sessionTimeout);
}

function LoginTimeout() {
    var current_name = "{{ session.user.name }}"
    $.get("/session_timeout", {"username": current_name}, function (data) {
        if (data == 'SUCC') {
            window.location.href = "/login";
        }
    });
}

function reload_warning_num() {
    $.get("/alert/count", function (data) {
        //$("#warning_num").text(data);
        if (parseInt(data) > 0 && parseInt(data) < 100) {
            $("#warning_num").css('display', 'block');
            //$("#warning_num").text(data);
        } else if (parseInt(data) > 99) {
            $("#warning_num").css('display', 'block');
            //$("#warning_num").text("99+")
        } else {
            $("#warning_num").css('display', 'none');
        }
        $("#grid_alert_table").trigger('reloadGrid');
    })
}
//system-alert show
var refresh_timeout;

function login_timeout_timer() {
    reload_warning_num();
    clearTimeout(refresh_timeout)
    refresh_timeout = setTimeout('login_timeout_timer()', 60000);
}

function rtrim(s) {
    return s.replace(/\;*$/g, '');
}

function detail_open(gid, rid) {
    var detail_title = '';
    var detail_content = '';
    var html = '';
    var colNames = $("#" + gid).jqGrid('getGridParam', 'colNames');
    var colModel = $("#" + gid).jqGrid('getGridParam', 'colModel');
    html += '<div class="detail-box"><div class="detail-keyvalue"><div class="detail-key">属性</div><div class="detail-value">值</div></div><div class="detail-content">';
    for (var i = 0; i < colModel.length; i++) {
        if (colModel[i].name == 'cb') {
            continue;
        }
        if (colModel[i].hidden) {
            continue;
        }

        if (colModel[i].detailHidden) {
            continue;
        }
        detail_title = "<div class='detail-title'>" + colNames[i] + ":</div>";
        detail_content = "<div class='detail-text'>" + $("#" + gid).jqGrid('getCell', rid, colModel[i].name) + "</div><br/>";
        html += detail_title + detail_content;
    }

    html += '</div></div>';
    angular.element('#grid_detail_controller').scope().open(html);
}

function bindMouseEvent(id, obj) {
    /* 为小图标绑定鼠标移入移出事件 */
    //obj  的键值对：
    //      key：class为fa-question-circle的i元素的itype的值
    //      value：与key对应的值
    $('.fa-question-circle').on('mouseover', function () {
        var itype = $(this).attr('itype');
        var $parent = $(this).parent();
        var $tip = $(id).find('.tip');

        var text = obj[itype];
        $tip.find('p').text(text);

        //计算tip的位置
        var fright;
        var top = $(this)[0].offsetTop;
        var left = $(this)[0].offsetLeft;
        var ptop = $parent[0].offsetTop;
        var theight = $tip.height();
        var twidth = $tip.outerWidth();

        var totalRight = $parent.outerWidth(true) - left;
        var tright = twidth * 0.2;

        var ftop = (top + ptop - theight - 20) + 'px';

        if (!$parent.next().get(0)) {
            fright = (totalRight - tright - 4 + 35) + 'px';
        } else {
            fright = (totalRight - tright - 4 + 350) + 'px';
        }
        $tip.css({
            'top': ftop,
            'right': fright
        });
    }).on('mouseout', function () {
        var $tip = $(id).find('.tip');
        $tip.css({
            'top': '-9999px',
            'right': '-9999px'
        });
    });
}

function makeEllipsis(cellvalue, option, type) {
    var gid = option.gid;
    var colModNm = option.colModel.name;
    var outerWidth = $('#' + gid + '_' + colModNm).width() - 20;
    var html = '';
    switch (type) {
        case 'span':
            html += '<span style="display:inline-block;text-overflow:ellipsis; white-space:nowrap;overflow:hidden;width:' + outerWidth + 'px;">' + cellvalue + '</span>';
            break;
        default:
            html += '<a style="display:inline-block;text-overflow:ellipsis; white-space:nowrap;overflow:hidden;width:' + outerWidth + 'px;" ' +
                ' href="#" onclick="detail_open(\'' + option.gid + '\',\'' + option.rowId + '\')">' + cellvalue + '</a>'

    }
    return html;
}

function row2object(row, gid) {
    var row_obj = {}
    var colModel = $("#" + gid).jqGrid('getGridParam', 'colModel');
    var j = 0;
    for (var i = 0; i < colModel.length; i++) {
        if(colModel[i].name == 'cb') {
            continue;
        }
        row_obj[colModel[i].name] = row[j++];
    }
    return row_obj;
}

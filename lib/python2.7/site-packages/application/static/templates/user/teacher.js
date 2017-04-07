var enable_submit=true;
function register_teacher(){
var bValid = true;
var teacher_number=$("#teacher_register_modal").find("#login-teacher")

var password=$("#teacher_register_modal").find("#teacher_password")
var mail=$("#teacher_register_modal").find("#teacher_mail")

if(bValid){
if(enable_submit) {
enable_submit = false;
var $submitBtn = $('.modal-footer').find('.btn-blue');
$submitBtn.html('<i class="fa fa-spinner fa-spin" style="margin:3px 6px;"></i>');
 $('.rtn-tip').slideUp('fast');
  $.post("/user/teacher/create",{
      "teacher_number":$.trim(teacher_number.val()),
      "password":$.trim(password.val()),
      "e_mail":$.trim(mail.val()),
  },function(data){
      var data=eval("("+data+")");;
      console.log(typeof(data));
      console.log(data);
         if (data.reply.is_success){
           enable_submit = true;
       }else{
       console.log(typeof(data));
        console.log(data);
         var error = data.reply.error;
         $('.rtn-tip').text(error).slideDown('fast');
         $submitBtn.html('ok');
         enable_submit = true;
       }

     });
     }
  }
}


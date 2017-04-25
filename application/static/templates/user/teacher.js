var enable_submit=true;
function register_teacher(){
var bValid = true;
var teacher_number=$("#teacher_register_modal").find("#login-teacher")
var name=$("#teacher_register_modal").find("#teacher_name")
var password=$("#teacher_register_modal").find("#teacher_password")
var mail=$("#teacher_register_modal").find("#teacher_mail")
var college=$("#teacher_register_modal").find("#teacher_college")
var subject=$("#teacher_register_modal").find("#teacher_subject")
var role=$("#teacher_register_modal").find("#teacher_role")
if(bValid){
if(enable_submit) {
enable_submit = false;
var $submitBtn = $('.modal-footer').find('.btn-blue');
$submitBtn.html('<i class="fa fa-spinner fa-spin" style="margin:3px 6px;"></i>');
 $('.rtn-tip').slideUp('fast');
  $.post("/user/create",{
      "identity":'t',
      "teacher_number":$.trim(teacher_number.val()),
      "teacher_password":$.trim(password.val()),
      "teacher_name":$.trim(name.val()),
      "teacher_mail":$.trim(mail.val()),
      "teacher_role":$.trim(role.val()),
      "teacher_college":$.trim(college.val()),
      "teacher_subject":$.trim(subject.val()),
      "teacher_role":$.trim(role.val()),
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


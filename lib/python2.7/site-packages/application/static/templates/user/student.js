      var enable_submit=true;
      function register_student(){
     var bValid = true;
     var name=$("#student_register_modal").find("#login-student")
     var password=$("#student_register_modal").find("#student_password")
    console.log(name.val())
     var mail=$("#student_register_modal").find("#student_mail")


     if(bValid){
         if(enable_submit) {
            enable_submit = false;
            var $submitBtn = $('.modal-footer').find('.btn-blue');
            $submitBtn.html('<i class="fa fa-spinner fa-spin" style="margin:3px 6px;"></i>');
             $('.rtn-tip').slideUp('fast');
              $.post("/user/student/create",{
                  "student_number":$.trim(name.val()),
                  "e_mail":$.trim(mail.val()),
                  "password":$.trim(password.val()),
              },function(data){
                  var data=eval("("+data+")");;
                  console.log(typeof(data));
                  console.log(data);
                     if (data.reply.is_success){
//                         var success_msg = data.
//                        $('.rtn-tip').text(success_msg).slideDown('fast')
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


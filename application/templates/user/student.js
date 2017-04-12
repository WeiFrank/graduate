      var enable_submit=true;
      function register_student(){
     var bValid = true;
     var number=$("#student_register_modal").find("#login-student")
     var password=$("#student_register_modal").find("#student_password")
//     var job=$("#student_register_modal").find("#student_job")
//     console.log(job.val())
     var name=$("#student_register_modal").find("#student_name")
     var mail=$("#student_register_modal").find("#student_mail")
     var college=$("#student_register_modal").find("#student_college")
     var subject=$("#student_register_modal").find("#student_subject")
     var student_class=$("#student_register_modal").find("#student_class")
     var student_role=$("#student_register_modal").find("#student_role");
     var student_time=$("#student_register_modal").find("#student_time");


     if(bValid){
         if(enable_submit) {
            enable_submit = false;
            var $submitBtn = $('.modal-footer').find('.btn-blue');
            $submitBtn.html('<i class="fa fa-spinner fa-spin" style="margin:3px 6px;"></i>');
             $('.rtn-tip').slideUp('fast');
              $.post("/user/create",{
                  "identity":'s',
                  "student_number":$.trim(number.val()),
                  "student_mail":$.trim(mail.val()),
                  "student_password":$.trim(password.val()),
                  "student_name":$.trim(name.val()),
                  "student_college":$.trim(college.val()),
                  "student_subject":$.trim(subject.val()),
                  "student_class":$.trim(student_class.val()),
                  "student_role":$.trim(student_role.val()),
                  "student_time":$.trim(student_time.val()),
              },function(data){
                  var data=eval("("+data+")");;
                  console.log(typeof(data));
                  console.log(data);
                     if (data.reply.is_success){

                        $('.rtn-tip').text(data.reply.success_msg).slideDown('fast')
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


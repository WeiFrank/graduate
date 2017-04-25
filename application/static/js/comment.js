var enable_submit=true;
     function submit_comment(){
        var bValid = true;

        var aid = $(".comment-reply").attr("ans-id");
        var content = $("#comment-write").val();
        console.log(aid)
        console.log(content)
         if(bValid){
         if(enable_submit) {
            enable_submit = false;

             $('.rtn-tip').slideUp('fast');
              $.post("/qa/comment/add",{
                "aid":aid,
                "content":content,
              },function(data){
                  var data=eval("("+data+")");
                   if (data.reply.is_success){

                       enable_submit = true;
                   }else{
                     var error = data.reply.error;
                     $('.rtn-tip').text(error).slideDown('fast');

                     enable_submit = true;
                   }
              });
          }
       }
};
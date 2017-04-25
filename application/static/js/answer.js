$(document).ready(function() {

    $("#submit").click(function(){
         var content = $("#answer-write").val();
        $.post("/qa/answer/add", {
                 "qid": $(".qid").text(),
                 "rid": $("#reply-info").attr("rid"),
                 "rtype": $("#reply-info").attr("rtype"),
                 "content": content,
                 },function(data){
                    $("#reply-info").attr("rtype", "1");
                   data=eval("("+data+")");
                 if(data.reply.is_success){

                  window.location.reload();
            }

        });
    });
    $("#reply-answer").click(function(){
        $("#reply-info").attr("rtype", "2");
        $("#reply-info").attr("rid", $(this).attr("ans-id"));
        console.log( $("#reply-info").attr("rid", $(this).attr("ans-id")))
    });
});
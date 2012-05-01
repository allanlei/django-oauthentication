$(window).load(function(){
    $("#serviceSelector").change(function(e){
        $("form.login").hide();
        $("#" + $(this).val()).show();
    }).trigger("change");
});

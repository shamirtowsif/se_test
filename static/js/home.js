$(document).ready(function(){

    $("#loginModal form").submit(function(e){
        e.preventDefault();

        $.ajax({
            url: "/login/",
            type: "POST",
            data: $(this).serialize(),
            success: function(){
                location.reload();
            }
        });
    });


    $("#signupModal form").submit(function(e){
        e.preventDefault();

        $.ajax({
            url: "/signup/",
            type: "POST",
            data: $(this).serialize(),
            success: function(){
                location.reload();
            }
        });
    });

    $("#logoutBtn").click(function(){

        $.ajax({
            url: "/logout/",
            type: "POST",
            data: {
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(){
                location.reload();
            }
        });

    });

});

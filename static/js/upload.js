$(document).ready(function () {

    $("#upload-form").on("submit", function (e) {
        e.preventDefault();

        let formData = new FormData();
        let fileInput = $("#video-input")[0].files[0];

        if (!fileInput) {
            alert("Please select a video file.");
            return;
        }

        formData.append("video", fileInput);

        $.ajax({
            url: "/videos/upload/",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                "X-CSRFToken": $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function (response) {
                window.location.href = "/profile/";
                console.log(response);
            },
            error: function (xhr) {
                console.log(xhr.responseText);
            }
        });
    });
});

$(document).ready(function() {

    function renderVideos(videos) {

        const grid = $("#video-grid");
        grid.empty();

        $("#profile-stats").text(
            `0 Following · 0 Followers · ${videos.length} Videos`
        );

        if (!videos.length) {
            grid.append("<p class='text-muted'>No videos uploaded yet.</p>");
            return;
        }

        videos.forEach(function(video) {

            const card = `
                <div class="col-md-3 mb-4">
                    <a href="/video/${video.id}/" class="text-decoration-none text-dark">
                        <div class="video-card">
                            <video muted>
                                <source src="${video.video_url}" type="video/mp4">
                            </video>
                        </div>
                        <div class="video-title">
                            ${video.title}
                        </div>
                    </a>
                </div>
            `;

            grid.append(card);
        });
    }

    function loadVideos() {

        $.ajax({
            url: "/videos/",
            method: "GET",
            dataType: "json",

            success: function(response) {
                renderVideos(response);
            },

            error: function() {
                $("#video-grid").html(
                    "<p class='text-danger'>Error loading videos.</p>"
                );
            }
        });
    }

    loadVideos();

});

$(document).ready(function() {
    function timeAgo(dateString) {
        const now = new Date();
        const past = new Date(dateString);
        const seconds = Math.floor((now - past) / 1000);

        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(seconds / 3600);
        const days = Math.floor(seconds / 86400);
        const weeks = Math.floor(seconds / 604800);

        if (seconds < 60) return `${seconds}s`;
        if (minutes < 60) return `${minutes}m`;
        if (hours < 24) return `${hours}h`;
        if (days < 7) return `${days}d`;
        return `${weeks}w`;
    }
    const pathParts = window.location.pathname.split("/");
    const videoId = pathParts[pathParts.length - 2];

    $.ajax({
        url: `/videos/${videoId}/`,
        method: "GET",
        success: function(data) {

            $("#video-container").html(`
                <video class="w-100 rounded-top" controls>
                    <source src="${data.video_url}" type="video/mp4">
                </video>

                <div class="card-body">
                    <h5 class="card-title">${data.title}</h5>
                    <p class="card-text text-secondary">
                        Uploaded by ${data.uploaded_by} • ${timeAgo(data.uploaded_at)} ago
                    </p>

                    <div class="d-flex gap-3 mt-3">
                        <button class="btn btn-outline-light btn-sm">Like</button>
                        <button class="btn btn-outline-light btn-sm">Share</button>
                        <button class="btn btn-outline-light btn-sm">Comment</button>
                    </div>
                </div>
            `);
        },
        error: function() {
            $("#video-container").html("<p class='p-4'>Video not found</p>");
        }
    });

});

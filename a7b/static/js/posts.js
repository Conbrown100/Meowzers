function showError(message) {
    $('#messages').html(message);
}

function getProfileID() {
    return parseInt($('#profile-id').html());
}

function getPosts() {
    $.ajax({
        type: 'GET',
        url: '/api/posts/',
        data: { 'profile_id' : getProfileID() },
        dataType: 'json',
        success: function(posts) {
            posts.forEach(function(post) {
                insertPost(post);
            });
        },
        error: function() {
            showError('Cannot post. Try again later.');
            $('#btn-post').prop('disabled', false);
        }
    });

}

function insertPost(post) {
    $('#btn-post').prop('disabled', false);

    var posthtml = $('<div class="post rounded" postid="' + post.id + '"></     div>');
    posthtml.append('<p>' + post.content + '</p>');
    posthtml.append('<a href="#" class="do-like">Like</a> ' +
                    '<a href="#" class="show-likes">(0 likes)</a>');
    $('#posts').append(posthtml);
}

function sendPost() {
    var form = $('#post-form')[0];
    var data = new FormData(form);

    $('#btn-post').prop('disabled', true);

    $.ajax({
        type: 'POST',
        url: '/api/posts/',
        data: data,
        processData: false,
        contentType: false,
        success: insertPost,
        error: function() {
            showError('Cannot post. Try again later.');
            $('#btn-post').prop('disabled', false);
        }
    });
}

$(function() {
    getPosts();

    $('#btn-post').click(function(event) {
        event.preventDefault();
        sendPost();
    });
});


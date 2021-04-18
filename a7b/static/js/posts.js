function showError(message) {
    $('#messages').html(message);
}


function getProfileID() {
    return parseInt($('#profile-id').html());
}


function getMyProfileID() {
    return parseInt($('#my-profile-id').html());
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


function likePost(post){
    $.ajax({
        type: 'POST',
        url: '/api/posts/'+post.id+'/like/',
        success: function(returnPost){ 
          postElement = $('#posts').find('div[postid=' + returnPost.id + ']');
          postElement.find('.do-like').html('Unlike');
          postElement.find('.show-likes').html(returnPost.numLikes +' likes');
        }
    });
}


function unlikePost(post){
    $.ajax({
        type: 'POST',
        url: '/api/posts/'+post.id+'/unlike/',
        success: function(returnPost){ 
          postElement = $('#posts').find('div[postid=' + returnPost.id + ']');
          postElement.find('.do-like').html('Like');
          postElement.find('.show-likes').html(returnPost.numLikes +' likes');
        }
    });
}


function likedState(post) {
  myProfileID = getMyProfileID()
  if (post.likedBy.includes(myProfileID)){
      return "Unlike";
  }
  return "Like";
}


function insertPost(post) {
    $('#btn-post').prop('disabled', false);

    var posthtml = $('<div class="post rounded" postid="'+post.id+'"></     div>');
    posthtml.append('<p>' + post.content + '</p>');
    posthtml.append('<a href="#" class="do-like">'+likedState(post)+'</a> ' +
                    '<a href="#" class="show-likes">'+post.numLikes+' likes</a>');
    $('#posts').append(posthtml);
    //add ability to (un)like posts to link
    var thisPost = $('#posts').find('div[postid=' + post.id + ']');
    var likeLink = thisPost.find('.do-like');
    
    likeLink.click(function(event){
      event.preventDefault();
      if (likeLink.html() == 'Like'){
        likePost(post);
      }
      else{
        unlikePost(post);
      }
    });
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


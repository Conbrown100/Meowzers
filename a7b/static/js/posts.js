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


function showLikes(post) {
$.ajax({
    type: 'GET',
    url: '/api/posts/'+post.id+'/likes/',
    data: { 'profile_id' : getProfileID() },
    dataType: 'json',
    success: function(profiles) {
      var modalhtml = $('<div class=modal-body-content></div>');
      profiles.forEach(function(profile) {
        modalhtml.append('<p>' + profile.username + '</p>');  
      });
      $('.modal-body').html(modalhtml);
    },
    error: function() {
        $('.modal-body').html('Cannot show likes. Try again later.');
        showError('Cannot show likes. Try again later.');
    }
});
}


function insertPost(post) {
    $('#post-content').val('');
    $('#btn-post').prop('disabled', false);

    var posthtml = $('<div class="post rounded" postid="'+post.id+'"></     div>');
    posthtml.append('<p>' + post.content + '</p>');
    posthtml.append('<a href="#" class="do-like">'+likedState(post)+'</a> ' +
                    '<a href="#" class="show-likes" data-toggle="modal" data-target="#showLikesModal">'+post.numLikes+' likes</a>');
    $('#posts').append(posthtml);
    //add ability to (un)like posts to link
    var thisPost = $('#posts').find('div[postid=' + post.id + ']');
    var likeLink = thisPost.find('.do-like');
    var showLink = thisPost.find('.show-likes');
    
    likeLink.click(function(event){
      event.preventDefault();
      if (likeLink.html() == 'Like'){
        likePost(post);
      }
      else{
        unlikePost(post);
      }
    });

    showLink.click(function(event){
      event.preventDefault();
      $('.modal-body').html('');
      showLikes(post);
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


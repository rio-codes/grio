$.get('grioblog.csv', function(data) {
    var posts = data.trim().split('\n');
    var lastPost = (posts[posts.length - 1].split(','));
    var timeNow = jQuery.timeago(new Date()); 
    var timeSince= jQuery.timeago(lastPost[0]); 
    $('.post').append('Time since post: ' + timeSince + '<br>');
    $('.post').append('The post: ' + lastPost[1] + '<br>');
});
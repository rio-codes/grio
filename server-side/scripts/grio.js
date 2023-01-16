$.get('grioblog.csv', function(data) {
    var posts = data.trim().split('\n');
    var lastPost = (posts[posts.length - 1].split(','));
    var timeNow = jQuery.timeago(new Date()); 
    var timeSince= jQuery.timeago(lastPost[0]); 
    $('.grio__timestamp').append(timeSince + '<br>');
    $('.grio__post').append(lastPost[1] + '<br>');
});
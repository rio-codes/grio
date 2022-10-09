$.get('grioblog.csv', function(data) {
    var posts = data.trim().split('\n');
    var lastPost = posts[posts.length - 1].split(',');
    $(".post").append('This is the most recent date: ' + lastPost[0] + '<br>');
    $(".post").append('This is the most recent post: ' + lastPost[0]);
});
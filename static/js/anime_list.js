$(function() {
    $('button.subscribe-botton').on('click', function() {
        var mikan_id = $(this).attr('id');
        

        $.ajax({
          url: "/anime/subscribe_anime?mikan_id="+mikan_id,
          method: "POST",
          success: function(result) {
            console.log(result);
          },
          fail: function(error) {
            console.log(error);
          }
        })

    });
});
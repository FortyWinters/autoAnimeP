$(function() {
    $('button.update-button').on('click', function() {
        // 更新番剧列表
        $.ajax({
            url: "/anime/update_anime_list",
            method: "GET",
            success: function(result) {
                window.location.reload();
            },
            fail: function(error) {
                console.log(error);
            }
        })
    });

    $('button.subscribe-button').on('click', function() {
        var mikan_id = $(this).attr('id');
        var subscribe_status = $(this).attr('subscribe_status');

        if(subscribe_status == 0) {
            // 订阅番剧
            $.ajax({
              url: "/anime/subscribe_anime?mikan_id="+mikan_id,
              method: "POST",
              success: function(result) {
                console.log(result);
                window.location.reload();
              },
              fail: function(error) {
                console.log(error);
              }



    });
})


$(function() {
    $('button.subscribe-botton').on('click', function() {
        var mikan_id = $(this).attr('id');
        var subscribe_status = $(this).attr('subscribe_status');
        if(subscribe_status==0) {
          // 订阅番剧
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
          $(this).attr('subscribe_status', 1) 
          $(this).css("background-color", "red"); 

          // 更新种子
          $.ajax({
            url: "/anime/insert_anime_seed?mikan_id="+mikan_id,
            method: "POST",
            success: function(result) {
              console.log(result);
            },
            fail: function(error) {
              console.log(error);
            }
          })

        } else {
          // 取消订阅番剧
          $.ajax({
            url: "/anime/cancel_subscribe_anime?mikan_id="+mikan_id,
            method: "POST",
            success: function(result) {
              console.log(result);
            },
            fail: function(error) {
              console.log(error);
            }
          })
          $(this).attr('subscribe_status',0)
          $(this).css("background-color", "#d6d6d6"); 

          // 删除种子
          $.ajax({
            url: "/anime/delete_anime_seed?mikan_id="+mikan_id,
            method: "POST",
            success: function(result) {
              console.log(result);
            },
            fail: function(error) {
              console.log(error);
            }
          })

        }
    });
});
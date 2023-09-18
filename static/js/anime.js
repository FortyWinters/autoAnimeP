


$(function() {
    $('button.anime-button').on('click', function() {
        // 番剧列表更新
        $.ajax({
            url: "/anime/update_anime_list",
            method: "GET",
            async: false,
            success: function(result) {
                window.location.reload();
            },
            fail: function(error) {
                console.log(error);
            }
        })

        window.location.reload();
    });

    $('button.subscribe-button').on('click', function() {
        var mikan_id = $(this).attr('id');
        var subscribe_status = $(this).attr('subscribe_status');



        if(subscribe_status == 0) {
            // 订阅番剧
            $.ajax({
                url: "/anime/subscribe_anime?mikan_id="+mikan_id,
                method: "POST",
                async: false,
                success: function(result) {
                    console.log(result);
                    // update_button.disabled = false;
                },
                fail: function(error) {
                    console.log(error);
                }
            });

            // // 更新种子
            // $.ajax({
            //     url: "/anime/insert_anime_seed?mikan_id="+mikan_id,
            //     method: "POST",
            //     async: false,
            //     success: function(result) {
            //         console.log(result);
            //     },
            //     fail: function(error) {
            //         console.log(error);
            //     }
            // });

            // // 下载订阅番剧
            // $.ajax({
            //     url: "/anime/download_subscribe_anime?mikan_id="+mikan_id,
            //     method: "POST",
            //     async: false,
            //     success: function(result) {
            //         console.log(result)
            //     },
            //     fail: function(error) {
            //         console.log(error);
            //     }
            // });

            window.location.reload();
        } else {
            // 取消订阅番剧
            $.ajax({
                url: "/anime/cancel_subscribe_anime?mikan_id="+mikan_id,
                method: "POST",
                async: false,
                success: function(result) {
                    console.log(result);
                    update_button.disabled = true;
                    window.location.reload();
                },
                fail: function(error) {
                    console.log(error);
                }
            });

            window.location.reload();

            // 删除种子
            $.ajax({
                url: "/anime/delete_anime_seed?mikan_id="+mikan_id,
                method: "POST",
                async: false,
                success: function(result) {
                    console.log(result);
                },
                fail: function(error) {
                    console.log(error);
                }
            });

            window.location.reload();
        }
    });


    $('button.update-button').on('click', function() {
        var mikan_id = $(this).attr('id');
        console.log('update-button', mikan_id)
    });

    

})
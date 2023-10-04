$(function() {
    $('button.anime-button').on('click', function() {
        this.disabled = true;
        this.style.backgroundColor = "#d6d6d6";
        
        var path = window.location.pathname;
        var parts = path.split('/');
        var year = parts[2]; 
        var season = parts[3];

        fetch("/anime/update_anime_list?year=" + year +"&season=" + season, {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            console.log(data)
            this.disabled = false;
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
        });

    });

    $('button.subscribe-button').on('click', function() {
        var mikan_id = $(this).attr('id');
        var subscribe_status = $(this).attr('subscribe_status');
        this.disabled = true;
        this.style.backgroundColor = "#d6d6d6";

        if(subscribe_status == 0) {
            // 订阅番剧
            fetch("/anime/subscribe_anime?mikan_id="+mikan_id, {method: 'POST'})
            .then(response => response.json())
            .then(data => {
                console.log(data)
                this.disabled = false;
                window.location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
            });

        } else {
            // 取消订阅番剧
            fetch("/anime/cancel_subscribe_anime?mikan_id="+mikan_id, {method: 'POST'})
            .then(response => response.json())
            .then(data => {
                console.log(data)
                // 删除种子
                return fetch("/anime/delete_anime_seed?mikan_id="+mikan_id, {method: 'POST'});
            })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                this.disabled = false;
                window.location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    });

    $('button.update-button').on('click', function() {
        var mikan_id = $(this).attr('id');
        this.style.backgroundColor = "#d6d6d6";
        this.disabled = true;
        console.log(mikan_id);

        // 种子更新
        fetch("/anime/insert_anime_seed_thread?mikan_id="+mikan_id, {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            console.log(data)
            // 下载番剧
            return fetch("/anime/download_subscribe_anime?mikan_id="+mikan_id, {method: 'POST'});
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            this.style.backgroundColor = "orange";
            this.disabled = false;
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
})
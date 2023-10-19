$(function() {
    $('button.anime-button').on('click', function() {
        this.disabled = true;
        this.style.backgroundColor = "#d6d6d6";
        
        var path = window.location.pathname;
        var parts = path.split('/');
        var year = parts[2]; 
        var season = parts[3];

        // 更新番剧列表
        updateAnimeList(year, season)
    });

    $('button.subscribe-button').on('click', function() {
        var mikanId = $(this).attr('id');
        var subscribeStatus = $(this).attr('subscribe_status');
        this.disabled = true;
        this.style.backgroundColor = "#d6d6d6";

        if(subscribeStatus == 0) {
            // 订阅番剧
            subscribeAnime(mikanId)
        } else {
            // 取消订阅番剧
            cancleSubscribeAnime(mikanId)
        }
    });

    $('button.update-button').on('click', function() {
        var mikanId = $(this).attr('id');
        var animeType = $(this).attr('type');
        this.disabled = true;
        this.style.backgroundColor = "#d6d6d6";

        // 抓取种子
        getAnimeSeed(mikanId, animeType)
    });

    $('button.download-button').on('click', function() {
        var mikanId = $(this).attr('id');
        this.style.backgroundColor = "#d6d6d6";
        this.disabled = true;

        // 下载番剧
        downloadAnime(mikanId)
    });

    $('button.clean-button').on('click', function() {
        var mikanId = $(this).attr('id');
        this.style.backgroundColor = "#d6d6d6";
        this.disabled = true;

        // 删除番剧数据
        deleteAnimeData(mikanId)
    });
})

function subscribeAnime(mikanId) {
    fetch("/anime/subscribe_anime?mikan_id="+mikanId, {method: 'POST'})
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

function cancleSubscribeAnime(mikanId) {
    fetch("/anime/cancel_subscribe_anime?mikan_id="+mikanId, {method: 'POST'})
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

function updateAnimeList(year, season) {
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
}

function deleteAnimeData(mikanId) {
    fetch("/anime/delete_anime_data?mikan_id="+mikanId, {method: 'POST'})
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

function getAnimeSeed(mikanId, animeType) {
    fetch("/anime/insert_anime_seed_thread?mikan_id=" + mikanId + '&anime_type=' + animeType, {method: 'POST'})
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

function downloadAnime(mikanId) {
    fetch("/anime/download_subscribe_anime?mikan_id="+mikanId, {method: 'POST'})
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
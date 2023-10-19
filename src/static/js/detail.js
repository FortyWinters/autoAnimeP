function downloadSingleEpisode(mikan_id, episode) {
    fetch('/anime/download_single_episode?mikan_id=' + mikan_id + '&episode=' + episode, {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            console.log(data)
            window.location.reload();
        })
        .catch(error => console.error('Error:', error));
}

function downloadSingleEpisodeBySubgroup(seed_url) {
    fetch('/anime/download_single_episode_by_subgroup?seed_url=' + seed_url, {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            console.log(data)
            window.location.reload();
        })
        .catch(error => console.error('Error:', error));
}

function showSeeds(subgroupId) {
    var allSubgroupSeedDivs = document.querySelectorAll('.subgroup-seed');
    allSubgroupSeedDivs.forEach(function(div) {
        if (div.id !== subgroupId) {
            div.style.display = "none";
        } else {
            div.style.display = "block";
        }
    });
}

function recoverSingleSeed(seedUrl) {
    fetch('/anime/recover_single_seed?seed_url=' + seedUrl, {method: 'POST'})
    .then(response => response.json())
    .then(data => {
        console.log(data)
        window.location.reload();
    })
    .catch(error => console.error('Error:', error)); 
}

function recoverEpisodeSeed(mikanId, episode) {
    fetch('/anime/recover_episode_seed?mikan_id=' + mikanId + '&episode=' + episode, {method: 'POST'})
    .then(response => response.json())
    .then(data => {
        console.log(data)
        window.location.reload();
    })
    .catch(error => console.error('Error:', error)); 
}

document.addEventListener('DOMContentLoaded', function() {
    var contextMenus = document.querySelectorAll('.context-menu');
    var contextMenu;
    var episodes = document.querySelectorAll('.episode');
    var targetElement;
    var episodeId;

    // 将点击事件监听器绑定到所有的 .context-menu 元素
    contextMenus.forEach(function(menu) {
        menu.addEventListener('click', function(e) {
            // 在这里处理 .context-menu 元素的点击事件
            var ep = targetElement.innerHTML;
            var mikanId = targetElement.getAttribute("data-id");
            var seedUrl = targetElement.getAttribute("data-url");

            switch (episodeId) {
                case 'downloaded-ep':                            
                    switch (e.target.id) {
                        case 'delete':
                            console.log('delete');
                            console.log(ep);
                            console.log(mikanId);
                            break;
                        case 'subscribe':
                            console.log('subscribe');
                            break;
                        default:
                            break;
                    }
                    break;         
                case 'undownloaded-ep':
                    switch (e.target.id) {
                        case 'download':
                            downloadSingleEpisode(mikanId, ep);
                            break;
                        case 'recover':
                            recoverEpisodeSeed(mikanId, ep);
                            break;
                        case 'subscribe':
                            console.log('subscribe');
                            break;
                        default:
                            break;
                    }
                    break;
                case 'downloaded-sd':
                    switch (e.target.id) {
                        case 'delete':
                            console.log('delete');
                            break;
                        default:
                            break;
                    }
                    break;
                case 'undownloaded-sd':
                    switch (e.target.id) {
                        case 'download':
                            downloadSingleEpisodeBySubgroup(seedUrl);
                            break;
                        default:
                            break;
                    }
                    break;
                case 'failed-sd':
                    switch (e.target.id) {
                        case 'recover':
                            recoverSingleSeed(seedUrl);
                            break;
                        default:
                            break;
                    }
                    break;
                default:
                    break;
            }
        });
    });

    episodes.forEach(function(episode) {
        episode.addEventListener('contextmenu', function(e) {
            contextMenus.forEach(function(menu) {
                menu.style.display = 'none';
            });
            e.preventDefault();
            targetElement = e.target;
            episodeId = targetElement.id;
            contextMenu = document.getElementById(episodeId + '-menu');
            contextMenu.style.display = 'block';
            contextMenu.style.left = e.pageX + 'px';
            contextMenu.style.top = e.pageY + 'px';
        });
    });

    document.addEventListener('click', function(e) {
        contextMenus.forEach(function(menu) {
            menu.style.display = 'none';
        });  
    });
});

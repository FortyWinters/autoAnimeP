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
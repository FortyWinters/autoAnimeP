function getTorrentInfo() {
    fetch('/download/get_torrent_web_info?mikan_id=3141&episode=2', {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            const info = data.data;
            const done = Math.round(parseFloat(info.Done.trim()));
            const infoDiv = document.getElementById('torrentInfo');
            infoDiv.innerHTML = `
                <progress value=${done} max="100"></progress>
                <p>Done: ${info.Done}</p>
                <p>Download Speed: ${info.Download_speed}</p>
                <p>ETA: ${info.ETA}</p>
                <p>Name: ${info.Name}</p>
                <p>Peers: ${info.Peers}</p>
                <p>Seeds: ${info.Seeds}</p>
                <p>Size: ${info.Size}</p>
                <p>State: ${info.State}</p>
            `;
            setTimeout(getTorrentInfo, 1000);
        })
        .catch(error => console.error('Error:', error));
}

getTorrentInfo(); // 启动轮询
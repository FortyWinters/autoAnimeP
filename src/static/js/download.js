function getTorrentInfo() {
    fetch('/download/get', {method: 'GET'})
        .then(response => response.json())
        .then(data => {
            const info_list = data.data;
            var string = '';
            const infoDiv = document.getElementById('torrentInfo');
            info_list.forEach(function(info) {
                const done = Math.round(parseFloat(info.Done.trim()));
                string = string + `
                    <tr>
                    <td><progress value=${done} max="100"></progress></td>
                    <td>${info.Done}</td>
                    <td>${info.Download_speed}</td>
                    <td>${info.ETA}</td>
                    <td>${info.Peers}</td>
                    <td>${info.Seeds}</td>
                    <td>${info.Size}</td>
                    <td>${info.State}</td>
                    </tr>
                `
            });
            console.log(string)
            infoDiv.innerHTML = string;
            setTimeout(getTorrentInfo, 1000);
        })
        .catch(error => console.error('Error:', error));
}

getTorrentInfo()

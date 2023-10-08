function getTorrentInfo() {
    fetch('/download/get_qb_download_progress', {method: 'GET'})
        .then(response => response.json())
        .then(data => {
            const info_list = data.data;
            const infoDiv = document.getElementById('torrentInfo');
            var html_string = `
                <tr>
                    <th class="column-name">番名</th>
                    <th class="column-episode">集数</th>
                    <th class="column-progress">进度</th>
                    <th class="column-done">已完成</th>
                    <th class="column-speed">下载速度</th>
                    <th class="column-eta">剩余时间</th>
                    <th class="column-peers">用户</th>
                    <th class="column-seeds">做种数</th>
                    <th class="column-size">大小</th>
                    <th class="column-state">状态</th>
                    <th class="column-button"></td>
                </tr>`;
            if (info_list.length > 0) {
                info_list.forEach(function(info) {
                    const done = Math.round(parseFloat(info.Done.trim()));
                    html_string += `
                        <tr>
                            <td class="column-name" title='${info.Name}'>
                                <a href="/anime/detail/${info.mikan_id}">${info.anime_name}</a>
                            </td>
                            <td class="column-episode">${info.episode}</td>
                            <td class="column-progress">
                                <progress value=${done} max="100"></progress>
                            </td>
                            <td class="column-done">${info.Done}</td>
                            <td class="column-speed">${info.Download_speed}</td>
                            <td class="column-eta">${info.ETA}</td>
                            <td class="column-peers">${info.Peers}</td>
                            <td class="column-seeds">${info.Seeds}</td>
                            <td class="column-size">${info.Size}</td>
                            <td class="column-state">${info.State}</td>
                            <td class="column-button">
                                <button class="task-button" id="resume" onclick="handleTaskResume('${info.torrent_name}')">恢复</button>
                                <button class="task-button" id="pause" onclick="handleTaskPause('${info.torrent_name}')">暂停</button>
                                <button class="task-button" id="delete" onclick="handleTaskDelete('${info.torrent_name}')">删除</button>
                            </td>
                        </tr>`
                });
            }
            infoDiv.innerHTML = html_string;
            setTimeout(getTorrentInfo, 2000);
        })
        .catch(error => console.error('Error:', error));
}

getTorrentInfo()

function handleTaskDelete(torrent_name) {
    fetch("/download/delete_task_by_torrent_name?torrent_name=" + torrent_name, {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function handleTaskStart(torrent_name) {
    fetch("/download/start_task_by_torrent_name?torrent_name=" + torrent_name, {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function handleTaskPause(torrent_name) {
    fetch("/download/pause_task_by_torrent_name?torrent_name=" + torrent_name, {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function handleTaskResume(torrent_name) {
    fetch("/download/resume_task_by_torrent_name?torrent_name=" + torrent_name, {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
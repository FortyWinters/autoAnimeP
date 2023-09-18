爬虫：
1. 如果没有新种子，并且 anime_task 中的重下标记位为 false，结束进程；
2. 如果有新种子，或者 anime_task 中的重下标记位为 true，则调用 runTask。

runTask：
1. 读 anime_task 获取已经添加的任务；
2. 读 anime_seed 获取可以添加的全部任务；
3. anime_seed - anime_task 得到需要执行的新任务 anime_task_episode_lists_new；
4. 从 anime_task 中筛选出已经存在的，但是需要重新执行的任务 anime_task_reload；
5. anime_task_episode_lists_new + anime_task_reload 得到真正需要执行的任务animeTask;
6. 根据 anime_task 下载种子  
   6.1 下载成功，回写 anime_task 成功标记位  
   6.2 下载失败，重复下载两次  
     6.2.1 下载成功，跳转 6.1  
     6.2.2 下载失败，回写 anime_task 失败标记位  

qb:
1. task_status（新字段）代表视频下载任务状态；
2. qb下载后回写

db:
- anime_list
  - Spider生产
  - 共享
- anime_seed
  - Spider生产
  - AddAnimeTask消费
- anime_task
  - AddAnimeTask生产
  - AddqbTask消费
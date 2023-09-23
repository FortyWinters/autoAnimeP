爬虫：
1. 如果没有新种子，并且 anime_task 中的重下标记位为 false，结束进程；
2. 如果有新种子，或者 anime_task 中的重下标记位为 true，则调用 runTask。

runTask：
1. 读 anime_task 获取已经添加的任务；
2. 读 anime_seed 获取**可以添加**的全部任务；
   1. 可以添加：mikan_id && seed_status == 0

3. 根据 anime_task 和 anime_seed 进行**筛选**:
   1. 筛选 : episode && (anime_seed - anime_task )；

4. 按照 animeTask 更新 anime_seed 表标记位

   1. seed_status == 1
5. 根据 anime_task 下载种子 

   1. 下载成功，得到 anime_task_status_lists，插入 anime_task;


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
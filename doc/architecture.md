爬虫：
1. 如果没有新种子，并且 anime_task 中的重下标记位为 false，结束进程；
2. 如果有新种子，或者 anime_task 中的重下标记位为 true，则调用 runTask。

runTask：
1. 读 ANIME_TASK 获取已经添加的任务 anime_task；
2. 读 ANIME_SEED 获取**可以添加**的全部任务 anime_seed；
   1. 可以添加：mikan_id && seed_status == 0

3. 根据 anime_task 和 anime_seed 进行**筛选**, 获得新任务列表 anime_task:
   1. 筛选 : episode && (anime_seed - anime_task )；

4. 按照 anime_task 更新 ANIME_SEED 标记位

   1. seed_status == 1
5. 根据 anime_task 下载种子 

   1. 下载成功，得到 anime_task_status_lists，插入 ANIME_TASK;



- ANIME_SEED 和 ANIME_TASK 对比筛出种子列表 anime_task
- ANIME_SEED 中，将 anime_task 中的种子状态标为1
- 下载anime_task中的种子，下载成功则插入 ANIME_TASK
- 下载失败的种子，不会进入ANIME_TASK，且不会进入下一轮筛选

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

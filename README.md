# autoAnime

## 流程 & Todo List:
1. ~~后端抓取当季度所有番剧资料，存入mysql。~~
2. ~~前端展示当季度番剧列表，用户选择追番。~~
3. ~~前端将追番表单post到后端，并初始化mysql。~~
4. 后端每天轮询爬取更新番剧，并把种子存入mysql。
5. 后端读取/轮询mysql，发现有新种子，则上传qb。上传同时需要根据番剧名称确认下载路径。
6. init.sh 脚本实现自动化部署。
7. ~~图床不做了~~
8. 日志
   - ~~基础日志功能~~
   - ~~修复日志重复打印~~
   - ~~日志大小超过阈值时分割日志文件~~
   - 添加日志打印到终端的选项，完善log_config，yaml对应功能
10. ~~数据库crud [@bjrbh](https://github.com/bjrbh)~~
11. 守护进程拉起定时任务（4、5）

## 使用
### flask测试
```
sh test.sh

// 数据库更新
flask db migrate
flask db upgrade
```

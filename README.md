# autoAnime

## 流程 & Todo List:
1. ~~后端抓取当季度所有番剧资料，存入mysql。~~
2. ~~前端展示当季度番剧列表~~，用户选择追番。
3. 前端将追番表单post到后端，并初始化mysql。
4. 后端每天轮询爬取更新番剧，并把种子存入mysql。
5. 后端读取/轮询mysql，发现有新种子，则上传qb。上传同时需要根据番剧名称确认下载路径。
6. init.sh 脚本实现自动化部署。
7. 图床
8. 日志
9. 数据库crud

## 使用
### flask测试
```
sh test.sh

// 数据库更新
flask db migrate
flask db upgrade
```

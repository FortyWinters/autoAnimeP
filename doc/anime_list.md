api: https://mikanani.me/Home/BangumiCoverFlowByDayOfWeek?year=&seasonStr=

mikan范围:
year:2013-2023
seasonStr:
    '秋': %E7%A7%8B
    '夏': %E5%A4%8F
    '春': %E6%98%A5
    '冬': %E5%86%AC

anime所有已经更新anime_list的合并，订阅的在前
提供每个季度的入口, 首次点进为空白, 点击获取番剧列表后再爬取
进入某一季度，点击刷新列表, 只抓这一季度的anime_list

spider:
- get_anime_list(year, season)
- 能否爬到是否完结的状态，定时轮询需要排除完结的番剧
- img的重下机制，暂无

anime_list:
- year
- broadcast_season(播出季度)
    - 春: 1
    - 夏: 2 
    - 秋: 3
    - 冬: 4
- season_number
    - 第一季: 1
    - 第二季: 2
- is_finished
    - 未完结: 0
    - 完结: 1

或需要一个清除缓存的按钮？
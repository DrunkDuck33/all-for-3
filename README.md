# all-for-3
[望夫石bot](https://www.douban.com/group/topic/267085589/?_dtcc=1&_i=34171577i3poRg) for [珈樂的皇珈酒館@豆瓣](https://www.douban.com/group/carol)

## Monitoring

https://github.com/DrunkDuck33/all-for-3/blob/master/controller.py#L44

## Technical Stuff

### Douban Auth

參考[繞過 Android SSL Pinning](https://juejin.cn/post/6931940051496468494)，再繞過Pinning之後抓包獲取一個32位的auth。

### Bilibili接口

基本上就是抓Chrome的包。`BiliBot.get_app_info`為app端包重放，如果需要修改vmid的話，參考[哔哩哔哩Sign计算](https://github.com/lkeme/Enc2Dec/blob/master/Bilibili/sign.py)去修改簽名。

## 不知道要不要做的

+ 爬評論區
+ QQ音樂
+ 微博

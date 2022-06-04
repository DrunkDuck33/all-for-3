# all-for-3
[望夫石bot](https://www.douban.com/group/topic/267085589/?_dtcc=1&_i=34171577i3poRg) for [珈樂的皇珈酒館@豆瓣](https://www.douban.com/group/carol)

## Monitoring

https://github.com/DrunkDuck33/all-for-3/blob/master/controller.py#L44

## Technical Stuff

### Douban Auth

參考[繞過 Android SSL Pinning](https://juejin.cn/post/6931940051496468494)，再繞過Pinning之後抓包獲取一個32位的auth。

### Bilibili接口

基本上就是抓Chrome的包。`BiliBot.get_app_info`為app端包重放，如果需要修改vmid的話，參考[哔哩哔哩Sign计算](https://github.com/lkeme/Enc2Dec/blob/master/Bilibili/sign.py)去修改簽名。

### QQ音樂動態（部分）

不得不說大廠的APP逆向還是有一些的難度。做了一個比較sloppy的版本，包重放，用Quantumult抓包然後重放。如果想自己搭建的可以去抓自己的包，URL在源碼裡，過濾一下就行。

在逆向過程中，由於騰訊Q音客戶端的SSL證書驗證是自實現的，因此無法在apk中抓到http流量。另一點是apk和ipa的實現似乎大相徑庭，在iOS抓到的包中header字段"Mask"和"Sign"找不到對應的apk實現，可能是在so文件中實現，回頭可以看下。

對於QQ音樂的版本，我最開始用的是102_e282dc94654e5db812c29bcc3c9ace3f.apk這個apk（忘了版本號了，好像是8.x），這個版本中有QQ音樂的社交功能（動態等），但沒有跟聽功能等。再之後就開始黑盒分析最新版本的apk，結果就是上面所說的，被SSL驗證暫時打敗。

## 不知道要不要做的

+ 爬評論區
+ QQ音樂 （部分）
+ 微博

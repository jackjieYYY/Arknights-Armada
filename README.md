# Arknights-Armada

明日方舟修改器 / Arknights Cheat

利用 [mitmproxy](https://www.mitmproxy.org/) 来实现对明日方舟数据的中间人攻击，从而修改部分我们希望修改的数据。
通过设置PAC代理的方式可以支持任意设备、模拟器使用，支持多个用户同时使用。

**仅供学习使用，被封号我不管，禁止违法用途。**~~我已经爽够了（划掉~~



## 主要功能

- 全干员满级、满潜、满精、满信赖
- 自定义替换干员。例如：扣扣哒油改能天使、全部干员改能天使（抽不到能天使我枯了）
- 支持龙门
- 支持代理指挥

## 使用说明

1. 安装mitmproxy

2. 在手机或模拟器中信任mitmproxy证书

3. 下载 Kengxxiao 大佬提取解包的游戏数据 [character_table.json](https://github.com/Kengxxiao/ArknightsGameData/blob/master/zh_CN/gamedata/excel/character_table.json)，放入脚本同级目录。

4. 执行 mitmdump.exe -s .\🐍.py --ssl-insecure -p 12450

5. 配置手机代理

6. 重新进入游戏，看到控制台输出干员信息并且游戏内看板娘变为**~~我老婆~~**精二能天使即开启成功

   ![开启成功](https://i.loli.net/2020/03/19/nh9GsmqZlu4JUyf.png)

   ![满潜满精满等级](mr.assets/Az3GS1ZCMUFQBK2.png)

   ![自定义修改干员](https://i.loli.net/2020/03/19/5SpxzwyBjh4efA9.png)

## PAC代理

由于手机端使用WiFi代理设置会让流量全部走代理，如果部署在远端服务器对网络会造成一定影响，所以建议使用PAC代理的方式只代理明日方舟域名。

ak-gs-localhost.hypergryph.com 国服

gs.arknights.jp 日服

其他服没玩，可以自己抓包看一下

```
function FindProxyForURL(url, host) {
if (dnsDomainIs(host, "ak-gs-localhost.hypergryph.com") || dnsDomainIs(host, "gs.arknights.jp")) {
  return "PROXY 192.168.1.1:12450";
}
  return "DIRECT";
}
```

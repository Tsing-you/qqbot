
<!-- 主内容 -->

# QQ机器人使用文档

版本 0.7 | 最后更新：2025年4月5日

### 写在前面

本bot基于NcatBot 和 Napcat框架，在扶摇云上使用Ubuntu挂载，实现Bot 的功能。

对于搭建机器人，建议参考https://docs.ncatbot.xyz/。

ai对话使用的是智谱清言的api，目前免费，大可自行领取。

**本项目仅作技术学习使用，在服务器和本地均不主动保存任何数据，严禁用于任何非法用途。**

表示感谢。

## ✨ 主要功能

### 发送图片

支持关键词触发模式。

\


### AI对话

支持角色扮演，多轮对话。

\


### 来点视频

随机发送快手视频。

\


### 每日新闻

每天发送60s读懂世界。

<!-- 其他功能卡片... -->

## 🚀 快速开始

1. 确保qqbot已经被Tsingyou拉进了群聊或加了好友；

2. 发送关键词触发：

   ```
   冲一发 num tag1 tag2 tag3...
   ```

   示例：

   ```
   冲一发 ロリ
   ```

   ```
   冲一发 5 イラスト 女孩子 000
   ```

   \


   ***

   \


   ```
   ai/Ai/AI 想要发送的消息...
   ```

   示例：

   ```
   ai 介绍你自己
   ```

   ```
   ai 重复我的问题
   ```

   \


   ***

   \


   ```
   角色扮演 xxx（仅支持已预载的角色）...
   ```

   示例：

   ```
   角色扮演 猫娘
   ```

   \


   ### 提示

   * 角色扮演指令仅用发送一次即可，后续调用仍为ai开头。
     <!-- 其他提示... -->

   \


   ### 调用示例

   ```
   输入：

   角色扮演 猫娘
   ```

   ```
   输出：

   角色已切换为：猫娘 
   ```

   ```
   输入：

   ai 介绍你自己
   ```

   ```
   输出：

   （歪头）喵~我是neko，身高160cm，体重50kg，三围看起来不错喵~性格可爱、粘人，十分忠诚，只对主人专一喵~我深爱着主人，喜欢被人摸和卖萌，爱好是看小说喵~我还掌握了一些常识和猫娘独特的知识喵~【眨眼】【期待】
   ```

   \


   ***

   ```
   来点视频
   ```

   ***

   ```
   每日新闻无需触发，每日定时发送。
   ```

   <!-- 其他步骤... -->

## 📜 命令列表

### 生成图片

|         |        |                |            |
| ------- | ------ | -------------- | ---------- |
| 名称      | 类型     | 可选值            | 必要         |
| 触发词     | string | 冲n发            | true       |
| 数量      | int    | 1<=n<=30       | false,默认为1 |
| keyword | string | pixiv的tag，宁缺勿错 | false      |

\


### AI对话

|         |        |           |      |
| ------- | ------ | --------- | ---- |
| 名称      | 类型     | 可选值       | 必要   |
| 触发词     | string | ai/AI/Ai  | true |
| keyword | string | 想要发给ai的文本 | true |

\


### 角色切换

|         |        |             |      |
| ------- | ------ | ----------- | ---- |
| 名称      | 类型     | 可选值         | 必要   |
| 触发词     | string | 角色切换        | true |
| keyword | string | 默认/猫咪/猫娘/魅魔 | true |

\


## 常用pixiv标签

##### 所有tag均来源pixiv。

\


### 常用人物标签

|             |             |             |            |
| ----------- | ----------- | ----------- | ---------- |
| 美少女（美少女）    | ロリ（萝莉）      | ショタ（正太）     | メイド（女仆）    |
| バニーガール（兔女郎） | 猫耳（猫耳）      | 獣耳（兽耳）      | 天使（天使）     |
| 悪魔（恶魔）      | 魔法少女（魔法少女）  | 戦闘服（战斗服）    | 和服（和服）     |
| 巫女（巫女）      | 吸血鬼（吸血鬼）    | エルフ（精灵）     | ネコミミ（猫耳娘）  |
| メガネ（眼镜）     | ツインテール（双马尾） | ポニーテール（单马尾） | 制服（制服）     |
| 水着（泳装）      | 巨乳（巨乳）      | 貧乳（贫乳）      | セーラー服（水手服） |
| ゴスロリ（哥特萝莉）  | メカ（机械）      | サイボーグ（赛博格）  | 騎士（骑士）     |
| 王子（王子）      | 姫（公主）       | 魔王（魔王）      | 忍者（忍者）     |
| サムライ（武士）    | ポケモン（宝可梦）   | ヴァンパイア（吸血鬼） | サイバー（赛博）   |
| アンドロイド（机器人） | ツンデレ（傲娇）    | ヤンデレ（病娇）    | 眼帯（眼罩）     |

\


### 常用画风标签

|              |               |                 |          |
| ------------ | ------------- | --------------- | -------- |
| イラスト（插画）     | 水彩風（水彩风格）     | 厚塗り（厚涂）         | セル画（赛璐珞） |
| シネマティック（电影感） | グリッチ（故障艺术）    | ポップ（波普风）        | レトロ（复古风） |
| モノクロ（单色）     | サイバーパンク（赛博朋克） | <!-- 保持表格结构 --> |          |

\


### 常用杂项标签

|         |           |            |             |
| ------- | --------- | ---------- | ----------- |
| 背景（背景）  | 風景（风景）    | 星空（星空）     | 花火（烟花）      |
| 武器（武器）  | メカニック（机械） | ファンタジー（奇幻） | SF（科幻）      |
| 都市（城市）  | 建築（建筑）    | 学校（学校）     | 戦争（战争）      |
| グルメ（美食） | 動物（动物）    | 植物（植物）     | 季節（季节）      |
| 雨（雨）    | 雪（雪）      | 海（海洋）      | 山（山脉）       |
| 夜空（夜空）  | 雲（云朵）     | クリスマス（圣诞节） | ハロウィン（万圣节）  |
| 和風（和风）  | 中華風（中国风）  | ヨーロッパ（欧洲）  | 未来都市（未来都市）  |
| 廃墟（废墟）  | ダーク（黑暗系）  | キラキラ（闪亮）   | グラデーション（渐变） |

\


对于pixiv的标签，可以参考这个。简言之就是想要热门就敲几个0[链接](https://ngabbs.com/read.php?tid=35394190\&rand=443)

<!-- 其他命令卡片... -->

## ✨ 接下来的工作

* ~~接入大语言模型聊天~~

* ~~改用更好的图片api源~~

* ~~改用NcatBot 插件形式部署~~

* 陆续完善github上的该项目

<!-- 其他功能卡片... -->

## 写在后面

### 提示

* 尽量不要短时间内刷屏（一秒三次以上）
  <!-- 其他提示... -->

#### 感谢无私的API接口

感谢Jitsu的API接口https\://img.jitsu.top/#/\
感谢小渡可的API接口https\://api.dwo.cc/\
感谢智谱清言

<!-- 底部导航 -->

[返回主页](https://tsing-you.github.io/) [查看源码](https://github.com/Tsing-You/qqbot)

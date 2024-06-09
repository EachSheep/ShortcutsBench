<div align= "center">
    <h1> 🛠️ShortcutsBench🤖</h1>
</div>

<div align="center">

![Dialogues](https://img.shields.io/badge/Dataset\_Size-1.8G-red?style=flat-square)
![Dialogues](https://img.shields.io/badge/Shortcuts\_Num-15508-red?style=flat-square)


</div>

<!-- <p align="center">
  <a href="#model">Model</a> •
  <a href="#data">Data Release</a> •
  <a href="#web-ui">Web Demo</a> •
  <a href="#tool-eval">Tool Eval</a> •
  <a href="https://arxiv.org/pdf/2307.16789.pdf">Paper</a> •
  <a href="#citation">Citation</a>

</p> -->

</div>

*Read this in [English](README_EN.md).*

快捷指令（Shortcuts）是什么？

快捷指令是快捷指令开发者，在快捷指令App中，通过用户友好的图形化页面，使用快捷指令App中提供的基本动作构建的工作流。[苹果官方](https://support.apple.com/zh-cn/guide/shortcuts/welcome/ios)将其称之为“一种可让你使用 App 完成一个或多个任务的快捷方式。”

快捷指令可以帮你做什么？快捷指令可以一键帮你完成各种任务！例如：
* 日常生活：...
* 购物党：...
* 学生党：...
* 文字工作者：...
* 科研工作者：...
* ...

想要更多？请在[此]()查看我们已经收集的快捷指令。

[苹果开发者大会 WWDC'24]()在苹果设备上引入大量AI功能，我们十分关注苹果将如何把以ChatGPT为代表大语言模型与苹果设备结合，给用户带来更智能的体验，快捷指令一定会在此过程中发挥重要作用！

## 该数据集对您有什么帮助？

* 作为快捷指令用户：
  * 您可以在此数据集提供的海量快捷指令中找到您最心仪的快捷指令。
  * 您可以通过在苹果设备上引入更多的快捷指令，让Siri可以使用快捷指令完成复杂的任务。
* 作为快捷指令爱好者：
  * 您可以使用该数据集中海量的快捷指令链接（以及对应的源文件）研究如何编写快捷指令，为您自己的工作流量身定制快捷指令。
  * 您可以为此项目贡献更多的快捷指令。
* 作为研究者：
  * 研究自动化工作流的构建。快捷指令本质上是由一些列API调用（动作）构成的工作流。这些API由苹果和第三方App共同提供。
  * 研究低代码编程。快捷指令包含分支、循环、变量赋值等代码特征，也拥有用户友好的图形化用户界面，。
  * 研究基于API的智能体。基于API调用的智能体本质上是让大语言模型根据用户查询（任务）自主决定用不用API、什么时候用API、怎么用API。
  * 研究利用快捷指令微调大语言模型，从而促进大语言模型和手机/电脑/智能手表更紧密的结合。让“基于大语言模型的操作系统”真正成为现实。
  * ......

## 此项目任务清单（持续更新ing）

- [x] [快捷指令数据集]()，包含快捷指令元数据（标题、简介、来源等）、iCloud链接、快捷指令源文件。
- [ ] 快捷指令所涉及的API，包含API元数据（功能描述、名称、参数名称、参数类型、参数默认值、返回值名称, ......）和App本身。
- [ ] 快捷指令如何促进智能体的发展？欢迎大家关注我们即将放出的工作！

可以先赏个Star吗 ~~~

## 快捷指令使用指南（面向用户）

**搜索您想要的快捷指令？**

我们的快捷指令放在哪？怎么在本项目中搜索想要的快捷指令？（放一个你的README的结构，README里面放了啥）。
也可以移步快捷指令搜集站，推荐几个，全部网站给个链接。

- 在本仓库中，每个category下只保存了对应的README文件，用于记录该类别的所有文件的主要信息，这里的README结构如下：

**如何导入搜索到的快捷指令？**

搜索到快捷指令后如何导入快捷指令（使用苹果设备点击icloud链接后会自动在快捷指令中打开）。

## 数据集使用指南（面向快捷指令开发者和研究者）

**获取数据集**
   
您可以根据[✨✨数据集描述](#✨✨数据集描述)中的iCloud链接一个一个地下载快捷指令，或直接[百度网盘](https://pan.baidu.com/s/1pQMuMlAuW3Z6PLKP-tumPg?pwd=4nkm)或Google云中[Google Cloud](https://drive.google.com/drive/folders/1hhZXvO6JE3YmlI26Sbh9zrhJYVLBt3-O?usp=drive_link)获取全量数据。

| 数据源 | 包含类别 | 元数据所在位置 | 云盘链接 |
| :-------: | :----: | :----: | :----: |
| [Matthewcassinelli](https://matthewcassinelli.com/sirishortcuts/library/free) | × | [仓库位置](dataset/matthewcassinelli.com_sirishortcuts_library_free) | [源文件](https://drive.google.com/drive/folders/1nJzaE72VSoNf_r1335WCR9Uv_NlvOjV_?usp=drive_link)|
| [Routinehub](https://routinehub.co)| √  | [仓库位置](dataset/routinehub.co)| [源文件](https://drive.google.com/drive/folders/1BzcFM9wMfDDGbCjL3uWDrYh-5p9YL7do?usp=drive_link)|
| [MacStories](https://www.macstories.net/shortcuts)| √  | [仓库位置](dataset/www.macstories.net_shortcuts) |[源文件](https://drive.google.com/drive/folders/1_MsiwqHNZVAPJGzURZ4lrMz7nSpKz-Sc?usp=drive_link)|
| [ShareShortcuts](https://shareshortcuts.com)| √  | [仓库位置](dataset/shareshortcuts.com) |[源文件](https://drive.google.com/drive/folders/1LdjQYnCrvgKIuPeCBhztxGzbGrIIQk8D?usp=drive_link)|
| [ShortcutsGallery](https://shortcutsgallery.com)| √  | [仓库位置](dataset/shortcutsgallery.com) |[源文件](https://drive.google.com/drive/folders/1FsUR0DNHfgNJieSfDxPkyfiUBhOYxnLN?usp=drive_link)|
| [iSpazio](https://shortcuts.ispazio.net)| ×  | [仓库位置](dataset/shortcuts.ispazio.net) | [源文件](https://drive.google.com/drive/folders/1I2XYwjZrk3xuvpD9EnrPZe8AwfaMx92i?usp=drive_link)|
| [捷径库](https://jiejingku.net)| √  | [仓库位置](dataset/jiejingku.net) |[源文件](https://pan.baidu.com/s/1CH-tQ7PRGSJxdtkdR2TMuA?pwd=tzv8)|
| [少数派](https://shortcuts.sspai.com)| √  | [仓库位置](dataset/shortcuts.sspai.com) |[源文件](https://pan.baidu.com/s/18AbPTCJjRoI-6tnPtq0Vdw?pwd=q4mi)|
| [捷径范](https://jiejing.fun)| √  | [仓库位置](dataset/jiejing.fun) |[源文件](https://pan.baidu.com/s/1I8NKqtvLXyTKbkUoP9IBGw?pwd=enr3)|
| [柯基捷径库](https://www.kejicut.com)| √  | [仓库位置](dataset/www.kejicut.com)|[源文件](https://pan.baidu.com/s/1x3znoUK7QRgg9aoD5m9yjA?pwd=y2ky)|
| [iOS快捷指令库](https://www.rcuts.com)| √  | [仓库位置](dataset/www.rcuts.com) |[源文件](https://pan.baidu.com/s/1H3BLJqhoNuCLJA2XpnWKTw?pwd=fx7j)|

**快捷指令源数据简介**

* 每一个文件代表一个快捷指令。文件名为快捷指令名称。
* 我们提供的快捷指令源文件为json格式，而从苹果设备中直接导出的快捷指令为iCloud链接（以链接形式分享）或是受到苹果加密后的快捷指令文件（以.shortcut为后缀）。
* 若您希望将某个快捷指令源文件导入快捷指令App，您需要在MacOS上进行以下操作：
  * 将json文件格式转化为plist文件格式。
  * 对该plist文件进行签名。
  * 将签名后的文件导入快捷指令App。

网盘中的快捷指令源数据以以下方式组织：

```
dataset/
├── matthewcassinelli.com_sirishortcuts_library_free # 网站名称
│ ├── file1
│ ├── file2
│ └── file3

或

dataset/
├── jiejingku.net # 网站名称
│ ├── category1 # 类型 
│ │ ├── file1 # 每一个具体的快捷指令
│ │ └── file2
│ ├── category2
│ │ └── file3
```

## 许可与引用

- 许可证：明确数据集的使用许可，如MIT、Apache等。

## 致谢

- 致谢：感谢为数据集做出贡献的个人和组织。


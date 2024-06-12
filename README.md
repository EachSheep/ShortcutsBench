<div align= "center">
    <h1> 🔧ShortcutsBench📱</h1>
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

**快捷指令（Shortcuts）是什么？**

快捷指令是由开发者在快捷指令App中，通过用户友好的图形化界面🖼️，利用提供的基本动作构建的工作流🔄。[苹果官方](https://support.apple.com/zh-cn/guide/shortcuts/welcome/ios)称其为“一种可让你使用 App 完成一个或多个任务的快捷方式。”📱✨

**该项目对您有什么帮助？**

[苹果开发者大会 WWDC'24](https://developer.apple.com/wwdc24/)在苹果设备上引入了大量AI功能🤖。我们非常关注苹果如何将以ChatGPT为代表的大语言模型与设备结合，为用户带来更智能的体验📱💡。在这个过程中，快捷指令一定会发挥重要作用！🚀

* 作为快捷指令用户📱：
  * 您可以在此数据集中找到您最心仪的快捷指令📱。
  * 您可以通过在苹果设备上引入更多快捷指令，让Siri完成复杂任务🗣️。
  * ......

* 作为快捷指令爱好者💡：
  * 您可以使用该数据集中的海量快捷指令链接（以及对应的源文件）研究如何编写快捷指令，定制您自己的工作流💡。
  * 您可以为此项目贡献更多的快捷指令📤。
  * ......

* 作为研究者🔬：
  * 研究自动化工作流的构建：快捷指令本质上是由一系列API调用（动作）构成的工作流，这些API由苹果和第三方App提供🔍。
  * 研究低代码编程：快捷指令包含分支、循环、变量赋值等代码特征，同时拥有用户友好的图形化界面🖥️。
  * 研究基于API的智能体：让大语言模型根据用户查询（任务）自主决定是否、何时以及如何使用API🔧。
  * 研究利用快捷指令微调大语言模型，促进大语言模型与手机、电脑、智能手表的紧密结合，实现“基于大语言模型的操作系统”的愿景📈。
  * ......

**如果这个项目对您有帮助，请给我们一个Star吧⭐️！感谢支持！🙏**

**该项目对比现有数据集的优势**

![Example Image](./assets/Comparison.png)

**关键词**：快捷指令, 苹果, WWDC'24, Siri, iOS, macOS, watchOS, 工作流, API调用, 低代码编程, 智能体, 大语言模型

## 快捷指令可以帮你做什么？

快捷指令可以一键帮你完成各种复杂任务！例如：

* 🏡 **日常生活** 🤹
  * [一键寻找附近酒馆](https://www.icloud.com/shortcuts/78ffd18288fd4da286bfd570993ea46e)
  * [节日提醒](https://www.icloud.com/shortcuts/5b3607d300e84e3d99889c7fb0258b92)
  * [百度贴吧签到](https://www.icloud.com/shortcuts/084dc19b51904a8a98e9135159fd2a61)
  * ......

* 🛍️ **购物党** 🛒
  * [购买PUBG Mobile UC](https://www.icloud.com/shortcuts/7234c2d743004377b4c74ea01d160648)
  * [复制淘宝口令](https://www.icloud.com/shortcuts/e8dabf3b52eb412f9bdfeb6ce163cec3)
  * ......

* 🧑‍🎓 **学生党** 🧮
  * [计算器](https://www.icloud.com/shortcuts/477e692d2646448fb6364539b0fcb608)
  * [放空心灵](https://www.icloud.com/shortcuts/5d1f7e70a3f24493be92be2ed427c070)
  * ......

* ⌨️ **文字工作者** 🔣
  * [翻译器](https://www.icloud.com/shortcuts/62f3fd91e29749fda1576f80f62423ed)
  * [制作PDF](https://www.icloud.com/shortcuts/964373096afc424d90be716ea7a88c6e)
  * ......

* 🧑‍🔬 **科研工作者** 🏫
  * [获取 arXiv bibtex 条目](https://www.icloud.com/shortcuts/2222c346272249ca96e06fb64ba53845)
  * ......

* .....


**想要更多？✨**

请查看我们在此项目中收集的快捷指令[📂](#快捷指令使用指南面向用户📱)。

## 此项目任务清单（持续更新中）📋

- [x] [快捷指令数据集](https://github.com/hiyoungshen/ShortcutsBench)：包含快捷指令元数据（标题、简介、来源等）、iCloud链接、快捷指令源文件。
- [ ] 快捷指令所涉及的API：包括API元数据（功能描述、名称、参数名称、参数类型、参数默认值、返回值名称等）和App本身📱。
- [ ] 快捷指令如何促进智能体的发展？欢迎大家关注我们即将发布的工作！🚀

## 快捷指令使用指南（面向用户）📱

**搜索您想要的快捷指令🔍**

想知道我们的快捷指令在哪里？如何在本项目中搜索到您需要的快捷指令？请按照以下步骤操作：

1. 在本仓库中，`dataset/${website name}/${category name}/README.md`文件用于记录该类别的所有快捷指令的元信息，包括名称、描述、iCloud下载链接等。每一个`README.md`文件的结构如下：
    ```markdown
    ### Name: Wine Shops # 快捷指令名称
    - URL: https://www.icloud.com/shortcuts/78ffd18288fd4da286bfd570993ea46e # 快捷指令iCloud链接
    - Source: https://shortcutsgallery.com # 快捷指令来源商店
    - Description: Look for Wine shop near by you # 快捷指令功能描述
    ```
2. 使用快捷键`Ctrl+F`，根据快捷指令的名称关键词直接在浏览器中进行检索🔎。

您也可以访问[快捷指令搜集站](#数据集使用指南面向快捷指令开发者和研究者📚)搜索您想要的快捷指令🌐。

**如何导入搜索到的快捷指令📥**

在苹果设备上，点击URL中的iCloud链接后，快捷指令将会自动打开并导入到您的快捷指令App中📲。

## 数据集使用指南（面向快捷指令开发者和研究者）📚

### 获取数据集

您可以根据[快捷指令使用指南](#快捷指令使用指南面向用户📱)中的iCloud链接逐一下载快捷指令，或直接从以下链接获取完整数据：

- [百度网盘](https://pan.baidu.com/s/1qVX03DjSfBXXXW5W96jtqQ?pwd=33s2)
- [Google云盘](https://drive.google.com/drive/folders/171d_iiyBpQSfC-nLFpFDBq2P0Y7Tqw_m?usp=sharing)

### 数据源与链接 🌐

| 数据源 | 元数据位置 | 云盘链接 |
| :-------: | :----: | :----: |
| [Matthewcassinelli](https://matthewcassinelli.com/sirishortcuts/library/free) | [ 在本仓库的位置](dataset/matthewcassinelli.com_sirishortcuts_library_free) | [Google云盘链接](https://drive.google.com/drive/folders/1Dq9A44qP5s6-HOducpg-pGRbsyCGRNsW?usp=drive_link) \| [百度网盘链接](https://pan.baidu.com/s/1Wru9TC_1MPqX26Ua6IzPQQ?pwd=3zwl) |
| [Routinehub](https://routinehub.co) | [ 在本仓库的位置](dataset/routinehub.co) | [Google云盘链接](https://drive.google.com/drive/folders/1IEhry0vnK48-GGF39kEMgQDtoSObR979?usp=drive_link) \| [百度网盘链接](https://pan.baidu.com/s/1WFZw-G_w9QZQDyAdcYe-Yg?pwd=lp6d) |
| [MacStories](https://www.macstories.net/shortcuts) | [ 在本仓库的位置](dataset/www.macstories.net_shortcuts) | [Google云盘链接](https://drive.google.com/drive/folders/11z32E2_mphNcrcz0jg2RZ0Tit6zxxJOy?usp=drive_link) \| [百度网盘链接](https://pan.baidu.com/s/1qfeCKUtTnO4gihSydfbYlg?pwd=u9p2) |
| [ShareShortcuts](https://shareshortcuts.com) | [ 在本仓库的位置](dataset/shareshortcuts.com) | [Google云盘链接](https://drive.google.com/drive/folders/197zOSqDcTlZp242NK38G1ShFs8Mi6qff?usp=drive_link) \| [百度网盘链接](https://pan.baidu.com/s/13M6PSPXhSMwAhDuRLlqbIw?pwd=j7gn) |
| [ShortcutsGallery](https://shortcutsgallery.com) | [ 在本仓库的位置](dataset/shortcutsgallery.com) | [Google云盘链接](https://drive.google.com/drive/folders/1ieovTT-QOZIpub8BW8I7MicM9KcwJDwB?usp=drive_link) \| [百度网盘链接](https://pan.baidu.com/s/1knXrn_OwPqUxaDvqSZQ1ag?pwd=ux9x) |
| [iSpazio](https://shortcuts.ispazio.net) | [ 在本仓库的位置](dataset/shortcuts.ispazio.net) | [Google云盘链接](https://drive.google.com/drive/folders/1lPmyxYE1UtKsOPNJU5b0zc6B7wyK-bns?usp=drive_link) \| [百度网盘链接](https://pan.baidu.com/s/1l2IIrcpK7WTYuT3Ec57SxA?pwd=0l0u) |
| [捷径库](https://jiejingku.net) | [ 在本仓库的位置](dataset/jiejingku.net) | [Google云盘链接](https://pan.baidu.com/s/1WdgWmGkRfevTyit4i14DOg?pwd=ud3d) \| [百度网盘链接](https://pan.baidu.com/s/1n0pxGttbsCttDZkVkOZiag?pwd=0yzg) |
| [少数派](https://shortcuts.sspai.com) | [ 在本仓库的位置](dataset/shortcuts.sspai.com) | [Google云盘链接](https://pan.baidu.com/s/1BQcGi12fhtxOLD8gpt135A?pwd=tjqi) \| [百度网盘链接](https://pan.baidu.com/s/1M2tR9lOFr-6rIeKoB7T8PQ?pwd=22fn) |
| [捷径范](https://jiejing.fun) | [ 在本仓库的位置](dataset/jiejing.fun) | [Google云盘链接](https://pan.baidu.com/s/1Hdco7WtgN0kEVfqcxJi3qQ?pwd=5732) \| [百度网盘链接](https://pan.baidu.com/s/16oSRINZK-gyy38x51QO7dQ?pwd=2fj4) |
| [柯基捷径库](https://www.kejicut.com) | [ 在本仓库的位置](dataset/www.kejicut.com) | [Google云盘链接](https://pan.baidu.com/s/1SBlhUB3H6VPm5mwW0fHHyw?pwd=0q7p) \| [百度网盘链接](https://pan.baidu.com/s/1kQwvwj5tQorJeYZ22w3iUw?pwd=8eah) |
| [iOS快捷指令库](https://www.rcuts.com) | [ 在本仓库的位置](dataset/www.rcuts.com) | [Google云盘链接](https://pan.baidu.com/s/1UZLcXjmAVCLwZKiK4638Ug?pwd=8vv0) \| [百度网盘链接](https://pan.baidu.com/s/1h8frW1928kfW38pnjJorGA?pwd=1c28) |


**快捷指令源文件简介**

网盘中的快捷指令源数据以以下目录结构组织：
```
dataset/
├── matthewcassinelli.com_sirishortcuts_library_free # 网站名称
│   ├── file1
│   ├── file2
│   └── file3

或

dataset/
├── jiejingku.net # 网站名称
│   ├── category1 # 类别 
│   │   ├── file1 # 每一个具体的快捷指令
│   │   └── file2
│   ├── category2
│   │   └── file3
```

每个文件代表一个快捷指令。文件名由快捷指令名称简单处理后生成，处理代码如下：
```python
file_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
```

我们提供的快捷指令源文件为`JSON`格式，而从苹果设备中导出的快捷指令为`iCloud`链接（以链接形式分享）或是受到苹果加密的快捷指令文件（以`.shortcut`为后缀）。

若您希望将某个快捷指令源文件导入快捷指令App，请在`macOS`上进行以下操作：
* 将`JSON`文件格式转换为`PLIST`文件格式📑。
* 对该`PLIST`文件进行签名🔏。
* 将签名后的文件导入快捷指令App📲。

## 许可声明 📜

本项目中的所有代码和数据集均依据`Apache License 2.0`进行许可。这意味着您可以自由地使用、复制、修改和分发本项目的内容，但需遵守以下条件：

- **版权声明**：必须在项目的所有副本中保留原始版权声明和许可证声明。
- **状态声明**：如果对代码进行了修改，必须在任何修改文件中标明所做的更改。
- **商标使用**：本许可不授予使用项目商标、服务标志或商品名称的权利。

完整的许可证文本请见[LICENSE](./LICENSE)。

此外，您还需遵守本项目数据来源，各个快捷指令分享站的许可协议。

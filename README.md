<div align= "center">
    <h1> 🛠️快捷指令数据集🤖</h1>
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
欢迎来到快捷指令数据集项目！这是一个开源项目，旨在收集用户创建的苹果快捷指令（也称为 Siri 快捷指令）数据集，以分享有用的工作流程并启发他人。


**💁‍♂️💁💁‍♀️ 加入我们 []()!**

*Read this in [English](README_EN.md).*


## 更新
- 1
- 2

## 项目概述

苹果快捷指令是 iOS 和 macOS 上一个强大的自动化工具，允许用户创建自定义工作流程来自动化各种任务。该项目旨在收集、组织和分享来自世界各地用户的各种快捷指令。



## ✨✨数据集描述
 - **数据来源**: 我们的快捷指令数据集来源于多个渠道：

    | 网站名称 | 包含类别 |在本仓库中的位置 | 网盘链接 |
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

 - **数据规模**: 总数据xx条，去重后xx条

 - **数据结构**: 详细说明数据集的结构，包括文件格式、字段解释等。
    - 我们将快捷指令文件按照如下结构存储在上述网盘链接中：

        ```
        dataset/
        ├── matthewcassinelli.com_sirishortcuts_library_free
        │ ├── file1
        │ ├── file2
        │ └── file3
        或
        dataset/
        ├── jiejingku.net
        │ ├── category1
        │ │ ├── file1
        │ │ └── file2
        │ ├── category2
        │ │ └── file3
        ```

    - 在本仓库中，每个category下只保存了对应的README文件，用于记录该类别的所有文件的主要信息，这里的README结构如下：

        ```markdown

        ### Name: 记录了快捷指令的Record Name，如：AC8B9297-70B1-4DF8-88A7-128D4C137F73

        - URL: 记录了快捷指令对应的iCloud链接，如：https://www.icloud.com/shortcuts/ac8b929770b14df888a7128d4c137f73

        - Description: 记录了该快捷指令在商店中的描述

        - Source: 记录了快捷指令所在商店的链接，如：https://shareshortcuts.com
        ```

        对于这里的README文件还有以下几个需要关注的点：

        - 对于Record Name字段相同的文件，我们规定：在原有的Record Name字段基础上，后续加入"_xxxxxxxx"来区分这些相同Record Name的文件。其中"xxxxxxxx"代表8位唯一标识符码
        - 部分快捷指令商店中包含了用户对每个快捷指令的评价，下载量，喜爱值等标签。我们在处理数据时综合这些标签，定义了优先级，对数据进行排序，README中的快捷指令顺序即为由优先级由大到小的顺序。



## 数据收集与预处理

 - 收集方法:
    1. 手动收集：我们团队成员手动收集有用的快捷指令分享网站。
    2. 自动抓取：开发自动化工具从快捷指令分享网站上抓取快捷指令的 iCloud 链接。
 - 预处理:
    3. 下载源文件：根据获取到的快捷指令 iCloud 链接下载快捷指令源文件。
 - 工具和技术
 - 

## 快捷指令使用指南

- **快速开始**:
    1. 获取数据集：您可以根据[✨✨数据集描述](#✨✨数据集描述)中给出的链接进行下载，或从如下链接中获取全数据集。
        - 英文部分：[Google Cloud](https://drive.google.com/drive/folders/1hhZXvO6JE3YmlI26Sbh9zrhJYVLBt3-O?usp=drive_link)
        - 中文部分：[百度网盘](https://pan.baidu.com/s/1x3sidPbP3-guZf59QGjd1g?pwd=r2v8)
    2. 分析数据集：您可以根据每个category下的README文件获取当前文件夹所有的快捷指令的主要信息。或通过如下代码快速得到所有JSON文件列表：

    ```python
    def get_all_json_files(directory):
        json_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.json'):
                    json_files.append(os.path.join(root, file))
        return json_files
    ```

- **注意事项**:
    1. 在dataset下的一级目录中，我们利用商店域名对文件夹进行命名，转换规则参考下面的代码：
    ```python
    def link2folder(link):
        folder = link.split("//")[-1].replace("/", "_")
        return folder
    ```

## 数据用途与场景

- 测试现有大模型智能体的决策能力，


## 贡献指南:

- 如通过什么联系方式来反馈意见等

## 许可与引用

- 许可证：明确数据集的使用许可，如MIT、Apache等。
- 引用格式：提供引用数据集的标准格式，方便用户在学术论文中引用。

## 支持与致谢

- 支持信息：提供获取支持的途径，如论坛、邮件列表等。
- 致谢：感谢为数据集做出贡献的个人和组织。


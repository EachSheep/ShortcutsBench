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

**What are Shortcuts?**

Shortcuts are workflows🔄 created by developers in the Shortcuts app using a user-friendly graphical interface🖼️. According to [Apple](https://support.apple.com/zh-cn/guide/shortcuts/welcome/ios), they are "a quick way to get one or more tasks done with your apps."📱✨

**How can this project help you?**

At [Apple's WWDC'24](https://developer.apple.com/wwdc24/), many AI features were introduced to Apple devices🤖. We're very interested in how Apple integrates large language models, such as ChatGPT, with devices to provide a smarter user experience📱💡. In this process, shortcuts will certainly play a crucial role!🚀

* As a Shortcuts user📱:
  * You can find your favorite shortcuts in this dataset📱.
  * You can integrate more shortcuts into your Apple devices to have Siri handle complex tasks🗣️.
  * ......

* As a Shortcuts enthusiast💡:
  * You can use the vast number of shortcut links (and corresponding source files) in this dataset to study how to write shortcuts and customize your workflows💡.
  * You can contribute more shortcuts to this project📤.
  * ......

* As a researcher🔬:
  * Study the construction of automated workflows: Shortcuts are essentially workflows composed of a series of API calls (actions) provided by Apple and third-party apps🔍.
  * Study low-code programming: Shortcuts include code features such as branching, looping, and variable assignment while having a user-friendly graphical interface🖥️.
  * Study API-based agents: Allow large language models to autonomously decide if, when, and how to use APIs based on user queries (tasks)🔧.
  * Study how to fine-tune large language models with shortcuts to closely integrate language models with phones, computers, and smartwatches, realizing the vision of an "LLM-based operating system"📈.
  * ......

**If you find this project helpful, please give us a star⭐️! Thank you for your support!🙏**

**Keywords**: Shortcuts, Apple, WWDC'24, Siri, iOS, macOS, watchOS, Workflow, API Call, Low-Code Programming, Intelligent Agent, Large Language Model

## What can Shortcuts do for you?

Shortcuts can help you complete various complex tasks with one click! For example:

* 🏡 **Daily Life** 🤹
  * [Find Nearby Wine Shops](https://www.icloud.com/shortcuts/78ffd18288fd4da286bfd570993ea46e)
  * [Holiday Reminder](https://www.icloud.com/shortcuts/5b3607d300e84e3d99889c7fb0258b92)
  * [Sign in to Baidu Tieba](https://www.icloud.com/shortcuts/084dc19b51904a8a98e9135159fd2a61)
  * ......

* 🛍️ **Shoppers** 🛒
  * [Buy PUBG Mobile UC](https://www.icloud.com/shortcuts/7234c2d743004377b4c74ea01d160648)
  * [Copy Taobao Command](https://www.icloud.com/shortcuts/e8dabf3b52eb412f9bdfeb6ce163cec3)
  * ......

* 🧑‍🎓 **Students** 🧮
  * [Calculator](https://www.icloud.com/shortcuts/477e692d2646448fb6364539b0fcb608)
  * [Relaxation](https://www.icloud.com/shortcuts/5d1f7e70a3f24493be92be2ed427c070)
  * ......

* ⌨️ **Writers** 🔣
  * [Translator](https://www.icloud.com/shortcuts/62f3fd91e29749fda1576f80f62423ed)
  * [Create PDF](https://www.icloud.com/shortcuts/964373096afc424d90be716ea7a88c6e)
  * ......

* 🧑‍🔬 **Researchers** 🏫
  * [Get arXiv BibTeX Entry](https://www.icloud.com/shortcuts/2222c346272249ca96e06fb64ba53845)
  * ......

* .....


**Want more?✨**

Check out the shortcuts we collected in this project [📂](#user-guide-for-shortcuts-users📱).

## Project Task List (Continuously Updating)📋

- [x] [Shortcuts Dataset](https://github.com/hiyoungshen/ShortcutsBench): Includes shortcut metadata (title, description, source, etc.), iCloud links, and shortcut source files.
- [ ] APIs involved in shortcuts: Including API metadata (function description, name, parameter names, parameter types, parameter default values, return value names, etc.) and the app itself📱.
- [ ] How do shortcuts promote the development of intelligent agents? Stay tuned for our upcoming work!🚀

## User Guide for Shortcuts Users📱

**Search for the Shortcuts You Want🔍**

Wondering where our shortcuts are? How to search for the shortcuts you need in this project? Follow these steps:

1. In this repository, `dataset/${website name}/${category name}/README.md` files record the metadata of all shortcuts in that category, including name, description, iCloud download link, etc. Each `README.md` file is structured as follows:
    ```markdown
    ### Name: Wine Shops # Shortcut name
    - URL: https://www.icloud.com/shortcuts/78ffd18288fd4da286bfd570993ea46e # Shortcut iCloud link
    - Source: https://shortcutsgallery.com # Shortcut source store
    - Description: Look for Wine shop near by you # Shortcut function description
    ```
2. Use `Ctrl+F` to search directly in the browser based on shortcut name keywords🔎.

You can also visit [Shortcut Collection Sites](#user-guide-for-developers-and-researchers📚) to search for the shortcuts you want🌐.

**How to Import the Shortcuts You Found📥**

On an Apple device, clicking the iCloud link in the URL will automatically open and import the shortcut into your Shortcuts app📲.

## User Guide for Developers and Researchers📚

### Obtain the Dataset

You can download shortcuts one by one from the iCloud links in the [User Guide](#user-guide-for-shortcuts-users📱) or get the complete data from the following links:

- [Baidu Netdisk](https://pan.baidu.com/s/1qVX03DjSfBXXXW5W96jtqQ?pwd=33s2)
- [Google Drive](https://drive.google.com/drive/folders/171d_iiyBpQSfC-nLFpFDBq2P0Y7Tqw_m?usp=sharing)

### Data Sources and Links 🌐

| Data Source | Metadata Location | Cloud Drive Link |
| :-------: | :----: | :----: |
| [Matthewcassinelli](https://matthewcassinelli.com/sirishortcuts/library/free) | [Location in this repository](dataset/matthewcassinelli.com_sirishortcuts_library_free) | [Google Drive](https://drive.google.com/drive/folders/1Dq9A44qP5s6-HOducpg-pGRbsyCGRNsW?usp=drive_link) \| [Baidu Netdisk](https://pan.baidu.com/s/1Wru9TC_1MPqX26Ua6IzPQQ?pwd=3zwl) |
| [Routinehub](https://routinehub.co) | [Location in this repository](dataset/routinehub.co) | [Google Drive](https://drive.google.com/drive/folders/1IEhry0vnK48-GGF39kEMgQDtoSObR979?usp=drive_link) \| [Baidu Netdisk](https://pan.baidu.com/s/1WFZw-G_w9QZQDyAdcYe-Yg?pwd=lp6d) |
| [MacStories](https://www.macstories.net/shortcuts) | [Location in this repository](dataset/www.macstories.net_shortcuts) | [Google Drive](https://drive.google.com/drive/folders/11z32E2_mphNcrcz0jg2RZ0Tit6zxxJOy?usp=drive_link) \| [Baidu Netdisk](https://pan.baidu.com/s/1ybVp-rqrT4PO6n5A-fnd4A?pwd=f7mu) |
| [ShortcutsGallery](https://shortcutsgallery.com) | [Location in this repository](dataset/shortcutsgallery.com) | [Google Drive](https://drive.google.com/drive/folders/1gIbYFHVwW1uc3YpmG4pEVoxxe5MN9V7R?usp=drive_link) \| [Baidu Netdisk](https://pan.baidu.com/s/1h4kJML9k9LC3e4U8w2jTog?pwd=qhu9) |
| [ShortcutsArchive](https://www.shortcutsarchive.com) | [Location in this repository](dataset/www.shortcutsarchive.com) | [Google Drive](https://drive.google.com/drive/folders/1hHb_ZDUkjbubIXv1A4vS2TQXkRNh17CJ?usp=drive_link) \| [Baidu Netdisk](https://pan.baidu.com/s/1_sHq6XnvbaqS_RRijgf6Nw?pwd=nua9) |
| [ShareShortcuts](https://shareshortcuts.com) | [Location in this repository](dataset/shareshortcuts.com) | [Google Drive](https://drive.google.com/drive/folders/1hzpeQCAAgHETf2r4kDWKxk-0urM7CIaF?usp=drive_link) \| [Baidu Netdisk](https://pan.baidu.com/s/1EumV3xSLpGR41obXT7ucSQ?pwd=shn6) |
| [SiriShortcuts](https://sirishortcuts.net) | [Location in this repository](dataset/sirishortcuts.net) | [Google Drive](https://drive.google.com/drive/folders/1hrE4rw5K44ioHnTG3jqxxi6UuevjF2Pe?usp=drive_link) \| [Baidu Netdisk](https://pan.baidu.com/s/1TTbA4XP5SKAGk6_tIdA84Q?pwd=wnak) |

### Dataset Composition

This dataset includes various shortcut metadata:

```markdown
### Name: Wine Shops # Shortcut name
- URL: https://www.icloud.com/shortcuts/78ffd18288fd4da286bfd570993ea46e # Shortcut iCloud link
- Source: https://shortcutsgallery.com # Shortcut source store
- Description: Look for Wine shop near by you # Shortcut function description
```

Click on the iCloud link in the URL to automatically import the shortcut into your Shortcuts app📲.



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

*Read this in [中文](README_ZH.md).*

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

You can also visit [Shortcut Collection Sites](#data-sources-and-links-) to search for the shortcuts you want🌐.

**How to Import the Shortcuts You Found📥**

On an Apple device, clicking the iCloud link in the URL will automatically open and import the shortcut into your Shortcuts app📲.

## User Guide for Developers and Researchers📚

### Obtain the Dataset

You can download shortcuts one by one from the iCloud links in the [User Guide](#user-guide-for-shortcuts-users) or get the complete data from the following links:

- [Baidu Netdisk](https://pan.baidu.com/s/1qVX03DjSfBXXXW5W96jtqQ?pwd=33s2)
- [Google Drive](https://drive.google.com/drive/folders/171d_iiyBpQSfC-nLFpFDBq2P0Y7Tqw_m?usp=sharing)

### Data Sources and Links 🌐

| Data Source | Metadata Location | Cloud Drive Link |
| :-------: | :----: | :----: |
| [Matthewcassinelli](https://matthewcassinelli.com/sirishortcuts/library/free) | [Location in our Repo](dataset/matthewcassinelli.com_sirishortcuts_library_free) | [Google Cloud](https://drive.google.com/drive/folders/1Dq9A44qP5s6-HOducpg-pGRbsyCGRNsW?usp=drive_link) \| [Baidu Netdisk](https://pan.baidu.com/s/1Wru9TC_1MPqX26Ua6IzPQQ?pwd=3zwl) |
| [Routinehub](https://routinehub.co) | [Location in our Repo](dataset/routinehub.co) | [Google Cloud](https://drive.google.com/drive/folders/1IEhry0vnK48-GGF39kEMgQDtoSObR979?usp=drive_link) \| [Baidu Netdisk](https://pan.baidu.com/s/1WFZw-G_w9QZQDyAdcYe-Yg?pwd=lp6d) |
| [MacStories](https://www.macstories.net/shortcuts) | [Location in our Repo](dataset/www.macstories.net_shortcuts) | [Google Cloud](https://drive.google.com/drive/folders/11z32E2_mphNcrcz0jg2RZ0Tit6zxxJOy?usp=drive_link) \| [Baidu Netdisk](https://pan.baidu.com/s/1qfeCKUtTnO4gihSydfbYlg?pwd=u9p2) |
| [ShareShortcuts](https://shareshortcuts.com) | [Location in our Repo](dataset/shareshortcuts.com) | [Google Cloud](https://drive.google.com/drive/folders/197zOSqDcTlZp242NK38G1ShFs8Mi6qff?usp=drive_link) \| [Baidu Netdisk](https://pan.baidu.com/s/13M6PSPXhSMwAhDuRLlqbIw?pwd=j7gn) |
| [ShortcutsGallery](https://shortcutsgallery.com) | [Location in our Repo](dataset/shortcutsgallery.com) | [Google Cloud](https://drive.google.com/drive/folders/1ieovTT-QOZIpub8BW8I7MicM9KcwJDwB?usp=drive_link) \| [Baidu Netdisk](https://pan.baidu.com/s/1knXrn_OwPqUxaDvqSZQ1ag?pwd=ux9x) |
| [iSpazio](https://shortcuts.ispazio.net) | [Location in our Repo](dataset/shortcuts.ispazio.net) | [Google Cloud](https://drive.google.com/drive/folders/1lPmyxYE1UtKsOPNJU5b0zc6B7wyK-bns?usp=drive_link) \| [Baidu Netdisk](https://pan.baidu.com/s/1l2IIrcpK7WTYuT3Ec57SxA?pwd=0l0u) |
| [Jiejingku](https://jiejingku.net) | [Location in our Repo](dataset/jiejingku.net) | [Google Cloud](https://pan.baidu.com/s/1WdgWmGkRfevTyit4i14DOg?pwd=ud3d) \| [Baidu Netdisk](https://pan.baidu.com/s/1n0pxGttbsCttDZkVkOZiag?pwd=0yzg) |
| [Sspai](https://shortcuts.sspai.com) | [Location in our Repo](dataset/shortcuts.sspai.com) | [Google Cloud](https://pan.baidu.com/s/1BQcGi12fhtxOLD8gpt135A?pwd=tjqi) \| [Baidu Netdisk](https://pan.baidu.com/s/1M2tR9lOFr-6rIeKoB7T8PQ?pwd=22fn) |
| [Jiejing.Fun](https://jiejing.fun) | [Location in our Repo](dataset/jiejing.fun) | [Google Cloud](https://pan.baidu.com/s/1Hdco7WtgN0kEVfqcxJi3qQ?pwd=5732) \| [Baidu Netdisk](https://pan.baidu.com/s/16oSRINZK-gyy38x51QO7dQ?pwd=2fj4) |
| [kejicut](https://www.kejicut.com) | [Location in our Repo](dataset/www.kejicut.com) | [Google Cloud](https://pan.baidu.com/s/1SBlhUB3H6VPm5mwW0fHHyw?pwd=0q7p) \| [Baidu Netdisk](https://pan.baidu.com/s/1kQwvwj5tQorJeYZ22w3iUw?pwd=8eah) |
| [rcuts](https://www.rcuts.com) | [Location in our Repo](dataset/www.rcuts.com) | [Google Cloud](https://pan.baidu.com/s/1UZLcXjmAVCLwZKiK4638Ug?pwd=8vv0) \| [Baidu Netdisk](https://pan.baidu.com/s/1h8frW1928kfW38pnjJorGA?pwd=1c28) |

**Source File Structure of Shortcuts**

The source data of shortcuts in the cloud disk is organized in the following directory structure:
```
dataset/
├── matthewcassinelli.com_sirishortcuts_library_free # Website name
│   ├── file1
│   ├── file2
│   └── file3

or

dataset/
├── jiejingku.net # Website name
│   ├── category1 # Category 
│   │   ├── file1 # Each specific shortcut
│   │   └── file2
│   ├── category2
│   │   └── file3
```

Each file represents a shortcut. The file name is generated from the shortcut name after simple processing, with the following code:
```python
file_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
```

The shortcut source files we provide are in `JSON` format. Shortcuts exported from Apple devices are either `iCloud` links (shared as links) or encrypted shortcut files (with the `.shortcut` suffix).

If you wish to import a shortcut source file into the Shortcuts app, please follow these steps on `macOS`:
* Convert the `JSON` file format to `PLIST` file format 📑.
* Sign the `PLIST` file 🔏.
* Import the signed file into the Shortcuts app 📲.

## License Statement 📜

All code and datasets in this project are licensed under the `Apache License 2.0`. This means you are free to use, copy, modify, and distribute the contents of this project, but must comply with the following conditions:

- **Copyright Notice**: The original copyright notice and license statement must be retained in all copies of the project.
- **State Changes**: If you modify the code, you must indicate the changes made in any modified files.
- **Trademark Use**: This license does not grant the right to use trademarks, service marks, or trade names of the project.

For the full license text, see [LICENSE](./LICENSE).

Additionally, you must comply with the license agreements of the data sources from each shortcut sharing site.

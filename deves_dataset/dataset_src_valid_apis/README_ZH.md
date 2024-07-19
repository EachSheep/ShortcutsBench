**根据`1_final_detailed_records_remove_repeat.json`获取API元信息的步骤**

如果你只想使用最终的快捷指令数据集（该数据集中的快捷指令涉及的API的元文件均存在），请直接使用`1_final_detailed_records_filter_apis.json`文件。

如果您想进一步了解我们是如何得到`1_final_detailed_records_filter_apis.json`文件的，请阅读以下内容。

**我们提供的所有在云盘上的文件，为了防止数据污染，我们设置了解压密码，所有的解码密码均为`shortcutsbench`**。

`1_final_detailed_records_filter_apis.json`文件，可从[Google云盘](https://drive.google.com/file/d/12DJ7kWe8oRgVgdLyfr1VItETyCrpO-7O/view?usp=sharing)或[百度网盘](https://pan.baidu.com/s/12cAPTPsdzE4DBSESXCOAoA?pwd=j0p8)获取。

注：我们在整理数据和处理脚本时，进行了大量重构以简化流程方便更好的理解（例如省略了对脏数据的手动清洗的过程描述），您按照以下步骤进行的处理得到的文件和我们的难免会有不同，我们尽力确保最小的不同。

## 依据快捷指令源文件提取App的唯一标识符

我们首先依据`1_final_detailed_records_remove_repeat.json`文件提取了App的唯一标识符并进行了手动标注，得到了`2_all_detailed_identifiers.json`。

`2_all_detailed_identifiers.json`文件，可从[Google云盘](../../data/2_all_detailed_identifiers.json)获取。

`2_all_detailed_identifiers.json`的每一个元素形如：
```json
{
    "AppName": "AsheKube.app.a-Shell-mini",
    "APIs": [
        {
            "APIName": "AsheKube.app.a-Shell-mini.ExecuteCommandIntent",
            "iOS_or_macOS": "iOS"
        },
        {
            "APIName": "AsheKube.app.a-Shell-mini.GetFileIntent",
            "iOS_or_macOS": "iOS"
        },
        {
            "APIName": "AsheKube.app.a-Shell-mini.PutFileIntent",
            "iOS_or_macOS": "iOS"
        }
    ]
}
```

## 下载所有快捷指令涉及的App

随后我们依据`2_all_detailed_identifiers.json`撰写下载App的脚本。

1. 使用[`ipatool`](https://github.com/majd/ipatool)下载App。
    下载需要三个步骤，即：

    1. `ipatool auth`登录账号，我们使用美区账号登陆。
    2. `ipatool purchase -b`购买App，我们筛出了需要直接付费购买的App。

        ```json
        [
            "br.com.marcosatanaka.play", 
            "https://apps.apple.com/us/app/play-save-videos-watch-later/id1596506190", 
            "$2.99",

            "com.alexhay.Console", 

            "com.culturedcode.ThingsMac", 
            "com.culturedcode.ThingsiPad", 
            "com.culturedcode.ThingsiPhone", 
            "com.culturedcode.ThingsTouch",
            "https://apps.apple.com/us/app/things-3/id904237743", 
            "$9.99", 

            "com.guidedways.2Do", 
            "https://apps.apple.com/us/app/2do-todo-list-tasks-notes/id303656546", 
            "$9.99",

            "com.jonny.spring", 
            "https://apps.apple.com/us/app/spring-lite-for-twitter/id1637405989",
            "https://apps.apple.com/us/app/spring-for-twitter/id1508706541",
            "https://apptopia.com/ios/app/1637405989/about", 
            "$17.99",
            
            "com.ngocluu.goodlinks", 
            "https://apps.apple.com/us/app/goodlinks/id1474335294", 
            "$9.99",
            
            "com.omz-software.Pythonista3", 
            "https://apps.apple.com/us/developer/omz-software/id285608316",
            "$9.99",

            "com.pcalc.mobile", 
            "https://apps.apple.com/us/app/pcalc/id284666222", 
            "$9.99",

            "com.phocusllp.due", 
            "https://apps.apple.com/us/app/due-reminders-timers/id390017969",
            "$7.99",

            "com.pixelmatorteam.pixelmator.x", 
            "https://apps.apple.com/us/app/pixelmator/id924695435",
            "$9.99",

            "com.reederapp.5.iOS", 
            "https://apps.apple.com/us/app/reeder-5/id1529445840",
            "$4.99",

            "com.tijo.opener.Opener"
            "https://apps.apple.com/us/app/opener-open-links-in-apps/id989565871",
            "$2",
        ]
        ```
    3. `ipatool download -b`下载App。
    
2. 经过以上三个步骤，可以成功下载在iOS的App Store上架的App。
如果该App存在macOS版本，则可以`purchase`成功，但不一定能`download`成功，这些App包括：

    ```json
    "com.iconfactory.Tot",
    "failed to apply patches: failed to open zip reader: zip: not a valid zip file",
    "https://apps.apple.com/us/app/tot-pocket/id1498235191",
    "ios和mac版的都有，下了mac版的",

    "maccatalyst.com.Christopher-Hannah.Text-Case",
    "failed to apply patches: failed to open zip reader: zip: not a valid zip file",
    "ios和mac版的都有，下了mac版的",

    "me.damir.dropover-mac",
    "failed to apply patches: failed to open zip reader: zip: not a valid zip file",
    "下了mac版的",

    "com.omnigroup.OmniFocus3.MacAppStore",
    "failed to apply patches: failed to open zip reader: zip: not a valid zip file",
    "下了mac版的",
    ```

    一些只有macOS版本的App：

    ```json
    "codes.rambo.AirBuddyHelper",
    "https://v2.airbuddy.app/",
    "$16.99",
    "ios和mac版的都有，下了mac版的",

    "com.hegenberg.BetterTouchTool",
    "https://folivora.ai/",
    "下了mac版的",

    "com.charliemonroe.Downie-4",
    "https://software.charliemonroe.net/downie/",
    "下了mac版的",

    "fyi.lunar.Lunar",
    "https://lunar.fyi/",
    "下了mac版的",

    "com.flexibits.fantastical2",
    "下了mac版的",
    ```

    以及一些已经废弃的，改名，或找不到的App如：

    ```json
    "ke.bou.WidgetPack",

    "com.iconfactory.TotMobile",

    "com.7Z88K9GUU8.com.rileytestut.AltStore",
    "https://altstore.io/",

    "com.atow.LaunchCuts",
    "https://apps.apple.com/us/app/launchcuts/id1489780246",
    "ios15之后下架，不要这个了",

    "com.jiejinghe.luke",
    "https://apptopia.com/ios/app/1444534071/about",
    "找到了，但是显示地区不可用，不要这个了",

    "com.dayonelog.dayoneiphone.post",
    "https://apps.apple.com/tw/app/day-one/id1055511498?l=en-GB&mt=12?l=en",
    "ios和mac版的都有，com.bloombuilt.dayone-ios，下了ios版的。",
    "古早的app是[这个](https://apps.apple.com/us/app/day-one-classic/id421706526)，不要了",


    "com.soulmen.ulysses.pad.attach",
    " https://apps.apple.com/lu/app/ulysses-writing-app/id1225570693，ios和ios和mac版的都有，com.ulyssesapp.ios，下了ios版的。",
    "古早的app，不要了",
    ```

**收集苹果第一方App**

经过以上步骤，我们搜集到了所有可搜集的第三方App，以及部分苹果第一方App，还存在需要苹果第一方的App没有搜集。

在App Store的苹果第一方App包括：

```json
[
    "com.apple.DocumentsApp",
    "com.apple.VoiceMemos",
    "com.apple.facetime",
    "com.apple.freeform",
    "com.apple.iBooks",
    "com.apple.mobilemail",
    "com.apple.mobilenotes",
    "com.apple.mobilephone",
    "com.apple.mobilesafari",
    "com.apple.mobileslideshow",
    "com.apple.mobiletimer",
    "com.apple.news",
    "com.apple.reminders",
    "com.apple.shortcuts",
    "com.apple.weather",
]
```

不在App Store的包括：
```json
[
    "com.apple.AccessibilityUtilities.AXSettingsShortcuts",
    "com.apple.NanoSettings",
    "com.apple.Notes",
    "com.apple.PBBridgeSupport",
    "com.apple.ShortcutsActions",
    "com.apple.TVRemoteUIServicecom.apple.clock",
    "com.apple.clock",
    "com.apple.iBooksX",
    "com.apple.mobiletimer-framework",
    "com.apple.musicrecognition",
    "com.apple.printcenter",
    "com.apple.iWork.Keynote",
    "is.workflow.actions"
]
```

我们在`macOS Sonoma`的`/Applications/`, `/System/Application/`搜集到了大部分苹果第一方的App。

**最终**：我们整理到的App可从[Google云盘](https://drive.google.com/file/d/1Xks3TXyVOWmMgoXui69CombPqJT6wbj4/view?usp=sharing)或者[百度网盘](https://pan.baidu.com/s/1UxBiOdncrS6dxLzvL5__GQ?pwd=h5b7)访问。

```
ToGetAPIs/
├── ios-free-apps # ios上的app，共57个
│   ├── ai.perplexity.app_1668000334_2.17.2.ipa
│   ├── ......
│   └── org.joinmastodon.app_1571998974_2024.3.ipa
├── ios-system-apps # 苹果第一方app，共8+10=18个
│   ├── com.apple.Keynote_361285480_14.0.ipa
│   ├── ......
│   ├── com.apple.weather_1069513131_1.9.ipa
│   └── useless # 部分虽然App存在，但是不存在API定义文件的App
├── mac-free-apps # mac版本的app，共13个
│   ├── codes.rambo.AirBuddyHelper
│   ├── ......
│   └── me.damir.dropover-mac
```

共`57+18+13=88`个第三方App。

除了第三方App，还包括如`com.apple.AccessibilityUtilities`和`is.workflow.actions`等指示的苹果操作系统和快捷指令App所提供的API。
我们从`/System/Library/PrivateFrameworks/WorkflowKit.framework/`中的`WFActions.json`文件中搜集到了这一部分API。

`/System/Library/PrivateFrameworks/WorkflowKit.framework/`文件可从[Google云盘](https://drive.google.com/file/d/1EqF2uRwAfviJ10fKJq6JBjBLebWDPrR_/view?usp=sharing)或[百度网盘](https://pan.baidu.com/s/1E7y6RzsWG1JR5pL9tn_1Vg?pwd=xw2m)获取。

## 从App中提取出API

至此，我们已经拥有了所有第三方App的文件。

随后，我们需要提取所有第三方App的含有API的配置文件以获取API的元信息。
而苹果操作系统和快捷指令App所提供的API则绝大部分在`/System/Library/PrivateFrameworks/WorkflowKit.framework/`中的`WFActions.json`文件中，不需要额外提取。

提取metadata的过程如下：
1. 首先复制一份`2_all_detailed_identifiers.json`文件，改名为`4_api_json.json`。
2. 将`ToGetAPIs`目录放到`$SHORTCUT_DATA`指示的目录下，并将所有`.ipa`格式的App解压放到相同目录。
3. 修改`4_extract_api_metadata.py`中的`app_dir_path`为App所在文件夹，运行`4_extract_api_metadata.py`，这会将`app_dir_path`所指示的文件夹下的所有API信息提取出来放到`4_api_json.json`中。

最终我们得到了`4_api_json.json`文件，该文件中存储着所有我们提取出的API信息。

由于提取出的API文件存在大量重复的API定义文件，我们进行了**初步**的去重，依据对应的api定义文件（即json文件）是否完全相同进行了初步去重，得到了`4_api_json_filter.json`文件。

注：此处的去重大大减小了API文件的大小，但依旧存在许多同名的API文件，在后续实验时，我们按照以下规则提取API文件：
1. 优先先择`.actionsdata`指示的文件。存在多个`.actionsdata`文件的，我们选择第一个。
2. 如果没有`.actionsdata`文件，我们选择`.intentdefinition`文件。存在多个`.intentdefinition`文件的，我们选择第一个。
我们确保了相同名字的API，我们只保留一个。

`4_api_json.json`文件可从[Google云盘](https://drive.google.com/file/d/1clvUZ8MOcziy9rCg5ugj5V9O0kg7-iCK/view?usp=sharing)或[百度网盘](https://pan.baidu.com/s/1uM3gJPBr_JRPw9SaZVzXSg?pwd=ghsl)获取。

`4_api_json_filter.json`文件可从[Google云盘](https://drive.google.com/file/d/1ZFk6IybvUq8BY8uF06ckqMii-dVV5-lF/view?usp=sharing)或[百度网盘](https://pan.baidu.com/s/1uEYXnTbFz7Nvaunvv8F6_w?pwd=zpft)获取。

**注：此时，我们拥有的API为`4_api_json_filter.json`指示的API + `WFActions.json`指示的API**。

## 依据提取出的API对快捷指令文件即`1_final_detailed_records_remove_repeat`进行筛选

我们获得的API由于App的更新、废弃等原因，可能存在诸多遗漏，为了保证所有快捷指令中的API都具有对应的API描述，我们依据提取出的API对快捷指令文件即`1_final_detailed_records_remove_repeat`进行筛选，筛掉那些在快捷指令中存在，但是没有API描述的快捷指令。

筛选的规则是：只要快捷指令中存在一个API不存在，即筛除掉这个快捷指令。我们手动筛选出了不存在的API，对应的处理脚本如`deves_dataset/dataset_src_valid_apis/4_check_apis_intersection.py`所示。

最终我们筛除掉的API如`deves_dataset/dataset_src_valid_apis/APIs_to_be_filtered_out.py`所示。

依据`deves_dataset/dataset_src_valid_apis/APIs_to_be_filtered_out.py`筛选快捷指令，生成`1_final_detailed_records_filter_apis.json`的处理代码如`deves_dataset/dataset_src_valid_apis/4_remove_shortcuts_indicated_in_filter_apis.py`所示。
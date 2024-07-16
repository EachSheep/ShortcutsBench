**Steps to Retrieve API Metadata from `1_final_detailed_records_remove_repeat.json`**

If you only want to use the final shortcuts dataset (where all the APIs' metadata files are present), please use the `1_final_detailed_records_filter_apis.json` file directly.

If you want to understand how we generated the `1_final_detailed_records_filter_apis.json` file, please read the following details.

**All the files we provide on the cloud drive are password-protected to prevent data contamination. The password for all files is `shortcutsbench`.**

You can obtain the `1_final_detailed_records_filter_apis.json` file from [Google Drive](https://drive.google.com/file/d/12DJ7kWe8oRgVgdLyfr1VItETyCrpO-7O/view?usp=sharing) or [Baidu Cloud](https://pan.baidu.com/s/12cAPTPsdzE4DBSESXCOAoA?pwd=j0p8).

Note: We have performed extensive restructuring of data and processing scripts to simplify the process and enhance understanding (for example, omitting the manual cleaning of dirty data). The files you generate by following the steps below might differ from ours, but we have endeavored to minimize these differences.

## Extracting Unique Identifiers for Apps Based on Shortcut Source Files

We first extracted the unique identifiers for apps from the `1_final_detailed_records_remove_repeat.json` file and manually annotated them to create `2_all_detailed_identifiers.json`.

The `2_all_detailed_identifiers.json` file can be obtained from [Google Drive](https://drive.google.com/file/d/1BkbjVKSPv2dHn16xTAhh0LNk2iVQEb-0/view?usp=sharing) or [Baidu Cloud](https://pan.baidu.com/s/1j0d1VDNWx3K5TTS4smM4Ug?pwd=z636).

Each element in `2_all_detailed_identifiers.json` looks like:
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

## Download All Apps Involved in Shortcuts

Next, we wrote a script to download the apps based on `2_all_detailed_identifiers.json`.

1. Use [`ipatool`](https://github.com/majd/ipatool) to download the apps. This process involves three steps:

    1. Log in to your account using `ipatool auth`. We logged in using a US account.
    2. Purchase the apps using `ipatool purchase -b`. We filtered out apps that require direct payment.

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

            "com.tijo.opener.Opener",
            "https://apps.apple.com/us/app/opener-open-links-in-apps/id989565871",
            "$2",
        ]
        ```
    3. Download the apps using `ipatool download -b`.

2. After completing the three steps above, you can successfully download apps listed on the iOS App Store.
If the app has a macOS version, the `purchase` will succeed, but the `download` might not. These apps include:

    ```json
    "com.iconfactory.Tot",
    "failed to apply patches: failed to open zip reader: zip: not a valid zip file",
    "https://apps.apple.com/us/app/tot-pocket/id1498235191",
    "Both iOS and macOS versions exist, downloaded the macOS version",

    "maccatalyst.com.Christopher-Hannah.Text-Case",
    "failed to apply patches: failed to open zip reader: zip: not a valid zip file",
    "Both iOS and macOS versions exist, downloaded the macOS version",

    "me.damir.dropover-mac",
    "failed to apply patches: failed to open zip reader: zip: not a valid zip file",
    "Downloaded the macOS version",

    "com.omnigroup.OmniFocus3.MacAppStore",
    "failed to apply patches: failed to open zip reader: zip: not a valid zip file",
    "Downloaded the macOS version",
    ```

    Some apps only have a macOS version:

    ```json
    "codes.rambo.AirBuddyHelper",
    "https://v2.airbuddy.app/",
    "$16.99",
    "Both iOS and macOS versions exist, downloaded the macOS version",

    "com.hegenberg.BetterTouchTool",
    "https://folivora.ai/",
    "Downloaded the macOS version",

    "com.charliemonroe.Downie-4",
    "https://software.charliemonroe.net/downie/",
    "Downloaded the macOS version",

    "fyi.lunar.Lunar",
    "https://lunar.fyi/",
    "Downloaded the macOS version",

    "com.flexibits.fantastical2",
    "Downloaded the macOS version",
    ```

    Additionally, some apps are deprecated, renamed, or not found:

    ```json
    "ke.bou.WidgetPack",

    "com.iconfactory.TotMobile",

    "com.7Z88K9GUU8.com.rileytestut.AltStore",
    "https://altstore.io/",

    "com.atow.LaunchCuts",
    "https://apps.apple.com/us/app/launchcuts/id1489780246",
    "Removed after iOS 15, not needed",

    "com.jiejinghe.luke",
    "https://apptopia.com/ios/app/1444534071/about",
    "Found but unavailable in the region, not needed",

    "com.dayonelog.dayoneiphone.post",
    "https://apps.apple.com/tw/app/day-one/id1055511498?l=en-GB&mt=12?l=en",
    "Both iOS and macOS versions exist, com.bloombuilt.dayone-ios, downloaded the iOS version",
    "The old version of the app is [here](https://apps.apple.com/us/app/day-one-classic/id421706526), not needed",

    "com.soulmen.ulysses.pad.attach",
    "https://apps.apple.com/lu/app/ulysses-writing-app/id1225570693, both iOS and macOS versions exist, com.ulyssesapp.ios, downloaded the iOS version",
    "The old version of the app, not needed",
    ```

**Collecting Apple's First-Party Apps**

After the above steps, we collected all the third-party apps we could find, as well as some of Apple's first-party apps. However, there are still some first-party apps that have not been collected.

The Apple first-party apps available on the App Store include:

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
    "com.apple.weather"
]
```

The apps not available on the App Store include:

```json
[
    "com.apple.AccessibilityUtilities.AXSettingsShortcuts",
    "com.apple.NanoSettings",
    "com.apple.Notes",
    "com.apple.PBBridgeSupport",
    "com.apple.ShortcutsActions",
    "com.apple.TVRemoteUIService",
    "com.apple.clock",
    "com.apple.iBooksX",
    "com.apple.mobiletimer-framework",
    "com.apple.musicrecognition",
    "com.apple.printcenter",
    "com.apple.iWork.Keynote",
    "is.workflow.actions"
]
```

We collected most of Apple's first-party apps from `/Applications/` and `/System/Applications/` on `macOS Sonoma`.

**Finally**: The collected apps can be accessed from [Google Drive](https://drive.google.com/file/d/1Xks3TXyVOWmMgoXui69CombPqJT6wbj4/view?usp=sharing) or [Baidu Cloud](https://pan.baidu.com/s/1UxBiOdncrS6dxLzvL5__GQ?pwd=h5b7).

```
ToGetAPIs/
├── ios-free-apps # Apps on iOS, totaling 57
│   ├── ai.perplexity.app_1668000334_2.17.2.ipa
│   ├── ......
│   └── org.joinmastodon.app_1571998974_2024.3.ipa
├── ios-system-apps # Apple's first-party apps, totaling 8+10=18
│   ├── com.apple.Keynote_361285480_14.0.ipa
│   ├── ......
│   ├── com.apple.weather_1069513131_1.9.ipa
│   └── useless # Apps that exist but do not have API definition files
├── mac-free-apps # Apps on macOS, totaling 13
│   ├── codes.rambo.AirBuddyHelper
│   ├── ......
│   └── me.damir.dropover-mac
```

A total of `57+18+13=88` third-party apps.

In addition to third-party apps, we also include APIs provided by Apple's operating system and shortcuts apps, such as `com.apple.AccessibilityUtilities` and `is.workflow.actions`. These APIs were collected from the `WFActions.json` file in `/System/Library/PrivateFrameworks/WorkflowKit.framework/`.

The `/System/Library/PrivateFrameworks/WorkflowKit.framework/` file can be obtained from [Google Drive](https://drive.google.com/file/d/1EqF2uRwAfviJ10fKJq6JBjBLebWDPrR_/view?usp=sharing) or [Baidu Cloud](https://pan.baidu.com/s/1E7y6RzsWG1JR5pL9tn_1Vg?pwd=xw2m).

## Extracting APIs from Apps

At this point, we have all the files for third-party apps.

Next, we need to extract configuration files containing APIs from all third-party apps to obtain the API metadata. Most of the APIs provided by Apple's operating system and shortcuts apps are in the `WFActions.json` file located at `/System/Library/PrivateFrameworks/WorkflowKit.framework/`, so no additional extraction is needed for those.

The process to extract metadata is as follows:
1. First, copy the `2_all_detailed_identifiers.json` file and rename it to `4_api_json.json`.
2. Place the `ToGetAPIs` directory in the location specified by `$SHORTCUT_DATA` and unzip all `.ipa` apps into the same directory.
3. Modify the `app_dir_path` in `4_extract_api_metadata.py` to point to the folder containing the apps, and run `4_extract_api_metadata.py`. This will extract all API information from the folder specified by `app_dir_path` into `4_api_json.json`.

Ultimately, we obtained the `4_api_json.json` file, which stores all the API information we extracted.

Since there were many duplicate API definition files in the extracted APIs, we performed an **initial** deduplication. This deduplication was based on whether the corresponding API definition files (i.e., JSON files) were identical, resulting in the `4_api_json_filter.json` file.

Note: This deduplication significantly reduced the size of the API files, but there are still many APIs with the same name. In subsequent experiments, we extracted API files according to the following rules:
1. Prefer files indicated by `.actionsdata`. If there are multiple `.actionsdata` files, we select the first one.
2. If there are no `.actionsdata` files, we select `.intentdefinition` files. If there are multiple `.intentdefinition` files, we select the first one.
We ensured that for APIs with the same name, we only retained one.

The `4_api_json.json` file can be obtained from [Google Drive](https://drive.google.com/file/d/1clvUZ8MOcziy9rCg5ugj5V9O0kg7-iCK/view?usp=sharing) or [Baidu Cloud](https://pan.baidu.com/s/1uM3gJPBr_JRPw9SaZVzXSg?pwd=ghsl).

The `4_api_json_filter.json` file can be obtained from [Google Drive](https://drive.google.com/file/d/1ZFk6IybvUq8BY8uF06ckqMii-dVV5-lF/view?usp=sharing) or [Baidu Cloud](https://pan.baidu.com/s/1uEYXnTbFz7Nvaunvv8F6_w?pwd=zpft).

**Note: At this stage, the APIs we have include those indicated by `4_api_json_filter.json` and `WFActions.json`.**

## Filtering Shortcut Files `1_final_detailed_records_remove_repeat` Based on Extracted APIs

Due to updates and deprecations of apps, the APIs we obtained may have many omissions. To ensure that all APIs in the shortcuts have corresponding API descriptions, we filter the shortcut file `1_final_detailed_records_remove_repeat` based on the extracted APIs, removing shortcuts that contain APIs without descriptions.

The filtering rule is: if a shortcut contains even one API that is missing, the entire shortcut is filtered out. We manually identified the missing APIs, and the corresponding script is shown in `deves_dataset/dataset_src_valid_apis/4_check_apis_intersection.py`.

The APIs we filtered out are listed in `deves_dataset/dataset_src_valid_apis/APIs_to_be_filtered_out.py`.

To filter the shortcuts based on `deves_dataset/dataset_src_valid_apis/APIs_to_be_filtered_out.py` and generate `1_final_detailed_records_filter_apis.json`, the processing code is shown in `deves_dataset/dataset_src_valid_apis/4_remove_shortcuts_indicated_in_filter_apis.py`.
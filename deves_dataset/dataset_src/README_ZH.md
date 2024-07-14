**从shortcuts的各种捷径商店收集到的原始快捷指令元数据 和 处理这些数据得到快捷指令源文件的脚本**

如果你只想使用最终的快捷指令数据集（未根据API的可用状态筛除掉部分快捷指令的全量数据集，即该数据集中的部分快捷指令包含我们没有获取到的部分API），请直接使用`1_final_detailed_records_remove_repeat.json`文件。

如果您想进一步了解我们是如何得到`1_final_detailed_records_remove_repeat.json`文件的，请阅读以下内容。

## 数据文件介绍

前期，我们收集了最流行的一些快捷指令站，然后使用爬虫获取了大量快捷指令的元数据，每个收集站对应的文件为：

* [Routinehub](https://routinehub.co)：`deves_dataset/dataset_src/routinehub.co.json`
* [MacStories](https://www.macstories.net/shortcuts)：`deves_dataset/dataset_src/www.macstories.net.json`
* [ShareShortcuts](https://shareshortcuts.com)：`deves_dataset/dataset_src/shareshortcuts.com.json`
* [ShortcutsGallery](https://shortcutsgallery.com)：`deves_dataset/dataset_src/shortcutsgallery.com.json`
* [iSpazio](https://shortcuts.ispazio.net)：`deves_dataset/dataset_src/shortcuts.ispazio.net.json`
* [Free Matthewcassinelli](https://matthewcassinelli.com/sirishortcuts/library/free)：`deves_dataset/dataset_src/free_matthewcassinelli.com.json`
* [Member Matthew Cassinelli](https://matthewcassinelli.com/membership/shortcuts/)：`deves_dataset/dataset_src/memberonly_matthewcassinelli.com.json`
* [捷径库](https://jiejingku.net)：`deves_dataset/dataset_src/jiejingku.com.json`
* [少数派](https://shortcuts.sspai.com)：`deves_dataset/dataset_src/shortcuts.sspai.com.json`
* [捷径范](https://jiejing.fun)：`deves_dataset/dataset_src/jiejing.fun.json`
* [柯基捷径库](https://www.kejicut.com)：`deves_dataset/dataset_src/www.kejicut.com.json`
* [iOS快捷指令库](https://www.rcuts.com)：`deves_dataset/dataset_src/www.rcuts.com.json`
* Shortcuts from Reddit/Quora：`deves_dataset/dataset_src/others.json`

## 配置环境变量

需要首先配置`export SHORTCUT_PROJECT=你的项目的绝对路径`。
比如我的项目目录为`$HOME/Source/shortcuts/`，则配置为`export SHORTCUT_PROJECT=$HOME/Source/shortcuts/`。

## 运行 `all_wo_repeat.py`

对所有从商店获取的数据进行去重处理（不包括`others.json`）。存在一些虽然URL相同，但是描述不同的数据，全部保留下来，`multiple`字段标识为`true`。
所有去重的数据存在`all_wo_repeat.json`中。

## 运行`all_detailed_records.py`

对所有`all_wo_repeat.json`和`others.json`中的数据（会对`all_wo_repeat.json`和`others.json`中的数据做合并去重，优先保留`all_wo_repeat.json`中的数据），向类似`https://www.icloud.com/shortcuts/api/records/cc2283b9eaa947e6a049b2020755fad1`的URL发送请求进一步获得相关数据，并存在`all_detailed_records.json`中。

发送请求的同时，会同时获取shortcut的源文件，并用`biplist`包解析存下。

**最终**：获得的`all_detailed_records.json`文件

`all_detailed_records.json`文件形如：

```json
{
    "Source": "https://matthewcassinelli.com/sirishortcuts/library/free",
    "MemberOnly": false,
    "NameINStore": "Show my Regal Unlimited Card",
    "CategoryInStore": null,
    "DescriptionInStore": "Opens the Regal website to your Unlimited account page so you can tap to reveal the QR code for your card number.",
    "Downloads": null,
    "Favorites": null,
    "Reads": null,
    "Rates": null,
    "URL": "https://www.icloud.com/shortcuts/e6fa8dd9e012484bb85c9967f0b83f02",
    "multiple": false,
    "records": {
        "created": {
        "userRecordName": "_bc43d2662d27d57a905202643637d01c",
        "timestamp": 1711823013767,
        "deviceID": "3CEEFEE1-EC52-4D27-9F59-81BF91700072"
        },
        "pluginFields": {},
        "recordType": "SharedShortcut",
        "deleted": false,
        "fields": {
        "icon": {
            "type": "ASSETID",
            "value": {
            "size": 26792,
            "fileChecksum": "AX7iZnwtB1nkHdl8/NcCfL7/TMRO",
            "downloadURL": "https://cvws.icloud-content.com/B/AX7iZnwtB1nkHdl8_NcCfL7_TMRO/${f}?o=AtV3k77520JIx_69n6o_KPTyWjYcJPW3vDK79OUwfxzckVVZq_DteQ3-jPyfWkrc7A&v=1&x=3&a=CAogKLlYNtaRkhnffr49it5GqPqwvyi20EIoWS_hIpLIH-sSexC8yv_26TEYvKfb-OkxIgEAUgT_TMROajBYuseqYl_CqXaI3xCi2mcqdnKe5zJHt2lu1koV7JZ8ehbvYuUS1kgjyGAObRrQ-oVyMGy6JwJflX9Y3KLrTh8S_dZL7ilVAjtXb3P0rzR4cu2FMEa92sOCWHmy-NX-uKa5wA&e=1712066057&fl=&r=7502267e-0357-481b-81b1-11c8ce54fd06-1&k=_&ckc=com.apple.shortcuts&ckz=_defaultZone&p=33&s=lBetKLn09o2ku8UamjLKPlsexgE"
            }
        },
        "signedShortcut": {
            "type": "ASSETID",
            "value": {
            "size": 22231,
            "downloadURL": "https://cvws.icloud-content.com/B/AV6xEPkQTR0twKp9EZNO0megzZxI/${f}?o=Aqt39yBqXb2-_xkrAC-dPNhvFGhcCAhUlIVd2yHArVNOY4EXbEhh1Ala5_0O4GbImA&v=1&x=3&a=CAog86QcagKTZ1vY8wjHeObZJSHBpvRv5baGcAyixzcGD5cSexC7yv_26TEYu6fb-OkxIgEAUgSgzZxIajBvoRULiAIQUlHDzhAwqnUxVY2LluvUelnruq6WK_DJEVdmuKND-cSSw8h3WGbzMphyML0JQ3jKc592SYOmhUbsqCvsdcFVipEaTSeitc5D6hXSE4apx9H2FpOj_TmRg0iomw&e=1712066057&fl=&r=7502267e-0357-481b-81b1-11c8ce54fd06-1&k=_&ckc=com.apple.shortcuts&ckz=_defaultZone&p=33&s=dZmVNNnym4L_wgMg1FKV1x9RyoQ",
            "fileChecksum": "AV6xEPkQTR0twKp9EZNO0megzZxI"
            }
        },
        "name": {
            "type": "STRING",
            "value": "Show my Regal Unlimited Card"
        },
        "icon_color": {
            "type": "NUMBER_INT64",
            "value": 4251333119
        },
        "shortcut": {
            "value": {
            "fileChecksum": "AZRGlbXV+PlrIHLh+fKjasSlq2KV",
            "downloadURL": "https://cvws.icloud-content.com/B/AZRGlbXV-PlrIHLh-fKjasSlq2KV/${f}?o=AgOT8iwitE4XXRIW4E6MD0xOiUaiQpGnkq2AVWGhCF3aIPvDZ1DWm0Wdpmn-G4EPZQ&v=1&x=3&a=CAogftFt4fIuUqDXyN7ePvPM_JL_fL1WmHwV2zbM5_H7DvYSexC8yv_26TEYvKfb-OkxIgEAUgSlq2KVajBjxWDhVgzeTEN4oOxkW_Sa3uOGYEnTd1SuA-cZtrMfaqAtBD_ClhJ1kaMfpg5UwN1yMHTb9CZ1FNVFC4aU6ZTV-PkoQsYa3JXmC2KgYLsORfMqqDmY7AR-n1ng_Cv9wx9s8Q&e=1712066057&fl=&r=7502267e-0357-481b-81b1-11c8ce54fd06-1&k=_&ckc=com.apple.shortcuts&ckz=_defaultZone&p=33&s=kpWKre48Kc61DCWwcgwxJy9zLxA",
            "size": 1704
            },
            "type": "ASSETID"
        },
        "maliciousScanningContentVersion": {
            "type": "NUMBER_INT64",
            "value": 1
        },
        "signingStatus": {
            "type": "STRING",
            "value": "APPROVED"
        },
        "icon_glyph": {
            "type": "NUMBER_INT64",
            "value": 59819
        },
        "signingCertificateExpirationDate": {
            "value": 1746060769000,
            "type": "TIMESTAMP"
        }
        },
        "recordChangeTag": "luef82uk",
        "modified": {
        "userRecordName": "_a702d02db102341342355d5ae64b8e07",
        "timestamp": 1711933371665,
        "deviceID": "2"
        },
        "recordName": "E6FA8DD9-E012-484B-B85C-9967F0B83F02"
    },
    "shortcut": {
      "WFWorkflowMinimumClientVersionString": "900",
      "WFWorkflowMinimumClientVersion": 900,
      "WFWorkflowIcon": {
        "WFWorkflowIconStartColor": 4251333119,
        "WFWorkflowIconGlyphNumber": 59819
      },
      "WFWorkflowClientVersion": "2510.0.2.1.3",
      "WFWorkflowOutputContentItemClasses": [],
      "WFWorkflowHasOutputFallback": false,
      "WFWorkflowActions": [
        {
          "WFWorkflowActionIdentifier": "is.workflow.actions.comment",
          "WFWorkflowActionParameters": {
            "WFCommentActionText": "Opens the Regal website to your Unlimited account page so you can tap to reveal the QR code for your card number."
          }
        },
        {
          "WFWorkflowActionIdentifier": "is.workflow.actions.url",
          "WFWorkflowActionParameters": {
            "WFURLActionURL": "https://experience.regmovies.com/unlimited",
            "UUID": "BD1FD9AE-BDDD-4FA5-994D-747D9AD1EFEC"
          }
        },
        {
          "WFWorkflowActionIdentifier": "is.workflow.actions.openurl",
          "WFWorkflowActionParameters": {
            "WFInput": {
              "Value": {
                "OutputUUID": "BD1FD9AE-BDDD-4FA5-994D-747D9AD1EFEC",
                "Type": "ActionOutput",
                "OutputName": "URL"
              },
              "WFSerializationType": "WFTextTokenAttachment"
            },
            "UUID": "40614FA6-3618-4C4C-97E3-07757D9C1B1E"
          }
        }
      ],
      "WFWorkflowInputContentItemClasses": [
        "WFAppContentItem",
        "WFAppStoreAppContentItem",
        "WFArticleContentItem",
        "WFContactContentItem",
        "WFDateContentItem",
        "WFEmailAddressContentItem",
        "WFFolderContentItem",
        "WFGenericFileContentItem",
        "WFImageContentItem",
        "WFiTunesProductContentItem",
        "WFLocationContentItem",
        "WFDCMapsLinkContentItem",
        "WFAVAssetContentItem",
        "WFPDFContentItem",
        "WFPhoneNumberContentItem",
        "WFRichTextContentItem",
        "WFSafariWebPageContentItem",
        "WFStringContentItem",
        "WFURLContentItem"
      ],
      "WFWorkflowImportQuestions": [],
      "WFQuickActionSurfaces": [],
      "WFWorkflowTypes": [],
      "WFWorkflowHasShortcutInputVariables": false
    }
}
```

我们发现存在部分 `"multiple" = true` 即iCloud链接相同，但是名称或描述却不相同的快捷指令。

## 运行merge_results.py

于是我们使用 `merge_results.py` 依据 `all_detailed_records.json` 文件生成 `final_detailed_records.json` 文件，这大大减小了文件体积，并去除了大量重复的快捷指令

使用`merge_results.py`前需要配置`SHORTCUT_DATA`环境变量，指示`all_detailed_records.json`存储的目录。

最终我们得到 `final_detailed_records.json` 文件：

```json
{
    "Source": ["https://matthewcassinelli.com/sirishortcuts/library/free"],
    "MemberOnly": [false],
    "NameINStore": ["Show my Regal Unlimited Card"],
    "CategoryInStore": [null],
    "DescriptionInStore": ["Opens the Regal website to your Unlimited account page so you can tap to reveal the QR code for your card number."],
    "Downloads": [null],
    "Favorites": [null],
    "Reads": [null],
    "Rates": [null],
    "URL": "https://www.icloud.com/shortcuts/e6fa8dd9e012484bb85c9967f0b83f02",
    "records": {xxx},
    "shortcut": {xxx}
}
```

## 手动去重

`final_detailed_records.json`中的文件的`NameINStore`字段和`DescriptionInStore`字段可能存在多个，我们进行了手动去重，只保留了一个。

最终，我们得到了`1_final_detailed_records_remove_repeat.json`
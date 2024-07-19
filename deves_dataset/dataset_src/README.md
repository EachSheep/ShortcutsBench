**Original Shortcut Metadata Collected from Various Shortcut Stores and Scripts for Processing These Data into Shortcut Source Files**

If you only want to use the final shortcut dataset (a comprehensive dataset without filtering out shortcuts based on API availability, meaning it includes some shortcuts for which we did not retrieve certain APIs), please use the `1_final_detailed_records_remove_repeat.json` file directly.

If you want to understand how we generated the `1_final_detailed_records_remove_repeat.json` file, please read the following content.

**All files we provide on the cloud drive are password-protected to prevent data corruption. The password for all files is `shortcutsbench`.**

The `1_final_detailed_records_remove_repeat.json` file can be downloaded from [Google Drive](https://drive.google.com/file/d/1oijSStXYGcmv6-THYVb6j0oCIfto_bVh/view?usp=sharing) or [Baidu Netdisk](https://pan.baidu.com/s/1VJMDcWv3diRzecQisA80bQ?pwd=4wv1).

## Data File Introduction

Initially, we collected metadata for numerous shortcuts from some of the most popular shortcut sites using web crawlers. The corresponding files for each collection site are:

* [Routinehub](https://routinehub.co): `deves_dataset/dataset_src/routinehub.co.json`
* [MacStories](https://www.macstories.net/shortcuts): `deves_dataset/dataset_src/www.macstories.net.json`
* [ShareShortcuts](https://shareshortcuts.com): `deves_dataset/dataset_src/shareshortcuts.com.json`
* [ShortcutsGallery](https://shortcutsgallery.com): `deves_dataset/dataset_src/shortcutsgallery.com.json`
* [iSpazio](https://shortcuts.ispazio.net): `deves_dataset/dataset_src/shortcuts.ispazio.net.json`
* [Free Matthew Cassinelli](https://matthewcassinelli.com/sirishortcuts/library/free): `deves_dataset/dataset_src/free_matthewcassinelli.com.json`
* [Member Matthew Cassinelli](https://matthewcassinelli.com/membership/shortcuts/): `deves_dataset/dataset_src/memberonly_matthewcassinelli.com.json`
* [捷径库](https://jiejingku.net): `deves_dataset/dataset_src/jiejingku.com.json`
* [少数派](https://shortcuts.sspai.com): `deves_dataset/dataset_src/shortcuts.sspai.com.json`
* [捷径范](https://jiejing.fun): `deves_dataset/dataset_src/jiejing.fun.json`
* [柯基捷径库](https://www.kejicut.com): `deves_dataset/dataset_src/www.kejicut.com.json`
* [iOS快捷指令库](https://www.rcuts.com): `deves_dataset/dataset_src/www.rcuts.com.json`
* Shortcuts from Reddit/Quora: `deves_dataset/dataset_src/others.json`

## Set Environment Variables

First, configure the environment variable `export SHORTCUT_PROJECT=your project's absolute path`.
For example, if my shortcuts directory is located at `$HOME/Source/shortcuts/`, configure it as `export SHORTCUT_PROJECT=$HOME/Source/shortcuts/`.

## Run `all_wo_repeat.py`

`all_wo_repeat.py`: Deduplicates all data obtained from the store (not include `others.json`). Some data have the same URL but different descriptions; all are retained and marked with the `multiple` field set to `true`.
All deduplicated data is stored in `all_wo_repeat.json`.

## Run `all_detailed_records.py`

For all data in `all_wo_repeat.json` and `others.json` (merging and deduplicating data from both files, prioritizing data from `all_wo_repeat.json`), send requests to URLs like `https://www.icloud.com/shortcuts/api/records/cc2283b9eaa947e6a049b2020755fad1` to further obtain related data, and store the results in `1_all_detailed_records.json`.

During the request process, the shortcut source files are also retrieved and parsed using the biplist package.

We have obtained the `1_all_detailed_records.json` file, which can be accessed via [Google Drive](https://drive.google.com/file/d/1KZf3mTCDuOimwbZY7wJ-2R_tDmASMB-V/view?usp=sharing) or [Baidu Netdisk](https://pan.baidu.com/s/1xx-C-w5aah7Mi04hXT47ZA?pwd=jkvp).

**Final**: The resulting `1_all_detailed_records.json` file

The `1_all_detailed_records.json` file is structured as follows:

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

We discovered that some shortcuts have `"multiple" = true`, indicating identical iCloud links, but differing names or descriptions.

## Run `merge_results.py`

Thus, we used `merge_results.py` to generate the `1_final_detailed_records.json` file based on `1_all_detailed_records.json`. This significantly reduced the file size and removed numerous duplicate shortcuts.

Before using `merge_results.py`, you need to set the `SHORTCUT_DATA` environment variable to indicate the directory where `1_all_detailed_records.json` is stored.

The final result is the `1_final_detailed_records.json` file:

The `1_final_detailed_records.json` file we obtained can be downloaded from [Google Drive](https://drive.google.com/file/d/1MwFyVdS1HmZvesl7AcgJaGcP1ghAk4J6/view?usp=sharing) or [Baidu Netdisk](https://pan.baidu.com/s/10lMA2--9WJQS5x7CnjNhkw?pwd=ioqv).

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

## Manual Deduplication

In `1_final_detailed_records.json`, there may be multiple entries for the `NameInStore` and `DescriptionInStore` fields. We manually deduplicated these entries, retaining only one.

Finally, we get `1_final_detailed_records_remove_repeat.json`。

The `1_final_detailed_records_remove_repeat.json` file we obtained can be downloaded from [Google Drive](https://drive.google.com/file/d/1oijSStXYGcmv6-THYVb6j0oCIfto_bVh/view?usp=sharing) or [Baidu Netdisk](https://pan.baidu.com/s/1VJMDcWv3diRzecQisA80bQ?pwd=4wv1).
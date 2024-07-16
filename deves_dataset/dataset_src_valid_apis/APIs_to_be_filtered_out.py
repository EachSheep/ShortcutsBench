no_apps_or_apis = [

    # This app is not available.
    'ke.bou.WidgetPack',
    'com.iconfactory.TotMobile',
    "com.7Z88K9GUU8.com.rileytestut.AltStore",
    "com.atow.LaunchCuts",
    "com.jiejinghe.luke",
    "com.dayonelog.dayoneiphone.post",
    "com.soulmen.ulysses.pad.attach",

    # This api is not available.
    "net.shinyfrog.bear-IOS.add",
    "net.shinyfrog.bear-IOS.create",
    "net.shinyfrog.bear-IOS.grab",
    "net.shinyfrog.bear-IOS.open",
    "net.shinyfrog.bear-iOS.SFCreateNoteIntent",
    "net.shinyfrog.bear-iOS.SFOpenNoteIntent",
    "com.google.chrome.ios.openurl",
    "com.burbn.instagram.openin",
    "com.flexibits.fantastical2.addevent",
    "com.getcardpointers.app.ShortcutsOfferEntity",
    "fyi.lunar.Lunar.Screen",
    "fm.overcast.overcast.add",
    "com.lifx.lifx.LFXLightSceneIntent",
    "com.microsoft.to-do.WLAddTaskIntent",
    "com.ulyssesapp.mac.ULNewSheetIntent",
    "com.ulyssesapp.mac.ULOpenIntent",
    "com.omnigroup.OmniFocus2.iPhone",
    "com.soulmen.ulysses.pad",
    "com.tapbots.Ivory.PTHIvoryOpenIntent",
    "com.tapbots.Ivory.PTHIvoryPostStatusIntent",
    "com.apple.Notes.ICNotesFolderIntent",

    "is.workflow.actions.file.getlink", # The API parameters have changed.
    "com.apple.mobiletimer-framework.MobileTimerIntents.MTCreateAlarmIntent",

    "net.whatsapp.WhatsApp", # The file lacks .intentdefinition or .actionsata.
    "com.skype.skype",

    # "com.rivian.ios.consumer", # This app package cannot be found to run on macOS
    # "com.google.chrome.ios", # Chrome on macOS does not support corresponding actions
    # "io.pushcut.Pushcut", # This package cannot run on macOS
    # "dk.simonbs.Scriptable", # This package cannot run on macOS
    # "com.6X.LockLauncher", # This package cannot run on macOS
    # "com.openai.chat", # This package cannot run on macOS
    # "com.ZoZoApp.ZoZoApp", # This package cannot run on macOS
    # "is.workflow.actions.runworkflow", # Referenced shortcuts might not exist

]

mobile_only_apis = [
    "com.apple.DocumentsApp.ScanDocument",
    "com.apple.DocumentsApp.SearchFile",
    "com.apple.NanoSettings.NPRFPingMyPhoneIntent",
    "com.apple.NanoSettings.NPRFSetAlwaysOnIntent",
    "com.apple.NanoSettings.NPRFSetAutoLaunchAudioAppsIntent",
    "com.apple.NanoSettings.NPRFSetFlashLightIntent",
    "com.apple.NanoSettings.NPRFSetSchoolTimeIntent",
    "com.apple.NanoSettings.NPRFSetSilentModeIntent",
    "com.apple.NanoSettings.NPRFSetTheaterModeIntent",
    "com.apple.NanoSettings.NPRFSetWakeOnWristRaiseIntent",
    "com.apple.NanoSettings.NPRFSetWaterLockIntent",
    "com.apple.Numbers.TNiOSAddValueIntent",
    "com.apple.Numbers.TNiOSOpenAnyDocumentIntent",
    "com.apple.PBBridgeSupport.BridgeIntents.COSSetGizmoFaceIntent",
    "com.apple.ShortcutsActions.CellularPlanEntity",
    "com.apple.ShortcutsActions.OpenCameraAction",
    "com.apple.ShortcutsActions.SetDefaultCellularPlanAction",
    "com.apple.ShortcutsActions.SetSilentModeAction",
    "com.apple.ShortcutsActions.TranscribeAudioAction",
    "com.apple.TVRemoteUIService.LaunchScreenSaverIntent",
    "com.apple.VoiceMemos.StopRecording",
    "com.apple.freeform.CRLiOSCreateBoardIntent",
    "com.apple.freeform.CRLiOSOpenBoardIntent",
    "com.apple.iBooksX.openin",
    "com.apple.mobilemail.OpenMailboxEntityAction",
    "com.apple.mobilemail.SearchMessagesAction",
    "com.apple.mobilenotes.AddTagsToNotesLinkAction",
    "com.apple.mobilenotes.CreateFolderLinkAction",
    "com.apple.mobilenotes.DeleteNotesLinkAction",
    "com.apple.mobilenotes.ICNotesFolderIntent",
    "com.apple.mobilenotes.SharingExtension",
    "com.apple.mobilesafari.BookmarkEntity",
    "com.apple.mobilesafari.CloseTab",
    "com.apple.mobilesafari.CreateNewPrivateTab",
    "com.apple.mobilesafari.CreateNewTabGroup",
    "com.apple.mobilesafari.ListenToPage",
    "com.apple.mobilesafari.OpenView",
    "com.apple.mobilesafari.TabEntity",
    "com.apple.mobileslideshow.OpenCollectionIntent",
    "com.apple.mobiletimer.CancelTimerIntent",
    "com.apple.mobiletimer.DeleteAlarmIntent",
    "com.apple.mobiletimer.GetCurrentTimerDetailsIntent",
    "com.apple.mobiletimer.LapStopwatchIntent",
    "com.apple.mobiletimer.PauseTimerIntent",
    "com.apple.mobiletimer.ResetStopwatchIntent",
    "com.apple.mobiletimer.ResumeTimerIntent",
    "com.apple.mobiletimer.StartStopwatchIntent",
    "com.apple.mobiletimer.StopStopwatchIntent",
    "com.apple.printcenter.PrintDocuments",
    "is.workflow.actions.alarm.create",
    "is.workflow.actions.alarm.toggle",
    "is.workflow.actions.appendnote",
    "is.workflow.actions.cellular.rat.set",
    "is.workflow.actions.filter.notes",
    "is.workflow.actions.folder",
    "is.workflow.actions.properties.note",
    "is.workflow.actions.runscene",
    "is.workflow.actions.shownote"
]

paid_apps = [
    'br.com.marcosatanaka.play', 
    'com.alexhay', 
    'com.culturedcode.ThingsMac',
    'com.culturedcode.ThingsiPad',
    'com.culturedcode.ThingsiPhone',
    'com.culturedcode.ThingsTouch',
    'com.guidedways.2Do', 
    'com.jonny.spring', 
    'com.ngocluu.goodlinks', 
    'com.omz-software.Pythonista', 
    'com.omz-software.Pythonista3', 
    'com.pcalc.mobile', 
    'com.phocusllp.due', 
    'com.pixelmatorteam.pixelmator.x', 
    'com.reederapp.5.iOS', 
    'com.reederapp.5.macOS', 
    'com.tijo.opener.Opener',
]

discoverable_false_apis = [
    "is.workflow.actions.sirikit.donation.handle",
    "is.workflow.actions.useractivity.open",
    "com.apple.mobiletimer-framework.MobileTimerIntents.MTToggleAlarmIntent",
    "is.workflow.actions.shazamMedia",
    "is.workflow.actions.cloudapp.upload"
]

# The API names and shortcut names might be different, so a mapping table is manually maintained.
# fakeapiname2trueapiname = {
#     "com.apple.iBooks.openin" : "com.apple.iBooksX.openin",
#     "com.apple.iBooks.BookReaderChangePageNavigationIntent" : "com.apple.iBooksX.BookReaderChangePageNavigationIntent",
#     "com.apple.iBooks.BookReaderNavigatePagesIntent" : "com.apple.iBooksX.BookReaderNavigatePagesIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXSetBackgroundSoundIntent" : "com.apple.AccessibilityUtilities.AXSettingsShortcuts.SetBackgroundSoundIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXSetBackgroundSoundVolumeIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.SetBackgroundSoundVolumeIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXSetLargeTextIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.SetLargeTextIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXSetLeftRightBalanceIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.SetLeftRightBalanceIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXSetSoundDetectorIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.SetSoundDetectorIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXStartGuidedAccessIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.StartGuidedAccessIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXStartMagnifierIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.StartMagnifierIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXStartRemoteWatchScreenIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.StartRemoteWatchScreenIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXStartSpeakScreenIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.StartSpeakScreenIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleAssistiveTouchIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.ToggleAssistiveTouchIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleAudioDescriptionsIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.ToggleAudioDescriptionsIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleBackgroundSoundsIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.ToggleBackgroundSoundsIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleCaptionsIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.ToggleCaptionsIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleClassicInvertIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.ToggleClassicInvertIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.ToggleColorFiltersIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleContrastIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.ToggleContrastIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleLEDFlashIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.ToggleLEDFlashIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleLiveCaptionsIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.ToggleLiveCaptionsIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleMonoAudioIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.ToggleMonoAudioIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleReduceMotionIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.ToggleReduceMotionIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleSmartInvertIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.ToggleSmartInvertIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleSoundDetectionIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.ToggleSoundDetectionIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleSwitchControlIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.ToggleSwitchControlIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleTransparencyIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.ToggleTransparencyIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleVoiceControlIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.ToggleVoiceControlIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleVoiceOverIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.ToggleVoiceOverIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleWhitePointIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.ToggleWhitePointIntent",
#     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleZoomIntent" :     "com.apple.AccessibilityUtilities.AXSettingsShortcuts.ToggleZoomIntent",
#     "com.ideasoncanvas.mindnode.ios.MNCViewDocumentIntent" : "com.ideasoncanvas.mindnode.macos.ViewDocumentIntent",
#     "com.ideasoncanvas.mindnode.ios.MNCQuickEntryIntent" : "com.ideasoncanvas.mindnode.macos.QuickEntryIntent",
#     "com.ideasoncanvas.mindnode.ios.MNCNewDocumentIntent" : "com.ideasoncanvas.mindnode.macos.NewDocumentIntent",
#     "com.ideasoncanvas.mindnode.ios.MNCExportToThingsIntent" : "com.ideasoncanvas.mindnode.macos.ExportToThingsIntent",
#     "com.ideasoncanvas.mindnode.ios.MNCExportTasksIntent" : "com.ideasoncanvas.mindnode.macos.ExportTasksIntent",
#     "com.ideasoncanvas.mindnode.ios.MNCExportDocumentIntent" : "com.ideasoncanvas.mindnode.macos.ExportDocumentIntent",
#     "com.ideasoncanvas.mindnode.macos.MNCNewDocumentIntent" : "com.ideasoncanvas.mindnode.macos.NewDocumentIntent"
# }
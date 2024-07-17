import json
import re

class WFActionsClass:
    """ The class of WFActions.

    Attributes:
        WFActions_dicts (dict): The dictionary of WFActions.
    """
    
    def __init__(self, WFActions_path) -> None:
        """Initialize the WFActionsClass.
        
        Args:
            WFActions_path (str): The path of the WFActions.json file.
        """

        with open(WFActions_path, "r") as f:
            self.WFActions_dicts = json.load(f)
        
        """Shortcuts APIs include a variety of parameter types, including primitive data types, enumerated data types, and advanced data types.

        Primitive data types in shortcuts correspond directly to their JSON counterparts: integer parameters correspond to JSON integers, 
        float parameters to JSON floats, and string parameters to JSON strings.

        Enumerated data types are represented as strings in shortcuts, meaning that enumerated parameters correspond to JSON strings.

        Advanced data types in shortcuts can be represented as primitive data types (integers, floats, and strings), dictionaries, or lists in JSON. 
        The exact representation is determined by the API developer.

        For Apple, advanced data types often begin with "WF," such as "WFAccountPickerParameter," where "WF" stands for "Workflow," 
        the predecessor of Shortcuts, and "AccountPickerParameter" indicates a parameter used for selecting account contacts. 
        While the names provide a hint about the data type's function, 
        understanding the relationship between JSON-formatted shortcuts and these advanced data types is crucial for generating subsequent API calls accurately.

        Currently, there is no perfect method to determine this one-to-one correspondence. 
        One effective approach is to infer these relationships through the shortcuts' behavior or by manual annotation.

        We manually annotated some parameters as advanced data types, which are represented as primitive data types in JSON. 
        During our capability testing of the intelligent agent, we fully **informed** the agent of a parameter's name, type, 
        and its corresponding data type in JSON. This should allow the agent to understand the parameter's function. 
        However, due to the lack of a specific correspondence, we cannot precisely evaluate the accuracy of filling these advanced data type parameters. 
        Therefore, we **only calculate the accuracy for parameters that are represented as primitive data types in JSON** 
        (which actually constitutes a significant portion of the parameters). 
        Even though we may not fully understand the exact correspondence between all parameter data types and their JSON representations, 
        we ensure the correspondence between all primitive data types, enumerated data types, and some advanced data types with their JSON representations. 
        """
        """`self.para_type_2_json_type` is the mapping of advanced data types to primitive data types. 
        Parameters that are non-primitive data types in JSON are directly mapped to the Object type.
        """
        self.para_type_2_json_type = {
            "WFAccountPickerParameter": "Object", # Optional parameters include ["Everyone", "Contacts Only", "Off"].
            "WFAirDropVisibilityParameter": "Object",
            "WFAppPickerParameter": "Object",
            "WFArchiveFormatParameter": "Object", # Optional parameters include ["zip", "iso", "gz"].
            "WFCalendarPickerParameter": "Object",
            "WFColorPickerParameter": "Object",
            "WFContactFieldParameter": "Object",
            "WFContactHandleFieldParameter": "Object",
            "WFContentArrayParameter": "Object",  # Dictionary type, includes keys WFKey, values WFValue, and type WFItemType.
            "WFCountryFieldParameter": "Object",
            "WFCurrencyQuantityFieldParameter": "Float", # It can be a single value, or it can be a complex structure like: "WFVenmoActionAmount": {"Value": {"Unit": "USD", "Magnitude": {"OutputUUID": "6FE54ED3-2513-4A22-96A1-DE5894F1F5FC", "Type": "ActionOutput", "OutputName": "Provided Input"}}, "WFSerializationType": "WFQuantityFieldValue"}
            "WFCustomDateFormatParameter": "String",  # Date format string
            "WFDateFieldParameter": "String",  # Dates in various formats, such as "1970-01-01T00:00:00Z".
            "WFDetectedDate": "String",  # Similar date strings
            "WFDictionaryParameter": "Object",  # Dictionary
            "WFDisplayPickerParameter": "Object",
            "WFDynamicEnumerationParameter": "Object",  # Dynamic enumerated parameters
            "WFDynamicTagFieldParameter": "Object",
            "WFEmailAddressFieldParameter": "Object", # Address object
            "WFEvernoteNotebookPickerParameter": "Object",
            "WFEvernoteTagsTagFieldParameter": "Object",
            "WFExpandingParameter": "Bool",  # Expand or not
            "WFFileLabelColorPickerParameter": "Object",
            "WFFilePickerParameter": "Object",
            "WFFitnessWorkoutTypePickerParameter": "Object",
            "WFFocusModesPickerParameter": "Object",
            "WFFontPickerParameter": "Object",
            "WFHealthCategoryAdditionalPickerParameter": "Object",
            "WFHealthCategoryPickerParameter": "Object",
            "WFHealthQuantityAdditionalFieldParameter": "Object", # Similar to {"Unit": "cm"}
            "WFHealthQuantityAdditionalPickerParameter": "Object",
            "WFHealthQuantityFieldParameter": "Object", # Similar to {"Unit": "fl_oz_us", "xx": ""}
            "WFHomeAccessoryPickerParameter": "Object",
            "WFHomeAreaPickerParameter": "Object",
            "WFHomeCharacteristicPickerParameter": "Object",
            "WFHomeServicePickerParameter": "Object",
            "WFImageConvertFormatPickerParameter": "Object",
            "WFIntentAppPickerParameter": "Object",
            "WFLightroomPresetPickerParameter": "Object",
            "WFListeningModePickerParameter": "Object",
            "WFLocalePickerParameter": "Object",  # Similar to en_US
            "WFLocationAccuracyParameter": "Object",  # Accuracy
            "WFLocationParameter": "Object",  # Location
            "WFMailSenderPickerParameter": "Object",
            "WFMakeImageFromPDFPageColorspaceParameter": "Object", #  Optional parameters include ["RGB"]
            "WFMakeImageFromPDFPageImageFormatParameter": "Object", #  Optional parameters include ["public.jpeg"]
            "WFMapsAppPickerParameter": "Object",
            "WFMeasurementUnitPickerParameter": "Object",
            "WFMediaPickerParameter": "Object",
            "WFMediaRoutePickerParameter": "Object",
            "WFNetworkPickerParameter": "Object",
            "WFNumberFieldParameter": "Integer",
            "WFOSAScriptEditorParameter": "Object",  # Code editor, a string, code
            "WFPaymentMethodParameter": "Object",
            "WFPhoneNumberFieldParameter": "Object",  # Photo Number
            "WFPhotoAlbumPickerParameter": "Object",
            "WFPlaylistPickerParameter": "Object",
            "WFPodcastPickerParameter": "Object",
            "WFPosterPickerParameter": "Object",
            "WFQuantityTypePickerParameter": "Object",
            "WFRemindersListPickerParameter": "Object",
            "WFRideOptionParameter": "Object",
            "WFSSHKeyParameter": "Object",
            "WFSearchLocalBusinessesRadiusParameter": "Object", # Similar to "Value": {"Unit": "km","Magnitude": 14.0}这样的值
            "WFSliderParameter": "Float",  # Slider
            "WFSpeakTextLanguagePickerParameter": "Object",
            "WFSpeakTextVoicePickerParameter": "Object",
            "WFStepperParameter": "Integer",  # Stepper
            "WFSwitchParameter": "Bool",
            "WFTagFieldParameter": "Object",
            "WFTextInputParameter": "String",
            "WFTimeZonePickerParameter": "Object",
            "WFTodoistProjectPickerParameter": "Object",
            "WFTranslateTextLanguagePickerParameter": "Object",
            "WFTrelloBoardPickerParameter": "Object",
            "WFTrelloListPickerParameter": "Object",
            "WFTumblrBlogPickerParameter": "Object",
            "WFTumblrComposeInAppParameter": "Object",
            "WFURLParameter": "String",
            "WFUnitQuantityFieldParameter": "Object", # Similar to "Value": {"Unit": "ft","Magnitude": "100"}
            "WFUnitTypePickerParameter": "Object",
            "WFVPNPickerParameter": "Object",
            "WFVariableFieldParameter": "String",
            "WFVariablePickerParameter": "Object",  # Selectable parameters only
            "WFWorkflowFolderPickerParameter": "Object",
            "WFWorkflowPickerParameter": "Object",
            "WFWorkoutGoalQuantityFieldParameter": "Object", # "Value": {"Unit": "min","Magnitude": "15"}
            "WFWorkoutTypePickerParameter": "Object",
            "WFiTunesStoreCountryPickerParameter": "Object"
        }
    
        self.return_type_2_json_type = {
            "AVAsset": "Object",
            "CLLocation": "Object",
            "EKEvent": "Object",
            "ENNoteRef": "Object",
            "INRideStatus": "Object",
            "MKMapItem": "Object",
            "MPMediaItem": "Object",
            "NSAttributedString": "Object",
            "NSDate": "Object",
            "NSDateComponents": "Object",
            "NSDecimalNumber": "Object",
            "NSDictionary": "Object",
            "NSMeasurement": "Object",
            "NSNumber": "Object",
            "NSString": "Object",
            "NSURL": "Object",
            "PHAsset": "Object",
            "REMReminder": "Object",
            "WFAppContentItem": "Object",
            "WFAppStoreAppContentItem": "Object",
            "WFArticle": "Object",
            "WFArticleContentItem": "Object",
            "WFBooleanContentItem": "Object",
            "WFContact": "Object",
            "WFContactContentItem": "Object",
            "WFContentItem": "Object",
            "WFDateContentItem": "Object",
            "WFDictionaryContentItem": "Object",
            "WFEmailAddress": "Object",
            "WFEmailAddressContentItem": "Object",
            "WFGenericFileContentItem": "Object",
            "WFGiphyObject": "Object",
            "WFHKSampleContentItem": "Object",
            "WFHKWorkoutContentItem": "Object",
            "WFImage": "Object",
            "WFImageContentItem": "Object",
            "WFLocationContentItem": "Object",
            "WFNumberContentItem": "Object",
            "WFPDFContentItem": "Object",
            "WFParkedCarContentItem": "Object",
            "WFPhoneNumber": "Object",
            "WFPhoneNumberContentItem": "Object",
            "WFPhotoMediaContentItem": "Object",
            "WFPodcastEpisodeContentItem": "Object",
            "WFPodcastShowContentItem": "Object",
            "WFPosterRepresentation": "Object",
            "WFSafariWebPage": "Object",
            "WFShazamMedia": "Object",
            "WFStreetAddress": "Object",
            "WFStringContentItem": "Object",
            "WFTimeInterval": "Object",
            "WFTrelloBoard": "Object",
            "WFTrelloCard": "Object",
            "WFTrelloList": "Object",
            "WFTripInfo": "Object",
            "WFURLContentItem": "Object",
            "WFWeatherData": "Object",
            "WFWorkflowReference": "Object",
            "WFiTunesProductContentItem": "Object",
            "com.adobe.pdf": "Object",
            "com.apple.coreaudio-format": "Object",
            "com.apple.m4a-audio": "Object",
            "com.apple.quicktime-movie": "Object",
            "com.compuserve.gif": "Object",
            "public.data": "Object",
            "public.folder": "Object",
            "public.html": "Object",
            "public.image": "Object",
            "public.mpeg-4": "Object",
            "public.plain-text": "Object"
        }

    def all_api2desc(self, need_api2paraname2paratype=False, need_api2parasummary=False):
        """Retrieve the mapping of all API names to their information.

        Args:
            need_api2paraname2paratype (bool, optional): Whether to get the parameter name to parameter type. Defaults to False.
            need_api2parasummary (bool, optional): Whether to get the parameter summary. Defaults to False.
        """

        all_api2info = {}
        if need_api2paraname2paratype:
            all_api2paraname2paratype = {} # {api name : {parameter name: parameter type}}
        if need_api2parasummary:
            all_api2parasummary = {} # {api name : parameter summary}

        for WFWorkflowActionIdentifier in self.WFActions_dicts:

            WFActions_dict = self.WFActions_dicts[WFWorkflowActionIdentifier]
            """Exclude shortcuts where Discoverable is False, as these shortcuts cannot be found when searching in the Shortcuts app."""
            if "Discoverable" in WFActions_dict:
                Discoverable = WFActions_dict["Discoverable"]
                if Discoverable == False:
                    continue

            if need_api2paraname2paratype:
                if WFWorkflowActionIdentifier not in all_api2paraname2paratype:
                    all_api2paraname2paratype[WFWorkflowActionIdentifier] = {}
                else:
                    raise ValueError("Duplicate API names.")
            if need_api2parasummary:
                if WFWorkflowActionIdentifier not in all_api2parasummary:
                    all_api2parasummary[WFWorkflowActionIdentifier] = {}
                else:
                    raise ValueError("Duplicate API names.")

            """the name of the API"""
            API_name = WFWorkflowActionIdentifier # The name of the API
            
            """the title of the API"""
            if "Name" in WFActions_dict:
                API_Title = WFActions_dict["Name"]  # The title of the API
            elif "ShortName" in WFActions_dict: # The short name of the API
                API_Title = WFActions_dict["ShortName"]
            elif "IntentName" in WFActions_dict: # The intent name of the API
                API_Title = WFActions_dict["IntentName"]
            else:
                raise ValueError("No title available.")
            
            """the description of the API"""
            if "Description" in WFActions_dict and "DescriptionSummary" in WFActions_dict["Description"]:
                API_description = WFActions_dict["Description"]["DescriptionSummary"]
            if "Description" in WFActions_dict and "DescriptionNote" in WFActions_dict["Description"]:
                if API_description:
                    API_description += ". " + WFActions_dict["Description"]["DescriptionNote"]
                else:
                    API_description = WFActions_dict["Description"]["DescriptionNote"]
            
            """The parameter description of the API"""
            simple_para_descs = []  # A brief description of the function parameters.
            complex_para_descs = []  # A detailed description of the function parameters.
            
            if "Parameters" in WFActions_dict:
                WFActions_dict_Parameters = WFActions_dict["Parameters"]
                for WFActions_dict_Parameter in WFActions_dict_Parameters:
                    
                    ParameterName = WFActions_dict_Parameter["Key"]
                    valueType, defaultValue = None, ""  # Parameter name, parameter type, default value

                    para_desc = "" # combine ParameterDisplayName, ParameterDisplayDesc, TypeDisplayName, INTypeDesc, EnumDisplayName, INEnumDesc together to generate the parameter description
                    ParameterDisplayName, ParameterDisplayDesc = "", ""
                    TypeDisplayName, INTypeDesc = "", ""
                    EnumDisplayName, INEnumDesc = "", ""

                    # Prepare ParameterDisplayName
                    if "Label" in WFActions_dict_Parameter:
                        ParameterDisplayName = WFActions_dict_Parameter["Label"]
                    if "Placeholder" in WFActions_dict_Parameter and WFActions_dict_Parameter["Placeholder"] != ParameterDisplayName:
                        if ParameterDisplayName:
                            ParameterDisplayName += f". {
                                WFActions_dict_Parameter['Placeholder']}"
                        else:
                            ParameterDisplayName += f"{WFActions_dict_Parameter['Placeholder']})"
                    
                    # Prepare ParameterDisplayDesc
                    if "Description" in WFActions_dict_Parameter:
                        ParameterDisplayDesc = WFActions_dict_Parameter["Description"]
                    if "Description" in WFActions_dict:
                        Description = WFActions_dict["Description"]
                        if "DescriptionInput" in Description:
                            DescriptionInput = Description["DescriptionInput"]
                            Input = WFActions_dict["Input"]
                            if "ParameterKey" in Input:
                                ParameterKey = Input["ParameterKey"]
                                if ParameterKey == ParameterName:
                                    if ParameterDisplayDesc:
                                        ParameterDisplayDesc += ". " + DescriptionInput
                                    else:
                                        ParameterDisplayDesc = DescriptionInput

                    Class = WFActions_dict_Parameter["Class"] # Parameter type
                    if "ResultType" in WFActions_dict_Parameter:
                        ResultType = WFActions_dict_Parameter["ResultType"]
                    else:
                        ResultType = None
                    
                    # Prepare EnumDisplayName & INEnumDesc
                    if "Items" in WFActions_dict_Parameter or "PossibleUnits" in WFActions_dict_Parameter: # For enumerated data types, it includes the fields Items and PossibleUnits.
                        ResultType = "Enum"
                        INEnumDesc += "The value of this Enum must be one of the following values (The text in parentheses describes the value): "
                        if "Items" in WFActions_dict_Parameter:
                            INEnumValues = WFActions_dict_Parameter["Items"]
                        else:
                            INEnumValues = WFActions_dict_Parameter["PossibleUnits"]
                        for INEnumValue in INEnumValues:
                            if INEnumValue != INEnumValues[-1]: # If there is a next value
                                INEnumDesc += f'"{INEnumValue}", '
                            else:
                                INEnumDesc += f'"{INEnumValue}"'
                    
                    # Prepare valueType
                    valueType = Class
                    if valueType in self.para_type_2_json_type:
                        if self.para_type_2_json_type[valueType] == "Object": # If the type is an advanced data type
                            valueType = valueType + "(Object)"
                        else:
                            valueType = self.para_type_2_json_type[valueType] # If the data type is represented as a primitive data type in JSON, it is directly mapped to the corresponding primitive data type.
                    if ResultType:
                        valueType = ResultType

                    # Prepare defaultValue
                    if "DefaultValue" in WFActions_dict_Parameter:
                        defaultValue = WFActions_dict_Parameter["DefaultValue"]

                    if defaultValue:
                        if isinstance(defaultValue, str):
                            tmp_para_str = f"{ParameterName}: {
                                valueType} = \"{defaultValue}\""
                            simple_para_descs.append(tmp_para_str)

                            if need_api2paraname2paratype:
                                all_api2paraname2paratype[API_name][ParameterName] = f"{
                                    valueType} = \"{defaultValue}\""
                        elif isinstance(defaultValue, bool) or isinstance(defaultValue, int) or isinstance(defaultValue, float):
                            tmp_para_str = f"{ParameterName}: {
                                valueType} = {defaultValue}"
                            simple_para_descs.append(tmp_para_str)

                            if need_api2paraname2paratype:
                                all_api2paraname2paratype[API_name][ParameterName] = f"{
                                    valueType} = {defaultValue}"
                        elif isinstance(defaultValue, list):
                            tmp_para_str = f"{ParameterName}: {
                                valueType} = {defaultValue}"
                            simple_para_descs.append(tmp_para_str)

                            if need_api2paraname2paratype:
                                all_api2paraname2paratype[API_name][ParameterName] = f"{
                                    valueType} = {defaultValue}"
                        elif isinstance(defaultValue, dict):
                            tmp_para_str = f"{ParameterName}: {
                                valueType} = {defaultValue}"
                            simple_para_descs.append(tmp_para_str)

                            if need_api2paraname2paratype:
                                all_api2paraname2paratype[API_name][ParameterName] = f"{
                                    valueType} = {defaultValue}"
                        else:
                            print(API_name, ParameterName)
                            raise ValueError("Parameter default value type error.")
                    else:
                        tmp_para_str = f"{ParameterName}: {valueType}"
                        simple_para_descs.append(tmp_para_str)

                        if need_api2paraname2paratype:
                            all_api2paraname2paratype[API_name][ParameterName] = f"{
                                valueType}"

                    # Prepare para_desc
                    for cur_desc in [ParameterDisplayName, ParameterDisplayDesc, TypeDisplayName, INTypeDesc, EnumDisplayName, INEnumDesc]:
                        if cur_desc:
                            para_desc += " " + cur_desc + "."

                    """RequiredResources indicates that this parameter has dependencies on other parameters, 
                    meaning it will only be valid when other parameters have specific values.
                    """
                    INIntentParameterRelationship = None
                    if "RequiredResources" in WFActions_dict_Parameter:
                        INIntentParameterRelationship = WFActions_dict_Parameter["RequiredResources"]
                        tmp_desc_str = ""
                        for cur_required_resource in INIntentParameterRelationship:
                            tmp_key_str, tmp_desc_str = "", ""
                            if "WFParameterKey" in cur_required_resource:
                                WFParameterKey = cur_required_resource["WFParameterKey"]
                                value_type = None
                                if "WFParameterValue" in cur_required_resource:
                                    value_type = type(
                                        cur_required_resource["WFParameterValue"])
                                    if value_type in [int, float, bool]:
                                        WFParameterValue = cur_required_resource["WFParameterValue"]
                                    else:
                                        WFParameterValue = f'"{
                                            cur_required_resource["WFParameterValue"]}"'
                                elif "WFParameterValues" in cur_required_resource:
                                    value_type = type(
                                        cur_required_resource["WFParameterValues"][0])
                                    if value_type in [int, float, bool]:
                                        WFParameterValue = ", ".join(
                                            cur_required_resource["WFParameterValues"])
                                    else:
                                        WFParameterValue = ", ".join(
                                            [f'"{value}"' for value in cur_required_resource["WFParameterValues"]])
                                else:
                                    continue

                                WFParameterClass = cur_required_resource["WFResourceClass"]
                                if not tmp_key_str:
                                    tmp_key_str = WFParameterKey
                                else:
                                    tmp_key_str += f', "{WFParameterKey}"'
                                if not tmp_desc_str:
                                    tmp_desc_str = f'the value of "{
                                        WFParameterKey}" is {WFParameterValue}'
                                else:
                                    tmp_desc_str += f', "{
                                        WFParameterKey}" is {WFParameterValue}'
                                para_desc += f""" This value depends on the value of {
                                    tmp_key_str}. This parameter is only valid when {tmp_desc_str}."""

                    complex_para_descs.append(f"{ParameterName}: {para_desc}")

            """The return value of the API"""
            return_value_name, return_value_type, return_value_desc = "", "", ""
            return_value_display_name = ""
            return_value_INTypeDisplayName, return_value_INTypeDesc = "", ""
            return_value_INEnumDisplayName, return_value_INEnumDesc = "", ""
            return_value_name_is_API = False
            if "Output" in WFActions_dict:
                Output = WFActions_dict["Output"]
                
                # Prepare return_value_name, return_value_name_is_API
                if "OutputName" in Output:
                    return_value_name = Output["OutputName"]
                else:
                    return_value_name = API_Title
                    return_value_name_is_API = True
                
                # Prepare return_value_type
                if "Types" in Output:
                    return_value_types = Output["Types"]
                    if len(return_value_types) == 1:
                        return_value_type = return_value_types[0]
                        if return_value_type in self.return_type_2_json_type:
                            if self.return_type_2_json_type[return_value_type] == "Object":
                                return_value_type = return_value_type + \
                                    "(Object)"
                            else:
                                return_value_type = self.return_type_2_json_type[return_value_type]
                    else:
                        for cur_index, cur_return_value_type in enumerate(return_value_types):
                            if cur_return_value_type in self.return_type_2_json_type:
                                if self.return_type_2_json_type[cur_return_value_type] == "Object":
                                    return_value_types[cur_index] = cur_return_value_type + \
                                        "(Object)"
                                else:
                                    return_value_types[cur_index] = self.return_type_2_json_type[cur_return_value_type]
                        return_value_type = "(" + \
                            " or ".join(return_value_types) + ")"
                else:
                    return_value_type = ""

                # Prepare return_value_desc
                if "Description" in WFActions_dict:
                    Description = WFActions_dict["Description"]
                    if "DescriptionResult" in Description:
                        return_value_desc = Description["DescriptionResult"]

            # Prepare return_value_display_name, return_value_INTypeDisplayName, return_value_INEnumDisplayName, return_value_INTypeDesc, return_value_INEnumDesc
            # Prepare return_value_desc
            for cur_desc in [return_value_display_name, return_value_INTypeDisplayName, return_value_INEnumDisplayName, return_value_INTypeDesc, return_value_INEnumDesc]:
                if cur_desc:
                    return_value_desc += " " + cur_desc + "."

            # Prepare ParameterSummary and all_api2parasummary
            ParameterSummary = ""
            if "ParameterSummary" in WFActions_dict:
                if isinstance(WFActions_dict["ParameterSummary"], str):
                    ParameterSummary_str = WFActions_dict["ParameterSummary"]
                    ParameterSummary = ParameterSummary_str
                    if need_api2parasummary:
                        pattern = re.compile(r'\$\{(\w+)\}') # Match all occurrences of xxx in the form ${xxx} within ParameterSummary_str.
                        matches = pattern.findall(ParameterSummary_str)
                        all_api2parasummary[API_name] = {",".join(matches): ParameterSummary_str}
                elif isinstance(WFActions_dict["ParameterSummary"], dict):
                    def remove_parentheses(s):
                        pattern = r'\([^)]*\)' # Regular expression to match parentheses and their contents.
                        cleaned_string = re.sub(pattern, '', s) # Replace the matched content with an empty string.
                        return cleaned_string

                    ParameterSummary_dict = WFActions_dict["ParameterSummary"]
                    new_ParameterSummary_dict = {}
                    for para_key, para_value in ParameterSummary_dict.items():
                        new_ParameterSummary_dict[remove_parentheses(para_key)] = para_value
                    ParameterSummary_dict = new_ParameterSummary_dict
                    del new_ParameterSummary_dict

                    for para_key, para_value in ParameterSummary_dict.items():
                        remove_pare_para_key = remove_parentheses(para_key) # Remove all content enclosed in parentheses from para_key.
                        if not ParameterSummary:
                            ParameterSummary = f"({remove_pare_para_key}) {para_value}"
                        else:
                            ParameterSummary += f"; ({remove_pare_para_key}) {para_value}"

                    if need_api2parasummary:
                        all_api2parasummary[API_name] = ParameterSummary_dict
                else:
                    raise ValueError("ParameterSummary type error.")
            else:
                ParameterSummary_key = ""
                if API_Title and not API_description:
                    ParameterSummary_value = API_Title
                elif not API_Title and API_description:
                    ParameterSummary_value = API_description
                else:
                    ParameterSummary_value = API_Title

                ParameterSummary = f"({para_key}) {para_value}"

                if need_api2parasummary:
                    all_api2parasummary[API_name] = {ParameterSummary_key: ParameterSummary_value}

            API_name, API_Title, API_description, simple_para_descs, complex_para_descs, return_value_name, return_value_type, return_value_desc, ParameterSummary
            if need_api2paraname2paratype:
                if return_value_type:
                    all_api2paraname2paratype[API_name]["ThisIsReturnValue:" + return_value_name] = f"{return_value_type}"
                elif return_value_name and not return_value_name_is_API:
                    all_api2paraname2paratype[API_name]["ThisIsReturnValue:" + return_value_name] = f"Object"

            """The information of the API"""
            API_info = ""
            API_info += f"""{API_name}({", ".join(simple_para_descs)})"""
            if return_value_type:
                API_info += f""" -> {return_value_name}: {return_value_type}"""
            if API_info[-1] != "\n":
                API_info += "\n"

            if len(complex_para_descs) > 0:
                parameter_descs_str = "\n    ".join(complex_para_descs)
                API_info += f"""Parameters:
    {parameter_descs_str}"""
            if API_info[-1] != "\n":
                API_info += "\n"

            if return_value_type:
                API_info += f"""Return Value:
    {return_value_name}: {return_value_desc}"""
            if API_info[-1] != "\n":
                API_info += "\n"

            if API_Title:
                API_info += f"""Description:
    {API_Title}"""
            if API_description:
                API_info += f""": {API_description}"""
            if API_info[-1] != "\n":
                API_info += "\n"

            if ParameterSummary:
                API_info += f"""ParameterSummary: {ParameterSummary}"""
            if API_info[-1] != "\n":
                API_info += "\n"
            all_api2info[WFWorkflowActionIdentifier] = API_info

        if not need_api2paraname2paratype and not need_api2parasummary:
            return_value = all_api2info
            return return_value
        else:
            return_value = [all_api2info]
        if need_api2paraname2paratype:
            return_value.append(all_api2paraname2paratype)
        if need_api2parasummary:
            return_value.append(all_api2parasummary)
        return return_value

# if WFWorkflowActionIdentifier in [
#     "is.workflow.actions.conditional",
#     "is.workflow.actions.choosefrommenu",
#     "is.workflow.actions.repeat.count",
#     "is.workflow.actions.repeat.each",
# ]:
#     # return 0, "The API indicated by WFWorkflowActionIdentifier represents a special control flow."
#     continue

# if WFWorkflowActionIdentifier in [
#         'is.workflow.actions.filter.photos',
#         'is.workflow.actions.filter.reminders',
#         'is.workflow.actions.filter.locations',
#         'is.workflow.actions.filter.images',
#         'is.workflow.actions.filter.displays',
#         'is.workflow.actions.filter.music',
#         'is.workflow.actions.filter.health.quantity',
#         'is.workflow.actions.filter.windows',
#         'is.workflow.actions.filter.calendarevents',
#         'is.workflow.actions.filter.eventattendees',
#         'is.workflow.actions.filter.apps',
#         'is.workflow.actions.filter.articles',
#         'is.workflow.actions.filter.contacts',
#         'is.workflow.actions.filter.files'
#     ]:
#     # return 0, "The API indicated by WFWorkflowActionIdentifier is missing the Parameters parameter in self.WFActions_dicts."
#     continue
# elif WFWorkflowActionIdentifier in [
#         'is.workflow.actions.properties.trello',
#         'is.workflow.actions.properties.ulysses.sheet',
#         'is.workflow.actions.properties.workflow',
#         'is.workflow.actions.properties.podcast',
#         'is.workflow.actions.properties.podcastshow',
#         'is.workflow.actions.properties.locations',
#         'is.workflow.actions.properties.appstore',
#         'is.workflow.actions.properties.articles',
#         'is.workflow.actions.properties.reminders',
#         'is.workflow.actions.properties.eventattendees',
#         'is.workflow.actions.properties.images',
#         'is.workflow.actions.properties.safariwebpage',
#         'is.workflow.actions.properties.parkedcar',
#         'is.workflow.actions.properties.weather.conditions',
#         'is.workflow.actions.properties.itunesstore',
#         'is.workflow.actions.properties.files',
#         'is.workflow.actions.properties.music',
#         'is.workflow.actions.properties.health.quantity',
#         'is.workflow.actions.properties.shazam',
#         'is.workflow.actions.properties.calendarevents',
#         'is.workflow.actions.properties.ridestatus',
#         'is.workflow.actions.properties.appearance'
#     ]:
#     # return 0, "The API indicated by WFWorkflowActionIdentifier is missing the Parameters parameter in self.WFActions_dicts."
#     continue
# elif WFWorkflowActionIdentifier in [
#         'com.apple.TVRemoteUIService.LaunchApplicationIntent',
#         'com.apple.TVRemoteUIService.SleepAppleTVIntent',
#         'com.apple.TVRemoteUIService.PauseContentIntent',
#         'com.apple.TVRemoteUIService.ReduceLoudSoundsIntent',
#         'com.apple.TVRemoteUIService.WakeAppleTVIntent',
#         'com.apple.TVRemoteUIService.SkipContentIntent',
#         'com.apple.TVRemoteUIService.LaunchRemoteIntent',
#         'com.apple.TVRemoteUIService.ToggleSystemAppearanceIntent',
#         'com.apple.TVRemoteUIService.ToggleCaptionsIntent',
#         'com.apple.TVRemoteUIService.SwitchUserAccountIntent'
#     ]:
#     # return 0, "The API indicated by WFWorkflowActionIdentifier is missing the Parameters parameter in self.WFActions_dicts."
#     continue
# elif WFWorkflowActionIdentifier in [
#     "is.workflow.actions.flashlight", # "state," "operation" two parameters
#     "is.workflow.actions.appearance", # "state," "operation" two parameters
#     "is.workflow.actions.bluetooth.set",
#     "is.workflow.actions.airplanemode.set",
#     "is.workflow.actions.wifi.set",
#     "is.workflow.actions.orientationlock.set",
#     "is.workflow.actions.truetone.set",
#     "is.workflow.actions.nightshift.set",
#     "is.workflow.actions.lowpowermode.set",
#     "is.workflow.actions.cellulardata.set",
#     "is.workflow.actions.personalhotspot.set", # "operation", "onValue"
#     "is.workflow.actions.announcenotifications.set",
#     "is.workflow.actions.silenceunknowncallers.set",
#     "is.workflow.actions.display.always-on.set",
#     "is.workflow.actions.stagemanager.set" # Missing showDock, showRecentApps parameters.
# ]:
#     # return 0, "The API indicated by WFWorkflowActionIdentifier is missing the Parameters parameter in self.WFActions_dicts."
#     continue
# elif WFWorkflowActionIdentifier in [
#     "is.workflow.actions.setters.calendarevents", # "WFInput", "WFCalendarEventContentItemEndDate"
#     "is.workflow.actions.setters.contacts", # "WFContactContentItemNickname", "WFInput", "WFContactContentItemURLs", "WFContactContentItemFirstName", "ValueLabel"
#     "is.workflow.actions.setters.reminders" #  "WFContentItemPropertyName"
# ]:
#     # return 0, The API indicated by WFWorkflowActionIdentifier is missing the Parameters parameter in self.WFActions_dicts."
#     continue

# 存在ParameterOverrides
# if WFWorkflowActionIdentifier == "is.workflow.actions.ask": # The optional parameter types will vary depending on the value of WFInputType.
#     # return 0, "There are ParameterOverrides for the API indicated by WFWorkflowActionIdentifier."
#     continue
# elif WFWorkflowActionIdentifier in [ # Missing 'text' parameter.
#     "is.workflow.actions.text.split",
#     "is.workflow.actions.text.changecase",
#     "is.workflow.actions.text.match",
#     "is.workflow.actions.text.combine",
#     "is.workflow.actions.text.match.getgroup",
#     "is.workflow.actions.correctspelling",
#     "is.workflow.actions.setbrightness",
#     ]:
#     # return 0, "There are ParameterOverrides for the API indicated by WFWorkflowActionIdentifier."
#     continue
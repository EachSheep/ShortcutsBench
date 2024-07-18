import json
import re

class APIsClass:
    """The class of APIs.

    Attributes:
        api_files: The mapping from the app name to the corresponding json.
    """

    # def __init__(self, api_json_path, fail_api_json_path) -> None:
    def __init__(self, api_json_path) -> None:
        """Initialize the APIsClass.

        Args:
            api_json_path: The path of the json file that contains the successful api data.
            # fail_api_json_path: The path of the json file that contains the failed api data.
        
        Attributes:
            api_files: The mapping from the app name to the corresponding json.
        """

        with open(api_json_path, "r") as f:
            api_files = json.load(f)
        # with open(fail_api_json_path, "r") as f:
        #     fail_api_json = json.load(f)
        # api_files.extend(fail_api_json)

        self.api_files = {} # Mapping of app names to their corresponding JSON.
        for cur_api_file in api_files:
            AppName = cur_api_file["AppName"]
            self.api_files[AppName] = cur_api_file
        
        """Shortcuts APIs include various parameter types, such as primitive data types, enumerated data types, and advanced data types.

        Primitive data types in shortcuts correspond to their respective JSON data types: integer parameters map to JSON integers, 
        float parameters to JSON floats, and string parameters to JSON strings.

        Enumerated data types are represented as string types in shortcuts, meaning that enumerated parameters map to JSON strings.

        Advanced data types in shortcuts can be represented as primitive data types (integers, floats, and strings), dictionary data types, 
        or list data types in JSON. The specific representation is determined by the API developer.

        For the SiriKit framework, the number of advanced data types in its parameters is limited (as available on the official website), 
        so we can directly map them manually.
        """
        """SiriKit corresponds to the `intentdefinition` definition file."""
        self.INIntentParameterType2type = {
            "Integer": "Integer",
            "String": "String",
            "SpeakableString": "String",
            "Boolean": "Bool",
            "URL": "String",
            "Decimal": "Float",
            "Placemark": "Object",
            "File": "Object",
            "DateComponents": "String",
            "Distance": "Object",
            "TimeInterval": "Object",
        }

        self.actionsdata_para2type = {
            0: "String",
            1: "Bool",
            2: "Integer",
            7: "Float",  # <key>fadeDuration</key> <string>12.5</string>
            8: "String",  # Date
            9: "String",  # Date + Time
            10: "Object",  # Location
            11: "String",  # URL
            12: "Object",  # File, possibly an image?
        }


    def all_api2desc(self, need_api2paraname2paratype=False, need_api2parasummary=False):
        """Retrieve the mapping of all API names to their information.

        1. Prioritize the file indicated by `.actionsdata`. If there are multiple `.actionsdata` files, we select the first one.
        2. If there is no `.actionsdata` file, we choose the `.intentdefinition` file. If there are multiple `.intentdefinition` files, we select the first one.
        We ensure that for APIs with the same name, only one is retained.
        """
        all_api2info = {}
        if need_api2paraname2paratype:
            all_api2paraname2paratype = {} # {api name : {parameter name: parameter type}}
        if need_api2parasummary:
            all_api2parasummary = {} # {api name : parameter summary}

        for app_name in self.api_files: # Iterate over all the apps.
            cur_actionsdata_keys = list(self.api_files[app_name].keys())
            all_actionsdata_keys, all_intentdefinition_keys = [], []
            for cur_actionsdata_key in cur_actionsdata_keys:
                if "actionsdata" in cur_actionsdata_key and "widget" not in cur_actionsdata_key.lower() and "plugin" not in cur_actionsdata_key.lower():
                    all_actionsdata_keys.append(cur_actionsdata_key)
                elif "intentdefinition" in cur_actionsdata_key and "widget" not in cur_actionsdata_key.lower() and "plugin" not in cur_actionsdata_key.lower():
                    all_intentdefinition_keys.append(cur_actionsdata_key)
            all_actionsdata_keys.reverse()
            all_intentdefinition_keys.reverse()

            # Traverse all the intentdefinition files.
            for all_intentdefinition_key in all_intentdefinition_keys:
                cur_intentdefinition_file = self.api_files[app_name][all_intentdefinition_key]

                # APIs
                INIntents = cur_intentdefinition_file["INIntents"]

                tmp_INEnums = cur_intentdefinition_file["INEnums"]
                INEnums = {}  # INEnumName: Enum data type
                for INEnum in tmp_INEnums:
                    INEnumName = INEnum["INEnumName"]
                    INEnumDisplayName = INEnum["INEnumDisplayName"]
                    INEnums[INEnumName] = INEnum
                del tmp_INEnums

                tmp_INTypes = cur_intentdefinition_file["INTypes"]
                INTypes = {}  # INTypeName: Custom data type
                for INType in tmp_INTypes:
                    INTypeName = INType["INTypeName"]
                    INTypeDisplayName = INType["INTypeDisplayName"]
                    INTypes[INTypeName] = INType
                del tmp_INTypes

                for intentvalue in INIntents:
                    intentname = intentvalue["INIntentName"]
                    prefix_intentname = ""
                    if "INIntentClassPrefix" in intentvalue:
                        prefix_intentname = intentvalue["INIntentClassPrefix"]
                    intentname = prefix_intentname + intentname
                    if intentname[-6:] != "Intent": 
                        intentname += "Intent"
                    API_name = app_name + "." + intentname # API name

                    # Prepare all_api2paraname2paratype and all_api2parasummary.
                    if need_api2paraname2paratype:
                        if API_name not in all_api2paraname2paratype:
                            all_api2paraname2paratype[API_name] = {}
                        else:
                            all_api2paraname2paratype[API_name] = {}
                    if need_api2parasummary:
                        if API_name not in all_api2parasummary:
                            all_api2parasummary[API_name] = {}
                        else:
                            all_api2parasummary[API_name] = {}

                    # The title of the API
                    INIntentTitle = intentvalue["INIntentTitle"]

                    # The description of the API
                    if "INIntentDescription" in intentvalue:
                        INIntentDescription = intentvalue["INIntentDescription"]
                    else:
                        INIntentDescription = ""

                    # The parameters of the API
                    if "INIntentParameters" in intentvalue:
                        INIntentParameters = intentvalue["INIntentParameters"]
                    else:
                        INIntentParameters = []

                    parameters, parameter_descs = [], []
                    for INIntentParameter in INIntentParameters:
                        INIntentParameterName = INIntentParameter["INIntentParameterName"]
                        valueType, defaultValue = None, ""  # parameter type and default value
                        
                        para_desc = ""
                        INIntentParameterDisplayName = ""
                        INTypeDisplayName, INTypeDesc = "", ""
                        INEnumDisplayName, INEnumDesc = "", ""
                        
                        # Prepare valueType, INTypeDisplayName, INTypeDesc, INEnumDisplayName, INEnumDesc
                        if "INIntentParameterObjectType" not in INIntentParameter and "INIntentParameterEnumType" not in INIntentParameter:  # primitive
                            INIntentParameterType = INIntentParameter["INIntentParameterType"]
                            if INIntentParameterType in self.INIntentParameterType2type:
                                if self.INIntentParameterType2type[INIntentParameterType] == "Object":
                                    valueType = INIntentParameterType + "(Object)"
                                else:
                                    valueType = self.INIntentParameterType2type[INIntentParameterType]
                            elif INIntentParameterType == "Object":
                                valueType = f'({"Object"})'
                            else:
                                print(INIntentParameterType)
                                raise ValueError("This data type does not exist.")
                        
                        elif "INIntentParameterObjectType" in INIntentParameter and "INIntentParameterEnumType" not in INIntentParameter:  # entity
                            INIntentParameterType = INIntentParameter["INIntentParameterType"]
                            # If the current object is a custom data type, include INTypeDisplayName from INTypes, 
                            # which is the name of the custom data type, as part of the parameter description.
                            INIntentParameterObjectType = INIntentParameter["INIntentParameterObjectType"]
                            valueType = INIntentParameterObjectType + f'({"Object"})'
                            if INIntentParameterObjectType in INTypes:
                                INTypeDisplayName = INTypes[INIntentParameterObjectType]["INTypeDisplayName"]
                        
                        elif "INIntentParameterObjectType" not in INIntentParameter and "INIntentParameterEnumType" in INIntentParameter:  # enum
                            INIntentParameterType = INIntentParameter["INIntentParameterType"]
                            # If the current object is an enum data type, include INEnumDisplayName from INEnums, 
                            # which is the name of the enum data type, as part of the parameter description.
                            INIntentParameterEnumType = INIntentParameter["INIntentParameterEnumType"]
                            valueType = INIntentParameterEnumType + f'({"Enum"})'
                            if INIntentParameterEnumType in INEnums:
                                INEnumDisplayName = INEnums[INIntentParameterEnumType]["INEnumDisplayName"]
                                INEnumDesc += "The value of this Enum must be one of the following values (The text in parentheses describes the value): "
                                for INEnumValue in INEnums[INIntentParameterEnumType]["INEnumValues"]:
                                    INEnumValueName = INEnumValue["INEnumValueName"]
                                    if "INEnumValueIndex" not in INEnumValue:
                                        continue
                                    INEnumValueDisplayName = INEnumValue["INEnumValueDisplayName"]
                                    # If there is a next value
                                    if INEnumValue != INEnums[INIntentParameterEnumType]["INEnumValues"][-1]:
                                        INEnumDesc += '"' + INEnumValueName + '"' + f"({INEnumValueDisplayName}), "
                                    else:
                                        INEnumDesc += '"' + INEnumValueName + '"' + f"({INEnumValueDisplayName})"

                        # Prepare INIntentParameterDisplayName
                        if "INIntentParameterDisplayName" in INIntentParameter:
                            INIntentParameterDisplayName = INIntentParameter["INIntentParameterDisplayName"]

                        # Prepare defaultValue
                        if "INIntentParameterMetadata" in INIntentParameter:
                            INIntentParameterMetadata = INIntentParameter["INIntentParameterMetadata"]
                            if "INIntentParameterMetadataDefaultValue" in INIntentParameterMetadata:
                                INIntentParameterMetadataDefaultValue = INIntentParameterMetadata[
                                    "INIntentParameterMetadataDefaultValue"]
                                defaultValue = INIntentParameterMetadataDefaultValue  # Default parameter value
                            else:
                                pass
                        else:
                            pass
                        
                        # Prepare parameters and all_api2paraname2paratype
                        if defaultValue:
                            if isinstance(defaultValue, str):
                                tmp_para_str = f"{INIntentParameterName}: {
                                    valueType} = \"{defaultValue}\""
                                parameters.append(tmp_para_str)

                                if need_api2paraname2paratype:
                                    all_api2paraname2paratype[API_name][INIntentParameterName] = f"{
                                        valueType} = \"{defaultValue}\""
                            elif isinstance(defaultValue, bool) or isinstance(defaultValue, int) or isinstance(defaultValue, float):
                                tmp_para_str = f"{INIntentParameterName}: {
                                    valueType} = {defaultValue}"
                                parameters.append(tmp_para_str)

                                if need_api2paraname2paratype:
                                    all_api2paraname2paratype[API_name][INIntentParameterName] = f"{
                                        valueType} = {defaultValue}"
                            else:
                                raise ValueError("Invalid type for defaultValue.")
                        else:
                            tmp_para_str = f"{
                                INIntentParameterName}: {valueType}"
                            parameters.append(tmp_para_str)

                            if need_api2paraname2paratype:
                                all_api2paraname2paratype[API_name][INIntentParameterName] = f"{
                                    valueType}"

                        # Prepare para_desc
                        for cur_desc in [INIntentParameterDisplayName, INTypeDisplayName, INTypeDesc, INEnumDisplayName, INEnumDesc]:
                            if cur_desc:
                                para_desc += " " + cur_desc + "."
                        
                        """INIntentParameterRelationship indicates that this parameter has dependencies on other parameters.
                        """
                        INIntentParameterRelationship = None
                        if "INIntentParameterRelationship" in INIntentParameter:
                            INIntentParameterRelationship = INIntentParameter[
                                "INIntentParameterRelationship"]
                            if "INIntentParameterRelationshipParentName" in INIntentParameterRelationship:
                                INIntentParameterRelationshipParentName = INIntentParameterRelationship[
                                    "INIntentParameterRelationshipParentName"]
                                INIntentParameterRelationshipPredicateName = INIntentParameterRelationship[
                                    "INIntentParameterRelationshipPredicateName"]
                                if "INIntentParameterRelationshipPredicateValue" in INIntentParameterRelationship:
                                    INIntentParameterRelationshipPredicateValue = INIntentParameterRelationship[
                                        "INIntentParameterRelationshipPredicateValue"]
                                else:
                                    if INIntentParameterRelationshipPredicateName == "BooleanHasExactValue":
                                        INIntentParameterRelationshipPredicateValue = False
                                tmp_desc_str = ""
                                if INIntentParameterRelationshipPredicateName == "BooleanHasExactValue":
                                    if isinstance(INIntentParameterRelationshipPredicateValue, str):
                                        tmp_desc_str = f'the value of "{INIntentParameterRelationshipParentName}" is "{
                                            INIntentParameterRelationshipPredicateValue}"'
                                    elif isinstance(INIntentParameterRelationshipPredicateValue, bool) or isinstance(INIntentParameterRelationshipPredicateValue, int) or isinstance(INIntentParameterRelationshipPredicateValue, float):
                                        tmp_desc_str = f'the value of "{INIntentParameterRelationshipParentName}" is {
                                            INIntentParameterRelationshipPredicateValue}'
                                    else:
                                        raise ValueError(
                                            "Invalid type for INIntentParameterRelationshipPredicateValue.")
                                elif INIntentParameterRelationshipPredicateName == "EnumHasExactValue":
                                    if isinstance(INIntentParameterRelationshipPredicateValue, str):
                                        tmp_desc_str = f'the value of "{INIntentParameterRelationshipParentName}" is "{
                                            INIntentParameterRelationshipPredicateValue}"'
                                    elif isinstance(INIntentParameterRelationshipPredicateValue, bool) or isinstance(INIntentParameterRelationshipPredicateValue, int) or isinstance(INIntentParameterRelationshipPredicateValue, float):
                                        tmp_desc_str = f'the value of "{INIntentParameterRelationshipParentName}" is {
                                            INIntentParameterRelationshipPredicateValue}'
                                    else:
                                        raise ValueError(
                                            "Invalid type for INIntentParameterRelationshipPredicateValue.")
                                elif INIntentParameterRelationshipPredicateName == "HasAnyValue":
                                    tmp_desc_str = f'"{
                                        INIntentParameterRelationshipParentName} has any value'
                                para_desc += f""" This value depends on the value of "{
                                    INIntentParameterRelationshipParentName}". This parameter is only valid when {tmp_desc_str}."""

                        parameter_descs.append(
                            f"{INIntentParameterName}: {para_desc}")

                    """Prepare return value"""
                    return_value_name, return_value_type, return_value_desc = "", "", ""
                    return_value_name_is_API = False
                    return_value_display_name = ""
                    return_value_INTypeDisplayName, return_value_INTypeDesc = "", ""
                    return_value_INEnumDisplayName, return_value_INEnumDesc = "", ""
                    if "INIntentResponse" in intentvalue:
                        INIntentResponse = intentvalue["INIntentResponse"]
                        if "INIntentResponseOutput" in INIntentResponse:
                            INIntentResponseOutput = INIntentResponse["INIntentResponseOutput"]
                            # For example, in Taio's Docs - Create Document method, the Response may contain multiple parameters, 
                            # each with an INIntentResponseParameterName, INIntentResponseParameterType, and INIntentResponseParameterDisplayName.
                            INIntentResponseParameters = INIntentResponse["INIntentResponseParameters"]
                            INIntentResponseParameterType = INIntentResponseParameters[0]["INIntentResponseParameterType"]
                            if "INIntentResponseParameterDisplayName" in INIntentResponseParameters[0]:
                                # The first parameter is of the type indicated by return_value_name.
                                INIntentResponseParameterDisplayName = INIntentResponseParameters[0]["INIntentResponseParameterDisplayName"]
                            return_value_type = INIntentResponseParameterType
                            return_value_display_name = INIntentResponseParameterDisplayName
                            return_value_name = return_value_display_name

                            if INIntentResponseParameterType == "Object":
                                if "INIntentResponseParameterObjectType" in INIntentResponseParameters[0]:
                                    INIntentResponseObjectType = INIntentResponseParameters[
                                        0]["INIntentResponseParameterObjectType"]
                                    return_value_type = INIntentResponseObjectType + f'({"Object"})'
                                    if INIntentResponseObjectType in INTypes:
                                        return_value_INTypeDisplayName = INTypes[
                                            INIntentResponseObjectType]["INTypeDisplayName"]
                            elif INIntentResponseParameterType == "Integer" and "INIntentResponseParameterEnumType" in INIntentResponseParameters[0]:
                                INIntentResponseEnumType = INIntentResponseParameters[0]["INIntentResponseParameterEnumType"]
                                if INIntentResponseEnumType in INEnums:
                                    return_value_type = INIntentResponseEnumType + f'({"Enum"})'
                                    return_value_INEnumDisplayName = INEnums[INIntentResponseEnumType]["INEnumDisplayName"]

                                    return_value_INEnumDesc += "The value of this Enum must be one of the following values (The text in parentheses describes the value): "
                                    for INEnumValue in INEnums[INIntentResponseEnumType]["INEnumValues"]:
                                        INEnumValueName = INEnumValue["INEnumValueName"]
                                        if "INEnumValueIndex" not in INEnumValue:
                                            continue
                                        INEnumValueDisplayName = INEnumValue["INEnumValueDisplayName"]
                                        # If has next value
                                        if INEnumValue != INEnums[INIntentResponseEnumType]["INEnumValues"][-1]:
                                            return_value_INEnumDesc += '"' + INEnumValueName + '"' + f"({INEnumValueDisplayName}), "
                                        else:
                                            return_value_INEnumDesc += '"' + INEnumValueName + '"' + f"({INEnumValueDisplayName})"
                            else:
                                if return_value_type in self.INIntentParameterType2type:
                                    if self.INIntentParameterType2type[return_value_type] == "Object":
                                        return_value_type = return_value_type + "(Object)"
                                    else:
                                        return_value_type = self.INIntentParameterType2type[return_value_type]
                                else:
                                    raise ValueError("The data type does not exist.")
                        else:  # If INIntentResponseOutput does not exist and return_value_type is present, set return_value_name to INIntentTitle.
                            return_value_name = INIntentTitle
                            return_value_name_is_API = True
                    else:
                        pass

                    for cur_desc in [return_value_display_name, return_value_INTypeDisplayName, return_value_INTypeDesc, return_value_INEnumDisplayName, return_value_INEnumDesc]:
                        if cur_desc:
                            if not return_value_desc:
                                return_value_desc += cur_desc + "."
                            else:
                                return_value_desc += " " + cur_desc + "."

                    ParameterSummary = ""
                    if "INIntentManagedParameterCombinations" in intentvalue:
                        def remove_parentheses(s):
                            # A regular expression matches parentheses and their contents.
                            pattern = r'\([^)]*\)'
                            # Replace the matched content with an empty string.
                            cleaned_string = re.sub(pattern, '', s)
                            return cleaned_string

                        INIntentManagedParameterCombinations = intentvalue[
                            "INIntentManagedParameterCombinations"]
                        for INIntentManagedParameterCombination_key, INIntentManagedParameterCombination in INIntentManagedParameterCombinations.items():
                            if "INIntentParameterCombinationTitle" in INIntentManagedParameterCombination:
                                INIntentParameterCombinationTitle = INIntentManagedParameterCombination[
                                    "INIntentParameterCombinationTitle"]
                                remove_pare_INIntentManagedParameterCombination_key = remove_parentheses(
                                    INIntentParameterCombinationTitle)
                                if not ParameterSummary:
                                    ParameterSummary = f"({
                                        remove_pare_INIntentManagedParameterCombination_key}) " + INIntentParameterCombinationTitle
                                else:
                                    ParameterSummary += "; " + \
                                        f"({remove_pare_INIntentManagedParameterCombination_key}) " + \
                                        INIntentParameterCombinationTitle

                        tmp_ParameterSummary_dict = {}
                        for INIntentManagedParameterCombination_key, INIntentManagedParameterCombination in INIntentManagedParameterCombinations.items():
                            if "INIntentParameterCombinationTitle" in INIntentManagedParameterCombination:
                                INIntentParameterCombinationTitle = INIntentManagedParameterCombination[
                                    "INIntentParameterCombinationTitle"]
                                remove_pare_INIntentManagedParameterCombination_key = remove_parentheses(
                                    INIntentManagedParameterCombination_key)
                                tmp_ParameterSummary_dict[remove_pare_INIntentManagedParameterCombination_key] = INIntentParameterCombinationTitle

                        if need_api2parasummary:
                            all_api2parasummary[API_name] = tmp_ParameterSummary_dict

                        if not tmp_ParameterSummary_dict:
                            ParameterSummary_key = ""
                            ParameterSummary_value = INIntentTitle
                            ParameterSummary = f"({
                                ParameterSummary_key}) " + ParameterSummary_value

                            if need_api2parasummary:
                                all_api2parasummary[API_name] = {
                                    ParameterSummary_key: ParameterSummary_value}

                    elif "INIntentParameterCombinations" in intentvalue:
                        INIntentParameterCombinations = intentvalue["INIntentParameterCombinations"]

                        def remove_parentheses(s):
                            # A regular expression matches parentheses and their contents.
                            pattern = r'\([^)]*\)'
                            # Replace the matched content with an empty string.
                            cleaned_string = re.sub(pattern, '', s)
                            return cleaned_string

                        for INIntentParameterCombination_key, INIntentParameterCombination in INIntentParameterCombinations.items():
                            if "INIntentParameterCombinationTitle" in INIntentParameterCombination:
                                INIntentParameterCombinationTitle = INIntentParameterCombination[
                                    "INIntentParameterCombinationTitle"]
                                remove_pare_INIntentParameterCombination_key = remove_parentheses(
                                    INIntentParameterCombination_key)
                                if not ParameterSummary:
                                    ParameterSummary = f"({
                                        remove_pare_INIntentParameterCombination_key}) " + INIntentParameterCombinationTitle
                                else:
                                    ParameterSummary += "; " + \
                                        f"({remove_pare_INIntentParameterCombination_key}) " + \
                                        INIntentParameterCombinationTitle

                        tmp_ParameterSummary_dict = {}
                        for INIntentParameterCombination_key, INIntentParameterCombination in INIntentParameterCombinations.items():
                            if "INIntentParameterCombinationTitle" in INIntentParameterCombination:
                                INIntentParameterCombinationTitle = INIntentParameterCombination[
                                    "INIntentParameterCombinationTitle"]
                                remove_pare_INIntentParameterCombination_key = remove_parentheses(
                                    INIntentParameterCombination_key)
                                tmp_ParameterSummary_dict[remove_pare_INIntentParameterCombination_key] = INIntentParameterCombinationTitle

                        if need_api2parasummary:
                            all_api2parasummary[API_name] = tmp_ParameterSummary_dict
                    else:
                        INIntentParameterCombination_key = ""
                        INIntentParameterCombinationTitle = INIntentTitle
                        ParameterSummary = f"({
                            INIntentParameterCombination_key}) " + INIntentParameterCombinationTitle

                        if need_api2parasummary:
                            all_api2parasummary[API_name] = {
                                INIntentParameterCombination_key: INIntentParameterCombinationTitle}

                    API_name, INIntentTitle, INIntentDescription, parameters, parameter_descs, return_value_name, return_value_type, return_value_desc, ParameterSummary
                    if need_api2paraname2paratype:
                        if return_value_type:
                            all_api2paraname2paratype[API_name]["ThisIsReturnValue:" +
                                                                return_value_name] = return_value_type
                        elif return_value_name and not return_value_name_is_API:
                            all_api2paraname2paratype[API_name]["ThisIsReturnValue:" +
                                                                return_value_name] = f"Object"

                    API_info = ""
                    API_info += f"""{API_name}({", ".join(parameters)})"""
                    if return_value_type:
                        API_info += f""" -> {return_value_name}
                            : {return_value_type}"""
                    if API_info[-1] != "\n":
                        API_info += "\n"

                    if len(parameter_descs) > 0:
                        parameter_descs_str = "\n    ".join(parameter_descs)
                        API_info += f"""Parameters:
    {parameter_descs_str}"""
                    if API_info[-1] != "\n":
                        API_info += "\n"

                    if return_value_type:
                        API_info += f"""Return Value:
    {return_value_name}: {return_value_desc}"""
                    if API_info[-1] != "\n":
                        API_info += "\n"

                    if INIntentTitle:
                        API_info += f"""Description:
    {INIntentTitle}"""
                    if INIntentDescription:
                        API_info += f""": {INIntentDescription}"""
                    if API_info[-1] != "\n":
                        API_info += "\n"

                    if ParameterSummary:
                        API_info += f"""ParameterSummary: {ParameterSummary}"""
                    if API_info[-1] != "\n":
                        API_info += "\n"
                    all_api2info[API_name] = API_info

            # Find all APIs from all actions data.
            for all_actionsdata_key in all_actionsdata_keys:
                # The current actionsdata file.
                cur_actionsdata_file = self.api_files[app_name][all_actionsdata_key]

                actions = cur_actionsdata_file["actions"]

                tmp_enums = cur_actionsdata_file["enums"]
                enums = {}  # enum data type
                for enum in tmp_enums:
                    identifier = enum["identifier"]
                    displayTypeName = enum["displayTypeName"]["key"]
                    enums[identifier] = enum
                del tmp_enums

                tmp_entities = cur_actionsdata_file["entities"]
                entities = {}  # advanced data type
                for entity in tmp_entities.values():
                    typeName = entity["typeName"]
                    displayTypeName = entity["displayTypeName"]["key"]
                    entities[typeName] = entity
                del tmp_entities

                for intentname, intentvalue in actions.items():
                    if "isDiscoverable" in intentvalue:
                        isDiscoverable = intentvalue["isDiscoverable"]
                        if not isDiscoverable:
                            continue

                    API_name = app_name + "." + intentname
                    if need_api2paraname2paratype:
                        if API_name not in all_api2paraname2paratype:
                            all_api2paraname2paratype[API_name] = {}
                        else:
                            all_api2paraname2paratype[API_name] = {}

                    if need_api2parasummary:
                        if API_name not in all_api2parasummary:
                            all_api2parasummary[API_name] = {}
                        else:
                            all_api2parasummary[API_name] = {}

                    if "title" in intentvalue: # API title
                        description_title = intentvalue["title"]["key"]
                    else:
                        description_title = ""
                    if "descriptionMetadata" in intentvalue: # API description
                        descriptionMetadata = intentvalue["descriptionMetadata"]
                        description_text = descriptionMetadata["descriptionText"]["key"]
                    else:
                        descriptionMetadata = None
                        description_text = ""

                    parameter_dicts = intentvalue["parameters"]
                    parameters = []
                    parameter_descs = []
                    for parameter_dict in parameter_dicts:
                        name = parameter_dict["name"]  # parameter name
                        valueType = None  # parameter type
                        defaultValue = ""  # parameter default value

                        para_desc = ""
                        parameterTitle, parameterDescription = "", ""
                        entity_displayTypeName, entity_Desc = "", ""
                        enum_displayTypeName, enum_Desc = "", "" 

                        if "primitive" in parameter_dict["valueType"]:
                            tmp_valueType = parameter_dict["valueType"]["primitive"]["wrapper"]["typeIdentifier"]
                            if tmp_valueType in self.actionsdata_para2type:
                                if self.actionsdata_para2type[tmp_valueType] == "Object":
                                    valueType = str(
                                        tmp_valueType) + f'({"Object"})'
                                else:
                                    valueType = self.actionsdata_para2type[tmp_valueType]
                            else:
                                print(valueType)
                                raise ValueError("The data type does not exist.")
                        elif "linkEnumeration" in parameter_dict["valueType"]:
                            enum_identifier = parameter_dict["valueType"]["linkEnumeration"]["wrapper"]["identifier"]
                            valueType = enum_identifier + f'({"Enum"})'
                            if enum_identifier in enums:
                                cur_enum = enums[enum_identifier]
                                enum_displayTypeName = cur_enum["displayTypeName"]["key"]
                                enum_Desc += "The value of this Enum must be one of the following values (The text in parentheses describes the value): "
                                for enum_value in enums[enum_identifier]["cases"]:
                                    enum_value_identifier = enum_value["identifier"]
                                    enum_value_displayRepresentation = enum_value[
                                        "displayRepresentation"]["title"]["key"]
                                    # If there is another value available.
                                    if enum_value != enums[enum_identifier]["cases"][-1]:
                                        enum_Desc += '"' + enum_value_identifier + '"' + \
                                            f"({enum_value_displayRepresentation}), "
                                    else:
                                        enum_Desc += '"' + enum_value_identifier + \
                                            '"' + \
                                            f"({enum_value_displayRepresentation})"
                        elif "entity" in parameter_dict["valueType"]:
                            entity_value_identifier = parameter_dict["valueType"]["entity"]["wrapper"]["typeName"]
                            valueType = entity_value_identifier + \
                                f'({"Object"})'
                            if entity_value_identifier in entities:
                                entity_displayTypeName = entities[entity_value_identifier]["displayTypeName"]["key"]
                        elif "array" in parameter_dict["valueType"]:
                            if "primitive" in parameter_dict["valueType"]["array"]["wrapper"]["memberValueType"]:
                                tmp_valueType = parameter_dict["valueType"]["array"]["wrapper"][
                                    "memberValueType"]["primitive"]["wrapper"]["typeIdentifier"]
                                if tmp_valueType in self.actionsdata_para2type:
                                    if self.actionsdata_para2type[tmp_valueType] == "Object":
                                        valueType = tmp_valueType + \
                                            f'({"Object"})'
                                    else:
                                        valueType = self.actionsdata_para2type[tmp_valueType]
                                else:
                                    print(tmp_valueType)
                                    raise ValueError("The data type does not exist.")
                                valueType = "array(" + valueType + ")"
                            elif "linkEnumeration" in parameter_dict["valueType"]["array"]["wrapper"]["memberValueType"]:
                                valueType = "array(" + parameter_dict["valueType"]["array"]["wrapper"]["memberValueType"][
                                    "linkEnumeration"]["wrapper"]["identifier"] + f'({"Enum"})' + ")"
                            elif "entity" in parameter_dict["valueType"]["array"]["wrapper"]["memberValueType"]:
                                valueType = "array(" + parameter_dict["valueType"]["array"]["wrapper"]["memberValueType"]["entity"]["wrapper"]["typeName"] + f'({
                                    "Object"})' + ")"
                        elif "intents" in parameter_dict["valueType"]:
                            tmp_valueType = parameter_dict["valueType"]["intents"]["wrapper"]["typeIdentifier"]
                            if tmp_valueType in self.actionsdata_para2type:
                                if self.actionsdata_para2type[tmp_valueType] == "Object":
                                    valueType = str(
                                        tmp_valueType) + f'({"Object"})'
                                else:
                                    valueType = self.actionsdata_para2type[tmp_valueType]
                            else:
                                print(tmp_valueType)
                                raise ValueError("The data type does not exist.")
                        elif "measurement" in parameter_dict["valueType"]:
                            tmp_valueType = parameter_dict["valueType"]["measurement"]["wrapper"]["unitType"]
                            if tmp_valueType in self.actionsdata_para2type:
                                if self.actionsdata_para2type[tmp_valueType] == "Object":
                                    valueType = tmp_valueType + f'({"Object"})'
                                else:
                                    valueType = self.actionsdata_para2type[tmp_valueType]
                            else:
                                print(tmp_valueType)
                                raise ValueError("The data type does not exist.")
                        else:
                            print(parameter_dict["valueType"])
                            print(parameter_dict)
                            raise ValueError("The data type does not exist.")

                        if "title" in parameter_dict:
                            parameterTitle = parameter_dict["title"]["key"]

                        if "parameterDescription" in parameter_dict:
                            parameterDescription = parameter_dict["parameterDescription"]["key"]

                        if "typeSpecificMetadata" in parameter_dict:
                            typeSpecificMetadata = parameter_dict["typeSpecificMetadata"]
                            for key_name, value in zip(typeSpecificMetadata[::2], typeSpecificMetadata[1::2]):
                                if key_name == "LNValueTypeSpecificMetadataKeyDefaultValue":
                                    # Possible values include: int (primitive 1,2), string (primitive 0, Enum), double (measurement 1 7, primitive 7), array ()
                                    key_types = list(value.keys())
                                    for key_type in key_types:
                                        if key_type not in ["array"]:
                                            tmp_str = str(
                                                value[key_type]["wrapper"])
                                            defaultValue += tmp_str
                                        else:
                                            tmp_str = ""
                                            for tmp_line in value[key_type]["elements"]:
                                                for tmp_key, tmp_val in tmp_line.items():
                                                    tmp_real_val = tmp_val["wrapper"]
                                                    # If it is not the last element.
                                                    if tmp_key != value[key_type]["elements"][-1]:
                                                        tmp_str += tmp_real_val + \
                                                            f"({tmp_key}), "
                                                    else:
                                                        tmp_str += tmp_real_val + \
                                                            f"({tmp_key})"

                                            defaultValue += "array(" + \
                                                tmp_str + ")"
                                        # If it is not the last element.
                                        if key_type != key_types[-1]:
                                            defaultValue += " / "
                        if defaultValue:
                            if isinstance(defaultValue, str):
                                tmp_para_str = f"{name}: {
                                    valueType} = \"{defaultValue}\""
                                parameters.append(tmp_para_str)

                                if need_api2paraname2paratype:
                                    all_api2paraname2paratype[API_name][name] = f"{
                                        valueType} = \"{defaultValue}\""
                            elif isinstance(defaultValue, bool) or isinstance(defaultValue, int) or isinstance(defaultValue, float):
                                tmp_para_str = f"{name}: {
                                    valueType} = {defaultValue}"
                                parameters.append(tmp_para_str)

                                if need_api2paraname2paratype:
                                    all_api2paraname2paratype[API_name][name] = f"{
                                        valueType} = {defaultValue}"
                            else:
                                raise ValueError("Default value type error.")
                        else:
                            tmp_para_str = f"{name}: {valueType}"
                            parameters.append(tmp_para_str)

                            if need_api2paraname2paratype:
                                all_api2paraname2paratype[API_name][name] = f"{
                                    valueType}"

                        # Generate parameter description.
                        for cur_desc in [parameterTitle, parameterDescription, entity_displayTypeName, entity_Desc, enum_displayTypeName, enum_Desc]:
                            if cur_desc:
                                if not para_desc:
                                    para_desc = cur_desc + "."
                                else:
                                    para_desc += " " + cur_desc + "."
                        parameter_descs.append(f"{name}: {para_desc}")

                    def find_summary_triples(dictionary, debug=False):
                        triples = {}

                        def recurse(item, debug=False):
                            if debug:
                                print(json.dumps(item, indent=4))
                                input()
                            if isinstance(item, dict):
                                # This checks for the actionSummary anywhere in the dictionary
                                if 'wrapper' in item and 'summaryString' in item['wrapper']:
                                    summary = item['wrapper']['summaryString']
                                    format_string = summary.get(
                                        'formatString', '')
                                    parameter_identifiers = summary.get(
                                        'parameterIdentifiers', [])
                                    other_parameters = item['wrapper'].get(
                                        'otherParameterIdentifiers', [])
                                    all_identifiers = parameter_identifiers + other_parameters
                                    triples[",".join(
                                        all_identifiers)] = format_string

                                # Continue to recurse through all dictionary values
                                for value in item.values():
                                    recurse(value, debug)

                            elif isinstance(item, list):
                                # Recurse into each element in the list
                                for element in item:
                                    recurse(element, debug)

                        # Start recursion from the root of the dictionary
                        recurse(dictionary, debug=debug)

                        return triples

                    ParameterSummary = None
                    if "actionConfiguration" in intentvalue:

                        actionConfiguration = intentvalue["actionConfiguration"]
                        triples = find_summary_triples(actionConfiguration)

                        def remove_parentheses(s):
                            # Regular expression matching parentheses and their contents.
                            pattern = r'\([^)]*\)'
                            # Replace matched content with an empty string.
                            cleaned_string = re.sub(pattern, '', s)
                            return cleaned_string
                        for key, value in triples.items():
                            remove_pare_key = remove_parentheses(key)
                            if not ParameterSummary:
                                ParameterSummary = f"({
                                    remove_pare_key}) " + value
                            else:
                                ParameterSummary += "; " + \
                                    f"({remove_pare_key}) " + value

                        if need_api2parasummary:
                            all_api2parasummary[API_name] = triples

                        if ParameterSummary == None:
                            ParameterSummary_key = ""
                            if description_title and not description_text:
                                ParameterSummary_value = description_title
                            elif description_text and not description_title:
                                ParameterSummary_value = description_text
                            else:
                                ParameterSummary_value = description_title

                            ParameterSummary = f"({
                                ParameterSummary_key}) " + ParameterSummary_value

                            if need_api2parasummary:
                                all_api2parasummary[API_name] = {
                                    ParameterSummary_key: ParameterSummary_value}

                    else:
                        ParameterSummary_key = ""
                        if description_title and not description_text:
                            ParameterSummary_value = description_title
                        elif description_text and not description_title:
                            ParameterSummary_value = description_text
                        else:
                            ParameterSummary_value = description_title

                        ParameterSummary = f"({
                            ParameterSummary_key}) " + ParameterSummary_value

                        if need_api2parasummary:
                            all_api2parasummary[API_name] = {
                                ParameterSummary_key: ParameterSummary_value}

                    return_value_name, return_value_type, return_value_desc = "", "", ""
                    return_value_name_is_API = False
                    return_value_display_name = ""
                    return_value_INTypeDisplayName, return_value_object_desc = "", ""
                    return_value_INEnumDisplayName, return_value_enum_desc = "", ""
                    if descriptionMetadata and "resultValueName" in descriptionMetadata:
                        return_value_name = descriptionMetadata["resultValueName"]["key"]
                    else:  # If INIntentResponseOutput does not exist, and there is still a return value, set the name to 'description_title'.
                        return_value_name = description_title
                        return_value_name_is_API = True

                    if "outputType" in intentvalue:
                        outputType = intentvalue["outputType"]

                        if "primitive" in outputType:
                            tmp_valueType = outputType["primitive"]["wrapper"]["typeIdentifier"]
                            if tmp_valueType in self.actionsdata_para2type:
                                if self.actionsdata_para2type[tmp_valueType] == "Object":
                                    return_value_type = str(
                                        tmp_valueType) + f'({"Object"})'
                                else:
                                    return_value_type = self.actionsdata_para2type[tmp_valueType]
                            else:
                                print(tmp_valueType)
                                raise ValueError("The data type does not exist.")
                        elif "linkEnumeration" in outputType:
                            enum_identifier = outputType["linkEnumeration"]["wrapper"]["identifier"]
                            return_value_type = enum_identifier + f'({"Enum"})'

                            if enum_identifier in enums:
                                cur_enum = enums[enum_identifier]
                                return_value_INEnumDisplayName = cur_enum["displayTypeName"]["key"]

                                return_value_enum_desc += "The value of this Enum must be one of the following values (The text in parentheses describes the value): "
                                for enum_value in enums[enum_identifier]["cases"]:
                                    enum_value_identifier = enum_value["identifier"]
                                    enum_value_displayRepresentation = enum_value[
                                        "displayRepresentation"]["title"]["key"]
                                    # If there is another value.
                                    if enum_value != enums[enum_identifier]["cases"][-1]:
                                        return_value_enum_desc += '"' + enum_value_identifier + \
                                            '"' + \
                                            f"({enum_value_displayRepresentation}), "
                                    else:
                                        return_value_enum_desc += '"' + enum_value_identifier + \
                                            '"' + \
                                            f"({enum_value_displayRepresentation})"

                        elif "entity" in outputType:
                            entity_value_identifier = outputType["entity"]["wrapper"]["typeName"]
                            return_value_type = entity_value_identifier + \
                                f'({"Object"})'

                            if entity_value_identifier in entities:
                                return_value_INTypeDisplayName = entities[
                                    entity_value_identifier]["displayTypeName"]["key"]

                        elif "array" in outputType:
                            if "primitive" in outputType["array"]["wrapper"]["memberValueType"]:
                                tmp_valueType = outputType["array"]["wrapper"][
                                    "memberValueType"]["primitive"]["wrapper"]["typeIdentifier"]
                                if tmp_valueType in self.actionsdata_para2type:
                                    if self.actionsdata_para2type[tmp_valueType] == "Object":
                                        return_value_type = tmp_valueType + \
                                            f'({"Object"})'
                                    else:
                                        return_value_type = self.actionsdata_para2type[tmp_valueType]
                                    return_value_type = "array(" + \
                                        return_value_type + ")"
                                else:
                                    print(tmp_valueType)
                                    raise ValueError("The data type does not exist.")
                            elif "linkEnumeration" in outputType["array"]["wrapper"]["memberValueType"]:
                                return_value_type = "array(" + outputType["array"]["wrapper"]["memberValueType"]["linkEnumeration"]["wrapper"]["identifier"] + f'({
                                    "Enum"})' + ")"
                            elif "entity" in outputType["array"]["wrapper"]["memberValueType"]:
                                return_value_type = "array(" + outputType["array"]["wrapper"]["memberValueType"]["entity"]["wrapper"]["typeName"] + f'({
                                    "Object"})' + ")"
                        elif "intents" in outputType:
                            tmp_valueType = outputType["intents"]["wrapper"]["typeIdentifier"]
                            if tmp_valueType in self.actionsdata_para2type:
                                if self.actionsdata_para2type[tmp_valueType] == "Object":
                                    return_value_type = str(
                                        tmp_valueType) + f'({"Object"})'
                                else:
                                    return_value_type = self.actionsdata_para2type[tmp_valueType]
                            else:
                                print(tmp_valueType)
                                raise ValueError("The data type does not exist.")

                        elif "measurement" in outputType:
                            tmp_valueType = outputType["measurement"]["wrapper"]["unitType"]
                            if tmp_valueType in self.actionsdata_para2type:
                                if self.actionsdata_para2type[tmp_valueType] == "Object":
                                    return_value_type = str(
                                        tmp_valueType) + f'({"Object"})'
                                else:
                                    return_value_type = self.actionsdata_para2type[tmp_valueType]
                            else:
                                print(tmp_valueType)
                                raise ValueError("The data type does not exist.")
                        else:
                            print(outputType)
                            raise ValueError("The data type does not exist.")
                    for cur_desc in [return_value_display_name, return_value_INTypeDisplayName, return_value_object_desc, return_value_INEnumDisplayName, return_value_enum_desc]:
                        if cur_desc:
                            if not return_value_desc:
                                return_value_desc += cur_desc + "."
                            else:
                                return_value_desc += " " + cur_desc + "."

                    API_name, description_title, description_text, parameters, parameter_descs, return_value_name, return_value_type, return_value_desc, ParameterSummary
                    if need_api2paraname2paratype:
                        if return_value_type:
                            all_api2paraname2paratype[API_name]["ThisIsReturnValue:" + str(
                                return_value_name)] = return_value_type
                        elif return_value_name and not return_value_name_is_API:
                            all_api2paraname2paratype[API_name]["ThisIsReturnValue:" +
                                                                return_value_name] = f"Object"

                    API_info = ""
                    API_info += f"""{API_name}({", ".join(parameters)})"""
                    if return_value_type:
                        API_info += f""" -> {return_value_name}
                            : {return_value_type}"""
                    if API_info[-1] != "\n":
                        API_info += "\n"

                    if len(parameter_descs) > 0:
                        parameter_descs_str = "\n    ".join(parameter_descs)
                        API_info += f"""Parameters:
    {parameter_descs_str}"""
                    if API_info[-1] != "\n":
                        API_info += "\n"

                    if return_value_type:
                        API_info += f"""Return Value:
    {return_value_name}: {return_value_desc}"""
                    if API_info[-1] != "\n":
                        API_info += "\n"

                    if description_title:
                        API_info += f"""Description:
    {description_title}"""
                    if description_text:
                        API_info += f""": {description_text}"""
                    if API_info[-1] != "\n":
                        API_info += "\n"

                    if ParameterSummary:
                        API_info += f"""ParameterSummary: {ParameterSummary}"""
                    if API_info[-1] != "\n":
                        API_info += "\n"
                    all_api2info[API_name] = API_info

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
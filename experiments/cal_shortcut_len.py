"""Categorize the shortcuts into 5 groups based on their length. 
Due to the context length limitation of LLM, we will only evaluate the shortcuts in the first 4 groups.

The five groups are:
1. <= 1
2. (1, 5]
3. (5, 15]
4. (15, 30]
5. > 30

Special rule for calculating length:
1. For branching, use the longest branch length as the length of the branch.
2. skip the comment and alert actions:
    [
        "is.workflow.actions.comment",
        "is.workflow.actions.alert"
    ]
"""

import matplotlib.pyplot as plt
import numpy as np
import json
import os

SHORTCUT_DATA = os.getenv("SHORTCUT_DATA")

def cal_WFWorkflowActions_unique_apis_num(WFWorkflowActions):
    """Calculate the number of distinct APIs in WFWorkflowActions
    
    Args:
        WFWorkflowActions: the list of actions in the shortcut
    """

    if not WFWorkflowActions:
        return 0

    shortcut2avgAPI_set = set()
    i = 0
    while i < len(WFWorkflowActions):

        action = WFWorkflowActions[i]

        """calculate the number of distinct APIs in WFWorkflowActions 
        """
        if action["WFWorkflowActionIdentifier"] not in [
            "is.workflow.actions.conditional",
            "is.workflow.actions.choosefrommenu",
            "is.workflow.actions.repeat.count",
            "is.workflow.actions.repeat.each",
            "is.workflow.actions.comment",
            "is.workflow.actions.alert"
        ]:
            shortcut2avgAPI_set.add(action["WFWorkflowActionIdentifier"])
        i += 1

    shortcut2avgAPI = len(shortcut2avgAPI_set)

    return shortcut2avgAPI

def cal_WFWorkflowActions_len(WFWorkflowActions, URL):
    """Calculate the length of WFWorkflowActions
    
    Args:
        WFWorkflowActions: the list of actions in the shortcut
        URL: the iCloud URL of the shortcut
    """
    
    if not WFWorkflowActions:
        return 0
    
    WFWorkflowActions_len = 0
    i = 0
    while i < len(WFWorkflowActions):
        
        action = WFWorkflowActions[i]
        
        """For branches, use the longest branch length as the length of the branch.
        For loops, use the loop length as the length of the loop.
        """
        if action["WFWorkflowActionIdentifier"] in [
            "is.workflow.actions.conditional", # branching
            "is.workflow.actions.choosefrommenu", # branching
            "is.workflow.actions.repeat.count", # loop
            "is.workflow.actions.repeat.each", # loop                      
        ]:
            # For branches, recursively take the longest branch length as the current length.
            GroupingIdentifier = action["WFWorkflowActionParameters"]["GroupingIdentifier"]
            WFControlFlowMode = action["WFWorkflowActionParameters"]["WFControlFlowMode"]
            
            """WFControlFlowMode == 2 indicates the end of a branch or loop. 
            Normally, a shortcut should not start with WFControlFlowMode == 2 but with WFControlFlowMode == 1. 
            However, we found a few such shortcuts in our dataset. 
            Despite this error, these shortcuts can still be imported into the Shortcuts app and run correctly.
            """
            if WFControlFlowMode == 2:
                if action["WFWorkflowActionIdentifier"] == "is.workflow.actions.conditional":
                    i += 1
                    continue
                elif action["WFWorkflowActionIdentifier"] == "is.workflow.actions.choosefrommenu":
                    i += 1
                    continue
                elif action["WFWorkflowActionIdentifier"] == "is.workflow.actions.repeat.count":
                    i += 1
                    continue
                elif action["WFWorkflowActionIdentifier"] == "is.workflow.actions.repeat.each":
                    i += 1
                    continue
                else:
                    raise Exception("未知的分支")
           
            """Each branch/loop action has a GroupingIdentifier attribute at the beginning, middle, and end, indicating the start, middle, 
            and end of the branch/loop action.

            The following code is designed to find the middle/end of a branch/loop.
            """
            branchs = [WFWorkflowActions[i]]
            branchs_pos = [i]
            for j in range(i+1, len(WFWorkflowActions)):
                if "GroupingIdentifier" in WFWorkflowActions[j]["WFWorkflowActionParameters"] and WFWorkflowActions[j]["WFWorkflowActionParameters"]["GroupingIdentifier"] == GroupingIdentifier:
                    branchs.append(WFWorkflowActions[j])
                    branchs_pos.append(j)
                    if WFWorkflowActions[j]["WFWorkflowActionParameters"]["WFControlFlowMode"] == 2: # The final end of the branch has been found.
                        break
            
            if len(branchs) == 1: # if there is no corresponding branch, continue to the next action
                i += 1
                continue
            else: # if there are corresponding branches, recursively take the longest branch length as the current length.
                cur_WFWorkflowActions_len = 0
                for begin_pos, end_pos in zip(branchs_pos[:-1], branchs_pos[1:]):
                    cur_WFWorkflowActions_len = max(cur_WFWorkflowActions_len, cal_WFWorkflowActions_len(WFWorkflowActions[begin_pos + 1:end_pos], URL))
                WFWorkflowActions_len += cur_WFWorkflowActions_len
                i = branchs_pos[-1] + 1
        else: # if it is not a branch/loop, add 1 to the length
            if action["WFWorkflowActionIdentifier"] in [ # Skip the comment and alert actions
                "is.workflow.actions.comment",
                "is.workflow.actions.alert"
            ]:
                i += 1
            else:
                WFWorkflowActions_len += 1
                i += 1
    return WFWorkflowActions_len

def label_each_WFWorkflowAction_pos_inplace(WFWorkflowActions, URL):
    """Label the position of each WFWorkflowAction in the shortcut in place
    
    Args:
        WFWorkflowActions: the list of actions in the shortcut
        URL: the iCloud URL of the shortcut
    """

    if not WFWorkflowActions:
        return 0

    WFWorkflowActions_len = 0
    i = 0
    while i < len(WFWorkflowActions):
        
        action = WFWorkflowActions[i]

        """For branches, use the longest branch length as the length of the branch.
        For loops, use the loop length as the length of the loop.
        """
        if action["WFWorkflowActionIdentifier"] in [
            "is.workflow.actions.conditional", 
            "is.workflow.actions.choosefrommenu",
            "is.workflow.actions.repeat.count",
            "is.workflow.actions.repeat.each",                              
        ]:
            GroupingIdentifier = action["WFWorkflowActionParameters"]["GroupingIdentifier"]
            WFControlFlowMode = action["WFWorkflowActionParameters"]["WFControlFlowMode"]

            """WFControlFlowMode == 2 indicates the end of a branch or loop. 
            Normally, a shortcut should not start with WFControlFlowMode == 2 but with WFControlFlowMode == 1. 
            However, we found a few such shortcuts in our dataset. 
            Despite this error, these shortcuts can still be imported into the Shortcuts app and run correctly.
            """
            if WFControlFlowMode == 2:
                if action["WFWorkflowActionIdentifier"] == "is.workflow.actions.conditional":
                    i += 1
                    continue
                elif action["WFWorkflowActionIdentifier"] == "is.workflow.actions.choosefrommenu":
                    i += 1
                    continue
                elif action["WFWorkflowActionIdentifier"] == "is.workflow.actions.repeat.count":
                    i += 1
                    continue
                elif action["WFWorkflowActionIdentifier"] == "is.workflow.actions.repeat.each":
                    i += 1
                    continue
                else:
                    raise Exception("未知的分支")
            
            """Each branch/loop action has a GroupingIdentifier attribute at the beginning, middle, and end, indicating the start, middle, 
            and end of the branch/loop action.

            The following code is designed to find the middle/end of a branch/loop.
            """
            branchs = [WFWorkflowActions[i]]
            branchs_pos = [i]
            for j in range(i+1, len(WFWorkflowActions)):
                if "GroupingIdentifier" in WFWorkflowActions[j]["WFWorkflowActionParameters"] and WFWorkflowActions[j]["WFWorkflowActionParameters"]["GroupingIdentifier"] == GroupingIdentifier:
                    branchs.append(WFWorkflowActions[j])
                    branchs_pos.append(j)
                    if WFWorkflowActions[j]["WFWorkflowActionParameters"]["WFControlFlowMode"] == 2: # The final end of the branch has been found.
                        break
            if len(branchs) == 1:
                i += 1
                continue
            else:
                cur_WFWorkflowActions_len = 0
                for begin_pos, end_pos in zip(branchs_pos[:-1], branchs_pos[1:]):
                    cur_WFWorkflowActions_len = max(cur_WFWorkflowActions_len, cal_WFWorkflowActions_len(WFWorkflowActions[begin_pos + 1:end_pos], URL))
                
                """Label the position of each WFWorkflowAction in the shortcut"""
                action["pos"] = WFWorkflowActions_len + 1
                
                WFWorkflowActions_len += cur_WFWorkflowActions_len
                i = branchs_pos[-1] + 1
        else:
            if action["WFWorkflowActionIdentifier"] in [
                "is.workflow.actions.comment",
                "is.workflow.actions.alert"
            ]: # Skip the comment and alert actions
                i += 1
            else: # Add 1 to the length and label the position of the action
                WFWorkflowActions_len += 1

                """Label the position of each WFWorkflowAction in the shortcut"""
                action["pos"] = WFWorkflowActions_len
                i += 1
    return WFWorkflowActions_len

def useless_data_analysis(shortcut2len, shortcut2avgAPIs):
    """draw the distribution of the number of action sequences in the shortcuts
    figure1: the distribution of the number of action sequences in the shortcuts
    figure2: the distribution of the number of action sequences in the shortcuts, divided into 5 groups

    Args:
        shortcut2len: the length of each shortcut
        shortcut2avgAPIs: the average number of APIs in each shortcut
    """
    
    shortcut_lens, APIs_lens = list(shortcut2len.values()), list(shortcut2avgAPIs.values())
    new_shortcut_lens, new_API_lens = [], []
    for cur_shortcut_len, cur_API_len in zip(shortcut_lens, APIs_lens):
        if cur_shortcut_len > 0:
            new_shortcut_lens.append(cur_shortcut_len)
            new_API_lens.append(cur_API_len)
    shortcut_lens, APIs_lens = new_shortcut_lens, new_API_lens

    def plot_length_distribution(lengths):

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(lengths, bins=range(min(lengths), max(lengths) + 2), edgecolor='black', align='left')
        
        ax.set_xlabel('# Action Sequence', fontsize=16)
        ax.set_ylabel('Frequency', fontsize=16)
        ax.set_title('Distribution of # Action Sequence', fontsize=16)
        
        ax.set_yscale('log')
        ax.grid(True)
        
        ax.tick_params(axis='both', which='major', labelsize=14) # Set axis tick labels with larger font sizes

        plt.tight_layout()
        plt.savefig("tmp/length_distribution.png")
        return fig, ax

    fig, ax = plot_length_distribution(shortcut_lens) # Draw a bar chart.

    def plot_custom_length_distribution(lengths, avg_shortcut_lens):
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_ylim(0, max(lengths) + 500)

        labels = ['(0, 1]', '(1, 5]', '(5, 15]', '(15, 30]', '>30']
        colors = ['blue', 'green', 'orange', 'red', 'purple']
        hatch_patterns = ['/', '\\', '|', '-', '+']

        bars = []
        for i, (count, color, hatch, avg_val) in enumerate(zip(custom_shortcut_nums, colors, hatch_patterns, avg_shortcut_lens)):
            bar = ax.bar(labels[i], count, color=color, edgecolor='black', hatch=hatch, label=labels[i])
            bars.append(bar)
            ax.text(i, count + 5, f'Cnt: {count}\nAvg: {avg_val:.2f}', ha='center', va='bottom', fontsize=14) # Annotate each bar with its count value and average value

        overall_avg = np.sum([length * avg_val for length, avg_val in zip(lengths, avg_shortcut_lens)]) / np.sum(lengths) # Calculate and annotate the overall mean
        ax.axhline(overall_avg, color='grey', linestyle='--', linewidth=1)
        ax.text(len(labels)-5, max(lengths) + 100, f'Overall Avg: {overall_avg:.2f}', color='black', ha='center', va='bottom', fontsize=14)

        first_four_bins_lengths = [length * avg_val for length, avg_val in zip(lengths[:4], avg_shortcut_lens[:4])] # Calculate and annotate the mean of the first four bins
        first_four_bins_avg = np.sum(first_four_bins_lengths) / np.sum(lengths)
        ax.axhline(first_four_bins_avg, color='black', linestyle=':', linewidth=1)
        ax.text(len(labels)-5, max(lengths) + 300, f'(0, 30] Avg: {first_four_bins_avg:.2f}', color='black', ha='center', va='bottom', fontsize=14)

        for bar, label in zip(bars, labels): # Add a legend
            bar.set_label(label)
        
        ax.legend(title='Length Ranges', fontsize=12, title_fontsize=14)
        ax.set_xlabel('# Action Sequence', fontsize=16) # Set axis labels and title with larger font sizes
        ax.set_ylabel('Frequency', fontsize=16)
        ax.set_title('Distribution of # Action Sequence', fontsize=16)
        ax.tick_params(axis='both', which='major', labelsize=14) # Set axis tick labels with larger font sizes
        ax.grid(True, which="both", ls="--") # Set y-axis to logarithmic scale
        
        plt.tight_layout()
        plt.savefig("tmp/custom_length_distribution.png")

        return fig, ax

    """ Categorize the shortcuts into 5 groups based on their length.
    custom_shortcut_nums: the number of shortcuts in each group
    avg_shortcut_lens: the average length of shortcuts in each group
    avg_shortcut2avgAPI: the average number of APIs in shortcuts in each group
    """
    custom_shortcut_nums, avg_shortcut_lens, avg_shortcut2avgAPI = [0] * 5, [0] * 5, [0] * 5
    for cur_shortcut_len, cur_API_len in zip(shortcut_lens, APIs_lens):
        if cur_shortcut_len == 0:
            continue
        if cur_shortcut_len == 1:
            custom_shortcut_nums[0] += 1
            avg_shortcut_lens[0] += cur_shortcut_len
            avg_shortcut2avgAPI[0] += cur_API_len
        elif cur_shortcut_len <= 5:
            custom_shortcut_nums[1] += 1
            avg_shortcut_lens[1] += cur_shortcut_len
            avg_shortcut2avgAPI[1] += cur_API_len
        elif cur_shortcut_len <= 15:
            custom_shortcut_nums[2] += 1
            avg_shortcut_lens[2] += cur_shortcut_len
            avg_shortcut2avgAPI[2] += cur_API_len
        elif cur_shortcut_len <= 30:
            custom_shortcut_nums[3] += 1
            avg_shortcut_lens[3] += cur_shortcut_len
            avg_shortcut2avgAPI[3] += cur_API_len
        else:
            custom_shortcut_nums[4] += 1
            avg_shortcut_lens[4] += cur_shortcut_len
            avg_shortcut2avgAPI[4] += cur_API_len
    avg_shortcut_lens = [avg_val / custom_len for avg_val, custom_len in zip(avg_shortcut_lens, custom_shortcut_nums)]
    avg_shortcut2avgAPI = [avg_val / custom_len for avg_val, custom_len in zip(avg_shortcut2avgAPI, custom_shortcut_nums)]

    print("Number of shortcuts in each group:", custom_shortcut_nums)
    print("Total number of shortcuts in the first 4 groups:", sum(custom_shortcut_nums[:4]))
    print("Total number of shortcuts in all groups:", sum(custom_shortcut_nums))
    print()

    print("Average number of APIs involved in shortcuts for each group:", avg_shortcut2avgAPI)
    first_4_group_avg_APIs = np.sum([length * avg_API for length, avg_API in zip(custom_shortcut_nums[:4], avg_shortcut2avgAPI[:4])]) / np.sum(custom_shortcut_nums[:4])
    print("Average number of APIs involved in shortcuts for the first 4 groups:", first_4_group_avg_APIs)
    all_avg_APIs = np.sum([length * avg_API for length, avg_API in zip(custom_shortcut_nums, avg_shortcut2avgAPI)]) / np.sum(custom_shortcut_nums)
    print("Average number of APIs involved in shortcuts for all groups:", all_avg_APIs)
    print()

    print("Average length of shortcuts for each group:", avg_shortcut_lens)
    first_4_group_avg = np.sum([length * avg_val for length, avg_val in zip(custom_shortcut_nums[:4], avg_shortcut_lens[:4])]) / np.sum(custom_shortcut_nums[:4])
    print("Average length of shortcuts for the first 4 groups:", first_4_group_avg)
    all_avg = np.sum([length * avg_val for length, avg_val in zip(custom_shortcut_nums, avg_shortcut_lens)]) / np.sum(custom_shortcut_nums)
    print("Average length of shortcuts for all groups:", all_avg)
    print()

    fig, ax = plot_custom_length_distribution(custom_shortcut_nums, avg_shortcut_lens)

if __name__ == "__main__":

    final_detailed_records_path = os.path.join(SHORTCUT_DATA, "1_final_detailed_records_filter_apis.json")
    with open(final_detailed_records_path, "r") as rp:
        final_detailed_records = json.load(rp)

    final_detailed_records_filter_apis_leq_30 = []  # List of shortcuts with a length of 30 or less
    shortcut2len = {}  # Dictionary mapping each shortcut's iCloud URL to its length
    shortcut2avgAPIs = {}  # Dictionary mapping each shortcut's iCloud URL to its average number of unique APIs
    for i, cur_shortcut in enumerate(final_detailed_records):
        URL = cur_shortcut["URL"]
        shortcut = cur_shortcut["shortcut"]
        if shortcut is None:
            continue
        WFWorkflowActions = shortcut["WFWorkflowActions"]
        WFWorkflowActions_len = cal_WFWorkflowActions_len(WFWorkflowActions, URL) # Calculate the length of the shortcut
        avgAPIs = cal_WFWorkflowActions_unique_apis_num(WFWorkflowActions) # Calculate the average number of unique APIs in the shortcut
        if WFWorkflowActions_len > 0 and WFWorkflowActions_len <= 30:
            final_detailed_records_filter_apis_leq_30.append(cur_shortcut)
        shortcut2len[URL] = WFWorkflowActions_len
        shortcut2avgAPIs[URL] = avgAPIs

    """save the final_detailed_records_filter_apis_leq_30 to a json file"""
    with open(os.path.join(SHORTCUT_DATA, "1_final_detailed_records_filter_apis_leq_30.json"), "w") as wp:
        json.dump(final_detailed_records_filter_apis_leq_30, wp, indent=4, ensure_ascii=False)
    
    useless_data_analysis(shortcut2len, shortcut2avgAPIs) # Draw the distribution of the number of action sequences in the shortcuts
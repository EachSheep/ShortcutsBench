import matplotlib.pyplot as plt
import numpy as np
import os
import tiktoken
import json
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from generate_shortcut_desc import get_all_shortcuts_paras_that_is_necessary_in_query

from all_experiments import get_all_api_info

from all_experiments import evaluate_experiment
from all_experiments import evaluate_experiment2_basic_para
from all_experiments import evaluate_experiment2_return_para
from all_experiments import evaluate_experiment3

SHORTCUT_DATA = os.getenv("SHORTCUT_DATA")

model_names = [
    'gemini-1.5-pro',
    'qwen2-72b-instruct',
    'deepseek-chat',
    'deepseek-coder',
    'meta-llama/Llama-3-70b-chat-hf',
    'gemini-1.5-flash',
    'qwen2-57b-a14b-instruct',
    "gpt-4o-mini",
    "gpt-3.5-turbo",
    'GLM-4-Air',
]

exchange_rate = 7.1151
modelname2price = {
    'gemini-1.5-pro': [3.5, 10.5],
    'qwen2-72b-instruct': [5/exchange_rate, 10/exchange_rate],
    'deepseek-chat': [0.14, 0.28],
    'deepseek-coder': [0.14, 0.28],
    'meta-llama/Llama-3-70b-chat-hf': [0., 0.],
    'gemini-1.5-flash': [0.35, 1.05],
    'qwen2-57b-a14b-instruct': [3.5/exchange_rate, 7/exchange_rate],
    "gpt-4o-mini": [0.15, 0.6],
    "gpt-3.5-turbo": [0.5, 1.5],
    'GLM-4-Air': [1/exchange_rate, 1/exchange_rate],
}

categories = {
    1: "Productivity & Utilities",
    2: "Health & Fitness",
    3: "Entertainment & Media",
    4: "Lifestyle & Social",
    5: "Education & Reference",
    6: "Business & Finance",
    7: "Development & API",
    8: "Home & Smart Devices"
}

if __name__ =="__main__":

    all_api2info, all_api2paraname2paratype = get_all_api_info()
    final_detailed_records_path = os.path.join(
        SHORTCUT_DATA, "1_final_detailed_records_filter_apis_leq_30.json")
    with open(final_detailed_records_path, "r") as rp:
        final_detailed_records = json.load(rp)
    new_final_detailed_records = {}
    for i, cur_detailed_record in enumerate(final_detailed_records):
        URL = cur_detailed_record["URL"]
        shortcut = cur_detailed_record["shortcut"]
        if shortcut is None:
            continue
        new_final_detailed_records[URL] = cur_detailed_record
    final_detailed_records = new_final_detailed_records
    del new_final_detailed_records

    # Count all categories.
    # all_categories = set()
    # for cur_detailed_record in final_detailed_records.values():
    #     CategoriesInStore = cur_detailed_record["CategoryInStore"]
    #     for cur_category in CategoriesInStore:
    #         all_categories.add(cur_category)
    # print(f"All categories: {all_categories}")
    # exit(0)

    """"Mapping from shortcuts to action positions to parameter names."""
    all_shortcuts_paras_that_is_necessary_in_query = get_all_shortcuts_paras_that_is_necessary_in_query(
        list(final_detailed_records.values()), all_api2paraname2paratype)
    check_intersection_of_query_and_para_necessary_path = os.path.join(
        SHORTCUT_DATA, "json-gpt-3.5-turbo_check_intersection_of_query_and_para_necessary.json")
    with open(check_intersection_of_query_and_para_necessary_path, "r") as f:
        check_intersection_of_query_and_para_necessary = json.load(f)
    print(f"Number of necessary parameters, including String type: {len(all_shortcuts_paras_that_is_necessary_in_query)}, \
          Number of shortcuts excluding String type: {len(check_intersection_of_query_and_para_necessary)}")


    experiments1_res, experiments2_basic_para_res, experiments2_ret_val_res, experiments3_res = [], [], [], []
    experiments1_categories_res = []
    return_para_all_nums = []

    final_correct_num_every_len_level2s, final_all_num_every_len_level2s = [], []
    final_correct_num_every_len_level3s, final_all_num_every_len_level3s = [], []
    final_correct_num_every_len_level4s, final_all_num_every_len_level4s = [], []

    correct_num_api_nums, all_num_api_nums = [], []

    hall_numerators, percentage_numerators, percentage_denominators = [], [], []

    return_para_nopred_nums, return_para_formaterror_nums, return_para_chooseerror_nums = [], [], []

    system_para_ExtensionInput_correct_nums, system_para_CurrentDate_correct_nums, system_para_Clipboard_correct_nums, \
        system_para_DeviceDetails_correct_nums, system_para_Ask_correct_nums = [], [], [], [], []
    system_para_ExtensionInput_nums, system_para_CurrentDate_nums, system_para_Clipboard_nums, \
        system_para_DeviceDetails_nums, system_para_Ask_nums = [], [], [], [], []
    for MODEL_NAME in model_names:
        print(f"Processing model: {MODEL_NAME}")
        # In `MODEL_NAME`, slashes (/) will be replaced with underscores (_).
        path_model_name = MODEL_NAME.replace("/", "_")
        res_path = os.path.join(SHORTCUT_DATA, f"experiment_res_{path_model_name}.jsonl")
        already_processed_shortcuts_list = []  # Final saved experimental results
        if os.path.exists(res_path):
            with open(res_path, "r") as f:
                already_processed_shortcuts_list = [
                    json.loads(line) for line in f.readlines()]
        already_processed_shortcuts_set = set(
            [res["URL"] for res in already_processed_shortcuts_list])  # Processed shortcuts will not be reprocessed.

        def num_tokens_from_string(string: str, encoding_name: str) -> int:
            encoding = tiktoken.get_encoding(encoding_name)
            num_tokens = len(encoding.encode(string))
            return num_tokens

        correct_num, all_num, correct_num_list, all_num_list, categories_correct_num, categorys_all_num, \
            correct_num_every_len_level2, all_num_every_len_level2, \
            correct_num_every_len_level3, all_num_every_len_level3, \
            correct_num_every_len_level4, all_num_every_len_level4, \
                correct_num_api_num, all_num_api_num, \
                    hall_numerator, percentage_numerator, percentage_denominator = \
            evaluate_experiment(already_processed_shortcuts_list, print_or_not = False)
        experiments1_res.append([f"{cur_correct_num / cur_all_num * 100:.2f}" if cur_all_num else "inf" for cur_correct_num, cur_all_num in zip(correct_num_list, all_num_list)])
        experiments1_res[-1].append(f"{correct_num / all_num * 100:.2f}")
        experiments1_categories_res.append([f"{cur_correct_num / cur_all_num * 100:.2f}" if cur_all_num else "inf" for cur_correct_num, cur_all_num in zip(categories_correct_num, categorys_all_num)])
        
        final_correct_num_every_len_level2s.append(correct_num_every_len_level2)
        final_all_num_every_len_level2s.append(all_num_every_len_level2)
        final_correct_num_every_len_level3s.append(correct_num_every_len_level3)
        final_all_num_every_len_level3s.append(all_num_every_len_level3)
        final_correct_num_every_len_level4s.append(correct_num_every_len_level4)
        final_all_num_every_len_level4s.append(all_num_every_len_level4)

        correct_num_api_nums.append(correct_num_api_num)
        all_num_api_nums.append(all_num_api_num)

        hall_numerators.append(hall_numerator)
        percentage_numerators.append(percentage_numerator)
        percentage_denominators.append(percentage_denominator)
        
        para_correct_num, para_all_num, para_correct_num_list, para_all_num_list = \
            evaluate_experiment2_basic_para(already_processed_shortcuts_list, 
                                            all_shortcuts_paras_that_is_necessary_in_query, 
                                            check_intersection_of_query_and_para_necessary,
                                            print_or_not = False)
        experiments2_basic_para_res.append([f"{cur_correct_num / cur_all_num * 100:.2f}" if cur_all_num else "inf" for cur_correct_num, cur_all_num in zip(para_correct_num_list, para_all_num_list)])
        experiments2_basic_para_res[-1].append(f"{para_correct_num / para_all_num * 100:.2f}")
        
        return_para_correct_num, return_para_all_num, return_para_correct_num_list, return_para_all_num_list, \
            return_para_nopred_num_list, return_para_formaterror_num_list, return_para_chooseerror_num_list  = \
                evaluate_experiment2_return_para(already_processed_shortcuts_list, print_or_not = False)
        experiments2_ret_val_res.append([f"{cur_correct_num / cur_all_num * 100:.2f}" if cur_all_num else "inf" for cur_correct_num, cur_all_num in zip(return_para_correct_num_list[1:], return_para_all_num_list[1:])])
        experiments2_ret_val_res[-1].append(f"{return_para_correct_num / return_para_all_num * 100:.2f}")
        return_para_all_nums.append(return_para_all_num)
        return_para_nopred_nums.append(sum(return_para_nopred_num_list))
        return_para_formaterror_nums.append(sum(return_para_formaterror_num_list))
        return_para_chooseerror_nums.append(sum(return_para_chooseerror_num_list))

        system_para_correct_num, system_para_all_num, system_para_correct_num_list, system_para_all_num_list, \
            system_para_ExtensionInput_num, system_para_CurrentDate_num, system_para_Clipboard_num, \
            system_para_DeviceDetails_num, system_para_Ask_num, \
            system_para_ExtensionInput_correct_num, system_para_CurrentDate_correct_num, system_para_Clipboard_correct_num, \
            system_para_DeviceDetails_correct_num, system_para_Ask_correct_num = \
            evaluate_experiment3(already_processed_shortcuts_list, print_or_not = False)
        experiments3_res.append([f"{cur_correct_num / cur_all_num * 100:.2f}" if cur_all_num else "inf" for cur_correct_num, cur_all_num in zip(system_para_correct_num_list, system_para_all_num_list)])
        experiments3_res[-1].append(f"{system_para_correct_num / system_para_all_num * 100:.2f}")

        system_para_ExtensionInput_correct_nums.append(system_para_ExtensionInput_correct_num)
        system_para_CurrentDate_correct_nums.append(system_para_CurrentDate_correct_num)
        system_para_Clipboard_correct_nums.append(system_para_Clipboard_correct_num)
        system_para_DeviceDetails_correct_nums.append(system_para_DeviceDetails_correct_num)
        system_para_Ask_correct_nums.append(system_para_Ask_correct_num)

        system_para_ExtensionInput_nums.append(system_para_ExtensionInput_num)
        system_para_CurrentDate_nums.append(system_para_CurrentDate_num)
        system_para_Clipboard_nums.append(system_para_Clipboard_num)
        system_para_DeviceDetails_nums.append(system_para_DeviceDetails_num)
        system_para_Ask_nums.append(system_para_Ask_num)

    experiments1_res = np.array(experiments1_res).T
    experiments1_categories_res = np.array(experiments1_categories_res).T
    experiments2_basic_para_res = np.array(experiments2_basic_para_res).T
    experiments2_ret_val_res = np.array(experiments2_ret_val_res).T
    experiments3_res = np.array(experiments3_res).T

    return_para_nopred_accs = [return_para_nopred_num / return_para_all_num * 100 if return_para_all_num else 0 for return_para_nopred_num, return_para_all_num in zip(return_para_nopred_nums, return_para_all_nums)]
    return_para_formaterror_accs = [return_para_formaterror_num / return_para_all_num * 100 if return_para_all_num else 0 for return_para_formaterror_num, return_para_all_num in zip(return_para_formaterror_nums, return_para_all_nums)]
    return_para_chooseerror_accs = [return_para_chooseerror_num / return_para_all_num * 100 if return_para_all_num else 0 for return_para_chooseerror_num, return_para_all_num in zip(return_para_chooseerror_nums, return_para_all_nums)]

    print("experiments1_res:")
    print(experiments1_res)
    print()

    # The average decrease from (0,1] to (1,5].
    avg_drop_ratio = (np.mean([float(cur_val) for cur_val in experiments1_res[1]]) - np.mean([float(cur_val) for cur_val in experiments1_res[0]])) / np.mean([float(cur_val) for cur_val in experiments1_res[0]])
    print(f"The average decrease from (0,1] to (1,5]: {avg_drop_ratio:.2f}")
    min_drop_ratio = np.max([(float(cur_val) - float(experiments1_res[0][i])) / float(experiments1_res[0][i]) for i, cur_val in enumerate(experiments1_res[1])]) # Negative number
    min_drop_ratio_index = np.argmax([(float(cur_val) - float(experiments1_res[0][i])) / float(experiments1_res[0][i]) for i, cur_val in enumerate(experiments1_res[1])])
    print(f"The minimum drop from (0,1] to (1,5] is {min_drop_ratio:.2f}, corresponding to the model {model_names[min_drop_ratio_index]}.")
    max_drop_ratio = np.min([(float(cur_val) - float(experiments1_res[0][i])) / float(experiments1_res[0][i]) for i, cur_val in enumerate(experiments1_res[1])])
    max_drop_ratio_index = np.argmin([(float(cur_val) - float(experiments1_res[0][i])) / float(experiments1_res[0][i]) for i, cur_val in enumerate(experiments1_res[1])])
    print(f"The maximum drop from (0,1] to (1,5] is {max_drop_ratio:.2f}, corresponding to the model {model_names[max_drop_ratio_index]}.")
    # Average decrease from (0,1] to (5,15].
    avg_drop_ratio = (np.mean([float(cur_val) for cur_val in experiments1_res[2]]) - np.mean([float(cur_val) for cur_val in experiments1_res[0]])) / np.mean([float(cur_val) for cur_val in experiments1_res[0]])
    print(f"Average decrease from (0,1] to (5,15]: {avg_drop_ratio:.2f}")
    min_drop_ratio = np.max([(float(cur_val) - float(experiments1_res[0][i])) / float(experiments1_res[0][i]) for i, cur_val in enumerate(experiments1_res[2])])
    min_drop_ratio_index = np.argmax([(float(cur_val) - float(experiments1_res[0][i])) / float(experiments1_res[0][i]) for i, cur_val in enumerate(experiments1_res[2])])
    print(f"Minimum drop from (0,1] to (5,15] is {min_drop_ratio:.2f}, corresponding to the model {model_names[min_drop_ratio_index]}")
    max_drop_ratio = np.min([(float(cur_val) - float(experiments1_res[0][i])) / float(experiments1_res[0][i]) for i, cur_val in enumerate(experiments1_res[2])])
    max_drop_ratio_index = np.argmin([(float(cur_val) - float(experiments1_res[0][i])) / float(experiments1_res[0][i]) for i, cur_val in enumerate(experiments1_res[2])])
    print(f"Maximum drop from (0,1] to (5,15] is {max_drop_ratio:.2f}, corresponding to the model {model_names[max_drop_ratio_index]}")
    
    # Create a bar chart.
    experiments1_res_data = {
        'Model': [
            'Gemini\n1.5-Pro',
            'QWen\n2-72B', 
            'Deepseek\n2-chat', 
            'Deepseek\n2-coder', 
            'LLaMA\n3-70B', 
            'Gemini\n1.5-Flash',
            'QWen\n2-57B',
            'GPT\n4o-mini',
            'GPT\n3.5-turbo',
            'ChatGLM\n4-Air',
        ],
        '(0,1]': [float(cur_val) for cur_val in experiments1_res[0]],
        '(1,5]': [float(cur_val) for cur_val in experiments1_res[1]],
        '(5,15]': [float(cur_val) for cur_val in experiments1_res[2]],
        '(15,30]': [float(cur_val) for cur_val in experiments1_res[3]]
    }
    df = pd.DataFrame(experiments1_res_data)    
    fig, ax = plt.subplots(figsize=(12, 6)) # Plotting the bar chart
    bar_width = 0.8
    df.plot(x='Model', kind='bar', stacked=False, ax=ax, color=['#A5DF87', '#19a39f', '#4BA5E2', '#123E78'], width=bar_width)
    df = pd.DataFrame(experiments1_res_data)
    overall = [float(cur_val) for cur_val in experiments1_res[4]]
    ax.plot(df['Model'], overall, marker='o', color='r', linewidth=2, label='Overall') # Plot a line chart.
    # ax.set_title('API Selection Accuracy for Different Models', fontsize=22)
    # ax.set_xlabel('Different API-based Agent', fontsize=20)
    ax.set_xlabel('')
    ax.set_ylabel('API Selection Accuracy (%)', fontsize=20)
    ax.set_ylim(0, 100)
    ax.tick_params(axis='x', labelsize=18) # Adjusting tick label font sizes
    ax.tick_params(axis='y', labelsize=18, rotation=45)
    ax.xaxis.set_tick_params(rotation=45) # Rotate y-axis tick labels
    ax.legend(title='', bbox_to_anchor=(0.5, 0.99), loc='center', ncol=5, fontsize=18)
    ax.grid(axis='y', linestyle='--', linewidth=0.7)
    plt.tight_layout()

    # for i, model in enumerate(model_names):
    #     price_in, price_out = modelname2price[model]
    #     if price_in == 0 and price_out == 0:
    #         ax.text(i, max(df.iloc[:, 1:].max()), f'(unk, unk)', ha='center', va='bottom', fontsize=14)
    #     else:
    #         ax.text(i, max(df.iloc[:, 1:].max()), f'(${price_in:.2f}, ${price_out:.2f})', ha='center', va='bottom', fontsize=14)

    save_path = os.path.join(SHORTCUT_DATA, "experiment_res.pdf")
    plt.savefig(save_path)

    # Create a bar chart for each category.
    df = pd.DataFrame(experiments1_res_data)
    fig, axs = plt.subplots(2, 4, figsize=(24, 8))
    bar_labels, bar_handles = [], []
    for i, category in enumerate(categories.values()):
        cur_row = i // 4
        cur_col = i % 4
        cur_ax = axs[cur_row][cur_col]
        cur_data = {
            'Model': [
                'Gemini\n1.5-Pro',
                'QWen\n2-72B',
                'Deepseek\n2-chat', 
                'Deepseek\n2-coder', 
                'LLaMA\n3-70B',
                'Gemini\n1.5-Flash',
                'QWen\n2-57B',
                'GPT\n4o-mini',
                'GPT\n3.5-turbo',
                'ChatGLM\n4-Air',
            ],
            category: [float(cur_val) for cur_val in experiments1_categories_res[i]]
        }
        df = pd.DataFrame(cur_data)

        # Define rainbow colors for each model
        rainbow_colors = ['#d6efb3', '#b2e1b6', '#7ecdbb', '#52bcc2', '#31a5c2', '#1e8abd', '#2165ab', '#24459c', '#1c2d81', '#081d58']

        bar_width = 0.8
        # df.plot(x='Model', kind='bar', stacked=False, ax=cur_ax, color='#A5DF87', width=bar_width, legend=False)
        
        # Create the bar plot with different colors for each model
        for j, model in enumerate(df['Model']):
            bar = cur_ax.bar(model, df[category][j], color=rainbow_colors[j], width=bar_width)
            if i == 0:  # Collect legend handles and labels only in the first subplot.
                bar_handles.append(bar)
                bar_labels.append(model)
        
        filtered_values = df[category].replace([np.inf, -np.inf], np.nan).dropna()
        
        # Calculate mean and standard deviation
        mean_val = filtered_values.mean()
        std_val = filtered_values.std()
        # Add mean and standard deviation text
        cur_ax.axhline(mean_val, color='red', linestyle='--', linewidth=2)
        cur_ax.text(2, mean_val + 3, f'Mean: {mean_val:.2f}', color='red', fontsize=20, ha='center')
        cur_ax.text(2, mean_val - 8, f'Std: {std_val:.2f}', color='red', fontsize=20, ha='center')

        if cur_col == 0:
            cur_ax.set_ylabel('API Selection Accuracy (%)', fontsize=24)
        cur_ax.set_ylim(0, 100)
        cur_ax.tick_params(axis='x', labelsize=14) # Adjusting tick label font sizes
        

        cur_ax.tick_params(axis='y', labelsize=18)
        # cur_ax.xaxis.set_tick_params(rotation=75) # Rotate y-axis tick labels
        # cur_ax.legend(title='', bbox_to_anchor=(0.5, 1.1), loc='center', ncol=5, fontsize=18)
        cur_ax.grid(axis='y', linestyle='--', linewidth=0.7)
        cur_ax.set_xlabel("")
        cur_ax.set_xticklabels([])
        cur_ax.set_ylabel("")
        cur_ax.set_title(category, fontsize=22)
    
    # Add a unified y-axis label.
    fig.text(0, 0.5, 'API Selection Accuracy (%)', va='center', rotation='vertical', fontsize=24)
    # Add a unified legend.
    handles, labels = cur_ax.get_legend_handles_labels()
    bar_labels = ['Gemini-1.5-Pro', 'QWen-2-72B', 'Deepseek-2-chat', 'Deepseek-2-coder', 
                  'LLaMA-3-70B', 'Gemini-1.5-Flash', 'QWen-2-57B', 'GPT-4o-mini', 'GPT-3.5', 'ChatGLM-4-Air']
    fig.legend(handles=[bar[0] for bar in bar_handles], labels=bar_labels, loc='upper center', ncol=10, fontsize=16, bbox_to_anchor=(0.5, 0.999), columnspacing=0.5)
    
    plt.tight_layout(rect=[0.01, 0.01, 0.98, 0.93])
    save_path = os.path.join(SHORTCUT_DATA, "experiment_categories_res.pdf")
    plt.savefig(save_path)

    # Create a box plot.
    fig, ax = plt.subplots(figsize=(8, 5.5))

    # Create a DataFrame for plotting the box plot.
    boxplot_data = []
    models = [
        'Gemini\n1.5-Pro', 
        'QWen\n2-72B', 
        'Deepseek\n2-chat', 
        'Deepseek\n2-coder', 
        'LLaMA\n3-70B',
        'Gemini\n1.5-Flash',
        'QWen\n2-57B',
        'GPT\n4o-mini',
        'GPT\n3.5-turbo',
        'ChatGLM\n4-Air',
    ]
    rainbow_colors = ['#d6efb3', '#b2e1b6', '#7ecdbb', '#52bcc2', '#31a5c2', '#1e8abd', '#2165ab', '#24459c', '#1c2d81', '#081d58']

    for model in models:
        model_data = []
        for i, category in enumerate(categories.values()):
            cur_data = {
                'Model': models,
                category: [float(cur_val) for cur_val in experiments1_categories_res[i]]
            }
            df = pd.DataFrame(cur_data)
            model_value = df[df['Model'] == model][category].values[0]
            if np.isinf(model_value) or pd.isnull(model_value):
                # Ignore `inf` or `null` values when calculating the average.
                cleaned_category = df[category].replace([np.inf, -np.inf], np.nan)
                cleaned_category = cleaned_category.dropna()
                model_value = cleaned_category.mean()  # Replace `inf` or `null` values with the average.
            model_data.append(model_value)
        boxplot_data.append(model_data)

    # Plot a box plot.
    box = ax.boxplot(boxplot_data, patch_artist=True, boxprops=dict(facecolor='lightblue'), whis=4, widths=0.8)
    # Set the colors for the box plot.
    for patch, color in zip(box['boxes'], rainbow_colors):
        patch.set_facecolor(color)

    # Annotate the box plot with maximum values, minimum values, and medians.
    max_vals, min_vals = [], []
    for i, data in enumerate(boxplot_data):
        stats = pd.Series(data).describe()
        min_val = stats['min']
        # median_val = stats['50%']
        max_val = stats['max']
        ax.text(i + 0.8, min_val - 5, f'{min_val:.2f}', color='red', fontsize=12)
        ax.text(i + 0.8, max_val + 2, f'{max_val:.2f}', color='red', fontsize=12)

        max_vals.append(max_val)
        min_vals.append(min_val)
    diffs = [max_val - min_val for max_val, min_val in zip(max_vals, min_vals)]
    # Maximum difference
    max_diff = np.max(diffs)
    # Minimum difference
    min_diff = np.min(diffs)
    print("Max difference:", max_diff)
    print("Model with maximum difference:", models[np.argmax(diffs)])
    print("Min difference:", min_diff)
    print("Model with minimum difference:", models[np.argmin(diffs)])

    ax.set_xticks(range(1, len(models) + 1))
    ax.set_xticklabels(models, rotation=45, ha='center', fontsize=16)
    ax.tick_params(axis='y', labelsize=18)
    ax.set_ylim(0, 100)
    ax.set_ylabel('API Selection Accuracy (%)', fontsize=20)
    # ax.set_title('Box Plot of API Selection Accuracy by Model', fontsize=22)
    ax.grid(axis='y', linestyle='--', linewidth=0.7)

    plt.tight_layout()
    save_path = os.path.join(SHORTCUT_DATA, "experiment_models_boxplot.pdf")
    plt.savefig(save_path)

    print("experiments2_basic_para_res:")
    print(experiments2_basic_para_res)
    print()
    print("experiments2_ret_val_res:")
    print(experiments2_ret_val_res)
    print()
    models = [
        'Gemini\n1.5-Pro', 
        'QWen\n2-72B', 
        'Deepseek\n2-chat', 
        'Deepseek\n2-coder', 
        'LLaMA\n3-70B',
        'Gemini\n1.5-Flash',
        'QWen\n2-57B',
        'GPT\n4o-mini',
        'GPT\n3.5-turbo',
        'ChatGLM\n4-Air',
    ]
    experiments2_basic_para_res = np.array(experiments2_basic_para_res).astype(float)
    experiments2_ret_val_res = np.array(experiments2_ret_val_res).astype(float)

    # Print the average difference between the last row (overall) of `experiments2_ret_val_res` and the last row (overall) of `experiments2_basic_para_res`.
    avg_diff = experiments2_ret_val_res[-1] - experiments2_basic_para_res[-1]
    print("Average difference between the last row (overall) of experiments2_ret_val_res and experiments2_basic_para_res:", avg_diff)

    vmin = min(experiments2_basic_para_res.min(), experiments2_ret_val_res.min())
    vmax = max(experiments2_basic_para_res.min(), experiments2_ret_val_res.max())
    # Plotting the heatmap for experiments2_basic_para_res
    fig, axs = plt.subplots(2, 1, figsize=(24, 8))

    sns.heatmap(experiments2_basic_para_res, annot=True, fmt=".2f", cmap="YlGnBu", cbar=False, cbar_kws={'label': ''}, ax=axs[0], 
                annot_kws={"size": 28}, vmin=vmin, vmax=vmax)
    # ax.set_title("Experiments Basic Para Res Heatmap", fontsize=30)
    # axs[0].set_xlabel("Different API-based agents", fontsize=28)
    axs[0].set_ylabel("Primitive Para. Fill", fontsize=28)
    axs[0].tick_params(axis='both', which='major', labelsize=28)
    axs[0].set_yticklabels(['(0,1]', '(1,5]', '(5,15]', '(15,30]', 'Overall'], fontsize=26, rotation=45)
    axs[0].set_xticklabels([])
    # cbar = axs[0].collections[0].colorbar
    # cbar.ax.tick_params(labelsize=28)
    # cbar.set_label('Percentage', fontsize=28)

    # Plotting the heatmap for experiments2_ret_val_res
    sns.heatmap(experiments2_ret_val_res, annot=True, fmt=".2f", cmap="YlGnBu", cbar=True, cbar_ax=fig.add_axes([0.94, 0.25, 0.02, 0.7]), cbar_kws={'label': ''}, ax=axs[1],
                annot_kws={"size": 28}, vmin=vmin, vmax=vmax)
    # ax.set_title("Experiments Ret Val Res Heatmap", fontsize=30)
    # axs[1].set_xlabel("Different API-based agents", fontsize=28)
    axs[1].set_xlabel("")
    axs[1].set_ylabel("Prev. Actions Fill", fontsize=24)
    axs[1].tick_params(axis='both', which='major', labelsize=26)
    axs[1].set_yticklabels(['(1,5]', '(5,15]', '(15,30]', 'Overall'], fontsize=26, rotation=45)
    axs[1].set_xticklabels(models, fontsize=30)
    cbar = axs[1].collections[0].colorbar
    cbar.ax.tick_params(labelsize=26)
    # cbar.set_label('Percentage', fontsize=28)

    # fig.text(0, 0.5, 'Different Difficulty Level', va='center', rotation='vertical', fontsize=28)

    plt.tight_layout(rect=[0, 0, 0.92, 1])
    # plt.tight_layout(rect=[0, 0, 1.1, 1])
    save_path = os.path.join(SHORTCUT_DATA, "experiment_combined_heatmaps.pdf")
    plt.savefig(save_path)

    # The x-axis represents the models, and the y-axis represents the error rates. 
    # There are three types of errors: unpredicted parameters, incorrectly formatted parameters, 
    # and incorrect parameter choices. Each error type is represented by a separate line.
    num_api_nums = {
        'Model': [
            'Gemini\n1.5-Pro',
            'QWen\n2-72B',
            'Deepseek\n2-chat', 
            'Deepseek\n2-coder', 
            'LLaMA\n3-70B',
            'Gemini\n1.5-Flash',
            'QWen\n2-57B',
            'GPT\n4o-mini',
            'GPT\n3.5-turbo',
            'ChatGLM\n4-Air',
        ],
        'No Prediction': [float(cur_val) for cur_val in return_para_nopred_accs],
        'Format Error': [float(cur_val) for cur_val in return_para_formaterror_accs],
        'Choose Error': [float(cur_val) for cur_val in return_para_chooseerror_accs]
    }
    df = pd.DataFrame(num_api_nums)
    fig, ax = plt.subplots(figsize=(12, 3)) # Plotting the bar chart
    bar_width = 0.8
    df.plot(x='Model', kind='bar', stacked=False, ax=ax, color=['#A5DF87', '#19a39f', '#4BA5E2'], width=bar_width)
    df = pd.DataFrame(num_api_nums)
    # ax.set_xlabel('Different API-based Agents', fontsize=20)
    ax.set_xlabel('')
    ax.set_ylabel('Error Rate (%)', fontsize=16)
    ax.set_ylim(0, 20)
    ax.tick_params(axis='x', labelsize=18) # Adjusting tick label font sizes
    ax.tick_params(axis='y', labelsize=18)
    ax.xaxis.set_tick_params(rotation=25) # Rotate y-axis tick labels
    ax.legend(title='', bbox_to_anchor=(0.5, 0.99), loc='center', ncol=5, fontsize=18)
    ax.grid(axis='y', linestyle='--', linewidth=0.7)
    plt.tight_layout()
    save_path = os.path.join(SHORTCUT_DATA, "experiment_return_para_error.pdf")
    plt.savefig(save_path)

    print("experiments3_res:")
    print(experiments3_res)
    print()

    # Create a bar chart with the x-axis representing the models and the y-axis representing the error rates. The five bars represent:
    # system_para_ExtensionInput_correct_nums, system_para_CurrentDate_correct_nums, system_para_Clipboard_correct_nums, \
    #     system_para_DeviceDetails_correct_nums, system_para_Ask_correct_nums
    # system_para_ExtensionInput_nums, system_para_CurrentDate_nums, system_para_Clipboard_nums, \
    #     system_para_DeviceDetails_nums, system_para_Ask_nums

    system_para_ExtensionInput_accs = [system_para_ExtensionInput_correct_num / system_para_ExtensionInput_all_num * 100 if system_para_ExtensionInput_all_num else 0 for system_para_ExtensionInput_correct_num, system_para_ExtensionInput_all_num in zip(system_para_ExtensionInput_correct_nums, system_para_ExtensionInput_nums)]
    system_para_CurrentDate_accs = [system_para_CurrentDate_correct_num / system_para_CurrentDate_all_num * 100 if system_para_CurrentDate_all_num else 0 for system_para_CurrentDate_correct_num, system_para_CurrentDate_all_num in zip(system_para_CurrentDate_correct_nums, system_para_CurrentDate_nums)]
    system_para_Clipboard_accs = [system_para_Clipboard_correct_num / system_para_Clipboard_all_num * 100 if system_para_Clipboard_all_num else 0 for system_para_Clipboard_correct_num, system_para_Clipboard_all_num in zip(system_para_Clipboard_correct_nums, system_para_Clipboard_nums)]
    system_para_DeviceDetails_accs = [system_para_DeviceDetails_correct_num / system_para_DeviceDetails_all_num * 100 if system_para_DeviceDetails_all_num else 0 for system_para_DeviceDetails_correct_num, system_para_DeviceDetails_all_num in zip(system_para_DeviceDetails_correct_nums, system_para_DeviceDetails_nums)]
    system_para_Ask_accs = [system_para_Ask_correct_num / system_para_Ask_all_num * 100 if system_para_Ask_all_num else 0 for system_para_Ask_correct_num, system_para_Ask_all_num in zip(system_para_Ask_correct_nums, system_para_Ask_nums)]

    fig, ax = plt.subplots(figsize=(12, 6))
    system_para_res = {
        'Model': [
            'Gemini\n1.5-Pro',
            'QWen\n2-72B',
            'Deepseek\n2-chat', 
            'Deepseek\n2-coder', 
            'LLaMA\n3-70B',
            'Gemini\n1.5-Flash',
            'QWen\n2-57B',
            'GPT\n4o-mini',
            'GPT\n3.5-turbo',
            'ChatGLM\n4-Air'
        ],
        'ExtensionInput': [float(cur_val) for cur_val in system_para_ExtensionInput_accs],
        'CurrentDate': [float(cur_val) for cur_val in system_para_CurrentDate_accs],
        'Clipboard': [float(cur_val) for cur_val in system_para_Clipboard_accs],
        'DeviceDetails': [float(cur_val) for cur_val in system_para_DeviceDetails_accs],
        'Ask': [float(cur_val) for cur_val in system_para_Ask_accs]
    }
    df = pd.DataFrame(system_para_res)
    # df.plot(x='Model', kind='line', ax=ax, marker='o', linewidth=2)
    bar_width = 0.8
    df.plot(x='Model', kind='bar', stacked=False, ax=ax, color=['#A5DF87', '#19a39f', '#4BA5E2', '#123E78', '#FF0000'], width=bar_width)
    # ax.set_xlabel('Different API-based Agents', fontsize=20)
    ax.set_xlabel('')
    ax.set_ylabel('Accuracy (%)', fontsize=20)
    ax.set_ylim(0, 100)
    ax.tick_params(axis='x', labelsize=18) # Adjusting tick label font sizes
    ax.tick_params(axis='y', labelsize=18, rotation=45)
    ax.xaxis.set_tick_params(rotation=45) # Rotate y-axis tick labels
    ax.legend(title='', bbox_to_anchor=(0.5, 1.1), loc='center', ncol=5, fontsize=18)
    ax.grid(axis='y', linestyle='--', linewidth=0.7)
    plt.tight_layout()
    # save_path = os.path.join(SHORTCUT_DATA, "experiment_detailed_res.pdf")
    # plt.savefig(save_path)
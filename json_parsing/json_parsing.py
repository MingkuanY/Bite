import json

#json_file has all jsons and aggregate (send all to frontend every time)

all_jsons = {}

# Define a function to round values to 2 decimal points
def round_2(value):
    return round(value, 2)

# Define a dictionary with default percent daily values for each nutrient
dv_percentages = {
    'calories': 2000,  # Example value for calories
    'Total fat (g)': 70,
    'saturated fat (g)': 20,
    'trans fat (g)': 2,
    'Cholesterol (mg)': 300,
    'Sodium (mg)': 2300,
    'Potassium (mg)': 3500,
    'Total Carbs (g)': 300,
    'Dietary Fiber (g)': 25,
    'Sugars (g)': 50,
    'Protein (g)': 50,
    'Vitamin A (%)': 100,
    'Vitamin C (%)': 100,
    'Vitamin D (%)': 100,
    'Calcium (%)': 100,
    'Iron (%)': 100,
}

# Modify the parse_json function to include rounding and percent daily value
def parse_json(json_dict):
    
    #fix the first item dish name (remove duplicates, capitalize each word, turn list into one string)
    if len(list(set(json_dict['foodName']))) == 1:
        food_name = ' '.join(list(set(json_dict['foodName']))).title()
    else:
        food_name = ' '.join(list(set(json_dict['foodName']))).title() + ' Dish' #append the word "Dish" if more than one food detected
    json_dict['foodName'] = food_name

    parsed_data = {
        'Food Name': json_dict['foodName'],
        'Nutritional Info': {
            'Calories': {
                'quantity': round_2(json_dict['nutritional_info']['calories']),
                'unit': 'kcal',
                'percent_daily_value': round_2((json_dict['nutritional_info']['calories'] / dv_percentages['calories']) * 100)
            },
            'Total Fat': {
                'quantity': round_2(json_dict['nutritional_info']['totalNutrients']['FAT']['quantity']),
                'unit': 'g',
                'percent_daily_value': round_2((json_dict['nutritional_info']['totalNutrients']['FAT']['quantity'] / dv_percentages['Total fat (g)']) * 100)
            },
            'Saturated Fat': {
                'quantity': round_2(json_dict['nutritional_info']['totalNutrients']['FASAT']['quantity']),
                'unit': 'g',
                'percent_daily_value': round_2((json_dict['nutritional_info']['totalNutrients']['FASAT']['quantity'] / dv_percentages['saturated fat (g)']) * 100)
            },
            'Trans Fat': {
                'quantity': round_2(json_dict['nutritional_info']['totalNutrients']['FATRN']['quantity']),
                'unit': 'g',
                'percent_daily_value': round_2((json_dict['nutritional_info']['totalNutrients']['FATRN']['quantity'] / dv_percentages['trans fat (g)']) * 100)
            },
            'Cholesterol': {
                'quantity': round_2(json_dict['nutritional_info']['totalNutrients']['CHOLE']['quantity']),
                'unit': 'mg',
                'percent_daily_value': round_2((json_dict['nutritional_info']['totalNutrients']['CHOLE']['quantity'] / dv_percentages['Cholesterol (mg)']) * 100)
            },
            'Sodium': {
                'quantity': round_2(json_dict['nutritional_info']['totalNutrients']['NA']['quantity']),
                'unit': 'mg',
                'percent_daily_value': round_2((json_dict['nutritional_info']['totalNutrients']['NA']['quantity'] / dv_percentages['Sodium (mg)']) * 100)
            },
            'Potassium': {
                'quantity': round_2(json_dict['nutritional_info']['totalNutrients']['K']['quantity']),
                'unit': 'mg',
                'percent_daily_value': round_2((json_dict['nutritional_info']['totalNutrients']['K']['quantity'] / dv_percentages['Potassium (mg)']) * 100)
            },
            'Total Carbs': {
                'quantity': round_2(json_dict['nutritional_info']['totalNutrients']['CHOCDF']['quantity']),
                'unit': 'g',
                'percent_daily_value': round_2((json_dict['nutritional_info']['totalNutrients']['CHOCDF']['quantity'] / dv_percentages['Total Carbs (g)']) * 100)
            },
            'Dietary Fiber': {
                'quantity': round_2(json_dict['nutritional_info']['totalNutrients']['FIBTG']['quantity']),
                'unit': 'g',
                'percent_daily_value': round_2((json_dict['nutritional_info']['totalNutrients']['FIBTG']['quantity'] / dv_percentages['Dietary Fiber (g)']) * 100)
            },
            'Sugars': {
                'quantity': round_2(json_dict['nutritional_info']['totalNutrients']['SUGAR']['quantity']),
                'unit': 'g',
                'percent_daily_value': round_2((json_dict['nutritional_info']['totalNutrients']['SUGAR']['quantity'] / dv_percentages['Sugars (g)']) * 100)
            },
            'Protein': {
                'quantity': round_2(json_dict['nutritional_info']['totalNutrients']['PROCNT']['quantity']),
                'unit': 'g',
                'percent_daily_value': round_2((json_dict['nutritional_info']['totalNutrients']['PROCNT']['quantity'] / dv_percentages['Protein (g)']) * 100)
            },
            'Vitamin A': {
                'quantity': round_2(json_dict['nutritional_info']['totalNutrients']['VITA_RAE']['quantity']),
                'unit': '%'
            },
            'Vitamin C': {
                'quantity': round_2(json_dict['nutritional_info']['totalNutrients']['VITC']['quantity']),
                'unit': '%'
            },
            'Vitamin D': {
                'quantity': round_2(json_dict['nutritional_info']['totalNutrients']['VITD']['quantity']),
                'unit': '%'
            },
            'Calcium': {
                'quantity': round_2(json_dict['nutritional_info']['totalNutrients']['CA']['quantity']),
                'unit': '%'
            },
            'Iron': {
                'quantity': round_2(json_dict['nutritional_info']['totalNutrients']['FE']['quantity']),
                'unit': '%'
            },
        }
    }
    
    with open('json_file.jsonl', 'a') as file:
        file.write(parsed_data + "\n", file, indent=4)
    
    return parsed_data

def update_aggregate(json_dict): #adds the given json_dict to the aggregate values
    with open('dump_file.json', 'r') as file:
        aggregate_dict = json.load(file)
    
    #adds dump file and preexisting aggregate file vals together
    aggregate_data = {
        'Food Name': aggregate_dict['Food Name'] + [json_dict['Food Name']],
        'Nutritional Info': {
            'Calories': {
                'quantity': round_2(json_dict['Nutritional Info']['Calories']['quantity'] + aggregate_dict['Nutritional Info']['Calories']['quantity']),
                'unit': 'kcal',
                'percent_daily_value': (round_2((json_dict['Nutritional Info']['Calories']['quantity'] + aggregate_dict['Nutritional Info']['Calories']['quantity']) / dv_percentages['calories']) * 100)
            },
            'Total Fat': {
                'quantity': round_2(json_dict['Nutritional Info']['Total Fat']['quantity'] + aggregate_dict['Nutritional Info']['Total Fat']['quantity']),
                'unit': 'g',
                'percent_daily_value': round_2(((json_dict['Nutritional Info']['Total Fat']['quantity'] + aggregate_dict['Nutritional Info']['Total Fat']['quantity']) / dv_percentages['Total fat (g)']) * 100)
            },
            'Saturated Fat': {
                'quantity': round_2(json_dict['Nutritional Info']['Saturated Fat']['quantity'] + aggregate_dict['Nutritional Info']['Saturated Fat']['quantity']),
                'unit': 'g',
                'percent_daily_value': round_2(((json_dict['Nutritional Info']['Saturated Fat']['quantity'] + aggregate_dict['Nutritional Info']['Saturated Fat']['quantity']) / dv_percentages['saturated fat (g)']) * 100)
            },
            'Trans Fat': {
                'quantity': round_2(json_dict['Nutritional Info']['Trans Fat']['quantity'] + aggregate_dict['Nutritional Info']['Trans Fat']['quantity']),
                'unit': 'g',
                'percent_daily_value': round_2(((round_2(json_dict['Nutritional Info']['Trans Fat']['quantity'] + aggregate_dict['Nutritional Info']['Trans Fat']['quantity'])) / dv_percentages['trans fat (g)']) * 100)
            },
            'Cholesterol': {
                'quantity': round_2(json_dict['Nutritional Info']['Cholesterol']['quantity'] + aggregate_dict['Nutritional Info']['Cholesterol']['quantity']),
                'unit': 'mg',
                'percent_daily_value': round_2(((round_2(json_dict['Nutritional Info']['Cholesterol']['quantity'] + aggregate_dict['Nutritional Info']['Cholesterol']['quantity'])) / dv_percentages['trans fat (g)']) * 100)
            },
            'Sodium': {
                'quantity': round_2(json_dict['Nutritional Info']['Sodium']['quantity'] + aggregate_dict['Nutritional Info']['Sodium']['quantity']),
                'unit': 'mg',
                'percent_daily_value': round_2(((round_2(json_dict['Nutritional Info']['Sodium']['quantity'] + aggregate_dict['Nutritional Info']['Sodium']['quantity'])) / dv_percentages['trans fat (g)']) * 100)
            },
            'Potassium': {
                'quantity': round_2(json_dict['Nutritional Info']['Potassium']['quantity'] + aggregate_dict['Nutritional Info']['Potassium']['quantity']),
                'unit': 'mg',
                'percent_daily_value': round_2(((round_2(json_dict['Nutritional Info']['Potassium']['quantity'] + aggregate_dict['Nutritional Info']['Potassium']['quantity'])) / dv_percentages['trans fat (g)']) * 100)
            },
            'Total Carbs': {
                'quantity': round_2(json_dict['Nutritional Info']['Total Carbs']['quantity'] + aggregate_dict['Nutritional Info']['Total Carbs']['quantity']),
                'unit': 'g',
                'percent_daily_value': round_2(((round_2(json_dict['Nutritional Info']['Total Carbs']['quantity'] + aggregate_dict['Nutritional Info']['Total Carbs']['quantity'])) / dv_percentages['trans fat (g)']) * 100)
            },
            'Dietary Fiber': {
                'quantity': round_2(json_dict['Nutritional Info']['Dietary Fiber']['quantity'] + aggregate_dict['Nutritional Info']['Dietary Fiber']['quantity']),
                'unit': 'g',
                'percent_daily_value': round_2(((round_2(json_dict['Nutritional Info']['Dietary Fiber']['quantity'] + aggregate_dict['Nutritional Info']['Dietary Fiber']['quantity'])) / dv_percentages['trans fat (g)']) * 100)
            },
            'Sugars': {
                'quantity': round_2(json_dict['Nutritional Info']['Sugars']['quantity'] + aggregate_dict['Nutritional Info']['Sugars']['quantity']),
                'unit': 'g',
                'percent_daily_value': round_2(((round_2(json_dict['Nutritional Info']['Sugars']['quantity'] + aggregate_dict['Nutritional Info']['Sugars']['quantity'])) / dv_percentages['trans fat (g)']) * 100)
            },
            'Protein': {
                'quantity': round_2(json_dict['Nutritional Info']['Protein']['quantity'] + aggregate_dict['Nutritional Info']['Protein']['quantity']),
                'unit': 'g',
                'percent_daily_value': round_2(((round_2(json_dict['Nutritional Info']['Protein']['quantity'] + aggregate_dict['Nutritional Info']['Protein']['quantity'])) / dv_percentages['trans fat (g)']) * 100)
            },
            'Vitamin A': {
                'quantity': round_2(json_dict['Nutritional Info']['Vitamin A']['quantity'] + aggregate_dict['Nutritional Info']['Vitamin A']['quantity']),
                'unit': '%'
            },
            'Vitamin C': {
                'quantity': round_2(json_dict['Nutritional Info']['Vitamin C']['quantity'] + aggregate_dict['Nutritional Info']['Vitamin C']['quantity']),
                'unit': '%'
            },
            'Vitamin D': {
                'quantity': round_2(json_dict['Nutritional Info']['Vitamin D']['quantity'] + aggregate_dict['Nutritional Info']['Vitamin D']['quantity']),
                'unit': '%'
            },
            'Calcium': {
                'quantity': round_2(json_dict['Nutritional Info']['Calcium']['quantity'] + aggregate_dict['Nutritional Info']['Calcium']['quantity']),
                'unit': '%'
            },
            'Iron': {
                'quantity': round_2(json_dict['Nutritional Info']['Iron']['quantity'] + aggregate_dict['Nutritional Info']['Iron']['quantity']),
                'unit': '%'
            },
        }
    }
    
    with open('aggregate_file.json', 'w') as file:
        json.dump(aggregate_data, file, indent=4)
    
    return aggregate_data


def clear_aggregate(): #clears aggregate, food names list cleared and all values set to 0    
    aggregate_data = {
        'Food Name': [],
        'Nutritional Info': {
            'Calories': {
                'quantity': 0,
                'unit': 'kcal',
                'percent_daily_value': 0
            },
            'Total Fat': {
                'quantity': 0,
                'unit': 'g',
                'percent_daily_value': 0
            },
            'Saturated Fat': {
                'quantity': 0,
                'unit': 'g',
                'percent_daily_value': 0
            },
            'Trans Fat': {
                'quantity': 0,
                'unit': 'g',
                'percent_daily_value': 0
            },
            'Cholesterol': {
                'quantity': 0,
                'unit': 'mg',
                'percent_daily_value': 0
            },
            'Sodium': {
                'quantity': 0,
                'unit': 'mg',
                'percent_daily_value': 0
            },
            'Potassium': {
                'quantity': 0,
                'percent_daily_value': 0
            },
            'Total Carbs': {
                'quantity': 0,
                'unit': 'g',
                'percent_daily_value': 0
            },
            'Dietary Fiber': {
                'quantity': 0,
                'unit': 'g',
                'percent_daily_value': 0
            },
            'Sugars': {
                'quantity': 0,
                'unit': 'g',
                'percent_daily_value': 0
            },
            'Protein': {
                'quantity': 0,
                'unit': 'g',
                'percent_daily_value': 0
            },
            'Vitamin A': {
                'quantity': 0,
                'unit': '%'
            },
            'Vitamin C': {
                'quantity': 0,
                'unit': '%'
            },
            'Vitamin D': {
                'quantity': 0,
                'unit': '%'
            },
            'Calcium': {
                'quantity': 0,
                'unit': '%'
            },
            'Iron': {
                'quantity': 0,
                'unit': '%'
            },
        }
    }
    
    with open('aggregate_file.json', 'w') as file:
        json.dump(aggregate_data, file, indent=4)
    
    return aggregate_data




#executed code----
output = clear_aggregate()
print(output)

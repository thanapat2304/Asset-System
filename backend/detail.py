from backend.db_connection import connect_aep_portal
from mysql.connector import Error
import calendar
from collections import defaultdict

def execute_query(query, params=None):
    connection = connect_aep_portal()
    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Error executing query: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def calculate_depreciation(as_date, asset_value, as_type_id):
    try:
        asset_value = float(asset_value)
    except (ValueError, TypeError):
        raise ValueError("Asset value must be a number.")

    depreciation_data = []
    total_depreciation = 0

    type_data = {
        1: 20,
        2: 10,
        3: 15,
        4: 25,
    }
    
    if type_data:
        percent = type_data.get(as_type_id, 20) / 100
    else:
        percent = 0.2

    year = as_date.year
    while total_depreciation < asset_value:
        for month in range(1, 13):
            if total_depreciation >= asset_value:
                break

            if year == as_date.year and month < as_date.month:
                depreciation_data.append({
                    'year': year,
                    'month': month,
                    'depreciation': '-'
                })
                continue

            num_days_in_month = calendar.monthrange(year, month)[1]

            if calendar.isleap(year):
                days_in_year = 366
            else:
                days_in_year = 365

            if year == as_date.year and month == as_date.month:
                num_days_in_first_month = num_days_in_month - as_date.day + 1
                monthly_depreciation = asset_value * percent * (num_days_in_first_month / days_in_year)
                total_depreciation += monthly_depreciation
                depreciation_data.append({
                    'year': year,
                    'month': month,
                    'depreciation': monthly_depreciation
                })
                continue

            if total_depreciation + asset_value * percent * (num_days_in_month / days_in_year) > asset_value:
                if as_date.day == 1:
                    last_month_depreciation = asset_value * percent * (num_days_in_month / days_in_year) - 1
                else:
                    num_days_in_late_month = as_date.day - 1
                    last_month_depreciation = asset_value * percent * (num_days_in_late_month / days_in_year) - 1
                
                total_depreciation += last_month_depreciation
                depreciation_data.append({
                    'year': year,
                    'month': month,
                    'depreciation': last_month_depreciation
                })
                break

            monthly_depreciation = asset_value * percent * (num_days_in_month / days_in_year)
            total_depreciation += monthly_depreciation

            depreciation_data.append({
                'year': year,
                'month': month,
                'depreciation': monthly_depreciation
            })

        year += 1

    if depreciation_data:
        depreciation_data.pop()

    return depreciation_data


def group_depreciation_data_by_year(depreciation_data):
    grouped_data = defaultdict(lambda: {'months': ['-'] * 12, 'total': 0})

    for entry in depreciation_data:
        year = entry['year']
        month = entry['month'] - 1
        
        if isinstance(entry['depreciation'], (int, float)):
            depreciation_value = round(entry['depreciation'], 2)
        else:
            depreciation_value = 0
    
        grouped_data[year]['months'][month] = depreciation_value
        if isinstance(depreciation_value, (int, float)):
            grouped_data[year]['total'] += depreciation_value
    
    for year, data in grouped_data.items():
        data['total'] = round(data['total'], 2)
        data['total'] = "{:,.2f}".format(data['total'])
        
        data['months'] = [
            "{:,.2f}".format(value) if isinstance(value, (int, float)) else value
            for value in data['months']
        ]
    
    return grouped_data
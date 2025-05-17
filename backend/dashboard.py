from backend.db_connection import connect_aep_portal
import random

def fetch_COUNT_office():
    try:
        total_Succeed = random.randint(0, 20)
        formatted_Succeed = f"{total_Succeed:,}"
        return formatted_Succeed
    except Exception as e:
        print(f"Error generating mock data: {e}")
        return None

def fetch_COUNT_tool():
    try:
        total_Succeed = random.randint(0, 20)
        formatted_Succeed = f"{total_Succeed:,}"
        return formatted_Succeed
    except Exception as e:
        print(f"Error generating mock data: {e}")
        return None

def fetch_COUNT_car():
    try:
        total_Succeed = random.randint(0, 20)
        formatted_Succeed = f"{total_Succeed:,}"
        return formatted_Succeed
    except Exception as e:
        print(f"Error generating mock data: {e}")
        return None

def fetch_COUNT_tower():
    try:
        total_Succeed = random.randint(0, 10)
        formatted_Succeed = f"{total_Succeed:,}"
        return formatted_Succeed
    except Exception as e:
        print(f"Error generating mock data: {e}")
        return None

def fetch_COUNT_add():
    try:
        total_Succeed = random.randint(0, 10)
        formatted_Succeed = f"{total_Succeed:,}"
        return formatted_Succeed
    except Exception as e:
        print(f"Error generating mock data: {e}")
        return None

def fetch_COUNT_Total():
    try:
        total_Succeed = random.randint(100000, 1000000)
        formatted_Succeed = f"{total_Succeed:,}"
        return formatted_Succeed
    except Exception as e:
        print(f"Error generating mock data: {e}")
        return None

def get_topic_data():
    mock_types = ["อุปกรณ์สำนักงาน", "คอมพิวเตอร์", "เฟอร์นิเจอร์", "เครื่องใช้ไฟฟ้า", "พัสดุอื่นๆ"]

    result = []
    for as_type in mock_types:
        mock_asset_value = round(random.uniform(10000, 500000), 2)
        result.append({
            "AS_Type": as_type,
            "total_asset_value": mock_asset_value
        })

    return result

def fetch_monthly_asset_value():
    try:
        monthly_values = {i: round(random.uniform(0, 500000), 2) if random.random() > 0.2 else 0.00 for i in range(1, 13)}

        final_result = []
        for month in range(1, 13):
            final_result.append({
                'month': month,
                'total_asset_value': f"{monthly_values[month]:.2f}"
            })

        return final_result

    except Exception as e:
        print(f"Error generating mock monthly asset value: {e}")
        return []
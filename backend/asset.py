import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def get_as_tb_ms():
    try:
        mock_data = []
        branches = ["สาขากรุงเทพ", "สาขาเชียงใหม่", "สาขาขอนแก่น", "สาขาหาดใหญ่"]
        types = ["คอมพิวเตอร์", "เฟอร์นิเจอร์", "อุปกรณ์สำนักงาน", "เครื่องใช้ไฟฟ้า"]
        departments = ["บัญชี", "ไอที", "จัดซื้อ", "การตลาด"]
        users = ["สมชาย", "วราภรณ์", "นิรันดร์", "ศิริพร"]

        for i in range(20):
            as_date = datetime.now() - timedelta(days=random.randint(30, 365 * 5))
            delta = relativedelta(datetime.now().date(), as_date.date())
            usage_duration = f"{delta.years} ปี {delta.months} เดือน {delta.days} วัน"

            asset_value = round(random.uniform(10000, 300000), 2)

            row = {
                "id": i + 1,
                "Asset_Code": f"ASSET-{1000 + i}",
                "Account_Num": f"ACCT-{random.randint(1000, 9999)}",
                "YR": as_date.year,
                "Asset_Name": f"ทรัพย์สิน {i+1}",
                "AS_Date": as_date.date(),
                "Asset_Value": asset_value,
                "AS_Store": f"คลังเก็บที่ {random.randint(1, 5)}",
                "AS_Note": random.choice(["", "ใช้งานหนัก", "ต้องซ่อม", "สภาพดี"]),
                "Department": random.choice(departments),
                "AS_User": random.choice(users),
                "AS_SerialNum": f"SN-{random.randint(100000, 999999)}",
                "AS_File": None,
                "Status": random.choice(["ใช้งาน", "ชำรุด", "ขายแล้ว"]),
                "AS_Location_Name": random.choice(branches),
                "AS_Type_Name": random.choice(types),
                "Usage_Duration": usage_duration
            }

            mock_data.append(row)

        return mock_data

    except Exception as e:
        print(f"Error generating mock asset data: {e}")
        return []
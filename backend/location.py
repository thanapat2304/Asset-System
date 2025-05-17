from backend.db_connection import connect_aep_portal

def get_fda_location():
    branch_names = ["สาขากรุงเทพ", "สาขาเชียงใหม่", "สาขาภูเก็ต", "สาขาขอนแก่น", "สาขาหาดใหญ่"]
    
    sample_data = [
        {
            "AS_Name_Branch": name,
            "id": f"BR{idx}"
        }
        for idx, name in enumerate(branch_names, start=1)
    ]

    return sample_data
import pandas as pd

def get_similar_assets(asset_desc, region):
    """根据输入的设备描述和地域，从 data.csv 找类似设备"""
    df = pd.read_csv("data.csv")
    
    # 简单关键词匹配（比如识别出“数控机床”，就去匹配）
    filtered = df[df['设备类型'].str.contains(asset_desc, case=False, na=False)]
    
    # 如果指定了地域，就进一步过滤
    if region != "其他" and not filtered.empty:
        region_filtered = filtered[filtered['地域'] == region]
        if not region_filtered.empty:
            filtered = region_filtered
            
    return filtered

if __name__ == "__main__":
    # 本地测试一下
    result = get_similar_assets("数控机床", "北京")
    print(result)
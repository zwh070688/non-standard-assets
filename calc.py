def calculate_price_stats(df):
    """根据相似设备的成交价格，计算区间和置信度"""
    if df.empty:
        return None
        
    prices = df['成交价格'].tolist()
    avg_price = sum(prices) / len(prices)
    
    # 简单算个区间（最低价到最高价）
    min_price = min(prices)
    max_price = max(prices)
    
    # 置信度：只要匹配到的数据超过 2 条，就算高置信度
    if len(prices) >= 3:
        confidence = "高 (基于3条以上历史数据)"
    elif len(prices) == 2:
        confidence = "中 (基于2条历史数据)"
    else:
        confidence = "低 (仅有1条历史数据)"
        
    return {
        "平均价格": round(avg_price, 2),
        "价格区间": f"{round(min_price, 2)} ~ {round(max_price, 2)}",
        "置信度": confidence,
        "匹配数量": len(prices)
    }
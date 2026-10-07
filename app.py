import streamlit as st
import base64
from openai import OpenAI
from price import get_similar_assets
from calc import calculate_price_stats

st.set_page_config(page_title="非标资产价格发现", layout="wide")
st.title("非标资产价格发现与贷后管理系统")

st.markdown("### 1. 资产信息录入")
uploaded_file = st.file_uploader("上传设备照片", type=["jpg", "jpeg", "png"])
asset_desc = st.text_input("输入资产名称或描述（例如：数控机床、注塑机）")
region = st.selectbox("选择资产所在地域", ["北京", "上海", "广州", "深圳", "其他"])

st.markdown("### 2. 开始分析")
if st.button("开始价格发现"):
    if uploaded_file is not None:
        with st.spinner("正在识别中，请稍候……"):
           # 优先从云端配置读取Key，本地测试则在下方配置
            client = OpenAI(
            api_key=st.secrets.get("DEEPSEEK_API_KEY", "本地临时KEY"), 
            base_url="https://api.deepseek.com"
    )
            b64 = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
            
            try:
                # 1. AI 识别图片
                response = client.chat.completions.create(
                    model="deepseek-flash",
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "请描述图片中的设备，包括类型、外观特征、可能的品牌和型号。尽量简洁，如果能判断具体设备类型（例如：数控机床、注塑机），请着重说明。"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                        ],
                    }],
                )
                result = response.choices[0].message.content
                st.success("图片识别完成！")
                st.markdown("#### 🔍 AI 识别结果：")
                st.write(result)
                
                # 2. 进行价格比对与计算
                st.markdown("#### 💰 价格发现结果：")
                
                # 如果用户没有输入描述，我们尝试用 AI 结果的前几个字做简单匹配
                search_key = asset_desc if asset_desc else result[:6]
                
                similar_data = get_similar_assets(search_key, region)
                stats = calculate_price_stats(similar_data)
                
                if stats:
                    col1, col2, col3 = st.columns(3)
                    col1.metric("平均参考价", f"¥{stats['平均价格']:,}")
                    col2.metric("参考价格区间", f"¥{stats['价格区间']}")
                    col3.metric("置信度", stats['置信度'])
                    
                    with st.expander("查看历史拍卖明细"):
                        st.dataframe(similar_data)
                else:
                    st.warning("暂未找到类似设备的历史成交记录，无法给出价格参考。")
                
            except Exception as e:
                st.error(f"处理失败，报错信息：{e}")
    else:
        st.warning("请先上传一张设备照片。")

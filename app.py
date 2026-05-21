import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pykrx import stock
from datetime import datetime

# 1. 모바일 최적화 페이지 설정
st.set_page_config(
    page_title="TIMA 스타일 주도주 모니터링",
    layout="wide",
    initial_sidebar_state="collapsed",  # 모바일에서 사이드바 숨김
    menu_items=None  # 메뉴 버튼 제거
)

# CSS 모바일 최적화
st.markdown("""
    <style>
        /* 전체 여백 최소화 */
        .main {
            padding: 0 !important;
        }
        [data-testid="stMainBlockContainer"] {
            padding: 8px !important;
        }
        [data-testid="stVerticalBlock"] {
            gap: 0.5rem !important;
        }
        
        /* 카드 최적화 */
        [data-testid="stContainer"] {
            padding: 0 !important;
        }
        
        /* 텍스트 크기 최적화 */
        h1 { font-size: 18px !important; margin: 0 !important; }
        h2 { font-size: 16px !important; margin: 0 !important; }
        h3 { font-size: 14px !important; }
        
        /* 모바일 열 너비 */
        @media (max-width: 768px) {
            [data-testid="column"] {
                min-width: 100% !important;
            }
        }
    </style>
""")

# 2. 티마 감성 상단 바 (모바일 최적화)
st.markdown("""
    <div style="background: linear-gradient(135deg, #2b5f54 0%, #00a884 100%); 
                padding: 12px; border-radius: 8px; margin-bottom: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <div style="color: white; font-weight: bold; font-size: 16px; margin-bottom: 4px;">📊 TIMA 주도주</div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: rgba(255,255,255,0.9); font-size: 12px;">Premium 테마 모니터링</span>
            <span style="background-color: rgba(255,255,255,0.2); color: white; padding: 3px 8px; border-radius: 4px; font-size: 11px;"""" + datetime.today().strftime('%m-%d %H:%M') + """</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# 3. 데이터 수집 함수
@st.cache_data(ttl=60)
def get_tima_theme_data():
    url = "https://finance.naver.com/sise/theme.naver"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        
        theme_list = []
        table = soup.find("table", {"class": "type_1"})
        if table:
            rows = table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 3:
                    link = cols[0].find("a")["href"] if cols[0].find("a") else ""
                    theme_id = link.split("theme_no=")[-1] if link else ""
                    name = cols[0].text.strip()
                    try:
                        change_pct = float(cols[1].text.strip().replace('%', '').replace('+', ''))
                        if theme_id:
                            theme_list.append({"id": theme_id, "name": name, "change": change_pct})
                    except:
                        continue
        
        if not theme_list:
            return None
            
        top_themes = sorted(theme_list, key=lambda x: x['change'], reverse=True)[:4]
        
        # 최신 영업일 거래대금 가져오기
        today_str = datetime.today().strftime("%Y%m%d")
        try:
            df_vol = stock.get_market_price_change_by_ticker(today_str, today_str, "ALL")
        except:
            latest_day = stock.get_nearest_business_day_in_a_week()
            df_vol = stock.get_market_price_change_by_ticker(latest_day, latest_day, "ALL")
        
        df_vol = df_vol.reset_index()
        df_vol['종목명'] = df_vol['종목코드'].apply(lambda x: stock.get_market_ticker_name(x))
        vol_dict = df_vol.set_index('종목명')['거래대금'].to_dict()

        final_data = {}
        for t in top_themes:
            t_url = f"https://finance.naver.com/sise/theme_detail.naver?theme_no={t['id']}"
            t_res = requests.get(t_url, headers=headers, timeout=5)
            t_soup = BeautifulSoup(t_res.text, "html.parser")
            
            stocks_in_theme = []
            t_table = t_soup.find("table", {"class": "type_5"})
            if t_table:
                t_rows = t_table.find_all("tr")
                for tr in t_rows:
                    tds = tr.find_all("td", {"class": "name"})
                    if tds:
                        s_name = tds[0].text.strip()
                        tr_tds = tr.find_all("td")
                        try:
                            curr_price = tr_tds[1].text.strip().replace(',', '')
                            s_change = tr_tds[2].text.strip().replace('\n', '').replace('\t', '')
                            raw_vol = vol_dict.get(s_name, 0)
                            vol_billion = raw_vol / 100000000
                            
                            stocks_in_theme.append({
                                "name": s_name,
                                "price": int(curr_price) if curr_price.isdigit() else curr_price,
                                "change": s_change,
                                "vol": vol_billion
                            })
                        except:
                            continue
            
            final_data[t['name']] = {
                "theme_change": t['change'],
                "stocks": stocks_in_theme[:3]  # 모바일용 3개로 축소
            }
        return final_data
    except:
        return None

# 4. 화면 UI 출력 (모바일 최적화 - 세로 레이아웃)
data = get_tima_theme_data()

if data is None or len(data) == 0:
    st.info("⏰ 현재 장외 시간이거나 데이터를 가져올 수 없습니다.\n\n평일 주식 시장(09:00~15:30)에 실시간 주도주 테마가 활성화됩니다!")
else:
    theme_names = list(data.keys())
    
    for idx, name in enumerate(theme_names):
        theme_info = data[name]
        
        # 테마 헤더
        st.markdown(f"""
            <div style="background-color: #2b5f54; padding: 10px 12px; border-radius: 6px 6px 0 0; 
                        color: white; display: flex; justify-content: space-between; align-items: center; 
                        margin-top: {'16px' if idx > 0 else '0'};">
                <span style="font-weight: bold; font-size: 14px;">📌 {name}</span>
                <span style="background-color: #1dd1a1; color: white; padding: 3px 10px; 
                           border-radius: 12px; font-weight: bold; font-size: 12px;">+{theme_info['theme_change']:.1f}%</span>
            </div>
        """, unsafe_allow_html=True)
        
        # 테마 내 주식들
        with st.container(border=True):
            for i, s in enumerate(theme_info['stocks']):
                # 상승/하락 판별
                is_up = "-" not in str(s['change'])
                color = "#ff4444" if is_up else "#4444ff"
                arrow = "📈" if is_up else "📉"
                
                st.markdown(f"""
                    <div style="padding: 10px 0; {'' if i == len(theme_info['stocks'])-1 else 'border-bottom: 1px solid #e8e8e8;'}">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 10px;">
                            <div style="flex: 1; min-width: 0;">
                                <div style="font-weight: 600; font-size: 13px; color: #222; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                                    {s['name']}
                                </div>
                                <div style="font-size: 11px; color: #666; margin-top: 2px;">
                                    {s['price']:,} 원
                                </div>
                            </div>
                            <div style="text-align: right; white-space: nowrap;">
                                <div style="font-weight: 700; color: {color}; font-size: 13px;">
                                    {arrow} {s['change'].strip()}
                                </div>
                                <div style="font-size: 10px; color: #999; margin-top: 2px;">
                                    {s['vol']:,.0f}억
                                </div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("")  # 카드 간 간격

    # 하단 새로고침 버튼
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 새로고침", use_container_width=True, key="refresh_btn"):
            st.cache_data.clear()
            st.rerun()

# 푸터
st.markdown("""
    <div style="text-align: center; font-size: 10px; color: #999; margin-top: 16px; padding-top: 12px; border-top: 1px solid #e8e8e8;">
        💡 데이터는 60초마다 자동 업데이트됩니다
    </div>
""", unsafe_allow_html=True)

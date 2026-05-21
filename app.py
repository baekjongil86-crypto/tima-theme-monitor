            with grid_positions[idx]:
                theme_info = data[name]
                st.markdown(f"""
                    <div style="background-color: #2b5f54; padding: 8px 15px; border-radius: 5px 5px 0 0; color: white; display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: bold; font-size: 14px;">📌 {name}</span>
                        <span style="background-color: #e6f4ea; color: #0f9d58; padding: 2px 8px; border-radius: 4px; font-weight: bold;">+{theme_info['theme_change']}%</span>
                    </div>
                """, unsafe_allow_html=True)
                
                with st.container(border=True):
                    for s in theme_info['stocks']:
                        color = "#d93025" if "-" not in str(s['change']) else "#1967d2"
                        st.markdown(f"""
                            <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid #f0f0f0;">
                                <div>
                                    <div style="font-weight: bold; font-size: 13px; color:#333;">{s['name']}</div>
                                    <div style="font-size: 11px; color: #777;">{s['price']:,} 원</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-weight: bold; color: {color}; font-size: 13px;">{s['change'].strip()}</div>
                                    <div style="font-size: 10px; color: #999;">{s['vol']:,.0f}억</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

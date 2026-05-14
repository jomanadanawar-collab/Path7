st.markdown(f'''
<style>

@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');

* {{
    font-family: 'IBM Plex Sans Arabic', sans-serif !important;
    direction: {"rtl" if IS_AR else "ltr"};
}}

.stApp {{
    background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%);
}}

.glass-card {{
    background: white;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #E2E8F0;
    margin-bottom: 18px;
    text-align: {text_align};
}}

.dest-card {{
    background: white;
    padding: 18px;
    border-radius: 18px;
    border-{"right" if IS_AR else "left"}: 8px solid #0EA5E9;
    margin-bottom: 14px;
    text-align: {text_align};
    box-shadow: 0 3px 8px rgba(0,0,0,0.05);
}}

.map-btn {{
    background-color: #0284C7;
    color: white !important;
    padding: 8px 16px;
    border-radius: 10px;
    text-decoration: none;
    font-weight: bold;
    display: inline-block;
    margin-top: 10px;
}}

.stButton > button {{
    background: linear-gradient(90deg, #0284C7, #38BDF8) !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 10px 18px !important;
    font-weight: bold !important;
}}

div[data-testid="column"] .stButton > button {{
    width: 60px !important;
    height: 60px !important;
    border-radius: 15px !important;
    font-size: 18px !important;
    font-weight: bold !important;
}}

</style>
''', unsafe_allow_html=True)

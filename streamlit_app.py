import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

st.set_page_config(page_title="Scanner AI", page_icon="🆔", layout="centered")

# עיצוב RTL עברי
st.markdown("""<style> div[dir="rtl"] { text-align: right; } </style>""", unsafe_allow_html=True)

st.title("🆔 סורק תעודות חכם")
st.write("העלה תמונה והמערכת תחלץ את הפרטים באופן אוטומטי.")

api_key = st.sidebar.text_input("הכנס Google API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    file = st.file_uploader("העלה תעודה/רישיון (תמונה/PDF)", type=["jpg","png","pdf"])
    
    if file:
        img = Image.open(file)
        st.image(img, caption="הקובץ הועלה", use_container_width=True)
        
        if st.button("בצע סריקה 🔍"):
            with st.spinner("מנתח..."):
                prompt = "Extract from this document: Full Name, ID Number, DOB, and Address. Return ONLY valid JSON."
                response = model.generate_content([prompt, img])
                data = json.loads(response.text.replace("```json", "").replace("```", "").strip())
                
                st.subheader("פרטים שזוהו:")
                st.text_input("שם מלא", value=data.get("full_name"), key="n")
                st.text_input("מספר זהות", value=data.get("id_number"), key="i")
                st.text_input("תאריך לידה", value=data.get("dob"), key="d")
                st.text_input("כתובת", value=data.get("address"), key="a")
                st.info("ניתן להעתיק את הפרטים מתוך התיבות למעלה.")
else:
    st.info("בבקשה הכנס מפתח API בסרגל הצד (Sidebar) כדי להתחיל.")

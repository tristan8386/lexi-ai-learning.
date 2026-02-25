import google.generativeai as genai
import streamlit as st
import json
import re
import time

def configure_ai():
    try:
        # Lấy API Key từ file secrets.toml
        api_key = st.secrets["GENAI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # Kiểm tra và chọn model mạnh nhất hiện tại cho text
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m in models:
            if 'gemini-1.5-flash' in m:
                return genai.GenerativeModel(m)
        return genai.GenerativeModel(models[0]) if models else None
    except:
        return None

def extract_json(text):
    # Dùng Regex để tách khối JSON ra khỏi các đoạn text thừa (nếu có)
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            return None
    return None

def get_word_info(word):
    model = configure_ai()
    if not model: return {"error": "Lỗi cấu hình AI (API Key chưa đúng)"}

    # Prompt được tối ưu để AI trả về đúng định dạng ô lưới song ngữ
    prompt = f"""
    You are an IELTS Band 9 Expert. Analyze the word: "{word}".
    Return ONLY JSON with this format:
    {{
     "phonetic": "ipa",
     "word_class": "noun/verb...",
     "definition_en": "concise english definition",
     "definition_vi": "nghĩa tiếng Việt ngắn gọn",
     "ratings": {{"reading": 4, "listening": 3, "writing": 5, "speaking": 4, "life": 5}},
     "collocations": ["english colocation : nghĩa tiếng Việt"],
     "idioms": ["english idiom : nghĩa tiếng Việt"],
     "word_forms": {{
        "noun": "word : nghĩa",
        "verb": "word : nghĩa",
        "adj": "word : nghĩa",
        "adv": "word : nghĩa"
     }},
     "examples": ["english sentence : nghĩa tiếng Việt"],
     "synonyms": ["word : nghĩa"],
     "antonyms": ["word : nghĩa"],
     "nuance": "giải thích chi tiết sắc thái và cách dùng từ này trong IELTS bằng tiếng Việt"
    }}
    IMPORTANT: Every array/object value MUST follow "English : Vietnamese" format.
    Return NO text other than JSON.
    """
    
    # Cơ chế thử lại 2 lần nếu AI trả về lỗi định dạng
    for _ in range(2):
        try:
            res = model.generate_content(prompt)
            data = extract_json(res.text)
            if data: return data
        except Exception:
            time.sleep(1)
            
    return {"error": "Lexi đang bận một chút, em nhấn tìm lại lần nữa nhé!"}
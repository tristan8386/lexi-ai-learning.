import google.generativeai as genai
import streamlit as st
import json
import re
import time

def configure_ai():
    try:
        api_key = st.secrets["GENAI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # Quét danh sách model khả dụng
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Ưu tiên gemini-1.5-flash, nếu không có thì lấy cái đầu tiên
        for m in models:
            if 'gemini-1.5-flash' in m:
                return genai.GenerativeModel(m)
        return genai.GenerativeModel(models[0]) if models else None
    except:
        return None

def extract_json(text):
    # Dùng Regex để lấy nội dung JSON từ phản hồi của AI
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            return None
    return None

def get_word_info(word):
    """Lấy thông tin chi tiết của từ vựng"""
    model = configure_ai()
    prompt = f"""
    You are a Band 9 IELTS expert. Analyze the word "{word}".
    Return ONLY JSON:
    {{
     "phonetic":"",
     "word_class":"",
     "band_level":"",
     "definition_en":"",
     "definition_vi":"",
     "nuance":"",
     "collocations":[],
     "idioms":[],
     "word_family":[],
     "examples":[]
     "synonyms":[]"
     "antonyms":[]"
    }} Giải thích ý nghĩa ngắn gọn bằng tiếng việt ở phần "definition_vi" và giải thích chi tiết hơn ở phần "nuance". 
    Nếu không có thông tin nào, trả về chuỗi rỗng hoặc mảng rỗng.nếu không có idioms hoặc collocations,synonyms,antonyms thì trả về mảng rỗng.
    Nếu không có band level thì trả về chuỗi rỗng.
    Trình bày logic dễ nhìn để người dùng dễ hiểu.
    Trả về kết quả càng chi tiết càng tốt, đặc biệt là phần "nuance" và "examples".
    No explanation outside JSON.
    """
    for _ in range(2):
        try:
            res = model.generate_content(prompt)
            data = extract_json(res.text)
            if data: return data
        except Exception as e:
            time.sleep(1)
    return {"error": "AI không phản hồi hoặc hết lượt dùng (Rate Limit)."}

def evaluate_sentence(word, sentence):
    """Chấm điểm câu viết của người dùng (tính năng mở rộng)"""
    model = configure_ai()
    prompt = f"""
    You are a strict IELTS examiner. Evaluate this sentence focus on word "{word}": "{sentence}"
    Return ONLY JSON:
    {{
     "is_correct": true,
     "estimated_band":"",
     "lexical_resource_feedback":"",
     "grammar_feedback":"",
     "improved_version":"",
     "explanation_vi":""
    }}
    """
    try:
        res = model.generate_content(prompt)
        data = extract_json(res.text)
        return data if data else {"error": "Lỗi định dạng AI."}
    except:
        return {"error": "AI không thể đánh giá câu này."}
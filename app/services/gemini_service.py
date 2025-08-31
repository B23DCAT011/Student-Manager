from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os
from app.services.RAG.load_model import response


API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY!!!!!!!!!!")
genai.configure(api_key=API_KEY)


def gemini_generate_answer(percent: float, student_id: str = None)-> str:
    """
    Nhận đầu vào là phần trăm dự đoán (từ predict_percent) và mã sinh viên (nếu có), sinh câu trả lời tự nhiên cho client bằng Gemini.
    """
    if student_id:
        prompt = (
            f"Mã sinh viên: {student_id}.\n"
            f"Xác suất rớt môn dự đoán là: {percent}%.\n"
            "Hãy trả lời cho người dùng bằng tiếng Việt, văn phong thân thiện, dễ hiểu. Đưa ra một lời khuyên hoặc kết luận nếu có thể."
        )
    else:
        prompt = (
            f"Xác suất rớt môn dự đoán là: {percent}%.\n"
            "Hãy trả lời cho người dùng bằng tiếng Việt, văn phong thân thiện, dễ hiểu. Đưa ra một lời khuyên hoặc kết luận nếu có thể."
        )

    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)

    return response.text.strip()

def gemini_extract_grades(question: str):
    """
    Nhận đầu vào là câu hỏi của người dùng, trả về các điểm số được trích xuất từ câu hỏi đó.
    """
    model = genai.GenerativeModel('gemini-2.0-flash')

    prompt = (
        f"Trích xuất các điểm số, thông tin từ câu hỏi sau: {question}. nếu câu hỏi liên quan đến điểm số thì mới trả về"
        f"CHÍNH XÁC dưới dạng  5 phần tử theo thứ tự:"
        f"diem_chuyen_can, diem_giua_ky, diem_bai_tap, so_mon_da_rot, GPA"
        f"Nếu không có thông tin nào thì để 0,0,0,0,0."
        f"Ví dụ: 8.5, 7.0, 9.0, 1, 7.2"
        f"Nếu không thể trích xuất hay không liên quan,hãy trả về {question}"
    )

    response = model.generate_content(prompt)

    return response.text.strip()


def gemini_generate_answer_default(question: str) -> str:
    """
    Trả về câu trả lời chung chung nếu không trích xuất được điểm từ câu hỏi.
    """
    try:
        res = response(question)
        return res
    except Exception as e:
        print(f"Error in RAG processing: {e}")
        return gemini_fallback_answer(question)

def gemini_fallback_answer(question: str) -> str:
    """
    Fallback function using direct Gemini API when RAG fails
    """
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')

        prompt = f"""
        Bạn là một trợ lý AI thông minh cho hệ thống quản lý sinh viên.

        Câu hỏi: {question}

        Hãy trả lời câu hỏi bằng tiếng Việt, văn phong thân thiện và chuyên nghiệp.
        Nếu câu hỏi liên quan đến sinh viên, học tập, điểm số thì hãy đưa ra lời khuyên hữu ích.
        """

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return f"Xin lỗi, tôi không thể xử lý câu hỏi của bạn lúc này. Lỗi: {str(e)}"


# app/controllers/chatbot_controller.py
from flask import Blueprint, request, jsonify, render_template, send_from_directory
from flask_login import login_required, current_user
from app.utils.decorators import student_required
from app.services.gemini_service import gemini_generate_answer, gemini_extract_grades,gemini_generate_answer_default
from app.services.prediction_service import predict_percent
import os

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

@chatbot_bp.route("/process")
@student_required
def serve_index():
    """Phục vụ file chat interface"""
    return render_template('chatbot/process.html')

@chatbot_bp.route("/process", methods=["POST"])
@student_required
def process():
    try:
        # Nhận dữ liệu từ form hoặc fetch (application/x-www-form-urlencoded hoặc application/json)
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        question = data.get("question")
        if not question:
            return jsonify({"error": "Câu hỏi không được cung cấp"}), 400

        # Trích xuất điểm từ câu hỏi bằng Gemini
        input_data = gemini_extract_grades(question)
        if input_data == question:
            # Nếu không trích xuất được điểm, trả lời chung chung
            return jsonify({
                "answer": gemini_generate_answer_default(question)
            })

        # Dự đoán xác suất rớt môn
        percent = predict_percent(input_data)

        # Sinh câu trả lời tự nhiên bằng Gemini
        answer = gemini_generate_answer(percent, current_user.ma_sv)

        return jsonify({
            "ma_sinh_vien": current_user.ma_sv,
            "percent": percent,
            "answer": answer
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import random, os

app = Flask(__name__)
CORS(app)  # Enables cross-origin requests

# Knowledge base - easier to expand and maintain
KNOWLEDGE_BASE = {
    "admission": {
        "keywords": ["admission", "admit", "enroll", "registration", "apply"],
        "responses": [
            "📋 Admission process starts in June or post CET."
            " Required documents: 10th & 12th marksheets, ID proof, and passport photos.",
            "📋 .For further Enquiry : Visit the admin office or apply online at college-website.edu/admissions"
        ]
    },
    "fees": {
        "keywords": ["fees", "fee", "cost", "tuition", "payment", "scholarship"],
        "responses": [
            "💰 Fee structure:\n• Engineering: ₹84k/year\n• ME: ₹67k/year\n• MCA/: ₹71K/year\n• DIPLOMA: ₹45K\n\nScholarships available for merit students!"
        ]
    },
    "placement": {
        "keywords": ["placement", "job", "recruit", "package", "salary", "company", "career"],
        "responses": [
            "🎯 Placement highlights:\n• 85% placement rate\n• Top recruiters: TCS, Infosys, Wipro,\n• Highest package: ₹10+ LPA\n• Average package: ₹5+ LPA"
        ]
    },
    "aiml": {
        "keywords": ["aiml", "ai", "ml", "artificial intelligence", "machine learning", "data science"],
        "responses": [
            "🤖 AIML Branch covers:\n• Machine Learning & Deep Learning\n• Natural Language Processing\n• Computer Vision\n• Data Science & Analytics\n\nCareer prospects are excellent!"
        ]
    },
    "events": {
        "keywords": ["event", "fest", "hackathon", "workshop", "seminar", "cultural"],
        "responses": [
            "🎉 Upcoming events:\n• TechFest 2025 - March 15-17\n• Hackathon - April 5\n• Cultural Night - March 20\n\nRegister at events.college.edu"
        ]
    },
    "library": {
        "keywords": ["library", "book", "study", "reading"],
        "responses": [
            "📚 Library hours: 8 AM - 5 PM (Mon-Sat)\n• 50,000+ books\n• 15+ Computers Available\n• Digital library access\n• Group study rooms available"
        ]
    },
    "hostel": {
        "keywords": ["hostel", "accommodation", "room", "mess", "food"],
        "responses": [
            "🏠 Hostel facilities:\n• AC & Non-AC rooms\n• 24/7 WiFi\n• Mess with veg/non-veg options\n• Gym & recreation room\n\nFees: ₹60K-90K/year"
        ]
    },
    "contact": {
        "keywords": ["contact", "phone", "email", "address", "location", "reach"],
        "responses": [
            "📞 Contact us:\n• Phone: +91-77700-02544\n• Email: viva-technology.org\n• Address: VIVA Institute of Technology Shrigaon, Veer Sawarkar Road,Virar (E)401305"
        ]
    },
    "timing": {
        "keywords": ["timing", "time", "schedule", "hours", "open", "close"],
        "responses": [
            "⏰ Campus timings:\n• College: 8 AM - 5 PM\n• Library: 8 AM - 5 PM\n• Admin Office: 10 AM - 4 PM"
        ]
    },
    "greeting": {
        "keywords": ["hello", "hi", "hey", "good morning", "good evening"],
        "responses": [
            "👋 Hello! Welcome to Campus AI. How can I help you today?",
            "Hi there! 🎓 Ask me anything about admissions, placements, events, or campus life!"
        ]
    }
}

# Conversation history (in production, use a database)
conversations = {}

def get_response(user_message, session_id="default"):
    user_message = user_message.lower().strip()
    
    # Check each category
    for category, data in KNOWLEDGE_BASE.items():
        for keyword in data["keywords"]:
            if keyword in user_message:
                return random.choice(data["responses"])
    
    # Fallback with suggestions
    return "🤔 I'm not sure about that. Try asking about:\n• Admissions\n• Fees & Scholarships\n• Placements\n• Events\n• Hostel\n• Library\n• Contact info"

@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "name": "Campus AI Chatbot",
        "version": "2.0"
    })

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    session_id = data.get("session_id", "default")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    response = get_response(user_message, session_id)
    
    # Log conversation
    timestamp = datetime.now().isoformat()
    if session_id not in conversations:
        conversations[session_id] = []
    conversations[session_id].append({
        "user": user_message,
        "bot": response,
        "time": timestamp
    })
    
    return jsonify({
        "response": response,
        "timestamp": timestamp
    })

# Quick replies endpoint
@app.route("/quick-replies", methods=["GET"])
def quick_replies():
    return jsonify({
        "replies": [
            "Admission process",
            "Fee structure", 
            "Placement stats",
            "Upcoming events",
            "Hostel info",
            "Contact details"
        ]
    })
from flask import send_file  # Add to imports at top

@app.route('/chat.html')
def chat_page():
    return send_file('chat.html')

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)), host='0.0.0.0')

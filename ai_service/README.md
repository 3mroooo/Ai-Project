# AI Job Recommendation Service
Repo :
https://github.com/3mroooo/Ai-Project

## 🚀 تشغيل الخدمة محلياً
# 1. ينزلوها جوه مشروعهم
cd JobRecommendationSystem
git clone https://github.com/3mroooo/Ai-Project.git ai_service

# 2. يشغلوها
cd ai_service
pip install -r requirements.txt
python app.py
الـ API هيشتغل على: "http://localhost:5000"

🌐 الواجهة (GUI)
افتح ملف index.html في المتصفح.

📡 الـ Endpoints
POST /recommend
الوصف: توصية بوظائف بناءً على نص CV

الـ Body (JSON):

json
{
  "cv_text": "نص السيرة الذاتية هنا"
}
الـ Response:

json
[
  {
    "job_title": "Backend Developer",
    "company": "Tech Corp",
    "match_score": 85.5,
    "job_description": "..."
  }
]
POST /recommend-file
الوصف: رفع ملف CV

Form Data: key = cv (file)

GET /health
الوصف: فحص صحة الخدمة

📦 المكتبات المطلوبة
Flask==2.3.2

flask-cors==4.0.0

pandas==2.0.3

scikit-learn==1.3.0

🔗 ربطها بالبروجيكت الكبير
javascript
// من أي frontend (React, Angular, HTML)
fetch('http://localhost:5000/recommend', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ cv_text: "cv text here" })
})
.then(res => res.json())
.then(jobs => console.log(jobs))
text

---

## 📋 شرح لكل ملف:

Ai-Project/
└── ai_service/              # كل حاجة جوه المجلد ده
    ├── app.py
    ├── model.py
    ├── job_descriptions.csv
    ├── requirements.txt
    ├── index.html
    └── README.md
    
| الملف | بيحوي إيه | شغله إيه |
|-------|----------|----------|
| `app.py` | Flask server | بيستقبل الطلبات ويرد عليها |
| `model.py` | خوارزمية TF-IDF + مهارات | بيحسب درجة التوافق بين CV والوظائف |
| `job_descriptions.csv` | البيانات | فيه الوظائف والعناوين والوصف |
| `requirements.txt` | المكتبات | عشان يثبتوا اللي محتاجينه |
| `index.html` | واجهة مستخدم | عشان يختبروا الخدمة بسرعة |
| `README.md` | شرح | عشان يعرفوا يستخدموها |

---

## 🎯 إزاي التيم يستخدمها في البروجيكت الكبير:

### الطريقة 1: تشغيل محلي
```bash
python app.py


الطريقة 2: تشغيل على سيرفر (PythonAnywhere / Render)
الطريقة 3: الاتصال من الكود بتاعهم
*******************python********************
"
import requests

response = requests.post(
    "http://localhost:5000/recommend",
    json={"cv_text": "Python developer"}
)
jobs = response.json()
"
تحياتي 

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "job_descriptions.csv")
jobs_df = pd.read_csv(csv_path)

# ========== اكتشاف أسماء الأعمدة تلقائياً ==========
print("📊 CSV Columns:", jobs_df.columns.tolist())

# البحث عن عمود الوصف
desc_col = None
for col in jobs_df.columns:
    col_lower = col.lower()
    if 'description' in col_lower or 'desc' in col_lower:
        desc_col = col
        break

if desc_col is None:
    # لو ملقتش، خد العمود التاني (غالباً هو الوصف)
    desc_col = jobs_df.columns[1] if len(jobs_df.columns) > 1 else jobs_df.columns[0]

# البحث عن عمود العنوان
title_col = None
for col in jobs_df.columns:
    col_lower = col.lower()
    if 'title' in col_lower or 'job' in col_lower:
        title_col = col
        break

if title_col is None:
    title_col = jobs_df.columns[0]

print(f"✅ Using Title Column: {title_col}")
print(f"✅ Using Description Column: {desc_col}")

# ========== قائمة المهارات ==========
SKILLS = ["python", "java", "sql", "machine learning", "html", "css", "javascript", 
          "react", "angular", "django", "flask", "aws", "docker", "kubernetes",
          "tensorflow", "pytorch", "pandas", "numpy", "git", "linux"]

def extract_skills(text):
    text = text.lower()
    return [skill for skill in SKILLS if skill in text]

def skill_score(user_skills, job_text):
    job_text = job_text.lower()
    job_skills = [skill for skill in SKILLS if skill in job_text]
    if not job_skills:
        return 0
    common = set(user_skills).intersection(set(job_skills))
    return (len(common) / len(job_skills)) * 100

def text_similarity(cv_text, job_texts):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([cv_text] + job_texts)
    scores = cosine_similarity(vectors[0], vectors[1:])[0]
    return scores * 100

def recommend_jobs(cv_text, jobs_df):
    job_texts = jobs_df[desc_col].fillna('').astype(str).tolist()
    
    sim_scores = text_similarity(cv_text, job_texts)
    user_skills = extract_skills(cv_text)
    
    results = []
    for i, job in jobs_df.iterrows():
        skill_sc = skill_score(user_skills, str(job[desc_col]))
        text_sc = sim_scores[i]
        final_score = (0.6 * skill_sc) + (0.4 * text_sc)
        
        # جيب اسم الشركة لو موجود
        company = "Not specified"
        for col in jobs_df.columns:
            if 'company' in col.lower() or 'employer' in col.lower():
                company = str(job[col]) if pd.notna(job[col]) else "Not specified"
                break
        
        results.append({
            "job_title": str(job[title_col]) if pd.notna(job[title_col]) else f"Job {i}",
            "company": company,
            "job_description": str(job[desc_col])[:300] if len(str(job[desc_col])) > 300 else str(job[desc_col]),
            "match_score": round(final_score, 2)
        })
    
    results = sorted(results, key=lambda x: x["match_score"], reverse=True)
    return results[:5]
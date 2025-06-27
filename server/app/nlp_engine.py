import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

def preprocess(text):
    doc = nlp(text.lower())
    return " ".join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha])

def analyze_resume(resume, job_desc):
    resume_clean = preprocess(resume)
    jd_clean = preprocess(job_desc)

    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform([resume_clean, jd_clean])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    resume_tokens = set(resume_clean.split())
    jd_tokens = set(jd_clean.split())
    missing = jd_tokens - resume_tokens

    return score, missing

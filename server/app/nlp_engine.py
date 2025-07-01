import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

nlp = spacy.load("en_core_web_sm")

def preprocess(text):
    doc = nlp(text.lower())
    return " ".join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha])

def extract_keywords_from_text(text, min_length=2):
    """Extract meaningful keywords from text"""
    doc = nlp(text.lower())
    keywords = []
    
    # Extract entities
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "EVENT", "WORK_OF_ART", "LANGUAGE"]:
            keywords.append(ent.text.strip())
    
    # Extract noun phrases and important terms
    for token in doc:
        if (token.pos_ in ["NOUN", "PROPN", "ADJ"] and 
            not token.is_stop and 
            token.is_alpha and 
            len(token.text) >= min_length):
            keywords.append(token.lemma_)
    
    # Extract technical terms (words with specific patterns)
    tech_patterns = [
        r'\b[a-z]+\+\+\b',  # C++, etc.
        r'\b[a-z]+\.js\b',   # React.js, Node.js, etc.
        r'\b[a-z]+[0-9]+\b', # Python3, HTML5, etc.
        r'\b[A-Z]{2,}\b'     # SQL, API, etc.
    ]
    
    for pattern in tech_patterns:
        matches = re.findall(pattern, text.lower())
        keywords.extend(matches)
    
    return list(set(keywords))

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

def get_analysis_summary(resume, job_desc):
    """Get a complete analysis summary for reporting"""
    resume_clean = preprocess(resume)
    jd_clean = preprocess(job_desc)

    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform([resume_clean, jd_clean])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    # Basic token analysis
    resume_tokens = set(resume_clean.split())
    jd_tokens = set(jd_clean.split())
    missing_tokens = jd_tokens - resume_tokens
    matched_tokens = resume_tokens & jd_tokens
    
    # Enhanced keyword analysis
    resume_keywords = set(extract_keywords_from_text(resume))
    jd_keywords = set(extract_keywords_from_text(job_desc))
    
    missing_keywords = jd_keywords - resume_keywords
    matched_keywords = resume_keywords & jd_keywords

    return {
        "similarity_score": score,
        "missing_tokens": list(missing_tokens),
        "matched_tokens": list(matched_tokens), 
        "missing_keywords": list(missing_keywords),
        "matched_keywords": list(matched_keywords),
        "total_jd_tokens": len(jd_tokens),
        "total_resume_tokens": len(resume_tokens),
        "match_percentage": len(matched_tokens) / max(len(jd_tokens), 1) * 100
    }
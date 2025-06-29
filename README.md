# 📄 Resumetric

**Resumetric** is an AI-powered resume analysis tool that helps job seekers optimize their resumes by comparing them against job descriptions. The application uses natural language processing and machine learning to provide similarity scores, identify missing keywords, and generate actionable feedback.

## 🚀 Features

- **Resume-Job Description Matching**: Calculate similarity scores between resumes and job descriptions
- **Keyword Analysis**: Identify missing keywords from job descriptions in your resume
- **AI-Powered Feedback**: Get intelligent suggestions using Google's Gemini AI
- **PDF Processing**: Extract and analyze text from PDF resumes
- **Email Integration**: Send analysis results via email
- **Authentication**: Secure user authentication with JWT tokens
- **RESTful API**: Well-structured backend API with Flask

## 🛠️ Tech Stack

### Backend
- **Flask** - Python web framework
- **spaCy** - Natural language processing
- **scikit-learn** - Machine learning for TF-IDF and cosine similarity
- **Google Gemini AI** - AI-powered feedback generation
- **PyMuPDF** - PDF text extraction
- **Flask-JWT-Extended** - Authentication
- **Flask-Mail** - Email functionality
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **React** - Frontend framework (planned)
- **Vite** - Build tool (planned)

## 📁 Project Structure

```
resumetric/
├── client/                 # Frontend application (planned)
├── server/                 # Backend Flask application
│   ├── app/
│   │   ├── __init__.py    # Flask app factory
│   │   ├── auth.py        # Authentication routes
│   │   ├── db_utils.py    # Database utilities
│   │   ├── email_utils.py # Email functionality
│   │   ├── gemini_utils.py# AI integration
│   │   ├── nlp_engine.py  # NLP analysis engine
│   │   ├── pdf_parser.py  # PDF processing
│   │   ├── report_genrator.py # Report generation
│   │   ├── routes.py      # Main API routes
│   │   └── test_models.py # Testing utilities
│   ├── app.py            # Application entry point
│   ├── requirements.txt  # Python dependencies
│   └── aniketresume.pdf  # Sample resume file
└── README.md
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+ (for frontend)
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/resumetric.git
   cd resumetric/server
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Environment variables**
   Create a `.env` file in the server directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   SECRET_KEY=your_secret_key_here
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_app_password
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

### Frontend Setup (Coming Soon)
```bash
cd client
npm install
npm run dev
```

## 📚 API Documentation

### Core Endpoints

#### Resume Analysis
```http
POST /api/analyze
Content-Type: application/json
Authorization: Bearer <jwt_token>

{
  "resume_text": "Your resume content...",
  "job_description": "Job description content..."
}
```

**Response:**
```json
{
  "similarity_score": 0.75,
  "missing_keywords": ["python", "machine learning", "api"],
  "ai_feedback": [
    "Add more technical skills",
    "Include quantifiable achievements",
    "Highlight relevant experience"
  ]
}
```

#### Authentication
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

## 🔍 How It Works

1. **Text Preprocessing**: Resumes and job descriptions are cleaned using spaCy NLP
2. **Feature Extraction**: TF-IDF vectorization converts text to numerical features
3. **Similarity Calculation**: Cosine similarity measures resume-job description match
4. **Keyword Analysis**: Identifies missing important keywords
5. **AI Enhancement**: Google Gemini provides contextual improvement suggestions

## 🧪 Core NLP Engine

The heart of Resumetric is the NLP engine that:

```python
def analyze_resume(resume, job_desc):
    # Preprocess text (lemmatization, stop word removal)
    resume_clean = preprocess(resume)
    jd_clean = preprocess(job_desc)
    
    # Calculate TF-IDF vectors and similarity
    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform([resume_clean, jd_clean])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    
    # Find missing keywords
    missing = set(jd_clean.split()) - set(resume_clean.split())
    
    return score, missing
```

## 🔐 Security Features

- JWT-based authentication
- CORS protection
- Environment variable configuration
- Input validation and sanitization

## 🚧 Roadmap

- [ ] Complete React frontend implementation
- [ ] User dashboard with analysis history
- [ ] Resume template suggestions
- [ ] Batch processing for multiple resumes
- [ ] Integration with job boards
- [ ] Mobile application
- [ ] Advanced analytics and reporting

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Aniket** - *Initial work*

## 🙏 Acknowledgments

- spaCy for excellent NLP capabilities
- Google Gemini AI for intelligent feedback
- Flask community for the robust web framework
- scikit-learn for machine learning utilities

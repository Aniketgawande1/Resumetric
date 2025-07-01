import json
import csv
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import os

@dataclass
class ResumeAnalysisReport:
    """Data class to structure resume analysis results"""
    user_id: str
    user_email: str
    resume_filename: str
    job_title: str
    company_name: Optional[str]
    analysis_date: str
    similarity_score: float
    missing_keywords: List[str]
    matched_keywords: List[str]
    ai_feedback: List[str]
    suggestions: List[str]
    overall_rating: str
    strengths: List[str]
    weaknesses: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the report to dictionary format"""
        return asdict(self)

class ReportGenerator:
    """Generate comprehensive reports for resume analysis"""
    
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = reports_dir
        self.ensure_reports_directory()
    
    def ensure_reports_directory(self):
        """Create reports directory if it doesn't exist"""
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
    
    def calculate_overall_rating(self, similarity_score: float, missing_keywords_count: int) -> str:
        """Calculate overall rating based on similarity score and missing keywords"""
        if similarity_score >= 0.8 and missing_keywords_count <= 3:
            return "Excellent"
        elif similarity_score >= 0.6 and missing_keywords_count <= 6:
            return "Good"
        elif similarity_score >= 0.4 and missing_keywords_count <= 10:
            return "Fair"
        else:
            return "Needs Improvement"
    
    def generate_suggestions(self, missing_keywords: List[str], similarity_score: float) -> List[str]:
        """Generate actionable suggestions based on analysis"""
        suggestions = []
        
        if similarity_score < 0.5:
            suggestions.append("Consider restructuring your resume to better align with the job description")
            suggestions.append("Review the job requirements and add relevant experience")
        
        if len(missing_keywords) > 5:
            suggestions.append(f"Add these important keywords: {', '.join(missing_keywords[:5])}")
            suggestions.append("Include more technical skills mentioned in the job description")
        
        if similarity_score < 0.3:
            suggestions.append("Consider highlighting transferable skills if you lack direct experience")
            suggestions.append("Use action verbs and quantifiable achievements")
        
        suggestions.append("Tailor your resume summary to match the job requirements")
        suggestions.append("Include relevant certifications or courses")
        
        return suggestions
    
    def identify_strengths_weaknesses(self, matched_keywords: List[str], missing_keywords: List[str], 
                                    similarity_score: float) -> tuple[List[str], List[str]]:
        """Identify strengths and weaknesses based on analysis"""
        strengths = []
        weaknesses = []
        
        if len(matched_keywords) > 10:
            strengths.append("Strong keyword alignment with job requirements")
        
        if similarity_score > 0.6:
            strengths.append("Good overall content relevance")
        
        if len(matched_keywords) > 0:
            strengths.append(f"Relevant skills found: {', '.join(matched_keywords[:3])}")
        
        if len(missing_keywords) > 5:
            weaknesses.append("Missing several important keywords")
        
        if similarity_score < 0.4:
            weaknesses.append("Low content similarity with job description")
        
        if len(missing_keywords) > 0:
            weaknesses.append(f"Missing key requirements: {', '.join(missing_keywords[:3])}")
        
        return strengths, weaknesses
    
    def create_analysis_report(self, user_id: str, user_email: str, resume_filename: str,
                             job_title: str, company_name: Optional[str], similarity_score: float,
                             missing_keywords: List[str], matched_keywords: List[str],
                             ai_feedback: List[str]) -> ResumeAnalysisReport:
        """Create a comprehensive analysis report"""
        
        # Calculate derived metrics
        overall_rating = self.calculate_overall_rating(similarity_score, len(missing_keywords))
        suggestions = self.generate_suggestions(missing_keywords, similarity_score)
        strengths, weaknesses = self.identify_strengths_weaknesses(matched_keywords, missing_keywords, similarity_score)
        
        # Create report object
        report = ResumeAnalysisReport(
            user_id=user_id,
            user_email=user_email,
            resume_filename=resume_filename,
            job_title=job_title,
            company_name=company_name,
            analysis_date=datetime.now().isoformat(),
            similarity_score=round(similarity_score, 3),
            missing_keywords=missing_keywords,
            matched_keywords=matched_keywords,
            ai_feedback=ai_feedback,
            suggestions=suggestions,
            overall_rating=overall_rating,
            strengths=strengths,
            weaknesses=weaknesses
        )
        
        return report
    
    def generate_json_report(self, report: ResumeAnalysisReport, filename: Optional[str] = None) -> str:
        """Generate JSON format report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resume_analysis_{report.user_id}_{timestamp}.json"
        
        filepath = os.path.join(self.reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def generate_csv_report(self, reports: List[ResumeAnalysisReport], filename: Optional[str] = None) -> str:
        """Generate CSV format report for multiple analyses"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resume_analyses_batch_{timestamp}.csv"
        
        filepath = os.path.join(self.reports_dir, filename)
        
        if not reports:
            return filepath
        
        fieldnames = list(reports[0].to_dict().keys())
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for report in reports:
                # Convert lists to strings for CSV format
                row = report.to_dict()
                for key, value in row.items():
                    if isinstance(value, list):
                        row[key] = '; '.join(value)
                writer.writerow(row)
        
        return filepath
    
    def generate_html_report(self, report: ResumeAnalysisReport, filename: Optional[str] = None) -> str:
        """Generate HTML format report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resume_analysis_{report.user_id}_{timestamp}.html"
        
        filepath = os.path.join(self.reports_dir, filename)
        
        # Determine rating color
        rating_colors = {
            "Excellent": "#4CAF50",
            "Good": "#8BC34A",
            "Fair": "#FF9800",
            "Needs Improvement": "#F44336"
        }
        
        rating_color = rating_colors.get(report.overall_rating, "#9E9E9E")
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Resume Analysis Report - {report.user_email}</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    border-bottom: 3px solid #007bff;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }}
                .score-card {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .rating {{
                    background-color: {rating_color};
                    color: white;
                    padding: 10px 20px;
                    border-radius: 25px;
                    display: inline-block;
                    font-weight: bold;
                    margin: 10px 0;
                }}
                .section {{
                    margin-bottom: 25px;
                    padding: 15px;
                    border-left: 4px solid #007bff;
                    background-color: #f8f9fa;
                }}
                .section h3 {{
                    color: #333;
                    margin-top: 0;
                }}
                .keywords {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                    margin-top: 10px;
                }}
                .keyword {{
                    background-color: #007bff;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 15px;
                    font-size: 12px;
                }}
                .missing-keyword {{
                    background-color: #dc3545;
                }}
                .matched-keyword {{
                    background-color: #28a745;
                }}
                .suggestion, .feedback {{
                    background-color: #fff3cd;
                    border: 1px solid #ffeaa7;
                    border-radius: 5px;
                    padding: 10px;
                    margin: 5px 0;
                }}
                .strength {{
                    background-color: #d4edda;
                    border: 1px solid #c3e6cb;
                    border-radius: 5px;
                    padding: 8px;
                    margin: 3px 0;
                }}
                .weakness {{
                    background-color: #f8d7da;
                    border: 1px solid #f5c6cb;
                    border-radius: 5px;
                    padding: 8px;
                    margin: 3px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📄 Resume Analysis Report</h1>
                    <p><strong>Resumetric</strong> - AI-Powered Resume Optimization</p>
                </div>
                
                <div class="score-card">
                    <h2>Overall Similarity Score</h2>
                    <h1>{report.similarity_score:.1%}</h1>
                    <div class="rating">{report.overall_rating}</div>
                </div>
                
                <div class="section">
                    <h3>📋 Analysis Details</h3>
                    <p><strong>User:</strong> {report.user_email}</p>
                    <p><strong>Resume:</strong> {report.resume_filename}</p>
                    <p><strong>Job Title:</strong> {report.job_title}</p>
                    {f'<p><strong>Company:</strong> {report.company_name}</p>' if report.company_name else ''}
                    <p><strong>Analysis Date:</strong> {report.analysis_date}</p>
                </div>
                
                <div class="section">
                    <h3>✅ Strengths</h3>
                    {''.join([f'<div class="strength">• {strength}</div>' for strength in report.strengths])}
                </div>
                
                <div class="section">
                    <h3>⚠️ Areas for Improvement</h3>
                    {''.join([f'<div class="weakness">• {weakness}</div>' for weakness in report.weaknesses])}
                </div>
                
                <div class="section">
                    <h3>🎯 Matched Keywords</h3>
                    <div class="keywords">
                        {''.join([f'<span class="keyword matched-keyword">{keyword}</span>' for keyword in report.matched_keywords[:10]])}
                    </div>
                </div>
                
                <div class="section">
                    <h3>❌ Missing Keywords</h3>
                    <div class="keywords">
                        {''.join([f'<span class="keyword missing-keyword">{keyword}</span>' for keyword in report.missing_keywords[:15]])}
                    </div>
                </div>
                
                <div class="section">
                    <h3>💡 AI-Generated Feedback</h3>
                    {''.join([f'<div class="feedback">• {feedback}</div>' for feedback in report.ai_feedback])}
                </div>
                
                <div class="section">
                    <h3>🚀 Actionable Suggestions</h3>
                    {''.join([f'<div class="suggestion">• {suggestion}</div>' for suggestion in report.suggestions])}
                </div>
                
                <div class="footer">
                    <p>Generated by Resumetric - AI-Powered Resume Analysis Tool</p>
                    <p>Report generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def generate_summary_stats(self, reports: List[ResumeAnalysisReport]) -> Dict[str, Any]:
        """Generate summary statistics for multiple reports"""
        if not reports:
            return {}
        
        scores = [report.similarity_score for report in reports]
        ratings = [report.overall_rating for report in reports]
        
        stats = {
            "total_analyses": len(reports),
            "average_score": sum(scores) / len(scores),
            "highest_score": max(scores),
            "lowest_score": min(scores),
            "rating_distribution": {
                "Excellent": ratings.count("Excellent"),
                "Good": ratings.count("Good"),
                "Fair": ratings.count("Fair"),
                "Needs Improvement": ratings.count("Needs Improvement")
            },
            "most_common_missing_keywords": self._get_common_keywords([kw for report in reports for kw in report.missing_keywords]),
            "analysis_dates": [report.analysis_date for report in reports]
        }
        
        return stats
    
    def _get_common_keywords(self, keywords: List[str], top_n: int = 10) -> List[tuple]:
        """Get most common keywords from a list"""
        from collections import Counter
        return Counter(keywords).most_common(top_n)
    
    def export_user_history(self, user_id: str, reports: List[ResumeAnalysisReport]) -> str:
        """Export all reports for a specific user"""
        user_reports = [report for report in reports if report.user_id == user_id]
        
        if not user_reports:
            return ""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"user_history_{user_id}_{timestamp}.json"
        
        history_data = {
            "user_id": user_id,
            "total_analyses": len(user_reports),
            "export_date": datetime.now().isoformat(),
            "summary_stats": self.generate_summary_stats(user_reports),
            "reports": [report.to_dict() for report in user_reports]
        }
        
        filepath = os.path.join(self.reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
        
        return filepath

# Utility functions for easy usage
def create_quick_report(user_email: str, resume_filename: str, job_title: str, 
                       similarity_score: float, missing_keywords: List[str], 
                       ai_feedback: List[str], company_name: str = None) -> ResumeAnalysisReport:
    """Quick function to create a basic report"""
    generator = ReportGenerator()
    
    # Generate some matched keywords (dummy data for demo)
    all_possible_keywords = ["python", "javascript", "react", "node", "sql", "git", "api", "database"]
    matched_keywords = [kw for kw in all_possible_keywords if kw not in missing_keywords]
    
    return generator.create_analysis_report(
        user_id=user_email.split('@')[0],  # Simple user ID from email
        user_email=user_email,
        resume_filename=resume_filename,
        job_title=job_title,
        company_name=company_name,
        similarity_score=similarity_score,
        missing_keywords=missing_keywords,
        matched_keywords=matched_keywords,
        ai_feedback=ai_feedback
    )

# Example usage
if __name__ == "__main__":
    # Example of how to use the report generator
    generator = ReportGenerator()
    
    # Create a sample report
    sample_report = create_quick_report(
        user_email="john.doe@example.com",
        resume_filename="john_doe_resume.pdf",
        job_title="Full Stack Developer",
        company_name="Tech Corp",
        similarity_score=0.72,
        missing_keywords=["react", "mongodb", "docker", "aws"],
        ai_feedback=[
            "Add more specific technical skills",
            "Include quantifiable achievements",
            "Highlight leadership experience"
        ]
    )
    
    # Generate reports in different formats
    json_path = generator.generate_json_report(sample_report)
    html_path = generator.generate_html_report(sample_report)
    
    print(f"JSON report saved to: {json_path}")
    print(f"HTML report saved to: {html_path}")
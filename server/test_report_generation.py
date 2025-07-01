#!/usr/bin/env python3
"""
Test script to generate a comprehensive report from analysis data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.report_genrator import ReportGenerator
from datetime import datetime

def generate_test_report():
    """Generate a test report using your actual analysis data"""
    
    # Your actual analysis data
    analysis_data = {
        "score": 6.75,  # Already in percentage format from your output
        "missing_skills": [
            "familiarity", "platform", "familiar", "gcp", "docker", 
            "aw", "plus", "candidate", "database", "postgresql", "backend"
        ],
        "matched_skills": [
            "technology", "rest", "cloud", "apis", "experience", 
            "developer", "python", "mongodb", "git", "system", "authentication"
        ],
        "suggestions": [
            "Highlight Backend Skills and Experience",
            "Quantify Achievements", 
            "Streamline and Refocus the Summary"
        ],
        "generated_lines": [
            "Proficient in backend development utilizing GCP and AWS platforms",
            "Strong candidate with proven experience building applications on GCP"
        ]
    }
    
    # Create report generator
    report_generator = ReportGenerator()
    
    # Create comprehensive report
    report = report_generator.create_analysis_report(
        user_id="test_user",
        user_email="test@example.com",
        resume_filename="aniketresume.pdf",
        job_title="Backend Developer",
        company_name="Tech Company",
        similarity_score=analysis_data["score"] / 100,  # Convert to decimal
        missing_keywords=analysis_data["missing_skills"],
        matched_keywords=analysis_data["matched_skills"],
        ai_feedback=analysis_data["suggestions"]
    )
    
    # Generate different format reports
    json_path = report_generator.generate_json_report(report)
    html_path = report_generator.generate_html_report(report)
    
    print("📄 Report Generation Complete!")
    print(f"📊 JSON Report: {json_path}")
    print(f"🌐 HTML Report: {html_path}")
    print(f"📈 Overall Rating: {report.overall_rating}")
    print(f"🎯 Similarity Score: {report.similarity_score:.1%}")
    
    return json_path, html_path

if __name__ == "__main__":
    try:
        json_file, html_file = generate_test_report()
        print(f"\n✅ Success! Reports generated:")
        print(f"   JSON: {json_file}")
        print(f"   HTML: {html_file}")
        
        # Open HTML report in browser (optional)
        import webbrowser
        print(f"\n🌐 Opening HTML report in browser...")
        webbrowser.open(f"file://{os.path.abspath(html_file)}")
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")

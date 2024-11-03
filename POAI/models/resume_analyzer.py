import spacy
import textstat
from pdfminer.high_level import extract_text as extract_pdf_text
import docx
import os

nlp = spacy.load('en_core_web_sm')

# Extract text from PDF
def extract_text_from_pdf(file_path):
    try:
        return extract_pdf_text(file_path)
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {str(e)}")

# Extract text from DOCX
def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        raise ValueError(f"Error extracting text from DOCX: {str(e)}")

# Main resume analyzer function
def analyze_resume(file_path):
    file_extension = file_path.rsplit('.', 1)[1].lower()
    resume_text = ''
    
    if file_extension == 'pdf':
        resume_text = extract_text_from_pdf(file_path)
    elif file_extension == 'docx':
        resume_text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")
    
    if not resume_text:
        raise ValueError("No text found in the resume")
    
    # Run NLP analysis
    doc = nlp(resume_text)
    
    # Basic analysis
    word_count = len(resume_text.split())
    readability_score = textstat.flesch_reading_ease(resume_text)
    
    # Expanded keyword matching
    keywords = [
        'python', 'flask', 'javascript', 'data science', 'machine learning',
        'java', 'c++', 'react', 'node.js', 'aws', 'azure', 'docker', 'kubernetes',
        'sql', 'nosql', 'mongodb', 'devops', 'terraform', 'ansible', 'linux', 
        'cloud computing', 'salesforce', 'tensorflow', 'pytorch', 'git', 'github',
        'CI/CD', 'jenkins', 'jira', 'selenium', 'cypress', 'html', 'css', 'javascript',
        'bootstrap', 'angular', 'typescript', 'cybersecurity', 'blockchain'
    ]
    found_keywords = [word for word in keywords if word in resume_text.lower()]

    # Evaluate structure (check for necessary sections like 'Education', 'Experience')
    sections = ['education', 'experience', 'skills', 'projects']
    missing_sections = [section for section in sections if section not in resume_text.lower()]
    
    # Scoring efficiency with a minimum base score
    efficiency_score = calculate_efficiency(word_count, readability_score, found_keywords, missing_sections)
    
    # Generate detailed suggestions for improvement with positive reinforcement
    suggestions = generate_suggestions(word_count, readability_score, found_keywords, missing_sections)
    
    return {
        'word_count': word_count,
        'readability_score': readability_score,
        'found_keywords': found_keywords,
        'missing_sections': missing_sections,
        'efficiency_score': efficiency_score,
        'suggestions': suggestions
    }

# Calculate efficiency score with a base score to prevent a score of zero
def calculate_efficiency(word_count, readability_score, found_keywords, missing_sections):
    base_score = 30  # Base score to prevent demotivation
    score = base_score
    if 300 <= word_count <= 700:
        score += 40
    if readability_score > 50:
        score += 20
    if len(found_keywords) > 5:
        score += 20
    if not missing_sections:
        score += 10
    return max(score, base_score)

# Generate suggestions with positive reinforcement
def generate_suggestions(word_count, readability_score, found_keywords, missing_sections):
    suggestions = []
    
    if word_count > 700:
        suggestions.append("Try to shorten your resume to 1-2 pages.")
    else:
        suggestions.append("Great job keeping your resume concise!")

    if readability_score < 50:
        suggestions.append("Simplify language to improve readability.")
    else:
        suggestions.append("Your resume's readability is good!")

    if len(found_keywords) < 5:
        suggestions.append("Include more relevant skills and keywords like Python, DevOps, or Cloud.")
    else:
        suggestions.append("You've included a good number of relevant keywords!")

    if missing_sections:
        suggestions.append(f"Consider adding these sections: {', '.join(missing_sections)}.")
    else:
        suggestions.append("Your resume covers all necessary sections!")

    return suggestions

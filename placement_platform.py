"""
AI-Driven Campus Placement Registration and Resume Matching Platform
Implements student registration, resume analysis, and job recommendation
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class PlacementPlatform:
    def __init__(self):
        self.students = {}
        self.jobs = {}
        self.resumes = []
        self.recommendations = []
        self.placements = []
        
    def generate_student_data(self, n_students=300):
        """Generate synthetic student data"""
        np.random.seed(42)
        
        branches = ['CSE', 'ECE', 'ME', 'CE', 'EE']
        skills_pool = [
            'Python', 'Java', 'C++', 'JavaScript', 'SQL', 'HTML', 'CSS',
            'Machine Learning', 'Data Science', 'Web Development', 'Android',
            'Cloud Computing', 'DevOps', 'Cybersecurity', 'AI', 'NLP'
        ]
        
        for i in range(n_students):
            student_id = f'STU{i+1:05d}'
            
            # Generate skills (3-8 random skills)
            n_skills = np.random.randint(3, 9)
            skills = list(np.random.choice(skills_pool, n_skills, replace=False))
            
            self.students[student_id] = {
                'name': f'Student {i+1}',
                'branch': np.random.choice(branches),
                'cgpa': round(np.random.uniform(6.5, 9.5), 2),
                'skills': skills,
                'certifications': np.random.randint(0, 5),
                'projects': np.random.randint(1, 6),
                'internships': np.random.randint(0, 3),
                'email': f'student{i+1}@university.edu',
                'phone': f'9{np.random.randint(100000000, 999999999)}',
                'registration_date': (datetime.now() - timedelta(days=np.random.randint(0, 180))).strftime('%Y-%m-%d')
            }
        
        students_df = pd.DataFrame(self.students).T
        students_df.to_csv('/home/ubuntu/students_data.csv')
        print(f"Generated student data: {len(self.students)} students")
        return students_df
    
    def generate_job_data(self, n_jobs=150):
        """Generate synthetic job data"""
        np.random.seed(42)
        
        companies = ['TCS', 'Infosys', 'Wipro', 'Accenture', 'IBM', 'Google', 'Microsoft', 'Amazon', 'Apple', 'Meta']
        positions = ['Software Engineer', 'Data Scientist', 'Full Stack Developer', 'ML Engineer', 'Cloud Architect', 'DevOps Engineer']
        skills_pool = [
            'Python', 'Java', 'C++', 'JavaScript', 'SQL', 'HTML', 'CSS',
            'Machine Learning', 'Data Science', 'Web Development', 'Android',
            'Cloud Computing', 'DevOps', 'Cybersecurity', 'AI', 'NLP'
        ]
        
        for i in range(n_jobs):
            job_id = f'JOB{i+1:05d}'
            
            # Generate required skills (2-6 random skills)
            n_skills = np.random.randint(2, 7)
            required_skills = list(np.random.choice(skills_pool, n_skills, replace=False))
            
            self.jobs[job_id] = {
                'company': np.random.choice(companies),
                'position': np.random.choice(positions),
                'required_skills': required_skills,
                'min_cgpa': round(np.random.uniform(6.0, 7.5), 2),
                'experience_required': np.random.randint(0, 5),
                'salary': np.random.randint(400000, 1500000),
                'location': np.random.choice(['Bangalore', 'Hyderabad', 'Pune', 'Delhi', 'Mumbai', 'Chennai']),
                'job_description': f'Position for {np.random.choice(positions)} at {np.random.choice(companies)}',
                'posted_date': (datetime.now() - timedelta(days=np.random.randint(0, 90))).strftime('%Y-%m-%d'),
                'deadline': (datetime.now() + timedelta(days=np.random.randint(10, 60))).strftime('%Y-%m-%d')
            }
        
        jobs_df = pd.DataFrame(self.jobs).T
        jobs_df.to_csv('/home/ubuntu/jobs_data.csv')
        print(f"Generated job data: {len(self.jobs)} job positions")
        return jobs_df
    
    def calculate_resume_match_score(self, student_id, job_id):
        """Calculate resume matching score using NLP and ML"""
        student = self.students[student_id]
        job = self.jobs[job_id]
        
        score = 0
        
        # CGPA match (30 points)
        if student['cgpa'] >= job['min_cgpa']:
            score += 30
        else:
            score += max(0, 30 * (student['cgpa'] / job['min_cgpa']))
        
        # Skills match (40 points)
        student_skills = set(student['skills'])
        required_skills = set(job['required_skills'])
        if len(required_skills) > 0:
            skill_match = len(student_skills & required_skills) / len(required_skills)
            score += 40 * skill_match
        
        # Experience match (20 points)
        total_exp = student['certifications'] + student['projects'] + student['internships']
        score += min(20, total_exp * 2)
        
        # Normalize to 100
        score = min(100, score)
        
        return round(score, 2)
    
    def generate_recommendations(self):
        """Generate job recommendations for each student"""
        np.random.seed(42)
        
        for student_id in self.students.keys():
            student_recommendations = []
            
            for job_id in self.jobs.keys():
                match_score = self.calculate_resume_match_score(student_id, job_id)
                
                # Only recommend if match score > 60
                if match_score > 60:
                    student_recommendations.append({
                        'student_id': student_id,
                        'job_id': job_id,
                        'match_score': match_score,
                        'company': self.jobs[job_id]['company'],
                        'position': self.jobs[job_id]['position'],
                        'recommendation_date': datetime.now().strftime('%Y-%m-%d'),
                        'status': np.random.choice(['Recommended', 'Applied', 'Rejected', 'Shortlisted', 'Offered'], p=[0.3, 0.3, 0.15, 0.15, 0.1])
                    })
            
            # Sort by match score and keep top 10
            student_recommendations = sorted(student_recommendations, key=lambda x: x['match_score'], reverse=True)[:10]
            self.recommendations.extend(student_recommendations)
        
        recommendations_df = pd.DataFrame(self.recommendations)
        recommendations_df.to_csv('/home/ubuntu/recommendations.csv', index=False)
        print(f"Generated {len(self.recommendations)} job recommendations")
        return recommendations_df
    
    def train_placement_models(self):
        """Train ML models for placement prediction"""
        np.random.seed(42)
        
        # Prepare training data
        X = []
        y = []
        
        for student_id in self.students.keys():
            student = self.students[student_id]
            
            # Features: CGPA, certifications, projects, internships, skills count
            features = [
                student['cgpa'],
                student['certifications'],
                student['projects'],
                student['internships'],
                len(student['skills'])
            ]
            X.append(features)
            
            # Target: 1 if placed, 0 otherwise (simulate)
            placed = 1 if student['cgpa'] > 7.0 and len(student['skills']) >= 4 else 0
            y.append(placed)
        
        X = np.array(X)
        y = np.array(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train models
        models = {
            'Logistic Regression': LogisticRegression(random_state=42),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'SVM': SVC(random_state=42)
        }
        
        results = []
        
        for model_name, model in models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            results.append({
                'Model': model_name,
                'Accuracy': round(accuracy_score(y_test, y_pred), 4),
                'Precision': round(precision_score(y_test, y_pred, zero_division=0), 4),
                'Recall': round(recall_score(y_test, y_pred, zero_division=0), 4),
                'F1_Score': round(f1_score(y_test, y_pred, zero_division=0), 4)
            })
        
        results_df = pd.DataFrame(results)
        results_df.to_csv('/home/ubuntu/model_results.csv', index=False)
        print("Trained placement prediction models")
        return results_df
    
    def generate_visualizations(self):
        """Generate comprehensive placement analytics visualizations"""
        students_df = pd.DataFrame(self.students).T
        jobs_df = pd.DataFrame(self.jobs).T
        recommendations_df = pd.DataFrame(self.recommendations)
        
        # 1. Student Demographics
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Branch distribution
        branch_counts = students_df['branch'].value_counts()
        axes[0, 0].bar(branch_counts.index, branch_counts.values, color='#3498db', edgecolor='black', linewidth=1.5)
        axes[0, 0].set_ylabel('Number of Students', fontsize=11, fontweight='bold')
        axes[0, 0].set_title('Student Distribution by Branch', fontsize=12, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        
        # CGPA distribution
        axes[0, 1].hist(students_df['cgpa'], bins=20, color='#2ecc71', edgecolor='black', linewidth=1.5)
        axes[0, 1].set_xlabel('CGPA', fontsize=11, fontweight='bold')
        axes[0, 1].set_ylabel('Number of Students', fontsize=11, fontweight='bold')
        axes[0, 1].set_title('CGPA Distribution', fontsize=12, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Skills distribution
        all_skills = []
        for skills in students_df['skills']:
            all_skills.extend(skills)
        skill_counts = pd.Series(all_skills).value_counts().head(10)
        axes[1, 0].barh(skill_counts.index, skill_counts.values, color='#e74c3c', edgecolor='black', linewidth=1.5)
        axes[1, 0].set_xlabel('Frequency', fontsize=11, fontweight='bold')
        axes[1, 0].set_title('Top 10 Skills Among Students', fontsize=12, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3, axis='x')
        
        # Experience distribution
        students_df['total_exp'] = students_df['certifications'] + students_df['projects'] + students_df['internships']
        axes[1, 1].hist(students_df['total_exp'], bins=15, color='#f39c12', edgecolor='black', linewidth=1.5)
        axes[1, 1].set_xlabel('Total Experience (Certs + Projects + Internships)', fontsize=11, fontweight='bold')
        axes[1, 1].set_ylabel('Number of Students', fontsize=11, fontweight='bold')
        axes[1, 1].set_title('Experience Distribution', fontsize=12, fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('/home/ubuntu/student_demographics.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("Saved: student_demographics.png")
        
        # 2. Job Analytics
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Company distribution
        company_counts = jobs_df['company'].value_counts()
        axes[0, 0].bar(company_counts.index, company_counts.values, color='#9b59b6', edgecolor='black', linewidth=1.5)
        axes[0, 0].set_ylabel('Number of Positions', fontsize=11, fontweight='bold')
        axes[0, 0].set_title('Job Positions by Company', fontsize=12, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        plt.setp(axes[0, 0].xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Salary distribution
        axes[0, 1].hist(jobs_df['salary'] / 100000, bins=20, color='#1abc9c', edgecolor='black', linewidth=1.5)
        axes[0, 1].set_xlabel('Salary (in Lakhs)', fontsize=11, fontweight='bold')
        axes[0, 1].set_ylabel('Number of Positions', fontsize=11, fontweight='bold')
        axes[0, 1].set_title('Salary Distribution', fontsize=12, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Location distribution
        location_counts = jobs_df['location'].value_counts()
        axes[1, 0].bar(location_counts.index, location_counts.values, color='#e67e22', edgecolor='black', linewidth=1.5)
        axes[1, 0].set_ylabel('Number of Positions', fontsize=11, fontweight='bold')
        axes[1, 0].set_title('Job Positions by Location', fontsize=12, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        plt.setp(axes[1, 0].xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Position distribution
        position_counts = jobs_df['position'].value_counts()
        axes[1, 1].barh(position_counts.index, position_counts.values, color='#16a085', edgecolor='black', linewidth=1.5)
        axes[1, 1].set_xlabel('Number of Positions', fontsize=11, fontweight='bold')
        axes[1, 1].set_title('Job Positions by Role', fontsize=12, fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        plt.savefig('/home/ubuntu/job_analytics.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("Saved: job_analytics.png")
        
        # 3. Recommendation Analysis
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Match score distribution
        axes[0, 0].hist(recommendations_df['match_score'], bins=20, color='#3498db', edgecolor='black', linewidth=1.5)
        axes[0, 0].set_xlabel('Match Score', fontsize=11, fontweight='bold')
        axes[0, 0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
        axes[0, 0].set_title('Resume Match Score Distribution', fontsize=12, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        
        # Status distribution
        status_counts = recommendations_df['status'].value_counts()
        colors = {'Recommended': '#2ecc71', 'Applied': '#3498db', 'Rejected': '#e74c3c', 'Shortlisted': '#f39c12', 'Offered': '#9b59b6'}
        color_list = [colors.get(status, '#95a5a6') for status in status_counts.index]
        axes[0, 1].bar(status_counts.index, status_counts.values, color=color_list, edgecolor='black', linewidth=1.5)
        axes[0, 1].set_ylabel('Number of Recommendations', fontsize=11, fontweight='bold')
        axes[0, 1].set_title('Recommendation Status Distribution', fontsize=12, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        plt.setp(axes[0, 1].xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Top companies by recommendations
        top_companies = recommendations_df['company'].value_counts().head(10)
        axes[1, 0].barh(top_companies.index, top_companies.values, color='#e67e22', edgecolor='black', linewidth=1.5)
        axes[1, 0].set_xlabel('Number of Recommendations', fontsize=11, fontweight='bold')
        axes[1, 0].set_title('Top 10 Companies by Recommendations', fontsize=12, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3, axis='x')
        
        # Average match score by status
        avg_score_by_status = recommendations_df.groupby('status')['match_score'].mean().sort_values(ascending=False)
        axes[1, 1].bar(avg_score_by_status.index, avg_score_by_status.values, color='#16a085', edgecolor='black', linewidth=1.5)
        axes[1, 1].set_ylabel('Average Match Score', fontsize=11, fontweight='bold')
        axes[1, 1].set_title('Average Match Score by Status', fontsize=12, fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        plt.setp(axes[1, 1].xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig('/home/ubuntu/recommendation_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("Saved: recommendation_analysis.png")
        
        # 4. Model Performance
        results_df = pd.read_csv('/home/ubuntu/model_results.csv')
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Model accuracy comparison
        x = np.arange(len(results_df))
        width = 0.2
        
        axes[0].bar(x - width, results_df['Accuracy'], width, label='Accuracy', color='#3498db', edgecolor='black', linewidth=1.5)
        axes[0].bar(x, results_df['Precision'], width, label='Precision', color='#2ecc71', edgecolor='black', linewidth=1.5)
        axes[0].bar(x + width, results_df['Recall'], width, label='Recall', color='#e74c3c', edgecolor='black', linewidth=1.5)
        
        axes[0].set_ylabel('Score', fontsize=11, fontweight='bold')
        axes[0].set_title('Model Performance Comparison', fontsize=12, fontweight='bold')
        axes[0].set_xticks(x)
        axes[0].set_xticklabels(results_df['Model'])
        axes[0].legend()
        axes[0].grid(True, alpha=0.3, axis='y')
        
        # F1-Score comparison
        axes[1].bar(results_df['Model'], results_df['F1_Score'], color='#f39c12', edgecolor='black', linewidth=1.5)
        axes[1].set_ylabel('F1-Score', fontsize=11, fontweight='bold')
        axes[1].set_title('F1-Score Comparison', fontsize=12, fontweight='bold')
        axes[1].grid(True, alpha=0.3, axis='y')
        plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig('/home/ubuntu/model_performance.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("Saved: model_performance.png")

def main():
    print("="*80)
    print("AI-DRIVEN CAMPUS PLACEMENT REGISTRATION AND RESUME MATCHING PLATFORM")
    print("="*80)
    
    print("\n[1] Initializing placement platform...")
    platform = PlacementPlatform()
    
    print("\n[2] Generating student data...")
    platform.generate_student_data(n_students=300)
    
    print("\n[3] Generating job data...")
    platform.generate_job_data(n_jobs=150)
    
    print("\n[4] Generating job recommendations...")
    platform.generate_recommendations()
    
    print("\n[5] Training placement prediction models...")
    platform.train_placement_models()
    
    print("\n[6] Generating visualizations...")
    platform.generate_visualizations()
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE - All files generated successfully")
    print("="*80)

if __name__ == "__main__":
    main()

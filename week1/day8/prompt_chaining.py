import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from time import sleep

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("Api Error, There's no api_key")

client = Groq(api_key = my_api_key)

model = "qwen/qwen3.8-27b"
role = "user"

JD = """
Key Responsibilities1. Business Problem Solving & Analytics
Partner closely with cross-functional teams across Business, Product, Technology, Operations, Risk, and other functions to identify and define high-impact business problems.
Translate ambiguous business requirements into structured analytical problem statements and actionable hypotheses.
Independently identify relevant data sources, define analytical logic, and build robust solutions.
Generate actionable insights that influence business strategy and decision-making.
2. Data & Technical Expertise
Work extensively with large and complex datasets to extract, process, and analyse information.
Build efficient and scalable data solutions using SQL and Python.
Develop advanced analytical models, automation frameworks, and reusable datasets.
Ensure accuracy, robustness, and scalability of analytical solutions.
3. Dashboarding & Data Storytelling
Build intuitive and insightful dashboards using Tableau or similar visualization tools.
Go beyond reporting by identifying the underlying business drivers and translating data into actionable insights.
Develop self-service analytical solutions that enable stakeholders to independently access relevant information.
4. AI & Advanced Analytics
Identify opportunities to leverage AI and Generative AI to improve analytical workflows, business decision-making, and operational efficiency.
Build and experiment with AI-enabled solutions, including applications leveraging LLMs, automation, and intelligent decision systems.
Drive the adoption of AI within analytics to reduce manual effort and improve the speed and quality of insights.
Stay updated with emerging AI technologies and translate relevant capabilities into practical business use cases.
5. Cross-functional Collaboration
Work directly with senior stakeholders to understand business challenges and independently drive analytical initiatives.
Collaborate with Data Engineering, Technology, Product, and Business teams to ensure the availability and usability of relevant data.
Act as a bridge between business and technical teams by converting business problems into clear analytical requirements.
6. Ownership & Execution
Take complete ownership of analytical initiatives from problem definition to implementation and impact measurement.
Proactively identify opportunities and problems rather than waiting for detailed instructions.
Operate effectively in an ambiguous and fast-paced environment.
Challenge existing approaches and continuously look for opportunities to improve processes, tools, and decision-making.

What We Are Looking ForThe ideal candidate is:
High on ownership, taking responsibility for outcomes rather than just completing assigned tasks.
Hands-on technically, with the ability to independently work with SQL, Python, Tableau, and large datasets.
AI-native, with practical experience experimenting with and building AI-enabled solutions.
Business-oriented, with the ability to engage confidently with senior stakeholders and influence decisions.
Collaborative, with a strong ability to work across functions and bring different teams together to solve problems.
Experience in fintech is preferable.
"""

Resume = """
KHUSHEE YADAV
Data Analyst
Greater Noida, India  |  +91 90587 66554  |  khusheey569@gmail.com
linkedin.com/in/khushee-yadav  |  github.com/khsuhiyadav97  |  khsuhiyadav97.github.io/portfolio
SKILLS
Languages: Python, SQL
Analysis: Pandas, NumPy, SciPy, Excel, EDA, ETL, Data Cleaning, Feature Engineering
Visualization: Power BI, Tableau, Plotly, Seaborn, Matplotlib, Jupyter Notebook
Databases: SQLite, MySQL, PostgreSQL, SQLAlchemy
Tools: Git, GitHub, VS Code, Google Colab, Google Workspace, Agile
Soft Skills: Communication, Teamwork, Problem-Solving
EDUCATION
Bachelor of Computer Applications (BCA)   2024 – 2027 (Expected)
Indira Gandhi National Open University (IGNOU), Delhi
Relevant coursework: Data Structures, DBMS, Computer Networks, AI & ML
12th Grade — Science   90.2%
GMIC, Etawah (UP), UPMSP
EXPERIENCE / INTERNSHIPS
Data Analyst Intern — Bluestock Fintech  |  Remote (Part-time)  |  June 2026 – August 2026
• Built and automated an ETL pipeline in Python, SQL, and SQLite that cleaned and loaded 100,000+ scattered
AMFI mutual fund records into one dataset, replacing manual report generation with an automated process.
• Built a second ETL pipeline for Nifty100 market data in Python and SQL, cleaning inconsistent records so the
data became usable for trend analysis and dashboards.
PROJECTS
Mutual Fund Analytics Platform — 2026
github.com/khsuhiyadav97/Mutual-Fund-Analytics
• Combined 10 separate AMFI datasets (100,000+ rows) into a single 6-table SQLite database using an
automated SQLAlchemy pipeline, enabling fund comparison and trend tracking across the full dataset.
• Calculated Sharpe Ratio, Sortino Ratio, Alpha, Beta, CAGR, and Maximum Drawdown for 40 funds, then built a
0–100 scorecard to make risk-versus-return comparison easier.
• Built 9 Plotly/Seaborn visualizations and 10 SQL queries to surface patterns such as YoY SIP growth and
differences in expense ratios across funds.
Spotify Track Popularity Analysis — 2026
github.com/khsuhiyadav97/Music_Insights
• Cleaned and merged two Kaggle datasets in Pandas, resolving missing values, duplicates, and inconsistent
labels, to identify which audio features affect track popularity, finding that popular tracks tend to be louder, more
energetic, and less acoustic.
• Built a Power BI dashboard with KPI cards, scatter plots, and a genre filter so people without a data background
could explore the findings themselves.
"""

def ask_llm(system_prompt, user_prompt):
    system_message = {
        "role" : "system",
        "content" : system_prompt
    }
    user_message = {
        "role": "user",
        "content": user_prompt
    }
    messages = [system_message, user_message]
    response = client.chat.completions.create(model=model, messages= messages)
    answer = response.choices[0].message.content
    return answer

def extract_resume():
    system_prompt = """
You are a professional HR assistant
Your job is to extract the infromation from resume.
Do not make or invent other infromation that is not present"""

    user_prompt = f"""
Extract the following information from this resume:

    - Name
    - Email
    - Phone
    - Skills
    - Education
    - Work experience
    - Projects
    - Certifications

    Resume: {Resume}
"""
    return ask_llm(system_prompt, user_prompt)

def extract_jd():
    system_prompt = """
    You are a professional HR assistant
    Your job is to extract the infromation from JD.
    Do not make or invent other infromation that is not present"""

    user_prompt = f"""
Extract the infromation from Job Description:

Job title
Required skills
Required experience
Responsibilities
Required education
Preferred/nice-to-have skills
Certifications
Location
Employment type 
Key requirements 

Job_desciption = {JD}
"""
    return ask_llm(system_prompt, user_prompt)

def match():
    system_prompt = """
        You are a professional HR assistant
        Your job is to extract the infromation from JD and resume and match them, and give it a score between 1-100. Give a small verdict.
        Do not make or invent other infromation that is not present"""
    
    user_prompt = f"""
    Compare the extracted resume data against the extracted JD data.
    
     Extracted_Job_desciption = {jd}
     Extracted_Resume = {candidate}

 Give:
    - Match score from 1-100
    - Matching skills
    - Missing required skills
    - Experience match
    - Education match
    - Small verdict

    """
    return ask_llm(system_prompt, user_prompt)


candidate = extract_resume()
print(candidate)
sleep(2)
jd = extract_jd()
print(jd)
sleep(2)
score = match()
print(score)


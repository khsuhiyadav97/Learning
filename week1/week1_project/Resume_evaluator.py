import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("Api Error, There's no api_key")

client = Groq(api_key = my_api_key)

model = "qwen/qwen3.6-27b"
role = "Experienced HR Assistant"
# Structured format information

from pydantic import BaseModel

class Job_desciption(BaseModel):
    role : str
    required_skills : list[str]
    preferred_skills : list[str]
    experience : float | None
    educational_requirements : list[str]
    responsibilities : list[str]


jd_schema = Job_desciption.model_json_schema()

system_prompt = f"""
You are an experienced HR assistant. Your job is to analyse the job desciptions and extract structured information from these. Return only valid json matching this schema. {jd_schema}
Important:
 Do not return the schema itself.
 Do not return fields like "properties", "title", or "type".
 Fill this schema with the actual extracted info from this schema

 If minimum experience is not mentioned, return null.
 If information from a list is missing, return an empty list.
 Do not invent information.
"""

message_system = {
    "role": "system",
    "content": system_prompt
}
job_desciption = """Do you want to work on a product that is used by millions of people around the world daily, and growing rapidly? Do you care deeply about how software is designed with a focus on supporting global scale? Do you want to be part of a world-class team that continuously pushes the boundary of service and engineering excellence?

The Office Web Shared Org in IDC is looking for a Senior Software Engineer who is passionate about working on high-scale geo-distributed WXP Shared Platform. Web Shared is gearing up for investment in world class fundamentals for Office apps like performance and reliability along with adding Copilot value to Office. If you want hands-on experience in designing, building, re-architecting the apps that truly impact the customers across the world at a scale not found often in the industry – this is the role for you.

Microsoft’s mission is to empower every person and every organization on the planet to achieve more. As employees we come together with a growth mindset, innovate to empower others, and collaborate to realize our shared goals. Each day we build on our values of respect, integrity, and accountability to create a culture of inclusion where everyone can thrive at work and beyond.

Responsibilities

Core responsibilities include designing, owning and shipping software, writing secure, reliable, scalable and maintainable code.
Syncing with other teams for product features that span across teams and geographies, figuring out dependencies and driving them to completion.
You should have a solid understanding of the software development cycle.  
Successful candidates should have ability to ramp up quickly on new technologies and adopt solution from within the company or from the Open-Source community. In addition, solid problem solving & debugging skills are necessary.  
Candidate will be regularly participating in on call and reviewing customer feedback.  
Candidate is expected to make architectural changes in application to make it modernize, performant and reliable.  
Candidate will be helping other team members by actively working with them and participating in design and code reviews. Candidate will be growing team knowledge with regular knowledge sessions.  
Candidate must be self-driven, curious to learn, proactive, result oriented, a thought leader having solid communication and influencing skills.
Identifying opportunities to leveraging AI for making the organization more productive. 

Qualifications

Required/Minimum Qualifications:

Bachelor's Degree in Computer Science or related technical field AND 4+ years technical engineering experience with coding in languages including, but not limited to, C, C++, C#, Java, JavaScript, or Python.
OR equivalent experience.
Additional Or Preferred Qualifications

Other Requirements: Ability to meet Microsoft, customer and/or government security screening requirements are required for this role. These requirements include but are not limited to the following specialized security screenings:

Microsoft Cloud Background Check: This position will be required to pass the Microsoft Cloud background check upon hire/transfer and every two years thereafter. 

Preferred Qualifications

7+ years of professional experience designing, developing, testing, and shipping software.  
Proficiency in either service (C#, Java, etc.) and web (HTML5 and JavaScript/TypeScript, Webpack, react) technologies.  
Demonstrated technical aptitude for architecture, design, development, debugging, testing, etc.  
Experience with cloud platforms and services, such as Azure, AWS, or Google Cloud. 
Deep interest in AI, machine learning, or data science, or related technologies. 
Excellent communication, collaboration, and problem-solving skills. 
Ability to work independently and as part of a team in a fast-paced and dynamic environment. 
Passion for learning new skills and technologies and sharing them with others. 

This position will be open for a minimum of 5 days, with applications accepted on an ongoing basis until the position is filled.

Microsoft is an equal opportunity employer. All qualified applicants will receive consideration for employment without regard to age, ancestry, citizenship, color, family or medical care leave, gender identity or expression, genetic information, immigration status, marital status, medical condition, national origin, physical or mental disability, political affiliation, protected veteran or military status, race, ethnicity, religion, sex (including pregnancy), sexual orientation, or any other characteristic protected by applicable local laws, regulations and ordinances. If you need assistance with religious accommodations and/or a reasonable accommodation due to a disability during the application process, read more about requesting accommodations."""

prompt = f"""
Analyze the following job description {job_desciption}
"""
message_user = {
    "role" : "user",
    "content" : prompt
}
response_format = {
    "type" : "json_object"
}
messages = [message_system, message_user]
response = client.chat.completions.create(model = model, messages = messages, response_format = response_format)

answer = response.choices[0].message.content

# Load
import json
raw_json = answer
job_data = json.loads(raw_json)
jobD = Job_desciption(**job_data)

# You can see it directly
print(jobD.experience)
print(jobD.required_skills)


# Parsing
class MatchResult(BaseModel):
    score : float
    details : dict

class Experience(BaseModel):
    company : str | None = None
    role : str | None = None
    duration : str | None = None
    description : str | None = None
    skills_used : list[str] = []

class resume(BaseModel):
    name : str | None = None
    email : str | None = None
    phone : str | None = None

    total_experience_years : float | None = None

    skills : list[str] = []
    experinces : list[Experience] = []
    education : list[str] = []
    project : list[str] = []
    certifications : list[str] = []

resume_schema = resume.model_json_schema()

def final_score(job, Reusme):
    match_schema = MatchResult.model_json_schema()
    prompt = f"""You are an HR recruiter. 
    Compare the candidate's resume with the job description.
    
    JOB DESCRIPTION: 
    {job.model_dump_json(indent=2)}

    CANDIDATE RESUME:
    {resume.model_dumps_json(indent = 2)}
Return json matching this schema:
 {match_schema}

Give me:

1- Candidate's name
2- Matching skills
3- Missing important skills
4- Whether experience requirement is not
5- Overall matching percentage 0 to 100
6- A short final verdict."""


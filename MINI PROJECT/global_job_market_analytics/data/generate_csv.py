import csv, os, random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'csv')
os.makedirs(OUT, exist_ok=True)

COUNTRIES = [
    ('US','United States','North America','USD',63543,330000000),
    ('IN','India','Asia','INR',2277,1380000000),
    ('GB','United Kingdom','Europe','GBP',46510,67000000),
    ('CA','Canada','North America','CAD',52051,38000000),
    ('DE','Germany','Europe','EUR',50801,83000000),
    ('AU','Australia','Oceania','AUD',55060,26000000),
    ('SG','Singapore','Asia','SGD',65233,5900000),
    ('JP','Japan','Asia','JPY',39285,126000000),
    ('NL','Netherlands','Europe','EUR',57768,17600000),
    ('AE','United Arab Emirates','Middle East','AED',43103,10000000),
]

ROLES = [
    (1,'Software Engineer','Engineering','Mid-Senior',5),
    (2,'Data Analyst','Data & AI','Mid',3),
    (3,'Data Scientist','Data & AI','Senior',5),
    (4,'Machine Learning Engineer','Data & AI','Senior',6),
    (5,'AI Engineer','Data & AI','Senior',7),
    (6,'Web Developer','Engineering','Mid',3),
    (7,'Full Stack Developer','Engineering','Mid-Senior',4),
    (8,'Cloud Engineer','Infrastructure','Senior',5),
    (9,'DevOps Engineer','Infrastructure','Senior',5),
    (10,'Cyber Security Analyst','Security','Mid-Senior',4),
    (11,'Business Analyst','Business','Mid',3),
    (12,'UI/UX Designer','Design','Mid',3),
    (13,'Product Manager','Management','Senior',6),
    (14,'Database Administrator','Data & AI','Mid',3),
    (15,'Network Engineer','Infrastructure','Mid',3),
]

SKILLS = {
    1: [('Python','Technical',22),('Java/C++','Technical',18),('SQL','Technical',12),('Git/CI-CD','Technical',10),('Cloud Platforms','Technical',8),('Problem-Solving','Soft',10),('Communication','Soft',8),('Team Collaboration','Soft',7),('Critical Thinking','Soft',5)],
    2: [('SQL','Technical',25),('Python','Technical',20),('Data Viz Tools','Technical',15),('Excel','Technical',10),('Communication','Soft',12),('Critical Thinking','Soft',10),('Problem-Solving','Soft',8)],
    3: [('Python (Scikit/TF)','Technical',28),('SQL','Technical',18),('ML Algorithms','Technical',15),('Cloud Platforms','Technical',8),('Critical Thinking','Soft',10),('Communication','Soft',8),('Problem-Solving','Soft',8),('Team Collaboration','Soft',5)],
    4: [('Python (PyTorch/TF)','Technical',30),('MLOps/DevOps','Technical',18),('Cloud Platforms','Technical',14),('SQL','Technical',8),('Problem-Solving','Soft',10),('Critical Thinking','Soft',8),('Team Collaboration','Soft',7),('Adaptability','Soft',5)],
    5: [('Python (LLMs/TF)','Technical',32),('Cloud Platforms','Technical',18),('MLOps/DevOps','Technical',12),('SQL','Technical',7),('Problem-Solving','Soft',12),('Adaptability','Soft',8),('Communication','Soft',6),('Leadership','Soft',5)],
    6: [('JavaScript','Technical',25),('HTML/CSS','Technical',20),('Node.js','Technical',15),('SQL','Technical',10),('Communication','Soft',12),('Problem-Solving','Soft',10),('Adaptability','Soft',8)],
    7: [('JavaScript/Node.js','Technical',22),('Python/Backend','Technical',18),('SQL','Technical',15),('Cloud/DevOps','Technical',12),('HTML/CSS','Technical',8),('Problem-Solving','Soft',10),('Communication','Soft',8),('Team Collaboration','Soft',7)],
    8: [('AWS/Azure/GCP','Technical',30),('DevOps Tools','Technical',20),('Python/Scripting','Technical',15),('Networking','Technical',10),('Problem-Solving','Soft',10),('Adaptability','Soft',8),('Communication','Soft',7)],
    9: [('DevOps Tools','Technical',28),('Cloud Platforms','Technical',22),('Python/Shell','Technical',15),('SQL/Databases','Technical',8),('Problem-Solving','Soft',12),('Team Collaboration','Soft',8),('Communication','Soft',7)],
    10:[('Security Tools','Technical',25),('Networking','Technical',20),('Python/Scripting','Technical',15),('SQL','Technical',8),('Critical Thinking','Soft',14),('Problem-Solving','Soft',10),('Communication','Soft',8)],
    11:[('SQL','Technical',20),('Data Viz Tools','Technical',18),('Excel','Technical',12),('Python (basics)','Technical',8),('Communication','Soft',18),('Critical Thinking','Soft',12),('Problem-Solving','Soft',12)],
    12:[('Design Tools','Technical',30),('HTML/CSS','Technical',18),('Prototyping','Technical',12),('User Research','Technical',8),('Creativity','Soft',14),('Communication','Soft',10),('Adaptability','Soft',8)],
    13:[('SQL/Analytics','Technical',18),('Data Viz Tools','Technical',12),('Roadmapping Tools','Technical',10),('Leadership','Soft',20),('Communication','Soft',18),('Critical Thinking','Soft',12),('Team Collaboration','Soft',10)],
    14:[('SQL','Technical',35),('Database Systems','Technical',25),('Python/Scripting','Technical',12),('Cloud Platforms','Technical',8),('Problem-Solving','Soft',10),('Communication','Soft',7),('Critical Thinking','Soft',3)],
    15:[('Networking Protocols','Technical',30),('Network Tools','Technical',22),('Python/Scripting','Technical',12),('Cloud Networking','Technical',10),('Problem-Solving','Soft',12),('Communication','Soft',8),('Team Collaboration','Soft',6)],
}

BASE_SALARIES = {
    ('US',1):125000,('US',2):88000,('US',3):130000,('US',4):150000,('US',5):160000,('US',6):88000,('US',7):115000,('US',8):140000,('US',9):133000,('US',10):109000,('US',11):91000,('US',12):95000,('US',13):145000,('US',14):101000,('US',15):90000,
    ('IN',1):19800,('IN',2):13800,('IN',3):23500,('IN',4):30000,('IN',5):34000,('IN',6):11800,('IN',7):17500,('IN',8):22500,('IN',9):21300,('IN',10):18200,('IN',11):14200,('IN',12):12800,('IN',13):25500,('IN',14):15200,('IN',15):13200,
    ('GB',1):78000,('GB',2):54000,('GB',3):84000,('GB',4):96000,('GB',5):103000,('GB',6):54000,('GB',7):70000,('GB',8):87000,('GB',9):82000,('GB',10):68000,('GB',11):56000,('GB',12):58000,('GB',13):91000,('GB',14):63000,('GB',15):57000,
    ('CA',1):96000,('CA',2):67000,('CA',3):101000,('CA',4):117000,('CA',5):125000,('CA',6):67000,('CA',7):87000,('CA',8):107000,('CA',9):101000,('CA',10):84000,('CA',11):70000,('CA',12):73000,('CA',13):111000,('CA',14):78000,('CA',15):70000,
    ('DE',1):75000,('DE',2):54000,('DE',3):80000,('DE',4):92000,('DE',5):98000,('DE',6):54000,('DE',7):68000,('DE',8):82000,('DE',9):77000,('DE',10):64000,('DE',11):56000,('DE',12):57000,('DE',13):87000,('DE',14):61000,('DE',15):56000,
    ('AU',1):91000,('AU',2):64000,('AU',3):97000,('AU',4):111000,('AU',5):119000,('AU',6):64000,('AU',7):83000,('AU',8):102000,('AU',9):97000,('AU',10):80000,('AU',11):67000,('AU',12):70000,('AU',13):106000,('AU',14):76000,('AU',15):68000,
    ('SG',1):85000,('SG',2):60000,('SG',3):91000,('SG',4):104000,('SG',5):112000,('SG',6):60000,('SG',7):78000,('SG',8):96000,('SG',9):90000,('SG',10):75000,('SG',11):62000,('SG',12):65000,('SG',13):100000,('SG',14):70000,('SG',15):64000,
    ('JP',1):56000,('JP',2):39500,('JP',3):61000,('JP',4):71000,('JP',5):76000,('JP',6):39500,('JP',7):52000,('JP',8):64000,('JP',9):60000,('JP',10):52000,('JP',11):43500,('JP',12):45500,('JP',13):66500,('JP',14):47500,('JP',15):43500,
    ('NL',1):79000,('NL',2):57000,('NL',3):84000,('NL',4):96000,('NL',5):102000,('NL',6):57000,('NL',7):71000,('NL',8):86000,('NL',9):81000,('NL',10):67000,('NL',11):59000,('NL',12):61000,('NL',13):91000,('NL',14):64000,('NL',15):59000,
    ('AE',1):71000,('AE',2):50000,('AE',3):76000,('AE',4):87000,('AE',5):94000,('AE',6):50000,('AE',7):63000,('AE',8):78000,('AE',9):73000,('AE',10):60000,('AE',11):54000,('AE',12):56000,('AE',13):82000,('AE',14):58000,('AE',15):54000,
}

YEAR_MULT = {2015:0.72,2016:0.76,2017:0.80,2018:0.85,2019:0.90,2020:0.87,2021:0.92,2022:0.97,2023:1.05,2024:1.12,2025:1.20}

ROLE_GROWTH = {
    1:[100,104,109,115,121,118,124,130,142,158,172],
    2:[100,105,111,118,126,122,129,137,151,168,185],
    3:[100,107,115,124,134,130,139,149,166,187,210],
    4:[100,109,119,130,143,138,149,161,183,212,245],
    5:[100,110,122,135,150,145,157,171,198,235,278],
    6:[100,103,107,111,115,112,116,120,126,133,140],
    7:[100,105,111,117,124,120,127,134,147,162,178],
    8:[100,108,117,127,138,134,144,155,172,193,215],
    9:[100,107,115,123,132,128,137,147,162,180,199],
    10:[100,106,113,120,128,124,132,141,157,176,196],
    11:[100,103,107,111,115,112,116,120,126,133,140],
    12:[100,104,109,114,120,117,122,127,135,144,153],
    13:[100,105,111,117,124,120,127,134,147,160,175],
    14:[100,102,105,108,111,108,111,114,119,124,129],
    15:[100,102,104,107,110,107,110,113,118,123,128],
}

POSTINGS_BASE = {1:45,2:38,3:32,4:28,5:22,6:42,7:48,8:30,9:33,10:27,11:40,12:35,13:38,14:25,15:28}
COUNTRY_FACTOR = {'US':1.0,'IN':0.85,'GB':0.78,'CA':0.90,'DE':0.88,'AU':0.95,'SG':1.0,'JP':0.82,'NL':0.88,'AE':0.72}

# 1. countries.csv
with open(f'{OUT}/countries.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['code','name','region','currency','gdp_per_capita','population'])
    w.writerows(COUNTRIES)
print("countries.csv done")

# 2. job_roles.csv
with open(f'{OUT}/job_roles.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['id','title','category','experience_level','avg_years_exp'])
    w.writerows(ROLES)
print("job_roles.csv done")

# 3. salary_data.csv
rows = []
sid = 1
for (code,_,_,_,_,_) in COUNTRIES:
    for (rid,title,_,_,_) in ROLES:
        hybrid = BASE_SALARIES.get((code,rid),50000)
        for mode,factor in [('Onsite',0.96),('Hybrid',1.0),('Remote',1.03)]:
            avg = round(hybrid*factor)
            rows.append([sid,code,rid,mode,avg,round(avg*0.72),round(avg*1.38),round(avg*0.15)])
            sid+=1
with open(f'{OUT}/salary_data.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['id','country_code','role_id','work_mode','avg_salary_usd','min_salary_usd','max_salary_usd','avg_bonus_usd'])
    w.writerows(rows)
print(f"salary_data.csv done — {len(rows)} rows")

# 4. salary_trends.csv
rows = []
tid = 1
years = list(range(2015,2026))
for (code,_,_,_,_,_) in COUNTRIES:
    for (rid,_,_,_,_) in ROLES:
        base = BASE_SALARIES.get((code,rid),50000)
        for i,yr in enumerate(years):
            avg = round(base * list(YEAR_MULT.values())[i])
            rows.append([tid,code,rid,yr,avg,round(avg*1.02 if yr!=2020 else avg*0.98),round(avg*0.98 if yr!=2020 else avg*1.02)])
            tid+=1
with open(f'{OUT}/salary_trends.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['id','country_code','role_id','year','avg_salary_usd','q3_salary_usd','q1_salary_usd'])
    w.writerows(rows)
print(f"salary_trends.csv done — {len(rows)} rows")

# 5. demand_trends.csv
rows = []
did = 1
for (code,_,_,_,_,_) in COUNTRIES:
    for (rid,_,_,_,_) in ROLES:
        cf = COUNTRY_FACTOR.get(code,1.0)
        for i,yr in enumerate(years):
            idx = round(ROLE_GROWTH[rid][i],1)
            posts = round(POSTINGS_BASE[rid]*cf*ROLE_GROWTH[rid][i]/100,1)
            rows.append([did,code,rid,yr,idx,posts,round(posts*0.3,1)])
            did+=1
with open(f'{OUT}/demand_trends.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['id','country_code','role_id','year','demand_index','job_postings_thousands','remote_postings_thousands'])
    w.writerows(rows)
print(f"demand_trends.csv done — {len(rows)} rows")

# 6. skills.csv
rows = []
sid2 = 1
for rid,skills in SKILLS.items():
    for sname,stype,pct in skills:
        rows.append([sid2,rid,sname,stype,pct])
        sid2+=1
with open(f'{OUT}/skills.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['id','role_id','skill_name','skill_type','percentage'])
    w.writerows(rows)
print(f"skills.csv done — {len(rows)} rows")

# 7. job_postings.csv  (synthetic individual postings — 500 rows)
import random, datetime
random.seed(42)
companies = ['Google','Microsoft','Amazon','Meta','Apple','Netflix','Uber','Airbnb','Stripe','Palantir','IBM','Accenture','Deloitte','TCS','Infosys','Wipro','SAP','Oracle','Salesforce','Adobe']
exp_levels = ['Entry','Mid','Senior','Lead','Principal']
rows = []
for i in range(1,501):
    code = random.choice([c[0] for c in COUNTRIES])
    rid  = random.randint(1,15)
    base = BASE_SALARIES.get((code,rid),50000)
    mode = random.choice(['Onsite','Hybrid','Remote'])
    factor = {'Onsite':0.96,'Hybrid':1.0,'Remote':1.03}[mode]
    sal  = round(base*factor*(0.85+random.random()*0.3))
    yr   = random.randint(2022,2025)
    mo   = random.randint(1,12)
    rows.append([i,random.choice(companies),code,rid,mode,sal,random.choice(exp_levels),f"{yr}-{mo:02d}-01",random.randint(10,500)])
with open(f'{OUT}/job_postings.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['id','company','country_code','role_id','work_mode','salary_usd','experience_level','posted_date','applicants'])
    w.writerows(rows)
print(f"job_postings.csv done — {len(rows)} rows")

# 8. cost_of_living.csv
col_data = [
    ('US',100,3200,18,55,1.5),('IN',28,450,4,12,0.4),('GB',92,2800,16,50,1.4),
    ('CA',88,2400,15,48,1.3),('DE',82,1800,12,40,1.2),('AU',90,2300,14,45,1.35),
    ('SG',95,3000,10,50,1.45),('JP',78,1800,8,38,1.1),('NL',86,1900,13,42,1.25),('AE',85,2500,6,45,0.0),
]
with open(f'{OUT}/cost_of_living.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['country_code','col_index','avg_rent_usd','meal_cost_usd','transport_monthly_usd','income_tax_rate'])
    w.writerows(col_data)
print("cost_of_living.csv done")

print("\nAll 8 CSV datasets generated successfully!")

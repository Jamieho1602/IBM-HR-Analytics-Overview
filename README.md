
<img width="220" height="220" alt="HR Icon" src="https://github.com/user-attachments/assets/52ef2b35-b4fe-49db-85ee-a00e4b02cbda" />





**IBM HR Analytics - Employee Attrition & Predictive Modelling**

**Project Title : Identify Key Factors Associated with Employee Attrition and Improving Employee Retention**

**Tools: Python / Google Colab / Power BI / Logistic Regression**

**Prepared by Jamie Ho** 


## **Contents**
1. Project Overview
2. Five Research Problem Statements
3. Research Objectives
4. Dataset Overview
5. Methodology Application
6. Key Findings
7. Power BI Dashboard
8. HR Recommendations and Conclusion


## 📌 **Project Overview**

Employee attrition is a key HR challenge affecting workforce stability, productivity and organisational costs.

This project uses the **IBM HR Analytics sample dataset** to explore employee turnover patterns, identify factors associated with attrition and develop data-driven HR retention recommendations.

The project combines data analytics, predictive modelling and HR knowledge to identify factors associated with employee attrition and develop practical retention strategies guided by the Six Pillars of Total Rewards.


## 🎯 **Research Problem Statements And Objectives**

**1. Employee Attrition**

-   Problem: Which departments and job roles experience higher employee turnover?
-   Objective: Analyse attrition patterns across departments and job roles to identify priority areas for retention.

**2. Compensation & Rewards**

-   Problem : Are compensation and stock option levels associated with employee attrition?
-   Objective : Examine monthly income, job levels and stock option levels to identify potential compensation-related retention concerns.

**3. Employee Experience**

-   Problem : How do overtime, business travel and work-life balance relate to employee turnover?
-   Objective : Analyse working conditions and work-life balance to identify potential employee retention challenges.

**4. Employee Engagement**

-   Problem : Are employees with lower job satisfaction and job involvement more likely to leave?
-   Objective : Examine the relationship between employee engagement indicators and attrition.

**5. Talent Management & Retention**

-   Problem : How do employee tenure, performance ratings and promotion history relate to employee retention?
-   Objective : Identify retention challenges associated with career progression and employee tenure.


## 📊 Dataset Overview

| Description | Details |
|---|---|
| Dataset | IBM HR Analytics – Employee Attrition |
| Data Sources | Five HR datasets |
| Employees Analysed | 1,465 |
| Employees Who Left | 237 |
| Overall Attrition Rate | 16.18% |
| Target Variable | Attrition (Yes / No) |

The dataset is used for learning and demonstration purposes and does not represent an actual employer's workforce.


## 🛠️ Methodology

The project follows an end-to-end data analytics workflow using Python, Google Colab and Power BI, from data understanding and preparation to predictive modelling and HR recommendations.

**1. Data Understanding, Preparation & Cleaning**

-   Imported five HR datasets into Google Colab using Python and Pandas.
-   Explored the datasets to understand their structure, variables, data types and employee information.
-   Checked for missing values, duplicate records and data inconsistencies.
-   Removed five employee records with missing Age values, reducing the dataset from 1,470 to 1,465 employees.
-   Cleaned and standardised inconsistent data to improve data quality and reliability.

**2. Data Merging & Validation**

-   Merged the five cleaned HR datasets using the common employee identifier (EmployeeNumber).
-   Checked the merged data for consistency, duplicate employee records and data integrity.
-   Validated the final dataset containing 1,465 employees and 37 columns.

**3. Exploratory Data Analysis (EDA)**

-   Explored employee demographics, compensation, work experience, performance and employment status.
-   Analysed attrition patterns across departments, job roles and employee characteristics.
-   Examined relationships between attrition and monthly income, stock options, overtime, business travel, job satisfaction, job involvement and employee tenure.
-   Identified trends and patterns to support HR retention recommendations.

**4. Data Visualisation – Power BI**

-   Developed five interactive dashboard pages to communicate the findings:
-   HR Attrition Overview
-   Compensation & Rewards
-   Employee Experience
-   Talent & Retention
-   Predictive Analytics

**5. Predictive Modelling – Logistic Regression**

-   Developed a Logistic Regression model using selected employee characteristics to predict attrition.
-   Split the dataset into training (80%) and testing (20%) sets.
-   Evaluated model performance using accuracy, precision, recall, F1-score and a confusion matrix.
-   Interpreted the model results to identify factors associated with employee attrition.

**6. HR Recommendations**

-   Translated the analytical findings into practical HR retention recommendations using the Six Pillars of Total Rewards, focusing on compensation,
     work-life effectiveness, employee engagement and talent development.

## 🔎 Key Findings

**Compensation**: Employees who left had a lower average monthly income (4,787) than those who stayed (6,846). Employees without stock options recorded 24.48% attrition.

**Work-Life Effectiveness**: Employees working overtime recorded 30.53% attrition, compared with 10.49% among those without overtime.

**Employee Engagement**: Employees with the lowest job involvement rating recorded 33.73% attrition.

**Talent Retention**: Employees with 0–2 years of service recorded 29.91% attrition.

**Predictive Analytics**: The Logistic Regression model achieved 75.09% accuracy and 78.72% recall, with 37.00% precision.   


## 📈 Power BI Dashboard

The Power BI dashboard presents five analytical areas to explore employee attrition patterns, identify potential risk factors and support HR retention strategies.

**HR Attrition Overview** – Overall attrition trends and workforce demographics.

**Compensation & Rewards** – Relationships between compensation, stock options and attrition.

**Employee Experience** – Impact of overtime, business travel and employee satisfaction.

**Talent & Retention** – Attrition patterns associated with employee tenure and career progression.

**Predictive Analytics** – Logistic Regression results and model performance.

<img src="IBM%20HR%20Analytics%20Dashboard%20Overview.png" alt="IBM HR Analytics Portfolio" width="600">


## 💡 HR Recommendations

The findings support targeted employee retention strategies guided by the Six Pillars of Total Rewards:

**Compensation** – Benchmark salaries against external market rates for comparable job roles and levels, review internal pay equity, and evaluate long-term incentive (LTI) programmes, including stock options.

**Benefits** – Not evaluated, as employee benefits information was unavailable in the dataset.

**Work-Life Effectiveness** – Review excessive overtime and strengthen work-life balance.

**Recognition** – Not evaluated, as employee recongition information was unavilable in the dataset.

**Performance Management** – Review performance ratings, job involvement and employee engagement.

**Talent Development & Career Opportunities** – Strengthen early-tenure retention and review career progression and promotion opportunities.

These recommendations translate analytical findings into practical HR actions while acknowledging areas where additional data is required.


## 📁 Project Files

Python Notebook (IBM_HR_Analytics.ipynb) – Data understanding, cleaning, merging, exploratory data analysis (EDA) and Logistic Regression modelling.

**Power BI Dashboard:** [Download Power BI Dashboard](HR%20Analytics%20Presentation%20Recovered.pbix) – Five interactive dashboard pages covering HR Attrition Overview, Compensation & Rewards, Employee Experience, Talent & Retention, and Predictive Analytics.

Project Presentation – Summary of key findings, attrition patterns, predictive modelling results and HR recommendations guided by the Six Pillars of Total Rewards.

## 🌐 Interactive Streamlit Dashboard & Attrition Risk Simulator

Launch IBM HR Analytics Interactive Dashboard

The Streamlit application provides four interactive modules:

Executive Overview – Workforce KPIs and departmental attrition.

General Attrition – Analysis of overtime, job satisfaction and employee turnover.

High-Performer Retention – Analysis of attrition among high-performing employees.

Attrition Risk Simulator – Uses Logistic Regression to demonstrate how employee characteristics influence estimated attrition probabilities.
## Conclusion

This project demonstrates how Python, Power BI and predictive analytics can support evidence-based HR decision-making by identifying factors associated with employee attrition.

It also highlights the importance of combining data analytics with practical HR knowledge to develop employee retention strategies guided by a structured Total Rewards framework.

# 🍎 FooDee: Your Personalized Food Recommender for Diseases

## 📌 Overview
This project started from a simple question: *“If someone has a certain disease, what foods might actually help?”*  
Instead of just listing foods, we wanted to connect **genes, pathways, compounds, and food data** so the recommendations have some biological reasoning behind them.

---

## Data Sources
- **OMIM / Entrez Gene** – links between diseases and genes  
- **SMPDB** – molecular pathways and the compounds involved  
- **FooDB** – information on food constituents, amounts, and known health effects

By putting these together, we created a database that links:  
**Disease → Gene → Pathway → Compound → Food**

![ER Diagram](https://github.com/user-attachments/assets/79c49ac2-96b4-42fc-a611-ac3c6ee401f8)
*Entity–Relationship diagram*

---

## How It Works
We used PostgreSQL and Python to build the database.  
It supports five main queries:
1. **Find compounds related to a disease**  
   *Input:* disease name → *Output:* compounds involved in the pathways  

2. **Suggest foods for a disease**  
   Ranks foods by how much of those compounds they contain (top 5 shown).  

3. **Check health effects of a compound**  

4. **Find foods containing a specific compound**  

5. **Look up a compound’s description**  

---

## Validation Example
Case study: **Colorectal cancer (somatic)**  
- The database highlighted two compounds: **L-Methionine** and **Phytic acid**  
- Based on that, it suggested foods like *milk, red bell pepper, flaxseed, and carrot*  
- Looking into the literature:  
  - L-Methionine → results are mixed; some studies suggest a benefit, others don’t  
  - Phytic acid → consistently reported as anti-cancer / preventive  

So, the DB output was not random — it pointed us to compounds and foods that actually show up in research.

---

## Why It Matters
- It connects biomedical data to something practical: food choices  
- Helps explore how **diet, compounds, and diseases** might be linked  
- Can be a starting point for research, education, or just curiosity about food and health  
- And of course, it’s not a substitute for medical advice — more of a tool for exploration 😉

---

## Usage Example
| Menu | 0: Find compounds related to a disease | 1: Suggest foods for a disease |
|------|---------------------|-----------------|
| ![Menu](https://github.com/user-attachments/assets/b5fa8895-19c0-4587-b877-3cff65dba49b) | ![Disease → Compounds](https://github.com/user-attachments/assets/41659cd4-b9a4-46f6-8151-74afa9b736e8) | ![Disease → Foods](https://github.com/user-attachments/assets/b4e64ec5-7ef5-435c-8efe-98448909dce0) |

| 2: Check health effects of a compound | 3: Find foods containing a specific compound | 4: Look up a compound’s description |
|----------------------------|------------------|---------------|
| ![Compound → Health Effects](https://github.com/user-attachments/assets/2b6c2004-7595-4b9f-bf74-c09d5545b125) | ![Compound → Foods](https://github.com/user-attachments/assets/54e15cae-6eb8-45db-ac27-87da5640dc3a) | ![Compound Info](https://github.com/user-attachments/assets/79c76595-c035-47b3-be57-7a5aca8d5e2d) |


| Is L-Methionine intake effective against colorectal cancer? | Is Phytic acid intake effective against colorectal cancer? |
|---------------|---------------------|
| ![example1](https://github.com/user-attachments/assets/e00f35f6-e14c-4d38-8097-aaef5a40c931) | ![example2](https://github.com/user-attachments/assets/0db912a4-f833-4518-a434-1b47bcfd2093) |

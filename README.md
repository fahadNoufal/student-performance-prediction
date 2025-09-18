# 🎓 Student Performance Predictor

A simple web app that predicts **Math scores** based on **Reading** and **Writing** scores, along with demographic and parental education information.  
It visualizes the results with an interactive bar chart.

---

## 🚀 Features
- Input fields for:
  - Gender
  - Race/Ethnicity
  - Parental level of education
  - Lunch type
  - Test preparation course
  - Reading & Writing scores (via slider + number input)
- Predicts Math score (simulated in current version).
- Responsive bar chart visualization for:
  - Reading score
  - Writing score
  - Predicted Math score
- Fully responsive design.
- Docker support for easy deployment.

---

## 🖥️ Tech Stack
- **HTML5** – Structure  
- **CSS3** – Styling (responsive + modern UI)  
- **JavaScript (Vanilla)** – Logic, data handling, chart drawing  
- **Canvas API** – Custom bar chart rendering  
- **Docker** – Containerization  

---

## Run with Docker

Build the Docker image:

```
docker build -t student-performance-predictor .
```

Run the container:
```
docker run -d -p 8080:80 student-performance-predictor
```

Open your browser at http://localhost:8080
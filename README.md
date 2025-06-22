# Static Website CI/CD using AWS CodePipeline + S3

This project automates the deployment of a static website using a CI/CD pipeline with **GitHub**, **AWS CodeBuild**, **CodePipeline**, and **Amazon S3 (Static Website Hosting)**.

---

## 📁 Project Structure

s3-static-site-cicd/
├── website/
│ └── index.html
├── buildspec.yml
└── create_pipeline.py

---

## ⚙️ Services Used

- **GitHub** – Source repository
- **AWS CodePipeline** – Automates the entire CI/CD workflow
- **AWS CodeBuild** – Deploys the static site files to S3
- **Amazon S3** – Hosts the website as a static site

---

## 📌 How it Works

1. Code is pushed to the GitHub repo.
2. AWS CodePipeline is triggered.
3. CodeBuild runs `buildspec.yml` and uploads `index.html` to the root of the S3 bucket.
4. S3 serves the `index.html` as a static website.

---

## 🛠️ Tech Stack

- HTML
- AWS CodePipeline
- AWS CodeBuild
- AWS S3 (Static Hosting)

---

## 🧠 Lessons Learned

- How to fully automate S3 static site deployments using AWS services
- Writing a working `buildspec.yml` for CodeBuild
- Creating pipelines via Python using Boto3
- S3 static site behavior with index file placement

---

## 📸 Screenshots

Include the following screenshots:
- ✅ CodePipeline success status
- ✅ S3 static website page (open)

---

## 🔐 Note

The GitHub OAuth token used is private and securely managed. The deployment script shown is for educational purposes only.

---

## 👨‍💻 Author

**Pramit Dasgupta**  

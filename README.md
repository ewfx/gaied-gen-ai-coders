# 🚀 Gen AI Email Processing App

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)
- [Future Work](#future-work)  <!-- Added new section -->

---

## 🎯 Introduction
Gen AI Email Processing App is used for analyzing emails stored in eml, pdf and docx format. It provides key information like Summary of email, Request Type with its confidence score and key information key value pairs. App utilizes Gemini AI model (gemini-2.0-flash) for analying documents

## 🎥 Demo
🔗 [Live Demo](https://genai-email-processing-app-450383511585.asia-south1.run.app/)
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](/artifacts/demo/homepage.PNG)
![Screenshot 2](/artifacts/demo/EmailProcessingPageWithFileSelected.PNG)
![Screenshot 3](/artifacts/demo/EmailProcessingPageWithResult.PNG)
![Screenshot 4](/artifacts/demo/ManageRequestsPage.PNG)

## 💡 Inspiration
What inspired you to create this project? Describe the problem you're solving.

## ⚙️ What It Does
Key feature is application capability to read email message with attachments and extract key information from all attachments and in email body. It provides Gemini AI model capability to end user for summarizing and categorizing request types with key fields information

## 🛠️ How We Built It
Gen AI Email Processing App is built using apI of Gemini AI model - gemini-2.0-flash

## 🚧 Challenges We Faced
Major challenge is to get the json output using prompt engineering

## 🏃 How to Run
[Code](/code/GenAIEmailProcessingApp/README.md)


## 🏗️ Tech Stack
- 🔹 Frontend: Flask Bootstrap5
- 🔹 Backend: Flask, APIFlask, Python, Gemini AI model - gemini-2.0-flash
- 🔹 Database: PostgreSQL 
- 🔹 Other: OpenAI Documentation

## 👥 Team
- **Gen AI Coders** - [GitHub](https://github.com/ewfx/gaied-gen-ai-coders) 
- **Sivarajan C**
- **Durgesh**
- **Hiran**
- **Arpita**
- **Devi**

## 🔮 Future Work
- Adding offline document processing, User Authentication, Showing historical results, Improve API Error handling 
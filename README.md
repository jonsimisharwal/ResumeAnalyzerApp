🧠 Resume Analyzer using NLP & Streamlit
A smart, beginner-friendly web app that extracts key information from resumes like name, email, phone number, skills, college name, and project titles — all through a beautifully designed Streamlit interface.

✅ Built with:

Python

spaCy NLP

PyMuPDF for PDF text extraction

Streamlit for web interface
![image](https://github.com/user-attachments/assets/e0dd02d0-ef6c-4a4f-a196-f2d4b6e2c4a9)
![image](https://github.com/user-attachments/assets/f5aeb409-0139-4adb-ba95-1df6a4293fa1)

📂 Folder Structure

ResumeAnalyzer/
│
├── app.py               # Streamlit UI
├── resume_parser.py     # NLP logic for extraction
├── train_model.py       # (optional) for future ML training
├── requirements.txt     # Required libraries
├── sample_resume.pdf    # Example resume to test
└── README.md            # You're reading it :)

🛠 How to Run
Clone this repo


git clone https://github.com/yourusername/ResumeAnalyzer.git
cd ResumeAnalyzer
Create and activate virtual environment (Windows)

python -m venv venv
venv\Scripts\activate
Install dependencies

pip install -r requirements.txt
python -m spacy download en_core_web_sm
Run Streamlit app

streamlit run app.py

💡 Future Scope (Advanced Ideas)
Resume scoring & ranking
Batch upload & comparison
JD matching with resume
Save results to database
User login & export options

🤝 Contribute
Pull requests are welcome. For major changes, please open an issue first.

📬 Contact
📧 Email: jonsimisharwal@gmail.com

🔗 LinkedIn: https://www.linkedin.com/in/jonsi-misharwal-24295b286/


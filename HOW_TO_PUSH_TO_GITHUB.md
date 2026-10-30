# How to Push This Project to GitHub
# கிட்ஹப்பில் இந்த திட்டத்தை பதிவேற்றும் வழி

This folder is **already a Git repository** with clean commits.
You only need to create an empty repo on GitHub and push it.

தமிழ்: இந்த கோப்புறை ஏற்கனவே Git repository ஆக மாற்றப்பட்டுள்ளது.
நீங்கள் செய்ய வேண்டியது: GitHub-இல் ஒரு புதிய repository உருவாக்கி, push செய்யவும்.

---

## Part A - One time setup (only the first time)

### Step 1. Install Git on Windows
1. Download from https://git-scm.com/download/win
2. Install with all default options (just click Next, Next, Finish).

**தமிழ்:** Git-ஐ மேலே உள்ள இணைப்பிலிருந்து பதிவிறக்கி, default அமைப்புகளுடன் நிறுவவும்.

### Step 2. Tell Git your name and email
Open **Command Prompt** and type (change to your own name/email):

```
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

**தமிழ்:** உங்கள் பெயர் மற்றும் மின்னஞ்சலை Git-இடம் சொல்லவும். GitHub-இல் பயன்படுத்தும் அதே மின்னஞ்சலை கொடுங்கள்.

### Step 3. Create a GitHub account
1. Go to https://github.com and click **Sign up**
2. Verify your email.

**தமிழ்:** github.com-இல் இலவச கணக்கு உருவாக்கவும்.

---

## Part B - Push the project (every time you upload)

### Step 4. Create an EMPTY repository on GitHub
1. Log in to GitHub, click the **+** icon (top right) -> **New repository**
2. Repository name: `AI-Voice-Assistant`
3. Choose **Public** (so your teacher can see it) or Private.
4. **DO NOT** tick "Add a README file" - the README already exists here.
5. Click **Create repository**.

**தமிழ்:** GitHub-இல் புதிய repository உருவாக்கும்போது "Add a README file" என்ற பெட்டியை டிக் செய்ய வேண்டாம். Repository-இன் பெயர்: `AI-Voice-Assistant`.

### Step 5. Connect your folder to GitHub
In Command Prompt, go to the project folder and run
(use YOUR GitHub username in the last line):

```
cd path\to\AI_Voice_Assistant
git remote add origin https://github.com/YOUR-USERNAME/AI-Voice-Assistant.git
git push -u origin main
```

GitHub will open a login window - sign in with your browser.

**தமிழ்:** `git push -u origin main` என்ற கட்டளையை இயக்கியபின், GitHub உள்நுழைவு சாளரம் திறக்கும். அங்கு browser மூலம் login செய்யவும். அதன்பிறகு உங்கள் திட்டம் GitHub-இல் பதிவேறும்.

### Step 6. Check the result
Refresh your GitHub page. You will see all the files:
`main.py`, `gui.py`, `README.md`, and more.

Done! Your project is now on GitHub.

**தமிழ்:** முடிந்தது! உங்கள் திட்டம் இப்போது GitHub-இல் உள்ளது. வகுப்பில் demo செய்யும்போது இந்த link-ஐ காட்டலாம்.

---

## Part C - If you change the code later

```
cd path\to\AI_Voice_Assistant
git add .
git commit -m "Explain what you changed"
git push
```

**தமிழ்:** குறியீட்டில் (code) மாற்றம் செய்தபின், மேலே உள்ள மூன்று கட்டளைகளையும் இயக்கவும். `git add .` மாற்றங்களை சேர்க்கும், `git commit` சேமிக்கும், `git push` GitHub-இல் பதிவேற்றும்.

---

## Safety checklist (VERY IMPORTANT)

- [x] `.gitignore` already blocks the `.env` file - your API key can never be uploaded.
- [ ] Never copy your API key into any code file.
- [ ] Check your GitHub repo after pushing - you should NOT see `.env` there.
- [ ] If you ever upload a secret by mistake, delete that key at https://z.ai/manage-apikey/apikey-list and create a new one.

**தமிழ்:** `.gitignore` கோப்பு `.env`-ஐ தடுக்கிறது, எனவே உங்கள் API key ஒருபோதும் GitHub-இல் பதிவேறாது. Push செய்தபின் ஒருமுறை சரிபார்க்கவும்.

---

## Common errors and fixes

| Error message | Fix |
|---|---|
| `remote: Repository not found` | Check the username and repo name in Step 5 |
| `Updates were rejected` | Run `git pull origin main --rebase` then push again |
| `git is not recognized` | Restart Command Prompt after installing Git |
| Asked for username/password | Use the browser login window; a password will not work |

**தமிழ்:** பிழை வந்தால் மேலே உள்ள அட்டவணையில் தீர்வை தேடவும். "Updates were rejected" என்றால் முதலில் `git pull origin main --rebase` இயக்கவும்.

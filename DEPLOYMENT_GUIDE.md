# Rational Function Gaming App - Deployment Guide

## Complete Steps to Deploy Your App via GitHub and Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at share.streamlit.io)
- Your app files (already created in this project)

---

## Step 1: Prepare Your Files for Deployment

### 1.1 Create requirements.txt
Your app needs a requirements.txt file listing all dependencies:

```
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.21.0
plotly>=5.15.0
sympy>=1.12
```

### 1.2 Verify Your File Structure
Your project should have this structure:
```
rational-function-app/
├── app.py                    # Main Streamlit app
├── requirements.txt          # Dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── data/
│   └── leaderboard.py       # Leaderboard management
├── game_modes/
│   ├── practice_mode.py     # Practice game mode
│   ├── timed_challenge.py   # Timed challenges
│   └── multiplayer_quiz.py  # Multiplayer functionality
└── utils/
    ├── function_generator.py # Rational function generator
    ├── graph_analyzer.py    # Graph analysis tools
    └── scoring_system.py    # Scoring and achievements
```

---

## Step 2: Create GitHub Repository

### 2.1 Create New Repository on GitHub
1. Go to [github.com](https://github.com)
2. Click the green "New" button or go to [github.com/new](https://github.com/new)
3. Repository settings:
   - **Repository name**: `rational-function-gaming-app` (or your preferred name)
   - **Description**: `Interactive Streamlit app for learning rational functions through gaming`
   - **Visibility**: Public (required for free Streamlit deployment)
   - **Initialize**: Don't check any boxes (we'll upload existing files)
4. Click "Create repository"

### 2.2 Upload Your Files to GitHub

#### Option A: Using GitHub Web Interface (Easiest)
1. On your new repository page, click "uploading an existing file"
2. Drag and drop all your project files or click "choose your files"
3. Upload files in this order:
   - First: `app.py`, `requirements.txt`
   - Then: Create folders (`data/`, `game_modes/`, `utils/`, `.streamlit/`) and upload files to each
4. For each upload:
   - Add commit message like "Add main app files" or "Add game modes"
   - Click "Commit changes"

#### Option B: Using Git Command Line
```bash
# Navigate to your project folder
cd /path/to/your/project

# Initialize git repository
git init

# Add GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/rational-function-gaming-app.git

# Add all files
git add .

# Commit files
git commit -m "Initial commit: Rational Function Gaming App"

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Step 3: Deploy to Streamlit Cloud

### 3.1 Access Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Authorize Streamlit to access your GitHub repositories

### 3.2 Deploy Your App
1. Click "New app" button
2. Fill in deployment settings:
   - **Repository**: Select `YOUR_USERNAME/rational-function-gaming-app`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: Choose a custom URL like `rational-function-game` (optional)

3. Click "Deploy!"

### 3.3 Wait for Deployment
- Initial deployment takes 2-5 minutes
- Streamlit will install dependencies from requirements.txt
- You'll see build logs in real-time
- Once complete, your app will be live!

---

## Step 4: Test Your Deployed App

### 4.1 Verify Core Functionality
1. **Homepage**: Check welcome screen and navigation
2. **Practice Mode**: Generate a function and test question answering
3. **Timed Challenge**: Start a quick challenge to verify timing works
4. **Multiplayer Quiz**: Test room creation and joining
5. **Leaderboard**: Verify score tracking and display

### 4.2 Test on Different Devices
- Desktop browser
- Mobile browser
- Tablet (if available)

---

## Step 5: Share Your App

Your app will be available at:
- **Default URL**: `https://YOUR_USERNAME-rational-function-gaming-app-app-RANDOM.streamlit.app`
- **Custom URL**: `https://rational-function-game.streamlit.app` (if you set a custom URL)

### 5.1 Share Links
- Copy the URL from Streamlit Cloud dashboard
- Share with students, teachers, or anyone interested in learning rational functions!

---

## Step 6: Managing Updates

### 6.1 Making Changes
1. Edit files in your GitHub repository (web interface or git commands)
2. Commit changes
3. Streamlit automatically redeploys when you push to the main branch
4. Changes typically take 1-2 minutes to appear

### 6.2 Monitoring Your App
- Streamlit Cloud dashboard shows:
  - App status (running/stopped/error)
  - Recent deployments
  - Error logs
  - Usage analytics

---

## Troubleshooting Common Issues

### Issue 1: Import Errors
**Problem**: Module not found errors
**Solution**: 
- Check that all dependencies are in requirements.txt
- Verify file paths in import statements are correct
- Ensure all folders have `__init__.py` files if needed

### Issue 2: File Not Found Errors
**Problem**: Leaderboard or other files can't be created
**Solution**: 
- Streamlit Cloud is read-only except for temporary files
- Leaderboard data will reset between sessions (this is normal for the free tier)

### Issue 3: Memory or Performance Issues
**Problem**: App runs slowly or crashes
**Solution**:
- Optimize function generation for lower difficulty levels
- Reduce number of plot points if graphs are slow
- Consider caching with `@st.cache_data` for expensive computations

### Issue 4: App Won't Start
**Problem**: Deployment fails or app shows errors
**Solution**:
- Check requirements.txt has correct package versions
- Look at deployment logs in Streamlit Cloud dashboard
- Verify app.py has no syntax errors

---

## Additional Tips

### Security Best Practices
- Never commit API keys or secrets to GitHub
- Use Streamlit secrets management for sensitive data
- Keep your repository public for free deployment

### Performance Optimization
- Use `@st.cache_data` for expensive function generations
- Minimize real-time updates in multiplayer mode
- Consider reducing graph resolution for mobile devices

### Educational Use
- Create a QR code linking to your app for classroom use
- Consider adding a "Teacher Dashboard" for tracking class progress
- Document how to use the app in README.md

---

## Your App URLs
After deployment, bookmark these URLs:
- **Live App**: [Your Streamlit URL]
- **GitHub Repo**: `https://github.com/YOUR_USERNAME/rational-function-gaming-app`
- **Streamlit Dashboard**: [Streamlit Cloud Dashboard URL]

---

## Support Resources
- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Community Forum](https://discuss.streamlit.io)
- [GitHub Help](https://help.github.com)

Your rational function gaming app is now ready to help students learn mathematics in an engaging, interactive way!
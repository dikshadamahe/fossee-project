# Demo Video Recording Guide

This guide helps you create a 2-3 minute demo video for FOSSEE submission.

---

## 🎬 Recommended Tools

| Tool | Platform | Free? | Notes |
|------|----------|-------|-------|
| **OBS Studio** | All | ✅ | Best quality, more setup |
| **Loom** | All | ✅ (5min) | Easiest, includes webcam |
| **ShareX** | Windows | ✅ | Simple screen recording |
| **QuickTime** | macOS | ✅ | Built-in, basic features |

---

## 📝 Video Script (2-3 minutes)

### Part 1: Introduction (0:00 - 0:20)
```
"Hello! This is a demo of the Chemical Equipment Parameter Visualizer,
a hybrid web and desktop application built for FOSSEE.

The app allows users to upload CSV files containing chemical equipment 
data, view statistical analysis, and generate PDF reports.

Let's see it in action."
```

### Part 2: Web Application Demo (0:20 - 1:20)

1. **Show Login/Register** (10 sec)
   - Click Login button
   - Show register form
   - Register/Login

2. **Upload CSV** (15 sec)
   - Navigate to Upload page
   - Drag and drop `sample_data.csv`
   - Show upload success

3. **Dashboard** (20 sec)
   - Navigate to Dashboard
   - Show summary statistics
   - Highlight charts (pie chart, line charts)

4. **History** (10 sec)
   - Navigate to History
   - Show dataset list
   - Click to view a dataset

5. **PDF Report** (15 sec)
   - Click "Download Report"
   - Show PDF opens/downloads

### Part 3: Desktop Application Demo (1:20 - 2:00)

1. **Launch App** (5 sec)
   - Show desktop app opening
   - Note the similar design

2. **Same Features** (25 sec)
   - Upload same CSV
   - Show Matplotlib charts
   - Show data table
   - Download PDF

3. **Login** (10 sec)
   - Show login dialog
   - Mention it connects to same backend

### Part 4: Technical Overview (2:00 - 2:30)

```
"The application uses:
- Django REST Framework for the backend API
- React with Chart.js for the web frontend  
- PyQt5 with Matplotlib for the desktop app
- SQLite for data storage

Both frontends connect to the same API, ensuring consistent data.

The web app is deployed on Vercel, and the desktop app is available
as a standalone executable on GitHub Releases.

Thank you for watching!"
```

---

## 🎥 Recording Tips

### Setup
1. Close unnecessary applications
2. Set resolution to 1920x1080 (or 1280x720)
3. Use a clean browser (no bookmarks bar)
4. Have sample_data.csv ready on desktop

### Recording
1. Record in one take if possible
2. Move mouse slowly and deliberately
3. Pause briefly on important screens
4. Keep narration clear and paced

### Audio
1. Use a good microphone if available
2. Record in a quiet environment
3. Add background music (optional, keep it subtle)

### Post-Production
1. Trim dead air at start/end
2. Add title card with project name
3. Export as MP4 (H.264, 30fps)

---

## 📤 Upload Options

| Platform | Max Length | Link Sharing |
|----------|------------|--------------|
| **YouTube** (Unlisted) | Unlimited | ✅ Easy |
| **Loom** | 5 min free | ✅ Easy |
| **Google Drive** | Unlimited | ✅ Share link |
| **GitHub Release** | 2GB | ✅ Direct link |

### Recommended: YouTube Unlisted
1. Upload to YouTube
2. Set visibility to "Unlisted"
3. Copy link for submission

---

## ✅ Checklist

Before recording:
- [ ] Backend running at localhost:8000
- [ ] Web app running at localhost:5173
- [ ] Desktop app ready to launch
- [ ] sample_data.csv on desktop
- [ ] Clean browser (incognito mode)
- [ ] Microphone tested

After recording:
- [ ] Video is 2-3 minutes long
- [ ] All features demonstrated
- [ ] Audio is clear
- [ ] No sensitive data visible
- [ ] Uploaded and link ready

---

## 📋 Submission

Add video link to:
1. README.md (Demo Video section)
2. Google Form submission
3. GitHub repository description

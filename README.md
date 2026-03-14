# Aryan Gorde Portfolio Website

A modern, responsive, and lightweight personal portfolio website built with plain HTML, CSS, and JavaScript for GitHub Pages deployment on **aryangorde.com**.

## Tech Stack

- HTML5
- CSS3
- Vanilla JavaScript
- GitHub Pages (static hosting)

## Features

- Clean developer portfolio layout
- Responsive design for desktop, tablet, and mobile
- Smooth scrolling navigation
- Dark/light mode toggle with local storage persistence
- Subtle reveal animations on scroll
- Accessible structure (skip link, semantic landmarks, ARIA labels)
- SEO-ready meta tags
- Custom domain support via `CNAME`

## Project Structure

.
├── CNAME
├── README.md
├── index.html
├── script.js
├── style.css
└── assets/
    ├── Aryan_Gorde_Resume.pdf
    └── images/
        └── .gitkeep

## Local Run

1. Clone or download this repository.
2. Open `index.html` in your browser.

Optional with Python local server:

```bash
python3 -m http.server 5500
```

Then visit `http://localhost:5500`.

## GitHub Pages Deployment (Required Setup)

1. Create a new GitHub repository named:
   `aryangorde8.github.io`
2. Add all files from this project to that repository root.
3. Push to `main` branch.
4. Go to:
   **GitHub Repository → Settings → Pages**
5. Under **Build and deployment**:
   - Source: **Deploy from a branch**
   - Branch: **main**
   - Folder: **/ (root)**
6. Save and wait for deployment.

## Git Commands to Push

```bash
git init
git add .
git commit -m "Initial portfolio website"
git branch -M main
git remote add origin https://github.com/<your-username>/aryangorde8.github.io.git
git push -u origin main
```

Replace `<your-username>` with your GitHub username.

## Custom Domain Setup (aryangorde.com)

The repository already includes a `CNAME` file with:

`aryangorde.com`

### DNS Records

Add these records with your domain provider:

A records for root domain (`@`):

- 185.199.108.153
- 185.199.109.153
- 185.199.110.153
- 185.199.111.153

CNAME record:

- Host: `www`
- Value: `aryangorde8.github.io`

After DNS propagation, go to GitHub Pages settings and set custom domain to:

`aryangorde.com`

Enable **Enforce HTTPS** once available.

## Personalization Checklist

Before going live, update:

- Email in contact section (`your.email@example.com`)
- LinkedIn link placeholder (`your-linkedin`)
- GitHub username links if needed
- Replace `assets/Aryan_Gorde_Resume.pdf` with your actual resume

## Notes

- `index.html` is the site homepage.
- The setup is optimized for GitHub Pages static hosting.
- All section navigation links are configured as in-page anchors.

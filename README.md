# Khushbu Patidar - Portfolio (Django)

Interactive portfolio jiska poora content **admin panel** se change hota hai:
projects, skills, education, experience, photo, resume PDF, contact details, sab kuch.
Code ko haath lagane ki zarurat nahi.

---

## 1. Pehli baar run kaise karein

**Zaruri:** Python 3.10 ya usse naya (`python --version` se check karo).

Zip ko extract karo, phir us folder me terminal / CMD kholo (VS Code me: *Terminal > New Terminal*).

### Windows
```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_portfolio
python manage.py createsuperuser
python manage.py runserver
```

### Mac / Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_portfolio
python manage.py createsuperuser
python manage.py runserver
```

Ye commands kya karte hain:

| Command | Kaam |
|---|---|
| `python -m venv venv` + `activate` | Is project ke liye alag Python environment banata hai |
| `pip install -r requirements.txt` | Django aur baaki packages install karta hai |
| `migrate` | Database (SQLite) ki tables banata hai |
| `seed_portfolio` | Resume wala data (skills, projects, education, photo, resume PDF) database me daalta hai |
| `createsuperuser` | Admin login banata hai (username, email, password khud choose karo) |
| `runserver` | Website start karta hai |

Ab browser me kholo:

- **Website:** http://127.0.0.1:8000/
- **Admin panel:** http://127.0.0.1:8000/admin/ (jo username/password `createsuperuser` me banaya wo daalo)

Server band karne ke liye terminal me `Ctrl + C`.
**Agli baar** sirf venv activate karo aur `python manage.py runserver` chalao (baaki commands dobara nahi chahiye).

---

## 2. Admin panel se kya-kya badal sakti ho

Admin me login karke:

| Section | Kya karna hai |
|---|---|
| **Profile & resume** | **Naya resume PDF upload karo** (Resume field), photo badlo, naam, tagline, about text, email, phone, GitHub, LinkedIn edit karo. Save dabate hi site ke *View resume* aur *Download PDF* buttons naya resume dikhane lagte hain. |
| **Projects** | Naya project add karo, purana edit/delete karo, order badlo, screenshot upload karo. Har project me highlights (hover par dikhte hain), tech stack, live link, GitHub link hota hai. |
| **Skills** | Skill add/remove karo, category chuno, hover wali detail likho. *Is highlight* tick karoge to wo hero me photo ke paas sticker ban jayega (3-4 rakhna). |
| **Education** | MCA complete hone par period badlo (jaise `2026-2028`), *Is current* untick karo, CGPA/percentage add karo. |
| **Experience** | Internship ya job add karo. Jab tak koi entry nahi hai, ye section site par dikhta hi nahi. Pehli entry add karte hi apne aap nav me aa jata hai. |
| **Contact messages** | Website ke contact form se aaye messages yahan dikhte hain. |

Tips:
- **Order** field me chhota number pehle dikhta hai (1, 2, 3...). List page par hi order/visible badal sakti ho.
- Kisi cheez ko delete kiye bina chhupana ho to **Is visible** untick karo.
- Project ka screenshot nahi doge to colour cover + emoji icon dikhega (emoji bhi admin me badal sakti ho).

---

## 3. Design badalna ho to

- Colours aur fonts: `portfolio/static/css/style.css` ke sabse upar `:root { ... }` me (violet, sun, mint, coral, sky).
- Animations aur hover effects ka code: `portfolio/static/js/main.js`.
- Page ka layout: `portfolio/templates/portfolio/index.html`.

CSS/JS badalne ke baad browser me `Ctrl + Shift + R` (hard refresh) dabao.

---

## 4. Folder structure

```
khushbu_portfolio/
  manage.py
  requirements.txt
  config/                 settings, urls
  portfolio/
    models.py             Profile, Skill, Project, Education, Experience, ContactMessage
    admin.py              admin panel ki setting
    views.py, urls.py
    templates/portfolio/index.html
    static/css/style.css
    static/js/main.js
    seed_assets/          resume wali photo aur PDF (sirf seed ke liye)
    management/commands/seed_portfolio.py   resume ka data yahan hai
  media/                  admin se upload ki hui photo/resume/screenshots
  db.sqlite3              (migrate ke baad banta hai) tumhara saara content
```

Data bigad jaye ya fresh start chahiye: `python manage.py seed_portfolio --reset`
(dhyan rakho: ye admin me kiya hua sab content hata kar resume wala default data wapas daal deta hai).

---

## 5. Common problems

| Problem | Solution |
|---|---|
| `python` not found | Windows me `py` try karo, ya Python dobara install karo aur "Add to PATH" tick karo |
| `No module named django` | venv activate nahi hua ya `pip install -r requirements.txt` nahi chala |
| Photo/resume nahi dikh raha | `python manage.py seed_portfolio` chalaya? Ya admin > Profile & resume me upload karo |
| Port already in use | `python manage.py runserver 8080` |
| Fonts alag dikh rahe | Fonts Google se aate hain, internet chahiye. Offline me fallback fonts dikhte hain |

---

## 6. MySQL use karna ho (optional)

Default SQLite hai (kuch install nahi karna). MySQL chahiye to:

1. MySQL me ek database banao: `CREATE DATABASE portfolio CHARACTER SET utf8mb4;`
2. `pip install mysqlclient`
3. Ye environment variables set karke `migrate` aur `runserver` chalao:

```bash
# Mac/Linux
export DB_NAME=portfolio DB_USER=root DB_PASSWORD=yourpassword DB_HOST=127.0.0.1
# Windows (CMD)
set DB_NAME=portfolio & set DB_USER=root & set DB_PASSWORD=yourpassword & set DB_HOST=127.0.0.1
```

---

## 7. Render par deploy karna

- Build command: `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
- Start command: `gunicorn config.wsgi`
- Environment variables: `SECRET_KEY` (koi lambi random string), `DEBUG=0`
- **Dhyan do:** Render ke free plan par disk temporary hoti hai. Admin se upload ki hui photo/resume/screenshots aur SQLite database redeploy par ud sakte hain. Permanent chahiye to Render ka *Persistent Disk* + PostgreSQL/MySQL use karo, ya seedha Cloudinary jaisa media storage.
- Admin user Render ke Shell me `python manage.py createsuperuser` se banao, aur pehli baar `python manage.py seed_portfolio` chalao.

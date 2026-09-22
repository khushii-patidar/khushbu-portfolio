"""
Resume wala data pehli baar database me daalta hai (skills, projects, education,
photo aur resume PDF). Iske baad sab kuch admin panel se badla ja sakta hai.

    python manage.py seed_portfolio           # sirf tab chalega jab profile khaali ho
    python manage.py seed_portfolio --reset   # sab kuch dobara resume wale default data se bhar do
"""
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from portfolio.models import Education, Experience, Profile, Project, Skill

ASSETS = Path(__file__).resolve().parents[2] / "seed_assets"

SKILLS = [
    # (name, category, detail, highlight, order)
    ("Python", "backend", "Main language. Used in both of my projects.", True, 1),
    ("Django", "backend", "Powers RecipeHub-AI and Smart-Garage.", True, 2),
    ("HTML", "frontend", "Page structure for every UI I build.", False, 3),
    ("CSS", "frontend", "Responsive layouts and dark/light themes.", False, 4),
    ("JavaScript", "frontend", "DOM manipulation and ES6.", True, 5),
    ("MySQL", "database", "Relational database for app data.", True, 6),
    ("GitHub", "tools", "Version control and code hosting.", False, 7),
    ("VS Code", "tools", "My code editor.", False, 8),
    ("Render", "tools", "Both projects are deployed here.", False, 9),
]

PROJECTS = [
    {
        "title": "RecipeHub-AI",
        "subtitle": "Recipe Generator Platform",
        "description": (
            "A Django platform for managing recipes, with an AI-powered kitchen "
            "assistant that helps generate recipes and answers cooking questions."
        ),
        "highlights": (
            "Integrated an AI-powered kitchen assistant for recipe generation and support\n"
            "Built recipe management with full CRUD operations in Django\n"
            "Deployed the application on Render"
        ),
        "tech_stack": "Python, Django, AI integration, Render",
        "live_url": "https://recipehub-ai.onrender.com/",
        "icon": "🍳",
        "accent": "sun",
        "order": 1,
    },
    {
        "title": "Smart-Garage",
        "subtitle": "AI-Powered Car Service Booking Platform",
        "description": (
            "A car service booking platform with separate roles for customers and "
            "mechanics, plus an AI chatbot that helps troubleshoot vehicle problems."
        ),
        "highlights": (
            "Role-based app for customers and mechanics with vehicle management and service booking\n"
            "AI chatbot for vehicle troubleshooting, connected through an API\n"
            "Responsive UI with a dark/light theme, deployed on Render"
        ),
        "tech_stack": "Django, AI chatbot API, Render",
        "live_url": "https://smart-garage-8wi9.onrender.com",
        "icon": "🚗",
        "accent": "violet",
        "order": 2,
    },
]

EDUCATION = [
    ("Indore International College", "MCA (Master of Computer Applications)", "Ongoing (2026)", "", True, 1),
    ("Mandsaur Institute of Technology - MIT", "BCA (Bachelor of Computer Applications)", "2023-2026", "CGPA 7.97", False, 2),
    ("Adarsh Higher Secondary School, Sitamau", "XII Standard", "2023", "78.8%", False, 3),
]

ABOUT = (
    "I'm an MCA student from Mandsaur, Madhya Pradesh. I work mainly with Python and "
    "Django, use MySQL for data, and build the front end with HTML, CSS and JavaScript.\n\n"
    "I like building things that actually go live. Both of my projects, RecipeHub-AI and "
    "Smart-Garage, are deployed on Render and use AI to help the people using them.\n\n"
    "I'm looking for an entry-level Python/Django developer role where I can work on "
    "real projects and keep improving as a developer."
)


class Command(BaseCommand):
    help = "Resume ke data se portfolio ko pehli baar bharta hai."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Purana content hata kar dobara seed karo.")

    def handle(self, *args, **options):
        if Profile.objects.exists() and not options["reset"]:
            self.stdout.write(self.style.WARNING(
                "Profile pehle se bani hui hai, kuch nahi badla. (Dobara seed karna ho to --reset lagao.)"
            ))
            return

        if options["reset"]:
            for model in (Skill, Project, Education, Experience, Profile):
                model.objects.all().delete()

        profile = Profile(
            name="Khushbu Patidar",
            headline="Python / Django Developer",
            typed_roles="Python Developer, Django Developer, AI-powered web apps, MCA student",
            tagline="I build Django web apps with AI features built in, and I ship them live.",
            about=ABOUT,
            email="khushboopatidar888@gmail.com",
            phone="9340297224",
            location="Mandsaur, Madhya Pradesh",
            github_url="https://github.com/khushii-patidar",
            open_to_work=True,
            availability_text="Open to entry-level Python/Django roles",
        )
        photo_path = ASSETS / "khushbu.jpeg"
        resume_path = ASSETS / "Khushbu_Patidar_Resume.pdf"
        if photo_path.exists():
            with photo_path.open("rb") as fh:
                profile.photo.save("khushbu.jpeg", File(fh), save=False)
        if resume_path.exists():
            with resume_path.open("rb") as fh:
                profile.resume.save("Khushbu_Patidar_Resume.pdf", File(fh), save=False)
        profile.save()

        for name, category, detail, highlight, order in SKILLS:
            Skill.objects.create(
                name=name, category=category, detail=detail, is_highlight=highlight, order=order
            )
        for data in PROJECTS:
            Project.objects.create(**data)
        for institution, degree, period, score, current, order in EDUCATION:
            Education.objects.create(
                institution=institution, degree=degree, period=period,
                score=score, is_current=current, order=order,
            )

        self.stdout.write(self.style.SUCCESS("Portfolio data ready. Ab admin panel se kuch bhi badal sakti ho."))

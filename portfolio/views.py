from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import ContactForm
from .models import Education, Experience, Profile, Project, Skill


def home(request):
    profile = Profile.load()
    skills = list(Skill.objects.filter(is_visible=True))
    projects = list(Project.objects.filter(is_visible=True))
    education = list(Education.objects.all())
    experiences = list(Experience.objects.filter(is_visible=True))

    skill_groups = []
    for key, label in Skill.CATEGORIES:
        items = [s for s in skills if s.category == key]
        if items:
            skill_groups.append({"key": key, "label": label, "skills": items})

    context = {
        "profile": profile,
        "skills": skills,
        "skill_groups": skill_groups,
        "stickers": [s for s in skills if s.is_highlight][:4],
        "projects": projects,
        "education": education,
        "experiences": experiences,
        "current_education": next((e for e in education if e.is_current), None),
        "live_count": sum(1 for p in projects if p.live_url),
        "skill_count": len(skills),
    }
    return render(request, "portfolio/index.html", context)


def resume_download(request):
    profile = Profile.load()
    if not profile.resume:
        raise Http404("Resume abhi upload nahi hua hai.")
    filename = f"{profile.name.replace(' ', '_')}_Resume.pdf"
    return FileResponse(
        profile.resume.open("rb"),
        as_attachment=True,
        filename=filename,
        content_type="application/pdf",
    )


@require_POST
def contact(request):
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

    # Honeypot: bots ye hidden field bhar dete hain.
    if request.POST.get("website"):
        return JsonResponse({"ok": True, "message": "Thanks!"}) if is_ajax else redirect("home")

    form = ContactForm(request.POST)
    if form.is_valid():
        form.save()
        if is_ajax:
            return JsonResponse({"ok": True, "message": "Message sent. I'll get back to you soon."})
        return redirect("home")

    if is_ajax:
        errors = {f: [str(e) for e in errs] for f, errs in form.errors.items()}
        return JsonResponse({"ok": False, "errors": errors}, status=400)
    return redirect("home")

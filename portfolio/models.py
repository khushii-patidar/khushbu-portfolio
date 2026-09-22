import re

from django.core.validators import FileExtensionValidator
from django.db import models


def _lines(text):
    return [line.strip() for line in (text or "").splitlines() if line.strip()]


def _csv(text):
    return [part.strip() for part in (text or "").split(",") if part.strip()]


class Profile(models.Model):
    """Sirf ek hi row hoti hai: tumhari basic info, photo aur resume."""

    name = models.CharField(max_length=100, default="Khushbu Patidar")
    headline = models.CharField(
        max_length=150,
        default="Python / Django Developer",
        help_text="Browser tab aur footer me dikhta hai. Example: Python / Django Developer",
    )
    typed_roles = models.CharField(
        max_length=300,
        blank=True,
        help_text="Comma se alag karo. Hero me \"I'm a ...\" ke baad ek-ek karke type hote hain.",
    )
    tagline = models.TextField(
        blank=True, help_text="Naam ke neeche chhoti si line."
    )
    about = models.TextField(
        blank=True, help_text="About section ka text. Paragraphs ke beech khaali line chhodo."
    )
    photo = models.ImageField(
        upload_to="profile/", blank=True, help_text="Hero section wali photo (portrait best rehti hai)."
    )
    resume = models.FileField(
        upload_to="resume/",
        blank=True,
        validators=[FileExtensionValidator(["pdf"])],
        help_text="Naya PDF upload karke Save karo. Site ke View/Download buttons turant naya resume dikhayenge.",
    )

    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=120, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    open_to_work = models.BooleanField(
        default=True, help_text="On rakho to hero me green 'available' badge dikhega."
    )
    availability_text = models.CharField(max_length=150, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profile & resume"
        verbose_name_plural = "Profile & resume"

    def __str__(self):
        return self.name

    # --- helpers used by the template -------------------------------------
    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def first_name(self):
        return self.name.split(" ", 1)[0]

    @property
    def last_name(self):
        parts = self.name.split(" ", 1)
        return parts[1] if len(parts) > 1 else ""

    @property
    def initials(self):
        return "".join(p[0] for p in self.name.split()[:2]).upper() or "?"

    @property
    def role_list(self):
        return _csv(self.typed_roles) or [self.headline]

    @property
    def about_paragraphs(self):
        return [p.strip() for p in re.split(r"\n\s*\n", self.about or "") if p.strip()]

    @property
    def phone_href(self):
        digits = re.sub(r"\D", "", self.phone or "")
        if len(digits) == 10:  # Indian number without country code
            digits = "91" + digits
        return f"+{digits}" if digits else ""

    @property
    def github_handle(self):
        return re.sub(r"^https?://(www\.)?", "", self.github_url or "").rstrip("/")

    @property
    def linkedin_handle(self):
        return re.sub(r"^https?://(www\.)?", "", self.linkedin_url or "").rstrip("/")

    def save(self, *args, **kwargs):
        self.pk = 1  # singleton
        old = Profile.objects.filter(pk=1).first()
        super().save(*args, **kwargs)
        # Photo/resume badalne par purani file disk se hata do.
        if old:
            for field in ("photo", "resume"):
                old_file = getattr(old, field)
                new_file = getattr(self, field)
                if old_file and old_file.name != new_file.name:
                    old_file.delete(save=False)


class Skill(models.Model):
    CATEGORIES = [
        ("backend", "Backend"),
        ("frontend", "Frontend"),
        ("database", "Database"),
        ("tools", "Tools & Platforms"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=60)
    category = models.CharField(max_length=20, choices=CATEGORIES, default="other")
    detail = models.CharField(
        max_length=160,
        blank=True,
        help_text="Optional. Skill par hover karne par ye chhoti si info dikhti hai.",
    )
    is_highlight = models.BooleanField(
        default=False, help_text="Hero me photo ke paas sticker ki tarah dikhao (3-4 rakhna best hai)."
    )
    order = models.PositiveIntegerField(default=10, help_text="Chhota number pehle dikhta hai.")
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    ACCENTS = [
        ("violet", "Violet"),
        ("sun", "Yellow"),
        ("coral", "Coral"),
        ("mint", "Mint"),
        ("sky", "Sky blue"),
    ]

    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=140, blank=True, help_text="Example: Recipe Generator Platform")
    description = models.TextField(help_text="2-3 line ka short summary.")
    highlights = models.TextField(
        blank=True, help_text="Hover par dikhne wale points. Ek line = ek point."
    )
    tech_stack = models.CharField(max_length=250, blank=True, help_text="Comma se alag karo: Python, Django, MySQL")
    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        help_text="Optional screenshot. Nahi doge to colour cover + icon dikhega.",
    )
    icon = models.CharField(
        max_length=8, default="✨", blank=True, help_text="Cover par dikhne wala emoji (jab screenshot na ho)."
    )
    accent = models.CharField(max_length=10, choices=ACCENTS, default="violet")
    order = models.PositiveIntegerField(default=10, help_text="Chhota number pehle dikhta hai.")
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        return _csv(self.tech_stack)

    @property
    def highlight_list(self):
        return _lines(self.highlights)


class Education(models.Model):
    institution = models.CharField(max_length=160)
    degree = models.CharField(max_length=160)
    period = models.CharField(max_length=60, help_text="Example: 2023-2026 ya Ongoing (2026)")
    score = models.CharField(max_length=40, blank=True, help_text="Example: CGPA 7.97 ya 78.8%")
    description = models.TextField(blank=True)
    is_current = models.BooleanField(default=False, help_text="Abhi padh rahi ho to tick karo.")
    order = models.PositiveIntegerField(default=10, help_text="Chhota number upar dikhta hai (latest ko 1 do).")

    class Meta:
        ordering = ["order", "id"]
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Experience(models.Model):
    """Internship / job. Koi entry nahi hogi to site par ye section dikhega hi nahi."""

    role = models.CharField(max_length=120)
    organization = models.CharField(max_length=160)
    period = models.CharField(max_length=60)
    description = models.TextField(blank=True, help_text="Ek line = ek point.")
    order = models.PositiveIntegerField(default=10, help_text="Chhota number upar dikhta hai (latest ko 1 do).")
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.role} @ {self.organization}"

    @property
    def point_list(self):
        return _lines(self.description)


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.created_at:%d %b %Y})"

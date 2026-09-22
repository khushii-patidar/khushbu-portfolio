from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html

from .models import ContactMessage, Education, Experience, Profile, Project, Skill

admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Yahin se apni website ka content badlo"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ("photo_preview", "resume_link")
    fieldsets = (
        ("Resume", {"fields": ("resume", "resume_link")}),
        ("Photo", {"fields": ("photo", "photo_preview")}),
        (
            "Hero section",
            {"fields": ("name", "headline", "typed_roles", "tagline", "open_to_work", "availability_text")},
        ),
        ("About section", {"fields": ("about",)}),
        ("Contact details", {"fields": ("email", "phone", "location", "github_url", "linkedin_url")}),
    )

    def has_add_permission(self, request):
        return not Profile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Sirf ek profile hai, to list dikhane ki jagah seedha edit form kholo.
        obj = Profile.objects.first()
        if obj:
            return redirect(reverse("admin:portfolio_profile_change", args=[obj.pk]))
        return redirect(reverse("admin:portfolio_profile_add"))

    @admin.display(description="Current photo")
    def photo_preview(self, obj):
        if obj and obj.photo:
            return format_html(
                '<img src="{}" style="height:140px;border-radius:12px;border:1px solid #ccc">', obj.photo.url
            )
        return "No photo yet"

    @admin.display(description="Current resume")
    def resume_link(self, obj):
        if obj and obj.resume:
            return format_html('<a href="{}" target="_blank">Open current resume (PDF)</a>', obj.resume.url)
        return "No resume yet"


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "detail", "is_highlight", "is_visible", "order")
    list_editable = ("is_highlight", "is_visible", "order")
    list_filter = ("category", "is_visible")
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "live_url", "is_visible", "order")
    list_editable = ("is_visible", "order")
    fieldsets = (
        (None, {"fields": ("title", "subtitle", "description", "highlights", "tech_stack")}),
        ("Links", {"fields": ("live_url", "github_url")}),
        ("Look", {"fields": ("image", "icon", "accent")}),
        ("Display", {"fields": ("order", "is_visible")}),
    )


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree", "institution", "period", "score", "is_current", "order")
    list_editable = ("is_current", "order")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "organization", "period", "is_visible", "order")
    list_editable = ("is_visible", "order")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "is_read")
    list_editable = ("is_read",)
    list_filter = ("is_read",)
    readonly_fields = ("name", "email", "message", "created_at")
    fields = ("name", "email", "message", "created_at", "is_read")

    def has_add_permission(self, request):
        return False

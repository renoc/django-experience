from django.contrib import admin

from .models import Experience, Rating, Review


class RatingAdmin(admin.TabularInline):
    model = Rating


class ReviewAdmin(admin.TabularInline):
    model = Review


class ExperienceAdmin(admin.ModelAdmin):
    model = Experience
    inlines = [RatingAdmin, ReviewAdmin]
    list_display = ['subject', 'user', 'average_score', 'timestamp']
    raw_id_fields = ['user']


admin.site.register(Experience, ExperienceAdmin)

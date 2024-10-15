from django.contrib import admin
from .models import Question, Choice

# Inline model for Choice to be displayed in the Question admin page
class ChoiceInline(admin.TabularInline):  # admin.StackedInline
    model = Choice
    extra = 3  # How many empty choice fields to display

# Customize the Question admin page
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']  # Adds a filter sidebar by publication date
    search_fields = ['question_text']  # Adds a search box for questions

# Register the customized Question admin
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
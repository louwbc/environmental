from django.contrib import admin
from record.models import Record

class RecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'added', 'adder')


admin.site.register(Record, RecordAdmin)

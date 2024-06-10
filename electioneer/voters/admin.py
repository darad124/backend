from django.contrib import admin
from .models import Student, Election, VotingRecord

admin.site.register(Student)
admin.site.register(Election)
admin.site.register(VotingRecord)

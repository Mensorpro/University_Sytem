from django.contrib import admin
from .models import Faculty, Student, Lecturer, Course, CourseUnit, Enrollment,Assignment,AssignmentSubmission

admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(Lecturer)
admin.site.register(Course)
admin.site.register(CourseUnit)
admin.site.register(Enrollment)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)



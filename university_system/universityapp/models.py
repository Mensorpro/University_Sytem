from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Faculties"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='students')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='lecturers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Rename Program to Course and update related names
class Course(models.Model):
    name = models.CharField(max_length=100)
    # Removed description field
    code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='courses', null=True, blank=True)  # Adjusted related_name from 'programs' to 'courses'
    # Removed lecturer field
    students = models.ManyToManyField(Student, through='Enrollment', related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('withdrawn', 'Withdrawn'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    enrollment_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Changed from auto_now_add=True to auto_now=True
    
    class Meta:
        # This ensures a student can only have ONE active enrollment
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'status'],
                condition=models.Q(status='active'),
                name='unique_active_enrollment'
            )
        ]
        
    def __str__(self):
        return f"{self.student} enrolled in {self.course}"

# Update CourseUnit foreign key to reference Course.
class CourseUnit(models.Model):
    title = models.CharField(max_length=100)
    # Removed: description field
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='units')  # Updated model reference from Program to Course
    # Removed: order and content fields
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.course.code} - {self.title}"
    
    class Meta:
        ordering = ['course', 'title']

# Update Assignment foreign key to reference Course.
class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')  # Updated model reference from Program to Course
    due_date = models.DateTimeField()
    total_marks = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.course.code}"

class AssignmentSubmission(models.Model):
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('late', 'Late Submission'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    submission_file = models.FileField(upload_to='submissions/', null=True, blank=True)
    submission_text = models.TextField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    grade = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    
    class Meta:
        unique_together = ('student', 'assignment')
    
    def __str__(self):
        return f"{self.student} - {self.assignment.title}"
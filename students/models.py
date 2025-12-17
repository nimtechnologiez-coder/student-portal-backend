from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password


# ==============================
# CUSTOM ADMIN MODEL
# ==============================
class Admin(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username


# ==============================
# MENTOR MODEL
# ==============================
class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, unique=True)
    expertise = models.CharField(max_length=150, blank=True)

    username_plain = models.CharField(max_length=150, blank=True)
    password_plain = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


# ==============================
# COURSE MODEL
# ==============================
class Course(models.Model):
    course_name = models.CharField(max_length=200)

    def __str__(self):
        return self.course_name


# ==============================
# BATCH MODEL
# ==============================
class Batch(models.Model):
    batch_name = models.CharField(max_length=100)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="batches"
    )

    def __str__(self):
        return f"{self.batch_name} ({self.course.course_name})"


# ==============================
# STUDENT MODEL
# ==============================
class Student(models.Model):

    CATEGORY_CHOICES = [
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("authorized", "Authorized"),
    ]

    ACCESS_CHOICES = [
        ("all_access", "All Access"),
        ("video_only", "Video Only"),
        ("authorized_access", "Authorized Access"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, default="")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True)

    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="full_time"
    )

    access_type = models.CharField(
        max_length=30,
        choices=ACCESS_CHOICES,
        default="all_access"
    )

    is_zoom_enabled = models.BooleanField(default=True)

    joining_date = models.DateField(null=True, blank=True)
    course_duration = models.CharField(max_length=50, blank=True, default="")
    end_date = models.DateField(null=True, blank=True)
    valid_upto = models.DateField(null=True, blank=True)

    password_plain = models.CharField(max_length=30, blank=True, default="")

    profile_photo = models.ImageField(
        upload_to="student_photos/",
        null=True,
        blank=True,
        default="default_profile.png"
    )

    def __str__(self):
        return self.user.username


# ==============================
# TOPIC / TASK MODEL
# ==============================
class Topic(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    mentor = models.ForeignKey(
        Mentor, on_delete=models.SET_NULL, null=True, blank=True
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    trainer = models.CharField(max_length=150, null=True, blank=True)
    total_hours = models.CharField(max_length=50, null=True, blank=True)

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("not_completed", "Not Completed"),
        ("review", "On Review"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    zoom_link = models.URLField(null=True, blank=True)
    video = models.FileField(upload_to="topic_videos/", null=True, blank=True)
    downloads = models.IntegerField(default=0)

    estimated_time = models.FloatField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    task_notes = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.title} - {self.student.user.username}"


# ==============================
# TASK SUBMISSION MODEL (PDF UPLOAD)
# ==============================
class TaskSubmission(models.Model):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="submissions"
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    file = models.FileField(
        upload_to="task_submissions/"
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("topic", "student")
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.student.user.username} - {self.topic.title}"



# ==============================
# ATTENDANCE MODEL
# ==============================
class Attendance(models.Model):

    STATUS_CHOICES = (
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Late", "Late"),
        ("Leave", "Leave"),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, null=True, blank=True
    )
    batch = models.ForeignKey(
        Batch, on_delete=models.SET_NULL, null=True, blank=True
    )

    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    remark = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {self.status}"


# ==============================
# HOLIDAY MODEL
# ==============================
class Holiday(models.Model):
    date = models.DateField(unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.date}"

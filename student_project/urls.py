from django.contrib import admin
from django.urls import path
from students import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # ==================================================
    # LOGIN / LOGOUT
    # ==================================================
    path('', views.admin_login, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # ==================================================
    # ADMIN DASHBOARD
    # ==================================================
    path('admindashboard/', views.admin_dashboard, name='admin_dashboard'),

    # ==================================================
    # STUDENTS
    # ==================================================
    path('student_list/', views.student_list, name='student_list'),
    path('addstudent/', views.add_student, name='add_student'),
    path('edit_student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),

    # ==================================================
    # TOPICS
    # ==================================================
    path('add_topic/', views.add_topic, name='add_topic'),
    path('edit_topic/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    path('update-topic/', views.update_topic, name='update_topic'),

    # ==================================================
    # REPORTS
    # ==================================================
    path('reports/', views.Reports, name='reports'),
    path('export_excel/', views.export_excel, name='export_excel'),

    # ==================================================
    # MENTORS
    # ==================================================
    path('create-mentor/', views.create_mentor, name='create_mentor'),
    path('mentor-dashboard/', views.mentor_dashboard, name='mentor_dashboard'),

    # 🔥 FIXED PATH (IMPORTANT)
    path(
        'mentor/today-topics/',
        views.mentor_today_topics,
        name='mentor_today_topics'
    ),

    path('delete-mentor/<int:mentor_id>/', views.delete_mentor, name='delete_mentor'),
    path('update-mentor/', views.update_mentor, name='update_mentor'),

    # ==================================================
    # NAVBAR + ATTENDANCE
    # ==================================================
    path('navbar/', views.Navbar, name='navbar'),
    path('attendance/', views.attendance_page, name='attendance_page'),
    path('edit-attendance/<int:id>/', views.edit_attendance, name='edit_attendance'),
    path('delete-attendance/<int:id>/', views.delete_attendance, name='delete_attendance'),
    path('admin-attendance/', views.admin_attendance_page, name='admin_attendance_page'),

    # ==================================================
    # TASKS
    # ==================================================
    path("tasks/", views.task_list, name="task_list"),

    # ==================================================
    # STUDENT APIs
    # ==================================================
    path("api/student/login/", views.student_login_api),
    path("api/student/change-password/", views.change_password_api),
    path("api/student/topics/", views.student_topics_api),
    # path("api/student/topics/pdf/", views.student_topics_pdf),
    # path("api/student/topics/excel/", views.student_topics_excel),
    path("api/student/video/stream/<int:topic_id>/", views.stream_video),

    # ==================================================
    # STUDENT DASHBOARD + PROFILE
    # ==================================================
    path("api/student/dashboard/", views.student_dashboard_api),
    path("api/student/profile/", views.student_profile_api),
    path("api/student_settings_api/", views.student_settings_api),
    path("api/student/course-progress/", views.student_course_progress_api),

    # ==================================================
    # STUDENT ATTENDANCE + TASK LOG
    # ==================================================
    path(
        "api/student/attendance-dashboard/",
        views.student_attendance_dashboard_api
    ),
    path(
        "api/student/task-log/",
        views.student_task_log_api,
        name="student_task_log_api"
    ),
]

# ==================================================
# MEDIA FILES
# ==================================================
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

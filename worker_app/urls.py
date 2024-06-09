from django.urls import path

from worker_app import views


urlpatterns = [
    path("work/display",views.display_work,name="display_work"),
    path("work/display/<int:id>",views.work_detail,name="work_detail"),
    path("work/change_status/<int:id>",views.change_status,name="change_status"),
    #calendar 
    path("calendar",views.work_calendar,name="work_calendar"),
    path("calendar/<int:month>/<int:year>",views.work_calendar2,name="work_calendar"),
    path("next/month",views.next_month,name='next_month'),
    path("prev/month",views.prev_month,name='prev_month'),
    path("now/month",views.now_month,name='now_month'),
    #work history
    path('work/history',views.work_hist,name="work_history"),

] 
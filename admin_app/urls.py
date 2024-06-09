from django.urls import path
from admin_app import views

urlpatterns = [
    #เบ็ตเตล็ด
    path("search/user",views.search_user,name="search_user"),
    #order
    path("dashboard",views.dashboard,name='dashboard'),
    path("dashboard/status/<int:id>",views.update_order,name='dash_status'),
    path("dashboard/order/<int:id>",views.admin_ord,name="dash_detail"),
    path("dashboard/accept/<int:id>",views.accept_order,name="accept_order"),
    path("dashboard/cancel/<int:id>",views.cancel_order,name="cancel_order"),
    #product
    path("dashboard/product",views.admin_product,name="admin_product"),
    path("dashboard/product/delete/<int:id>",views.product_delete,name="product_delete"),
    path("dashboard/create/product",views.create_product,name="product_create"),
    path("dashboard/product/update/<int:id>",views.update_product,name="product_update"),
    #user
    path("dashboard/manage/user",views.manage_user,name="manage_user"),
    path("dashboard/create/user",views.create_user,name="create_user"),
    path("dashboard/create/worker/<int:id>",views.create_worker,name="create_worker"),
    #worker
    path("dashboard/display/worker",views.work_display,name="work_display"),
    path("dashboard/display/assign",views.assign_display,name="assign_display"),
    path("dashboard/show/worker/<int:id>",views.worker_show,name="worker_show"),
    path("dashboard/assign/work/<int:work_id>/<int:worker_id>",views.worker_assign,name="worker_assign"),
    path("dashboard/worker",views.worker_show2,name="worker_show2"),
    path("assign/delete/<int:id>",views.delete_assign,name="delete_assign"),
    path("worker/delete/<int:id>",views.admin_delete_worker,name="worker_delete"),
    
    #worker_calendar
    path("dashboard/cal/<int:worker_id>",views.admin_calendar,name="admin_calendar"),
    path("dashboard/cal/<int:month>/<int:year>/<int:worker_id>",views.admin_calendar2,name="work_calendar"),
    path("next/month2/<int:worker_id>",views.next_month,name='next_month2'),
    path("prev/month2/<int:worker_id>",views.prev_month,name='prev_month2'),
    path("now/month2/<int:worker_id>",views.now_month,name='now_month2'),
    #report
    path("dashboard/report", views.report,name="report"),
    path("dashboard/report/worker",views.report_worker,name="report_worker"),
    #assign bill
    path("dashboard/display/work_detail/<int:id>",views.admin_work_detail,name="admin_work_detail"),
    path("dashboard/create_bill/<int:id>",views.create_bill,name="create_bill"),
    #pos
    path("dashboard/pos", views.pos,name="pos"),
    path("dashboard/inc/<int:id>", views.inc_cart,name="pos_inc"),
    path("dashboard/dec/<int:id>", views.dec_cart,name="pos_dec"),
    path("dashboard/add_cart/<int:id>", views.admin_cart,name="admin_cart"),
    path("dashboard/delete_cart/<int:id>", views.delete_pos,name="pos_delete"),
    path("dashboard/add_stock/<int:id>",views.add_stock,name="add_stock"),
    #req work
    path("dashboard/repair",views.repair,name="repair"),
    path("repair/delete/<int:id>",views.delete_repair,name="repair_delete"),
    path("dashboard/change/<int:id>",views.admin_change_status,name="admin_change"),
    path("dashboard/work/history",views.work_admin_history,name="admin_work_history"),   
]
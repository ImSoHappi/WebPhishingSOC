from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='management_home'),

    # CLIENTS VIEW
    path('client_list', views.client_list, name='management_client_list'),
    path('client/add_client/', views.add_client, name='management_add_client'),

    # CLIENT - XLSX
    path('<str:client_pk>/view', views.client_view, name='management_client_view'),
    path('<str:client_pk>/addXLS', views.client_addXLS, name='management_client_addXLS'),
    path('<str:client_pk>/addXLS/<int:file_id>/preview', views.client_xls_preview, name='management_client_xls_preview'),
    path('<str:client_pk>/addXLS/<int:file_id>/delete', views.client_xls_delete, name='management_client_xls_delete'),
    path('<str:client_pk>/addXLS/<int:file_id>/process', views.client_xls_process, name='management_client_xls_process'),
    path('<str:client_pk>/exportXLS', views.client_xls_export, name='management_client_xls_export'),
    
    # CLIENT - EXERCISE
    path('<str:client_pk>/exercise/add', views.client_exercise_crud, name='management_client_exercise_add'),
    path('<str:client_pk>/exercise/<str:exercise_pk>', views.client_exercise_crud, name='management_client_exercise_edit'),
    
    # CLIENT - EXERCISE - CAMPAIGN
    path('<str:client_pk>/exercise/<str:exercise_pk>/campaign/add', views.client_campaign_crud, name='management_client_campaign_add'),
    path('<str:client_pk>/exercise/<str:exercise_pk>/campaign/<str:campaign_pk>', views.client_campaign_crud, name='management_client_campaign_edit'),

    # CLIENT - COLABORATOR
    path('<str:client_pk>/colaborator/add', views.client_colaborator_crud, name='management_client_colaborator_add'),
    path('<str:client_pk>/colaborator/<str:colaborator_pk>', views.client_colaborator_crud, name='management_client_colaborator_edit'),
    
    path('<str:client_pk>/', views.client_view, name='management_client_view'),
    #path('campaign_list/', webviews.campaign_list, name='campaign_list'),
    #path('campaign_list/add_campaign/', webviews.add_campaign, name='add_campaign'),
    #path('campaign_detail/<int:campaign_pk>/', webviews.campaign_detail, name='campaign_detail'),
    
    #path('client/<int:client_pk>/exercise_list/', webviews.exercise_list, name='exercise_list'),
    #path('client/<int:client_pk>/add_exercise/', webviews.add_exercise, name='add_exercise'),
    #path('client/<int:client_pk>/<int:exercise_pk>/exercise_detail/', webviews.exercise_detail, name='exercise_detail'),
    
    #path('client/<int:client_pk>/<int:exercise_pk>/add_employees', webviews.add_employees, name='add_employees'),
]
from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('papers/', views.paper_list, name='paper_list'),
    path('papers/<int:paper_id>/', views.paper_detail, name='paper_detail'),
    path('papers/<int:paper_id>/delete/', views.delete_paper, name='delete_paper'),
    path('statements/<int:statement_id>/theme-toggle/<int:theme_id>/', views.toggle_statement_theme, name='toggle_statement_theme'),
    path('themes/', views.theme_list, name='theme_list'),
    path('themes/<int:theme_id>/delete/', views.delete_theme, name='delete_theme'),
    path('synthesis/', views.synthesis, name='synthesis'),
    path('export/csv/', views.export_csv, name='export_csv'),
]

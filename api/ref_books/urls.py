from django.urls import path
from ref_books import views

app_name = "ref_books"


urlpatterns = [
    path('refbooks/', views.DirectionListView.as_view(), name='direction-list'),
    path('refbooks/<id>/elements/', views.DirectionElementListView.as_view(), name='element-list'),
    path('refbooks/<id>/check_element/', views.CheckElementView.as_view(), name='check-element'),
]

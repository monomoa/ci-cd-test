from django.urls import path
from Board import views

app_name='Board'
urlpatterns = [
    path('', views.BoardList.as_view(), name='list'),
    path('<int:pk>/', views.BoardDetail.as_view(), name='detail'),
    path('create_board/', views.BoardCreate.as_view(),name='board_create'),
    path('delete_board/<int:pk>/', views.BoardDelete,name='board_delete'),
    path('update_board/<int:pk>/', views.BoardUpdate.as_view(),name='board_update'),
    path('download/<int:pk>', views.Board_download, name="Board_download"),
]


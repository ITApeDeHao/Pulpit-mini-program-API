from django.urls import path
from forum import views
urlpatterns = [
    path(r'intro/',views.GetIntro.as_view()),
    path(r'forum/',views.Forum.as_view()),
    path(r'spot/',views.Spot.as_view()),
    path(r'comment/',views.Comment.as_view())
]

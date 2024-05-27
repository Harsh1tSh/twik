from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.endpoints),
    path('advocates/', views.advocates_list, name="advocates"),
    # path("advocates/<str:username>/", views.advocate_detail)
    path("advocates/<str:username>/", views.AdvocateDetail.as_view()),

    #comapnies
    path("companies/", views.companies_list)
]

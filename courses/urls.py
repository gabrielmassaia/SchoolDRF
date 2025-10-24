from django.urls import path
from .views import AvaliacaoAPIView, AvaliacoesAPIView, CursoAPIView, CursosAPIView

urlpatterns = [
    # Courses URLs
    path('cursos/', CursosAPIView.as_view(), name='cursos'),
    path('cursos/<int:pk>/', CursoAPIView.as_view(), name='curso'),

    # Avaliações URLs
    path('avaliacoes/', AvaliacoesAPIView.as_view(), name='avaliacoes'),
    path('avaliacoes/<int:pk>/', AvaliacaoAPIView.as_view(), name='avaliacao'),
]
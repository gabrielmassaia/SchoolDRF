from django.urls import path
from .views import AvaliacaoAPIView, AvaliacoesAPIView, CursoAPIView, CursosAPIView, CursoViewSet, AvaliacaoViewSet
import rest_framework.routers as SimpleRouters

router = SimpleRouters.DefaultRouter()
router.register(r'cursos', CursoViewSet, basename='cursos')
router.register(r'avaliacoes', AvaliacaoViewSet, basename='avaliacoes')

urlpatterns = [
    # Courses URLs
    path('cursos/', CursosAPIView.as_view(), name='cursos'),
    path('cursos/<int:curso_pk>/', CursoAPIView.as_view(), name='curso'),
    path('cursos/<int:curso_pk>/avaliacoes/', AvaliacoesAPIView.as_view(), name='curso_avaliacoes'),
    path('cursos/<int:curso_pk>/avaliacoes/<int:avaliacao_pk>/', AvaliacaoAPIView.as_view(), name='curso_avaliacao'),

    # Avaliações URLs
    path('avaliacoes/', AvaliacoesAPIView.as_view(), name='avaliacoes'),
    path('avaliacoes/<int:avaliacao_pk>/', AvaliacaoAPIView.as_view(), name='avaliacao'),
]
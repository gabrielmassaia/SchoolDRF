from rest_framework import serializers
from .models import Curso, Avaliacao


class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'email': {'write_only': True}
        }
        model = Avaliacao
        fields = (
            'id',
            'curso',
            'nome',
            'email',
            'comentario',
            'avaliacao',
            'criacao',
            'atualizacao',
            'ativo'
        )


class CursoSerializer(serializers.ModelSerializer):

    #1. Nested Relationship
    # avaliacoes = AvaliacaoSerializer(many=True, read_only=True)
    #2. Hyperlinked Relationship
    # url = serializers.HyperlinkedIdentityField(view_name='curso', lookup_field='id')
    #3. Custom Field
    avaliacoes = serializers.PrimaryKeyRelatedField(Many=True, read_only=True)
    

    def get_avaliacoes_count(self, obj):
        return obj.avaliacoes.count()
    class Meta:
        model = Curso
        fields = (
            'id',
            'titulo',
            'url',
            'criacao',
            'atualizacao',
            'ativo',
            'avaliacoes'
        )

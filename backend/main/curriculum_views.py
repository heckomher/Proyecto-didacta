"""
API Views para el Currículum Nacional
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from .mongo_models import (
    UnidadCurricular, ObjetivoAprendizaje, ObjetivoTransversal,
    Habilidad, Actitud, ASIGNATURAS_CODIGO, NIVELES_CODIGO
)


class UnidadesCurricularesView(APIView):
    """
    GET /api/curriculum/unidades/{nivel}/{asignatura}/
    Retorna las unidades curriculares para un nivel y asignatura
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, nivel, asignatura):
        try:
            unidades = UnidadCurricular.objects(
                nivel=nivel,
                asignatura=asignatura
            ).order_by('numero')
            
            data = [{
                'codigo': u.codigo,
                'numero': u.numero,
                'nombre': u.nombre,
                'descripcion': u.descripcion,
                'horas_sugeridas': u.horas_sugeridas,
                'semanas_sugeridas': u.semanas_sugeridas,
                'oa_count': len(u.oa_codigos),
                'priorizado_2025': u.priorizado_2025
            } for u in unidades]
            
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class UnidadDetalleView(APIView):
    """
    GET /api/curriculum/unidad/{codigo}/
    Retorna detalle completo de una unidad con OA, OAT, habilidades, actitudes
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, codigo):
        try:
            unidad = UnidadCurricular.objects.get(codigo=codigo)
            
            # Obtener OAs
            oas = ObjetivoAprendizaje.objects(codigo__in=unidad.oa_codigos)
            oas_data = [{
                'codigo': oa.codigo,
                'numero': oa.numero,
                'descripcion': oa.descripcion,
                'eje': oa.eje,
                'priorizado_2025': oa.priorizado_2025,
                'indicadores': [{
                    'codigo': ind.codigo,
                    'descripcion': ind.descripcion,
                    'verbo_infinitivo': ind.verbo_infinitivo
                } for ind in oa.indicadores],
                'articulaciones_con': [{
                    'asignatura_codigo': art.asignatura_codigo,
                    'asignatura_nombre': art.asignatura_nombre,
                    'oa_relacionado': art.oa_relacionado,
                    'descripcion': art.descripcion
                } for art in (oa.articulaciones_con or [])]
            } for oa in oas]
            
            # Obtener OATs
            oats = ObjetivoTransversal.objects(codigo__in=unidad.oat_codigos)
            oats_data = [{
                'codigo': oat.codigo,
                'dimension': oat.dimension,
                'descripcion': oat.descripcion
            } for oat in oats]
            
            # Obtener Habilidades
            habs = Habilidad.objects(codigo__in=unidad.habilidades_codigos)
            habs_data = [{
                'codigo': h.codigo,
                'descripcion': h.descripcion,
                'tipo': h.tipo
            } for h in habs]
            
            # Obtener Actitudes
            acts = Actitud.objects(codigo__in=unidad.actitudes_codigos)
            acts_data = [{
                'codigo': a.codigo,
                'descripcion': a.descripcion
            } for a in acts]
            
            return Response({
                'codigo': unidad.codigo,
                'nivel': unidad.nivel,
                'asignatura': unidad.asignatura,
                'numero': unidad.numero,
                'nombre': unidad.nombre,
                'descripcion': unidad.descripcion,
                'horas_sugeridas': unidad.horas_sugeridas,
                'semanas_sugeridas': unidad.semanas_sugeridas,
                'priorizado_2025': unidad.priorizado_2025,
                'objetivos_aprendizaje': oas_data,
                'objetivos_transversales': oats_data,
                'habilidades': habs_data,
                'actitudes': acts_data
            })
        except UnidadCurricular.DoesNotExist:
            return Response({'error': 'Unidad no encontrada'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class OAsPorNivelAsignaturaView(APIView):
    """
    GET /api/curriculum/oa/{nivel}/{asignatura}/
    Retorna todos los OA para un nivel y asignatura
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, nivel, asignatura):
        try:
            oas = ObjetivoAprendizaje.objects(
                nivel=nivel,
                asignatura=asignatura
            ).order_by('numero')
            
            data = [{
                'codigo': oa.codigo,
                'numero': oa.numero,
                'descripcion': oa.descripcion,
                'eje': oa.eje,
                'priorizado_2025': oa.priorizado_2025,
                'indicadores_count': len(oa.indicadores),
                'articulaciones_con': [{
                    'asignatura_codigo': art.asignatura_codigo,
                    'asignatura_nombre': art.asignatura_nombre
                } for art in (oa.articulaciones_con or [])]
            } for oa in oas]
            
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class CodigosCurriculumView(APIView):
    """
    GET /api/curriculum/codigos/
    Retorna los códigos de asignaturas y niveles para nomenclatura
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({
            'asignaturas': ASIGNATURAS_CODIGO,
            'niveles': NIVELES_CODIGO
        })


class OATsView(APIView):
    """
    GET /api/curriculum/oat/
    Retorna todos los Objetivos de Aprendizaje Transversales
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        dimension = request.query_params.get('dimension', None)
        
        if dimension:
            oats = ObjetivoTransversal.objects(dimension=dimension)
        else:
            oats = ObjetivoTransversal.objects.all()
        
        data = [{
            'codigo': oat.codigo,
            'dimension': oat.dimension,
            'descripcion': oat.descripcion
        } for oat in oats]
        
        return Response(data)


class HabilidadesPorNivelAsignaturaView(APIView):
    """
    GET /api/curriculum/habilidades/{nivel}/{asignatura}/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, nivel, asignatura):
        try:
            habs = Habilidad.objects(nivel=nivel, asignatura=asignatura)
            data = [{
                'codigo': h.codigo,
                'descripcion': h.descripcion,
                'tipo': h.tipo
            } for h in habs]
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class ActitudesPorAsignaturaView(APIView):
    """
    GET /api/curriculum/actitudes/{asignatura}/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, asignatura):
        try:
            acts = Actitud.objects(asignatura=asignatura)
            data = [{
                'codigo': a.codigo,
                'descripcion': a.descripcion
            } for a in acts]
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

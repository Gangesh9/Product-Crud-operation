from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from myapp.models import Product
from myapp.serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from myapp.models import Product
from django.utils import timezone
from datetime import timedelta

@api_view(['GET'])
def top_5_products(request, period=None):
    if period == 'all':
        products = Product.objects.annotate(retrieval_count=Count('access_logs')).order_by('-retrieval_count')[:5]
    elif period == 'last_day':
        products = Product.objects.filter(access_logs__access_date__gte=(timezone.now() - timedelta(days=1))).annotate(retrieval_count=Count('access_logs')).order_by('-retrieval_count')[:5]
    elif period == 'last_week':
        products = Product.objects.filter(access_logs__access_date__gte=(timezone.now() - timedelta(days=7))).annotate(retrieval_count=Count('access_logs')).order_by('-retrieval_count')[:5]
    else:
        return Response({'error': 'Invalid period'})

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

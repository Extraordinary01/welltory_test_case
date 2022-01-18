from math import sqrt

from django.contrib.auth import authenticate, logout
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, \
    HTTP_201_CREATED
from rest_framework.permissions import IsAuthenticated
from .models import DataType, Correlation
from .serializers import CorrelationSerializer


@api_view(['POST'])
def custom_login(request):
    data = request.data
    try:
        username = data['username']
        password = data['password']
    except:
        return Response(status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is None:
        return Response(status=HTTP_401_UNAUTHORIZED)

    token, created = Token.objects.get_or_create(user=user)
    return Response(data={'token': token.key, }, status=HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def custom_logout(request):
    try:
        request.user.auth_token.delete()
        logout(request)
        return Response(status=HTTP_200_OK)
    except:
        return Response(status=HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calculate(request):
    data = request.data
    user_data = data["data"]
    x_data_type = DataType.objects.get_or_create(name=user_data["x_data_type"].strip())
    y_data_type = DataType.objects.get_or_create(name=user_data["y_data_type"].strip())
    x_data = {}
    for item in user_data["x"]:
        x_data[item["date"].strip()] = item["value"]
    result = []
    for item in user_data["y"]:
        if item["date"].strip() in x_data.keys():
            result.append({'x': x_data[item["date"].strip()], 'y': item["value"]})
    x_avg = sum(item['x'] for item in result) / len(result)
    y_avg = sum(item['y'] for item in result) / len(result)
    num = 0
    x_avg_sqr_sum = 0
    y_avg_sqr_sum = 0
    for item in result:
        num += (item['x'] - x_avg) * (item['y'] - y_avg)
        x_avg_sqr_sum += pow(item['x'] - x_avg, 2)
        y_avg_sqr_sum += pow(item['y'] - y_avg, 2)
    div = sqrt(x_avg_sqr_sum * y_avg_sqr_sum)
    r_value = num / div
    p_value = (r_value * sqrt(len(result) - 2)) / (sqrt(1 - pow(r_value, 2)))
    try:
        correlation = Correlation.objects.create(user_id=data["user_id"], x_data_type=x_data_type[0],
                                                 y_data_type=y_data_type[0], value=r_value, p_value=p_value)
        return Response(status=HTTP_201_CREATED)
    except:
        correlation = Correlation.objects.get(user_id=data["user_id"], x_data_type=x_data_type[0],
                                              y_data_type=y_data_type[0])
        correlation.value = r_value
        correlation.p_value = p_value
        correlation.save()
        return Response(status=HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_correlation(request):
    x_data_type = request.GET.get('x_data_type')
    y_data_type = request.GET.get('y_data_type')
    user_id = request.GET.get('user_id')
    try:
        correlation = Correlation.objects.get(user_id=user_id, x_data_type__name=x_data_type,
                                              y_data_type__name=y_data_type)
        serializer = CorrelationSerializer(correlation)
        return Response(serializer.data, status=HTTP_200_OK)
    except:
        return Response(status=HTTP_404_NOT_FOUND)

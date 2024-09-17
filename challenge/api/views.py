from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Receipt 
from .serializers import ReceiptSerializer

# Create your views here.

@api_view(["POST"])
def process(request):
    data = request.data
    if "items" not in data.keys():
        return Response({"Message": "Items key not found in json body"}, status=status.HTTP_400_BAD_REQUEST) 
    if not data["items"]:
        return Response({"Message": "Items list is empty"}, status=status.HTTP_400_BAD_REQUEST) 
    data["items"] =  ''.join([str(d) for d in data["items"]])
    receiptSerializer = ReceiptSerializer(data=data)
    if receiptSerializer.is_valid(): 
        receipt = receiptSerializer.save()
        return JsonResponse({"id": receipt.pk})
    else:
        return Response(receiptSerializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(["GET"])
def getPoints(request, id):
    if not Receipt.objects.filter(pk=id).exists():
        return Response({"Message": f"Receipt id of {id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
    receipt = Receipt.objects.get(pk=id)
    points = receipt.calculatePoints()
    return JsonResponse({'points': points})
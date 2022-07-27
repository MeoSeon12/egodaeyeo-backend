from multiprocessing import context
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from item.models import Item as ItemModel
from contract.models import Contract as ContractModel
from .serializers import ContractSerializer

class ContractView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, item_id):
        # user = request.user
        item = ItemModel.objects.get(id=item_id)
        contract = ContractModel.objects.get(item=item)
        
        contract_serializer = ContractSerializer(contract, context={"request": request})
        
        return Response(contract_serializer.data, status=status.HTTP_200_OK)

    # 대여신청 버튼 클릭시
    def post(self, request, item_id):
        user_id = request.user.id
        start_date = request.data.get("startTime")
        end_date = request.data.get("endTime")
        item = ItemModel.objects.get(id=item_id)

        contract_data = {
            "user": user_id,
            "item": item.id,
            "start_date": start_date,
            "end_date": end_date
        }

        contract_serializer = ContractSerializer(data=contract_data, context={"request": request})
    
        if contract_serializer.is_valid():
            contract_serializer.save()
            return Response(contract_serializer.data, status=status.HTTP_200_OK)
    
        return Response(contract_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, item_id):
        
        return Response({"msg": "status"})
    
    def delete(self, request, item_id):
        
        return Response({"msg": "status"})
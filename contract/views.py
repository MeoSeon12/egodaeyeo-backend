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
    
    #대여신청 도착 버튼 클릭시
    def get(self, request, item_id):
        item = ItemModel.objects.get(id=item_id)
        contract = ContractModel.objects.get(item=item)
        contract_serializer = ContractSerializer(contract)
        
        return Response(contract_serializer.data, status=status.HTTP_200_OK)

    # 대여신청 버튼 클릭시
    def post(self, request, item_id):
        user_id = request.user.id
        start_date = request.data.get("startTime")
        end_date = request.data.get("endTime")
        item = ItemModel.objects.get(id=item_id)
        
        try:
            print("여기로들어오아")
            contract = ContractModel.objects.get(item=item, user=user_id)
            if contract:
                return Response({"msg": "이미 대여신청한 물품입니다."})
            
        except ContractModel.DoesNotExist:

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
    
    #대여신청 내역 수락 클릭시
    def put(self, request, item_id):
        user_id = request.user.id
        item = ItemModel.objects.get(id=item_id, user=user_id)

        contract = ContractModel.objects.get(item=item)
        contract.status = "대여 중"
        contract.save()
        
        return Response({"msg": "대여 신청 수락"}, status=status.HTTP_200_OK)
    
    #대여신청 거절 클릭시
    def delete(self, request, item_id):
        user_id = request.user.id
        item = ItemModel.objects.get(id=item_id, user=user_id)
        contract = ContractModel.objects.get(item=item)
        
        contract.delete()
        
        return Response({"msg": "대여 신청 삭제"}, status=status.HTTP_200_OK)
from multiprocessing import context
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from item.models import Item as ItemModel
from contract.models import Contract as ContractModel
from .serializers import ContractSerializer
from chat.models import ChatRoom as ChatRoomModel


class ContractView(APIView):
    authentication_classes = [JWTAuthentication]
    
    #대여신청 도착 버튼 클릭시 계약날짜 정보 조회
    def get(self, request, item_id):
        room_id = request.GET.get('room_id', "")
        chatroom = ChatRoomModel.objects.get(id=room_id)
        
        item = ItemModel.objects.get(id=item_id)
        contract = ContractModel.objects.get(item=item, user=chatroom.inquirer)
        contract_serializer = ContractSerializer(contract)
        
        return JsonResponse(contract_serializer.data, status=status.HTTP_200_OK)

    # 대여신청 버튼 클릭시
    def post(self, request, item_id):
        user_id = request.user.id
        start_date = request.data.get("startTime")
        end_date = request.data.get("endTime")
        item = ItemModel.objects.get(id=item_id)
        
        try:
            contract = ContractModel.objects.get(item=item, user=user_id)
            if contract:
                return JsonResponse({"msg": "이미 대여신청한 물품입니다."})
            
        except ContractModel.DoesNotExist:
            contract_data = {
                "user": user_id,
                "item": item.id,
                "start_date": start_date,
                "end_date": end_date,
                "status": '검토 중'
            }

            contract_serializer = ContractSerializer(data=contract_data, context={"request": request})
        
            if contract_serializer.is_valid():
                contract_serializer.save()
                return JsonResponse(contract_serializer.data, status=status.HTTP_200_OK)
        
            return JsonResponse(contract_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #대여신청 내역 수락 클릭시
    def put(self, request, item_id):
        user_id = request.user.id
        room_id = request.GET.get('room_id', "")
        status_str = request.data.get('status')

        try:
            #아이템 status 변경
            item = ItemModel.objects.get(id=item_id, user=user_id)
            item.status = status_str
            item.save()
            
            #계약 status 변경 
            current_chat_room = ChatRoomModel.objects.get(item=item_id, id=room_id)
            contract = ContractModel.objects.get(item=item, user=current_chat_room.inquirer)
            contract.status = status_str
            contract.save()
            
            return JsonResponse({"msg": "계약 수정 완료", "status": contract.status, "room_id": current_chat_room.id}, status=status.HTTP_200_OK)
        except:
            return JsonResponse({"msg": "계약 수정 실패"}, status=status.HTTP_400_BAD_REQUEST)
        
        
    #대여신청 거절 클릭시
    def delete(self, request, item_id):
        user_id = request.user.id
        room_id = request.GET.get('room_id', "")
        try:
            item = ItemModel.objects.get(id=item_id, user=user_id)
            current_chat_room = ChatRoomModel.objects.get(item=item_id, id=room_id)
            contract = ContractModel.objects.get(item=item, user=current_chat_room.inquirer)
            contract.delete()
            
            return JsonResponse({"msg": "대여 신청 거절완료", "status" : None, "room_id": current_chat_room.id}, status=status.HTTP_200_OK)
        except ContractModel.DoesNotExist:
            return JsonResponse({"msg": "계약이 더이상 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        
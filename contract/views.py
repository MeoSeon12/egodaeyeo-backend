from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from item.models import Item as ItemModel
from contract.models import Contract as ContractModel
from .serializers import ContractSerializer
from chat.models import ChatRoom as ChatRoomModel
from django.db.models import Q


class ContractView(APIView):
    authentication_classes = [JWTAuthentication]
    
    #대여신청 도착 버튼 클릭시 계약날짜 정보 조회
    def get(self, request, item_id):
        room_id = request.GET.get('room_id', "")
        chatroom = ChatRoomModel.objects.get(id=room_id)
        
        item = ItemModel.objects.get(id=item_id)
        contract = ContractModel.objects.get(Q(item=item) & Q(user=chatroom.inquirer) & ~Q(status="대여 종료"))
        contract_serializer = ContractSerializer(contract)
        return Response(contract_serializer.data, status=status.HTTP_200_OK)

    # 대여신청 버튼 클릭시
    def post(self, request, item_id):
        user_id = request.user.id
        start_date = request.data.get("startTime")
        end_date = request.data.get("endTime")
        item = ItemModel.objects.get(id=item_id)
        
        contracts_status = ContractModel.objects.filter(item=item, user=user_id).values('status')
        
        if contracts_status.exists():
            #조회된 contract가 있는 경우 종료된 contract인지 진행되고 있는 contract인지 판단
            #진행되고 있지 않고 종료된 contract만 있다면, contract생성 (빌렸던 사람이 다시 빌리기 위한 로직)
            
            not_available_status_list = ['대여 중', '검토 중']
            contract_status_list = [contract_status['status'] for contract_status in contracts_status]
            
            for not_available_status in not_available_status_list:
                if not_available_status in contract_status_list:
                    return Response({"msg": "이미 신청한 물품입니다."}, status=status.HTTP_208_ALREADY_REPORTED)
                else:
                    continue
            
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
                return Response(contract_serializer.data, status=status.HTTP_200_OK)
            return Response(contract_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            #조회된 contract가 하나도 없는 경우 새로 생성
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
                return Response(contract_serializer.data, status=status.HTTP_200_OK)
        
            return Response(contract_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #대여신청 내역 수락 클릭시
    def put(self, request, item_id):
        user_id = request.user.id
        room_id = request.GET.get('room_id', "")
        status_ = request.data.get('status')

        try:
            item = ItemModel.objects.get(id=item_id, user=user_id)
            current_chat_room = ChatRoomModel.objects.get(item=item_id, id=room_id)
            contract = ContractModel.objects.get(Q(item=item) & Q(user=current_chat_room.inquirer) & ~Q(status="대여 종료"))
        except ItemModel.DoesNotExist:
            return Response({"msg": "아이템이 더이상 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        #아이템 status 변경
        item.status = status_
        item.save()
        
        #계약 status 변경 
        contract.status = status_
        contract.save()
        
        return Response({"msg": "계약 수정 완료", "status": contract.status, "room_id": current_chat_room.id}, status=status.HTTP_200_OK)
        
        
    #대여신청 거절 클릭시
    def delete(self, request, item_id):
        user_id = request.user.id
        room_id = request.GET.get('room_id', "")
        try:
            item = ItemModel.objects.get(id=item_id, user=user_id)
            current_chat_room = ChatRoomModel.objects.get(item=item_id, id=room_id)
            contract = ContractModel.objects.get(Q(item=item) & Q(user=current_chat_room.inquirer) & ~Q(status="대여 종료"))
            contract.delete()
            
            return Response({"msg": "대여 신청 거절완료", "status" : None, "room_id": current_chat_room.id}, status=status.HTTP_200_OK)
        except ContractModel.DoesNotExist:
            return Response({"msg": "계약이 더이상 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Community
from .serializers import CommunitySerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class CommunityAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        communities = Community.objects.all()
        serializer = CommunitySerializer(communities, many=True)
        return Response({"message": "모든 게시글 목록 조회 완료", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CommunitySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_id=request.user)
            return Response({"message": "게시글 작성 완료", "data": serializer.data}, status=status.HTTP_201_CREATED)
    
class CommunityDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        community = Community.objects.get(id=post_id)
        serializer = CommunitySerializer(community)
        return Response({"message": "게시글 상세 조회 완료", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def put(self, request, post_id):
        community = Community.objects.get(id=post_id)
        if community.user_id != request.user:
            return Response({"message": "게시글 수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommunitySerializer(community, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "게시글 수정 완료", "data": serializer.data}, status=status.HTTP_200_OK)
        
    def delete(self, request, post_id):
        community = Community.objects.get(id=post_id)
        if community.user_id != request.user:
            return Response({"message": "게시글 삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        community.delete()
        return Response({"message": "게시글 삭제 완료"}, status=status.HTTP_200_OK)
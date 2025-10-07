from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import PrayerFormSerializer


# Views
@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def prayer_form_view(request):
    """
    POST: Handle submision of prayer request form
    """
    if request.method == 'POST':
        serializer = PrayerFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    elif request.method == 'GET':
        if not request.user.is_authenticated:
            return Response({"error" : "Be an admin to view prayer requests"}, status=status.HTTP_401_UNAUTHORIZED)
        
        prayers = PrayerFormSerializer.objects.all().order_by('-created_at')
        serializer = PrayerFormSerializer(prayers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
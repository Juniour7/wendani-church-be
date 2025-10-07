from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import PrayerFormSerializer, BaptismFormSerializer, DedicationFromSerializer, MembershipSerializer, ContactFormSerializer
from .models import PrayerRequestForm, BaptismRequestForm, DedicationForm, MembershipTransferForm, ContactForm


# ---------- PRAYER REQUESTS ----------

@api_view(['POST'])
@permission_classes([AllowAny])
def prayer_form_submit_view(request):
    """Anyone can submit a prayer request."""
    serializer = PrayerFormSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prayer_form_list_view(request):
    """Authenticated users (or admins) can view all prayer requests."""
    prayers = PrayerRequestForm.objects.all().order_by('-created_at')
    serializer = PrayerFormSerializer(prayers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ---------- BAPTISM REQUESTS ----------

@api_view(['POST'])
@permission_classes([AllowAny])
def baptism_form_submit_view(request):
    """Anyone can submit a baptism request."""
    serializer = BaptismFormSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def baptism_form_list_view(request):
    """Authenticated users (or admins) can view baptism requests."""
    baptism_requests = BaptismRequestForm.objects.all().order_by('-created_at')
    serializer = BaptismFormSerializer(baptism_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ---------- DEDICATION REQUESTS ----------

@api_view(['POST'])
@permission_classes([AllowAny])
def dedication_form_submit_view(request):
    """Anyone can submit a dedication form."""
    serializer = DedicationFromSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dedication_form_list_view(request):
    """Authenticated users (or admins) can view dedication forms."""
    dedications = DedicationForm.objects.all().order_by('-created_at')
    serializer = DedicationFromSerializer(dedications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ---------- MEMEBERSHIP TRANSFER REQUESTS ----------

@api_view(['POST'])
@permission_classes([AllowAny])
def membership_submit_view(request):
    """Anyone can submit a memeberhsip transfer request"""
    serializer = MembershipSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def membership_form_view(request):
    """List all membership form requests"""
    if request.method == 'GET':
        members = MembershipTransferForm.objects.all().order_by('-created_at')
        serializer = MembershipSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ---------- MEMEBERSHIP TRANSFER REQUESTS ----------

@api_view(['POST'])
@permission_classes([AllowAny])
def contact_form_submit(request):
    """Submitting Contact Form"""
    serializer = ContactFormSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes(['GET'])
def contact_form_view(request):
    """List Contacts as Admin"""
    contacts = ContactForm.objects.all().order_by('-created_at')
    serializer = ContactFormSerializer(contacts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import PrayerFormSerializer, BaptismFormSerializer, DedicationFromSerializer, MembershipSerializer, ContactFormSerializer, EventsSerializer, AnnouncementsSerializer, BenevolenceSerializer
from .models import PrayerRequestForm, BaptismRequestForm, DedicationForm, MembershipTransferForm, ContactForm, Events, Announcements, BenevolenceForm


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


# ---------- BENEVOLENCE REQUESTS ENDPOINTS ----------

@api_view(['POST'])
@permission_classes([AllowAny])
def benevolence_submit_view(request):
    """
    Anyone can place a benevolence registration
    """
    if request.method == 'POST':
        serializer = BenevolenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def benevolence_list_view(request):
    """
    GET:
    - Authenticated users can:
      • View all benevolence forms
      • Update the status of a specific form using query params (?id=<id>&status=<new_status>)
    """
    form_id = request.query_params.get('id')
    new_status = request.query_params.get('status')

    # If admin/staff wants to change status
    if form_id and new_status:
        valid_statuses = [choice[0] for choice in BenevolenceForm.REGISTRATION_STATUS]

        if new_status not in valid_statuses:
            return Response(
                {"detail": f"Invalid status value. Must be one of: {valid_statuses}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            form = BenevolenceForm.objects.get(pk=form_id)
        except BenevolenceForm.DoesNotExist:
            return Response(
                {"detail": "Form not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        form.status = new_status
        form.save()

        serializer = BenevolenceSerializer(form)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Otherwise, just list all
    forms = BenevolenceForm.objects.all().order_by('-created_at')
    serializer = BenevolenceSerializer(forms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ---------- EVENTS HANDLING ENDPOINTS ----------


@api_view(['POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def events_submit(request):
    """
    POST: Create new events
    PUT: Update current events
    DELETE: Delete events 
    """
    # ------POST------
    if request.method == 'POST':
        serializer = EventsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # -------UPDATE-----
    elif request.method == 'PUT':
        event_id = request.data.get('id') or request.data.get('pk')
        if not event_id:
            return Response({"detail" : "Event ID is required to update."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            event = Events.objects.get(pk=event_id)
        except Events.DoesNotExist:
            return Response({"detail" : "Event Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EventsSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # ------DELETE-------
    elif request.method == 'DELTE':
        event_id = request.data('id') or request.data.get('pk')

        if not event_id:
            return Response({"detail" : "Event ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            events = Events.objects.get(pk=event_id)
        except Events.DoesNotExist:
            return Response({"detail" : "Events not found"}, status=status.HTTP_404_NOT_FOUND)
        
        events.delete()
        return Response({"detail" : "Event deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        

@api_view(['GET'])
@permission_classes([AllowAny])
def events_list_view(request,pk=None):
    """
    GET:
    - If `pk` is provided → Retrieve a single event
    - If `pk` is not provided → Retrieve all events
    """
    if request.method == 'GET':
        if pk: # detail view
            try:
                event = Events.objects.get(pk=pk)
            except Events.DoesNotExist:
                return Response({"detail" : "Event not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = EventsSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else: #list view
            events = Events.objects.all().order_by('date')
            serializer = EventsSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


# ---------- ANNOUNCEMENTS HANDLING ENDPOINTS ----------

@api_view(['POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def announcements_submit(request):
    """
    POST: Create new announcements files
    PUT: Update current announcements
    DELETE: Delete announcements
    """
    # -------POST--------
    if request.method == 'POST':
        serializer = AnnouncementsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # ------UODATE--------
    elif request.method == 'PUT':
        file_id = request.data.get('id') or request.data.get('pk')

        if not file_id:
            return Response({"detail" : "Announcements Id Required To update"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            file = Announcements.objects.get(pk=file_id)
        except Announcements.DoesNotExist:
            return Response({"detail" : "File does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AnnouncementsSerializer(file, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # -------DELETE------
    elif request.method == 'DELETE':
        file_id = request.data.get('id') or request.data.get('pk')

        if not file_id:
            return Response({"detail" : "You need file id to delete a file"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            file = Announcements.objects.get(pk=file_id)
        except Announcements.DoesNotExist:
            return Response({"error" : "File does not exists"}, status=status.HTTP_404_NOT_FOUND)
        
        file.delete()
        return Response({"detail" : "File deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def announcements_list_view(request):
    """
    GET: View a list of file uploads
    """
    if request.method == 'GET':
        files = Announcements.objects.all().order_by('-created_at')
        serializer = AnnouncementsSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
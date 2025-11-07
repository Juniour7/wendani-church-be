from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .utils import send_confirmation_email

from .serializers import (
    PrayerFormSerializer, BaptismFormSerializer, DedicationFromSerializer,
    MembershipSerializer, ContactFormSerializer, EventsSerializer,
    AnnouncementsSerializer, BenevolenceSerializer
)

from .models import (
    PrayerRequestForm, BaptismRequestForm, DedicationForm,
    MembershipTransferForm, ContactForm, Events, Announcements,
    BenevolenceForm
)


# =============================
# Base Permission Behavior
# =============================

class PublicSubmitView(ModelViewSet):
    """
    Allows ANYONE to create/submit forms,
    but restricts all other actions to authenticated users.
    """

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]



# ---------- PRAYER REQUESTS ----------

class PrayerRequestViewSet(PublicSubmitView):
    """
    Handle Form submission
    """
    queryset = PrayerRequestForm.objects.all().order_by('-created_at')
    serializer_class = PrayerFormSerializer

    def perform_create(self, serializer):
        """When a prayer request is submitted (POST), save the data only."""
        serializer.save()


    @action(detail=True, methods=['PATCH'], permission_classes=[IsAuthenticated])
    def update_status(self, request, pk=None):
        prayer = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(PrayerRequestForm.ACTION):
            return Response({"detail" : "Invalid Status"}, status=400)
        
        prayer.status = new_status
        prayer.save()
        return Response(self.get_serializer(prayer).data)



# ---------- BAPTISM REQUESTS ----------

class BaptismRequestViewSet(PublicSubmitView):
    queryset = BaptismRequestForm.objects.all().order_by('-created_at')
    serializer_class = BaptismFormSerializer

    @action(detail=True, methods=['PATCH'], permission_classes=[IsAuthenticated])
    def status_update(self, request, pk=None):
        baptism = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(BaptismRequestForm.ACTION):
            return Response({"detail" : "Invalid Status"})
        
        baptism.status = new_status
        baptism.save()
        return Response(self.get_serializer(baptism).data)



# ---------- DEDICATION REQUESTS ----------

class DedicationViewSet(PublicSubmitView):
    queryset = DedicationForm.objects.all().order_by('-created_at')
    serializer_class = DedicationFromSerializer

    @action(detail=True, methods=['PATCH'], permission_classes=[IsAuthenticated])
    def status_update(self, request, pk=None):
        dedication = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(DedicationForm.ACTION):
            return Response({"detail" : "Invalid Status"})
        
        dedication.status = new_status
        dedication.save()
        return Response(self.get_serializer(dedication).data)




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
@permission_classes([IsAuthenticated])
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
def events_submit(request, pk):
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
    elif request.method == 'DELETE':
        event_id = request.data.get('id') or request.data.get('pk')

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

class AnnouncementsListCreateView(APIView):
    """
    GET: List  all announcements
    POST: Create a new announcements
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """Listig all announcementsx"""
        files = Announcements.objects.all().order_by('-created_at')
        serializer = AnnouncementsSerializer(files, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """Creating a announcements"""
        serializer = AnnouncementsSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AnnouncementsDetailView(APIView):
    """
    GET: Retrieve an announcement
    PUT: Update an announcement
    DELETE: Delete an announcement
    """
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return Announcements.objects.get(pk=pk)
        except Announcements.DoesNotExist:
            return None
    
    def get( self, request, pk):
        announcement = self.get_object(pk)
        if not announcement:
            return Response({"detail": "Announcement not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AnnouncementsSerializer(announcement)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        announcement = self.get_object(pk)
        if not announcement:
            return Response({"detail": "Announcement not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AnnouncementsSerializer(announcement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        announcement = self.get_object(pk)
        if not announcement:
            return Response({"detail": "Announcement not found"}, status=status.HTTP_404_NOT_FOUND)
        announcement.delete()
        return Response({"detail": "Announcement deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

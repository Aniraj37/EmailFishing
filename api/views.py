from rest_framework.generics import GenericAPIView
from .serializers import FailureEmailByIDSerializer, ReadFileSerializer, FailureEmailSerializer
from utils.utility import project_return
from .filereader import read_setup_file, read_email_file, segment_extraction
from rest_framework import status
from .models import EmailScan, FailureEmail
from django.db import transaction
from utils.pagination import CustomPagination

class FileReader(GenericAPIView):
    serializer_class = ReadFileSerializer
    
    def post(self,request,*args, **kwargs):
        # --- store user input ---
        setup_file = request.FILES.get('setup')
        email_file = request.FILES.get('email')

        # --- check input ---
        if not setup_file or not email_file:
            return project_return(
                message = "File upload missing.",
                status = status.HTTP_400_BAD_REQUEST
            )
        
        # --- Call function and check ---
        setup_result = read_setup_file(setup_file)

        if not setup_result:
            return project_return(
                message="File is Empty / File Type not Supported.",
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            )
        
        # --- Call function and check ---
        email_result = read_email_file(email_file)
        if not email_result:
            return project_return(
                message="File is Empty / File Type not Supported.",
                status=status.HTTP_204_NO_CONTENT
            )
        
        # --- store extracted segments ---
        extracted_segments = segment_extraction(email_lines=email_result, rules=setup_result)

        # --- check if there is no matched phrase ---
        if not extracted_segments:
            return project_return(
                message="Email check complete: no suspicious phrases detected.",
                status = status.HTTP_200_OK
            )
        
        # --- store any flagged email to the database ---
        with transaction.atomic():
            email = EmailScan.objects.create(setup_file=setup_file, email_file=email_file)
            for phrase, data in extracted_segments.items():
                if data["status"] == "Segment_found" and data["total_count"] >0:
                    FailureEmail.objects.create(
                        email = email,
                        phrase = phrase,
                        start_line = data["start_line"],
                        segment_lines = data["segment_lines"],
                        matched_segments = data["matched_segments"],
                        total_count=data["total_count"]
                    )
        # --- Display result ---
        return project_return(
            message="Email check complete: suspicious phrases detected.",
            data = {"id":email.id,
                    "result":extracted_segments},
            status = status.HTTP_200_OK
        )


class FileReaderView(GenericAPIView):
    """
    - Fetches all the Failed EMails stored in the database
    """

    queryset = FailureEmail.objects.all()
    serializer_class = FailureEmailSerializer

    def get(self, request, *args, **kwargs):
        # --- fetch data from the database ---
        filter_obj = self.filter_queryset(self.get_queryset())
        data = self.paginate_queryset(filter_obj)
        email_obj = self.serializer_class(data, many=True)

        # --- Display results ---
        return project_return(
            message="Data fetched successfully.",
            data = self.get_paginated_response(email_obj.data),
            status=status.HTTP_200_OK
        )
class FileByIDView(GenericAPIView):
    """
    - returns all the found suspisious files for a particular file
    """

    queryset = FailureEmail.objects.all()
    serializer_class = FailureEmailByIDSerializer

    def get(self, request, *args, **kwargs):
        # --- filter data and fetch data from the database based on provided email_id ---
        email_obj = self.get_queryset().filter(email=kwargs.get("id"))

        # --- check data ---
        if not email_obj:
            return project_return(
                message="No data found.",
                status=status.HTTP_404_NOT_FOUND
            )
        
        # --- Paginate the data ---
        filter_obj = self.filter_queryset(email_obj)
        data = self.paginate_queryset(filter_obj)
        request_obj = self.serializer_class(data, many=True)

        # --- Display results ---
        return project_return(
            message="Data fetched successfully.",
            data={
                "id":kwargs.get("id"),
                "result": self.get_paginated_response(request_obj.data)
                },
            status=status.HTTP_200_OK,
        )
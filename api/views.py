from rest_framework.generics import GenericAPIView
from .serializers import ReadFileSerializer
from utils.utility import project_return
from .filereader import read_setup_file, read_email_file, segment_extraction
from rest_framework import status
from .models import EmailScan, FailureEmail

class FileReader(GenericAPIView):
    serializer_class = ReadFileSerializer
    

    def post(self,request,*args, **kwargs):
        setup_file = request.FILES.get('setup')
        email_file = request.FILES.get('email')

        if not setup_file or not email_file:
            print("Yes")
            return project_return(
                message = "File not uploaded.",
                status = status.HTTP_400_BAD_REQUEST
            )
        
        setup_result = read_setup_file(setup_file)

        if not setup_result:
            return project_return(
                message="File not supported.",
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            )
        

        email_result = read_email_file(email_file)
        if not email_result:
            return project_return(
                message="File is Empty / Wrong File Type",
                status=status.HTTP_204_NO_CONTENT
            )
        
        extracted_segments = segment_extraction(email_lines=email_result, rules=setup_result)

        if not extracted_segments:
            return project_return(
                message="There is no suspicious phrase found",
                data = extracted_segments,
                status = status.HTTP_204_NO_CONTENT
            )
        
        email = EmailScan.objects.create(setup_file=setup_file, email_file=email_file)

        return project_return(
            message="Successfully Read",
            data = extracted_segments,
            status = status.HTTP_200_OK
        )

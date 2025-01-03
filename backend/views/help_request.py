from django.core.files import File
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.models.help_request import HelpRequest
from backend.mailers.help_request_emailer import HelpRequestEmailer


class SubmitHelpRequestView(APIView):

    def post(self, request):
        try:
            # Extract data from request
            email = request.data.get('email')
            subject = request.data.get('subject')
            description = request.data.get('description')
            attachment = request.FILES.get('attachment')

            # Validate email
            validate_email(email)

            # Validate required fields
            if not all([email, subject, description]):
                raise ValidationError(
                    "Email, subject, and description are required fields.")

            # Create HelpRequest instance
            help_request = HelpRequest(
                email=email,
                subject=subject,
                description=description
            )

            if attachment:
                help_request.attachment.save(attachment.name, File(attachment))

            help_request.save()

            HelpRequestEmailer(help_request).send_confirmation_email()

            return Response({"message": "Help request created successfully"}, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

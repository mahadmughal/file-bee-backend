from django.http import JsonResponse
from rest_framework.views import APIView
from backend.models.file_conversion import DocumentConversion, SupportedConversion
from backend.models.user import CustomToken
from django.contrib.auth.models import AnonymousUser


class UploadAndCreateDocumentView(APIView):
    def post(self, request):
        auth_token = request.POST.get("auth_token")

        if auth_token == 'null':
            user = None
        else:
            try:
                token = CustomToken.objects.get(key=auth_token)
                if token.is_expired():
                    token.delete()
                    user = None
                else:
                    user = token.user

            except CustomToken.DoesNotExist:
                user = None

        original_file = request.FILES.get("original_file", None)
        if not original_file:
            return JsonResponse({"error": "original_file is required"}, status=400)

        converted_mimetype = request.POST.get("converted_mimetype")
        if not converted_mimetype:
            return JsonResponse({"error": "converted_mimetype is required"}, status=400)

        original_mimetype = SupportedConversion.get_original_mimetype(
            original_file.content_type, original_file.name.split('.')[-1])

        user = request.user if not isinstance(
            request.user, AnonymousUser) else None

        document_conversion = DocumentConversion.objects.create(
            original_file=original_file,
            original_filename=original_file.name,
            original_mimetype=original_mimetype,
            original_size=original_file.size,
            converted_mimetype=converted_mimetype,
            status="processing",
            user=user,
        )
        document_conversion.conversion()
        converted_file = document_conversion.converted_file

        if converted_file:
            return JsonResponse(
                document_conversion.to_dict(), status=200
            )
        else:
            return JsonResponse({'error': 'unable to convert file'}, status=500)


class TargetConversionsView(APIView):
    def get(self, request):
        supported_conversions = SupportedConversion.get_available_conversions_for_all_sources()
        return JsonResponse({'supported_conversions': supported_conversions})

from django.shortcuts import render
from django.http import FileResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from backend.models.file_conversion import DocumentConversion, SupportedConversion
from backend.auth import CustomTokenAuthentication


class UploadAndCreateDocumentView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        original_file = request.FILES.get("original_file", None)
        if not original_file:
            return JsonResponse({"error": "original_file is required"}, status=400)

        converted_mimetype = request.POST.get("converted_mimetype")
        if not converted_mimetype:
            return JsonResponse({"error": "converted_mimetype is required"}, status=400)

        original_mimetype = SupportedConversion.get_original_mimetype(
            original_file.content_type, original_file.name.split('.')[-1])

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
            response = FileResponse(open(converted_file.path, 'rb'))
            response['Content-Type'] = document_conversion.converted_mimetype
            response['Content-Disposition'] = f'attachment; filename="{
                document_conversion.converted_filename}"'
            return response
        else:
            return JsonResponse({'error': 'unable to convert file'}, status=500)


class TargetConversionsView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        supported_conversions = SupportedConversion.get_available_conversions_for_all_sources()
        return JsonResponse({'supported_conversions': supported_conversions})


class IndexView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request, "documents/index.html")

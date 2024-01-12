from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from backend.models import DocumentConversion, SupportedConversion
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pdb


@csrf_exempt
def upload_and_create_document(request):
    original_file = request.FILES.get("original_file", None)
    
    if not original_file:
        return JsonResponse({"error": "original_file is required"})

    converted_mimetype = request.POST.get("converted_mimetype", None)
    if not converted_mimetype:
        return JsonResponse({"error": "converted_mimetype is required"})

    document_conversion = DocumentConversion.objects.create(
        original_file=original_file,
        original_filename=original_file.name,
        original_mimetype=original_file.content_type,
        original_size=original_file.size,
        converted_mimetype=converted_mimetype,
        status="processing",
    )

    document_conversion.conversion()
    converted_file = document_conversion.converted_file

    if converted_file:
        response = FileResponse(open(converted_file.path, 'rb'))
        response['Content-Type'] = document_conversion.converted_mimetype
        response['Content-Disposition'] = f'attachment; filename="{document_conversion.converted_filename}"'
        return response
    else:
        return JsonResponse({'error': 'unable to convert file'})


def download_document(request, document_conversion_id):
    document_conversion = get_object_or_404(
        DocumentConversion, id=document_conversion_id
    )
    document = document_conversion.original_file

    with open(document.path, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/force-download")
        response["Content-Disposition"] = 'attachment; filename="{}"'.format(
            document.name
        )
        return response


def target_conversions(request):
    original_mimetype = request.GET.get("original_mimetype")

    if original_mimetype:
        supported_mimetypes = SupportedConversion.get_available_conversions_for_source(
            original_mimetype
        )
        return JsonResponse({"supported_mimetypes": list(supported_mimetypes)})
    else:
        return JsonResponse({"error": "Missing required parameter: original_mimetype"})


def index(request):
    return render(request, "documents/index.html")

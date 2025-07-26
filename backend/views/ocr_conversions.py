from django.http import JsonResponse
from rest_framework.views import APIView
from backend.models.file_conversion import SupportedConversion


class OCRSupportedConversionsView(APIView):
    """
    API view to get OCR-enabled supported conversions.
    Provides dynamic output format options based on uploaded file type.
    """

    def get(self, request):
        """
        Get all OCR-enabled supported conversions or filter by source mimetype.
        
        Query parameters:
        - source_mimetype: Filter conversions by source MIME type
        """
        try:
            source_mimetype = request.GET.get('source_mimetype')
            
            # Get OCR-enabled conversions
            ocr_conversions = SupportedConversion.objects.filter(
                available=True,
                ocr_enabled=True
            )
            
            # Filter by source mimetype if provided
            if source_mimetype:
                ocr_conversions = ocr_conversions.filter(
                    original_mimetype=source_mimetype
                )
            
            # Group conversions by source mimetype
            conversions_data = {}
            
            for conversion in ocr_conversions:
                source_type = conversion.original_mimetype
                
                if source_type not in conversions_data:
                    conversions_data[source_type] = {
                        'source_mimetype': source_type,
                        'source_extension': conversion.original_extension,
                        'target_formats': []
                    }
                
                conversions_data[source_type]['target_formats'].append({
                    'mimetype': conversion.target_mimetype,
                    'extension': conversion.target_extension,
                    'label': self._get_format_label(conversion.target_mimetype, conversion.target_extension)
                })
            
            # Convert to list and sort
            result = list(conversions_data.values())
            
            # Sort target formats by label for better UX
            for conversion_group in result:
                conversion_group['target_formats'].sort(key=lambda x: x['label'])
            
            return JsonResponse({
                'supported_conversions': result,
                'total_source_types': len(result)
            }, status=200)
            
        except Exception as e:
            return JsonResponse({
                'error': f'Failed to fetch OCR supported conversions: {str(e)}'
            }, status=500)

    def _get_format_label(self, mimetype, extension):
        """
        Generate a user-friendly label for the format.
        
        Args:
            mimetype: The MIME type
            extension: The file extension
            
        Returns:
            str: User-friendly label
        """
        format_labels = {
            'text/plain': 'Text',
            'application/pdf': 'PDF',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'Word',
            'application/msword': 'Word 97-2003',
            'text/csv': 'CSV',
            'text/html': 'HTML',
            'text/xml': 'XML',
            'application/xml': 'XML',
            'text/markdown': 'Markdown',
            'text/rtf': 'Rich Text',
            'application/rtf': 'Rich Text'
        }
        
        if mimetype in format_labels:
            return f"{format_labels[mimetype]} (.{extension})"
        
        # Fallback to extension-based label
        return f"{extension.upper()} (.{extension})"


class OCRTargetFormatsView(APIView):
    """
    API view to get available target formats for a specific source mimetype.
    """

    def get(self, request, source_mimetype):
        """
        Get target formats for a specific source mimetype.
        
        Args:
            source_mimetype: The source MIME type to get targets for
        """
        try:
            # Get OCR-enabled conversions for the source mimetype
            target_conversions = SupportedConversion.objects.filter(
                original_mimetype=source_mimetype,
                available=True,
                ocr_enabled=True
            )
            
            if not target_conversions.exists():
                return JsonResponse({
                    'error': f'No OCR conversions available for {source_mimetype}'
                }, status=404)
            
            # Build target formats list
            target_formats = []
            
            for conversion in target_conversions:
                target_formats.append({
                    'mimetype': conversion.target_mimetype,
                    'extension': conversion.target_extension,
                    'label': self._get_format_label(conversion.target_mimetype, conversion.target_extension)
                })
            
            # Sort by label for better UX
            target_formats.sort(key=lambda x: x['label'])
            
            return JsonResponse({
                'source_mimetype': source_mimetype,
                'target_formats': target_formats,
                'total_formats': len(target_formats)
            }, status=200)
            
        except Exception as e:
            return JsonResponse({
                'error': f'Failed to fetch target formats: {str(e)}'
            }, status=500)

    def _get_format_label(self, mimetype, extension):
        """
        Generate a user-friendly label for the format.
        Same as OCRSupportedConversionsView._get_format_label
        """
        format_labels = {
            'text/plain': 'Text',
            'application/pdf': 'PDF',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'Word',
            'application/msword': 'Word 97-2003',
            'text/csv': 'CSV',
            'text/html': 'HTML',
            'text/xml': 'XML',
            'application/xml': 'XML',
            'text/markdown': 'Markdown',
            'text/rtf': 'Rich Text',
            'application/rtf': 'Rich Text'
        }
        
        if mimetype in format_labels:
            return f"{format_labels[mimetype]} (.{extension})"
        
        return f"{extension.upper()} (.{extension})"
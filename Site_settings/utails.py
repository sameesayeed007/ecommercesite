from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.template.loader import render_to_string

from xhtml2pdf import pisa

def render_to_pdf(template_path, report , company):
    template = get_template(template_path)
    html = render_to_string(template_path, {'report': report ,'company':company })
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None




def render_to_pdf_product(template_path, report ):
    template = get_template(template_path)
    html = render_to_string(template_path, {'report': report})
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



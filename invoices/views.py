from django.shortcuts import render, get_object_or_404, redirect
from .models import Invoice, Item
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import io
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Invoice



def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'invoices/invoice_list.html', {'invoices': invoices})

def create_invoice(request):
    if request.method == 'POST':
        invoice = Invoice.objects.create(
            invoice_number=request.POST['invoice_number'],
            date=request.POST['date'],
            company_name=request.POST['company_name'],
            company_address=request.POST['company_address'],
            client_name=request.POST['client_name'],
            client_address=request.POST['client_address'],
            tax_rate=request.POST.get('tax_rate', 0.10)
        )
        return redirect('add_items', invoice_id=invoice.id)
    return render(request, 'invoices/create_invoice.html')

def add_items(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if request.method == 'POST':
        Item.objects.create(
            invoice=invoice,
            description=request.POST['description'],
            quantity=int(request.POST['quantity']),
            price=float(request.POST['price'])
        )
        return redirect('add_items', invoice_id=invoice.id)  # Allow adding more items
    return render(request, 'invoices/add_items.html', {'invoice': invoice})

def generate_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Similar PDF generation as before, adapted for Django
    story.append(Paragraph("Invoice", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Invoice Number: {invoice.invoice_number}", styles['Normal']))
    story.append(Paragraph(f"Date: {invoice.date}", styles['Normal']))
    story.append(Spacer(1, 12))

    company_info = f"<b>From:</b><br/>{invoice.company_name}<br/>{invoice.company_address}"
    client_info = f"<b>To:</b><br/>{invoice.client_name}<br/>{invoice.client_address}"
    story.append(Paragraph(company_info, styles['Normal']))
    story.append(Paragraph(client_info, styles['Normal']))
    story.append(Spacer(1, 12))

    data = [['Description', 'Quantity', 'Price', 'Total']]
    for item in invoice.items.all():
        total = item.quantity * item.price
        data.append([item.description, str(item.quantity), f"${item.price:.2f}", f"${total:.2f}"])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(table)
    story.append(Spacer(1, 12))

    subtotal = invoice.calculate_subtotal()
    tax = invoice.calculate_tax()
    total = invoice.calculate_total()
    story.append(Paragraph(f"Subtotal: ${subtotal:.2f}", styles['Normal']))
    story.append(Paragraph(f"Tax ({invoice.tax_rate*100}%): ${tax:.2f}", styles['Normal']))
    story.append(Paragraph(f"<b>Total: ${total:.2f}</b>", styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
    return response


@csrf_exempt
def delete_invoice(request, invoice_id):
    if request.method == 'POST':
        try:
            invoice = Invoice.objects.get(id=invoice_id)
            invoice.delete()
            return JsonResponse({'success': True})
        except Invoice.DoesNotExist:
            return JsonResponse({'error': 'Invoice not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

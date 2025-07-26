from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import HSN, Item

def add_hsn(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        gst_percentage = request.POST.get('gst_percentage')
        product_names = request.POST.get('product_names')
        HSN.objects.create(code=code, gst_percentage=gst_percentage, product_names=product_names)
        return redirect('add_hsn')
    return render(request, 'inventory/add_hsn.html')

def add_item(request):
    hsn_codes = HSN.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        quantity = int(request.POST.get('quantity'))
        closing_quantity = int(request.POST.get('closing_quantity') or 0)
        net_rate = float(request.POST.get('net_rate'))
        bill_rate = float(request.POST.get('bill_rate'))
        purchase_rate = float(request.POST.get('purchase_rate'))
        hsn_code_id = request.POST.get('hsn_code')
        hsn_code = HSN.objects.get(id=hsn_code_id) if hsn_code_id else None
        Item.objects.create(
            name=name,
            category=category,
            quantity=quantity,
            closing_quantity=closing_quantity or 0,
            net_rate=net_rate,
            bill_rate=bill_rate,
            purchase_rate=purchase_rate,
            hsn_code=hsn_code
        )
        return redirect('add_item')
    return render(request, 'inventory/add_item.html', {'hsn_codes': hsn_codes})

def current_stock(request):
    items = Item.objects.select_related('hsn_code').all().order_by('name')
    total_value = sum(item.stock_value for item in items)
    low_stock_count = sum(1 for item in items if item.current_quantity <= 5)
    return render(request, 'inventory/current_stock.html', {
        'items': items,
        'total_value': total_value,
        'low_stock_count': low_stock_count
    })

# Create your views here.

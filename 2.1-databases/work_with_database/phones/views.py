from django.shortcuts import render, get_object_or_404
from .models import Phone


def catalog(request):
    sort = request.GET.get('sort', '')

    if sort == 'name':
        phones = Phone.objects.all().order_by('name')
    elif sort == 'min_price':
        phones = Phone.objects.all().order_by('price')
    elif sort == 'max_price':
        phones = Phone.objects.all().order_by('-price')
    else:
        phones = Phone.objects.all()

    return render(request, 'catalog.html', {'phones': phones})


def phone_detail(request, slug):
    phone = get_object_or_404(Phone, slug=slug)
    return render(request, 'product.html', {'phone': phone})
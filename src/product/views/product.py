from django.views import generic
from django.db.models import Q
from django.db.models import Max
from datetime import date

from product.models import Variant, Product,ProductImage, ProductVariant

from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

    def post(self,request, **kwargs):
        print('hello')
        print(request.POST)


# product list logic 
class ListProductView(generic.ListView):
    model = Product
    template_name = ''
    context_object_name = 'product_list'
    ordering = ['id']
    paginate_by = 3
    paginate_orphans = 1

    def get_queryset(self):
        query = self.request.GET.get('title')
        price_form = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        date_qs = self.request.GET.get('date')

        products = Product.objects.all()

        # filter if query params title 
        if query == None:
            query = ''
        if query:
            products = Product.objects.filter(title__icontains=query)
            return products

        # filter by date 
        if date_qs == None:
            date_qs = ''
        if date_qs:
            products = Product.objects.filter(created_at__contains=date_qs)
            return products

        # filter by price range 
        if price_form == '':
            price_form =0
        if price_to == '':
            obj = Product.objects.aggregate(Max('product_variant_price__price'))
            price_to =(obj['product_variant_price__price__max'])
        if price_to:
            products = Product.objects.filter(product_variant_price__price__range=(price_form,price_to))
            return products 
        
        return products

    def get_context_data(self, **kwargs):
        context = super(ListProductView,self).get_context_data(**kwargs)
        context['total_product'] = Product.objects.all().count()
        print('count_pro:',Product.objects.all().count())

        variants = Variant.objects.all().distinct()
        print("all variants:",variants)
        return context
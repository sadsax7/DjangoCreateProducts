from django.shortcuts import render, redirect
from django import forms
from django.views.generic import TemplateView

from django.views import View

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutPageView(TemplateView): 
    template_name = 'pages/about.html' 
     
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "title": "About us - Online Store", 
            "subtitle": "About us", 
            "description": "This is an about page ...", 
            "author": "Developed by: Your Name", 
        }) 
 
        return context 
    

class Product: 
    products = [ 
        {"id":"1", "name":"TV", "description":"Best TV", "price": 1111}, 
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 992}, 
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 1543}, 
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 654} 
    ] 
 
class ProductIndexView(View): 
    template_name = 'products/index.html' 
 
    def get(self, request): 
        viewData = {} 
        viewData["title"] = "Products - Online Store" 
        viewData["subtitle"] =  "List of products" 
        viewData["products"] = Product.products 
 
        return render(request, self.template_name, viewData) 


class ProductShowView(View): 
    template_name = 'products/show.html' 
 
 
    def get(self, request, id): 
        viewData = {} 
        product = Product.products[int(id)-1] 
        viewData["title"] = product["name"] + " - Online Store" 
        viewData["subtitle"] =  product["name"] + " - Product information" 
        viewData["product"] = product 
 
        return render(request, self.template_name, viewData)
    

class ProductForm(forms.Form): 
    name = forms.CharField(required=True) 
    price = forms.FloatField(required=True) 
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("El precio debe ser mayor que cero")
        return price
 
 
class ProductCreateView(View): 
    template_name = 'products/create.html'
    success_template = 'products/success.html'

    def get(self, request): 
        form = ProductForm() 
        viewData = {} 
        viewData["title"] = "Create product" 
        viewData["form"] = form 
        return render(request, self.template_name, viewData) 

    def post(self, request): 
        form = ProductForm(request.POST) 
        if form.is_valid(): 
            # Obtener datos del formulario
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            
            # Generar un nuevo ID (el siguiente número en la secuencia)
            next_id = str(len(Product.products) + 1)
            
            # Crear un nuevo diccionario de producto
            new_product = {
                "id": next_id,
                "name": name,
                "description": "Producto nuevo",  # Descripción predeterminada
                "price": price
            }
            
            # Añadir el nuevo producto a la lista de productos
            Product.products.append(new_product)
            
            # Renderizar la plantilla de éxito con los datos del producto
            success_data = {
                "product_name": name,
                "product_price": price
            }
            
            return render(request, self.success_template, success_data)
        else: 
            viewData = {} 
            viewData["title"] = "Create product" 
            viewData["form"] = form 
            return render(request, self.template_name, viewData)
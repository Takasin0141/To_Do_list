from django.shortcuts import render

def helloworldfunction(request):
    return render(request, 'index.html')
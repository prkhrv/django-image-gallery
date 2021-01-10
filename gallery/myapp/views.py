from django.shortcuts import render,redirect
from .forms import ImageForm
from .models import Gallery,Tag
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.core.files.base import ContentFile
# from io import BytesIO
# from PIL import Image
from PIL import Image as PilImage
from django.views.decorators.cache import never_cache

# Create your views here.

@never_cache
def view(request,pk):
    imagePk = Gallery.objects.get(pk=pk)

    if request.method == "POST":
        my_image = Gallery.objects.get(pk=pk)

        rotate = request.POST.get('rotate')
        if rotate == 'Rotate Right':
            im = PilImage.open(my_image.image)
            rotated_image = im.rotate(-90,resample= PilImage.BICUBIC,expand=True)
            rotated_image.save(my_image.image.file.name, overwrite=True)
        elif rotate == 'Rotate Left':
            im = PilImage.open(my_image.image)
            rotated_image = im.rotate(90,resample=PilImage.BICUBIC,expand=True)
            rotated_image.save(my_image.image.file.name, overwrite=True)
        return redirect(f'/view/{pk}')

    return render(request,'view.html',{'img': imagePk})


def addImage(request):
    tags = Tag.objects.all()

    if request.method == "POST":

        tags = request.POST.getlist('tags')
        images = request.FILES.getlist('images')

        
        for img in images:
            gallery_item = Gallery.objects.create(image = img)
            for tag in tags:
                gallery_item.tags.add(tag)
            gallery_item.save()
        
        return HttpResponse("added successfully")
    return render(request, 'add.html',{'tags':tags})


def index(request):
    images = Gallery.objects.all()
    tags = Tag.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page', 1)
    
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)

    if request.method == "POST":
        filter_tags = request.POST.getlist('tags')
        filtered_images = Gallery.objects.filter(tags__name__in=filter_tags).distinct()
        paginator = Paginator(filtered_images, 8)
        page = request.GET.get('page', 1)
        
        try:
            filtered_images = paginator.page(page)
        except PageNotAnInteger:
            filtered_images = paginator.page(1)
        except EmptyPage:
            filtered_images = paginator.page(paginator.num_pages)

        return render(request, 'index.html',{'gallery_images':filtered_images,'tags':tags,'selected_tags':filter_tags})




    return render(request, 'index.html',{'gallery_images':images,'tags':tags})

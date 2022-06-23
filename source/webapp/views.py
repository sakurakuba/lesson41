from django.shortcuts import render


# Create your views here.
def index_view(request):
    # print(request.GET)
    # print(request.GET.getlist('my_param'))
    # print(request.GET.get('my_param', 10))
    # print(request.GET.get('other_param'))
    # print(request.GET.get('other_param', 10))
    return render(request, "index.html")


def article_create_view(request):
    if request.method == 'GET':
        return render(request, 'article_create.html')
    elif request.method == 'POST':
        context = {
            'title': request.POST.get('title'),
            'content': request.POST.get('content'),
            'author': request.POST.get('author')
        }
        return render(request, 'article_view.html', context)








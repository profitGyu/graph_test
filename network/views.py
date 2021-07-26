from django.core.checks import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def startup_graph(request):
    # login = False
    # try:
    #     token = request.session["accesstoken"]
    #     token = request.COOKIES["isLoginned"]
    #     login = True
    # except:
    #     pass
    # if login == False:
    #         # messages.info(request, '로그인 후 사용해 주세요.')
    #     return HttpResponseRedirect(reverse('pages:login'))
    # else:
    query = {}
    query["keyword"] = request.GET.get('keyword', "")
    query["comname"] = request.GET.get('comname', "")
    query["code"] = request.GET.get('code', "")
    if ''.join(list(query.values())) == "": # 아무런 조건도 없으면 query 를 넘기지 않는다.
        return render(request, 'graphs/graph_startup.html', {"menu":"startup"})
    return render(request, 'graphs/graph_startup.html', {'query':query, "menu":"startup"})

@csrf_exempt
def base_graph(request):

    return render(request, 'network/index.html')

def test(request):

    return render(request, 'network/test.html')
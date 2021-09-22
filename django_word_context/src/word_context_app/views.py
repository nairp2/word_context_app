from django.shortcuts import render
from word_context_app import nlp

# Create your views here.
def home(request):
    return render(request, 'home.html')

#def result(request):
#    query = str(request.GET['query'])
#    json = {'query': query}
#    return render(request, 'result.html', json)

def wordquery(request):
    #if request.method == 'POST':
    #    print(request.POST.dict())
    #    print(request.POST.get('query'))
    query = str(request.POST['query'])

    json = nlp.nlp_query(query)
    #json = {'query': query}
    return render(request, 'home.html', json)

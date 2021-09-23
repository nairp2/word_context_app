from django.shortcuts import render
from django.shortcuts import HttpResponse
from word_context_app import nlp
import json

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

    output = nlp.nlp_query(query)
    output_index = output.to_json(orient="records")
    data = []
    data = json.loads(output_index)
    context = {'d': data}
    #json = {'query': query}
    #return HttpResponse(output)
    return render(request, 'home.html', context)

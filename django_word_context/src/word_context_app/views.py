from django.shortcuts import render
from django.shortcuts import HttpResponse
from word_context_app import nlp
from word_context_app import script1
import json

# Create your views here.
def home(request):
    #paths = script1.script_load_paths()
    #context = {'paths': paths}
    return render(request, 'home.html')

#def path(request):
#    paths = script1.script_paths()
#    context = {'paths': paths}
#    return render(request, 'home.html', context)
#def result(request):
#    query = str(request.GET['query'])
#    json = {'query': query}
#    return render(request, 'result.html', json)

def wordquery(request):
    #if request.method == 'POST':
    #    print(request.POST.dict())
    #    print(request.POST.get('query'))
    query = str(request.POST['query'])

    #for filename, file in request.FILES.items():
    #    name = request.FILES[filename].name
    root = str(request.POST['root'])
    #path = str(request.POST['paths'])
    sim_score = float(request.POST['sim_score'])
    #if sim_score == 1.0:
    #    sim_score = 1.0
    #else:
    #    sim_score = 0.6

    print(query)
    print(root)
    #print(name)
    #print(path)
    print(sim_score)

    query_UI = "Query:  "
    root_UI = "Root directory:  "
    sim_UI = "Similarity Score Threshold: "
    #paths = script1.script_load_paths()

    output1, word_not_found = script1.script_select_paths(query, root, sim_score)

    output1_index = output1.to_json(orient="records")
    data1 = []
    data1 = json.loads(output1_index)

    #output = nlp.nlp_query(query)
    #output_index = output.to_json(orient="records")
    #data = []
    #data = json.loads(output_index)
    context = {'d': data1, 'word_not_found': word_not_found, 'query_UI': query_UI, 'root_UI': root_UI, 'sim_UI': sim_UI, 'query': query, 'root': root, 'sim_score': sim_score}
    #context = {'d': data, 'paths': data1}
    #json = {'query': query}
    #return HttpResponse(output)
    return render(request, 'home.html', context)

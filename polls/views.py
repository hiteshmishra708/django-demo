from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
import xml.etree.ElementTree as ET

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save('polls/static/polls/documents/' + myfile.name, myfile)
        
        extension = myfile.name[myfile.name.rfind('.') + 1:]
        print(extension)

        if isValidExtension(extension):
            tree = ET.parse(filename)
            root = tree.getroot()
            print('Expertise Data:')

            list = []
            for elem in root:
                for subelem in elem:
                    list.append(int(subelem.text))
            result = 0
            for i in list:
                result += i
            print(result)
            meanValue = result/len(list)
            print(meanValue)
            uploaded_file_url = fs.url(filename)
            return render(request, 'polls/simple_upload.html', {
                'uploaded_file_url': uploaded_file_url
            })
    return render(request, 'polls/simple_upload.html')

def isValidExtension(file):
    return True
from django.http import JsonResponse, HttpResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from projects.ai_util import *


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getRoutes(request):
    routes = ["hello", "deepak"]
    return Response(routes)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_answer(request):
    sample_sentence = request.POST["sentence"]
    #sample_sentence = " Person 1: Are there theatres in town? Person 2: There are 4 theatres in the center of town. Do you have a preference? Person 1: No, I don't have a preference. Which one do you recommend? Person 2: "
    s = generate_dialogue(ReformerLM=model, model_state=STARTING_STATE, start_sentence=sample_sentence, vocab_file=VOCAB_FILE, vocab_dir=VOCAB_DIR, max_len=120, temperature=0.2)
    return Response(s)
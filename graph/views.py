from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from graph.serializer import Match_query, CategoryQuerySerializer
from django.views.decorators.csrf import csrf_exempt
import requests, json


class GraphAPI(APIView):

    permission_classes = [AllowAny]
    serializer_class = Match_query

    @csrf_exempt
    def post(self, request):

        req = request.POST

        serializer = Match_query(req)
        data = serializer.get_value(req)
        if data:
            return Response(data, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def get(self, request):
        # https://neo4j.com/docs/http-api/current/actions/return-results-in-graph-format/

        URL = 'http://neo4j:8525@localhost:7474/db/neo4j/tx/commit'
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            'Access-Control-Allow-Origin': '*',
        }
  
        query = 'MATCH p=(a:Startup)-[:LINKED]-(b:Startup) return p'
        data = {
            "statements": [{
                "statement": query,
                "resultDataContents": ["graph"]
            }]
        }
        res = requests.post(URL, headers=headers, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
        data = res.json()

        am_data = self.convert_first(data)

        return Response(am_data)

    # def startup_query(self, query, params, other=False):


class GetCategoryInfo(APIView):

    permission_classes = [AllowAny]
    serializer_class = CategoryQuerySerializer

    @csrf_exempt
    def post(self, request):
        req = request.POST

        serializer = CategoryQuerySerializer(req)
        data = serializer.get_value(req)
        if data:
            return Response(data, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from graph.serializer import Match_query
from django.views.decorators.csrf import csrf_exempt
import requests, json

COLOR_CATEGORY = {'#b5e1a2': 'AI', '#3b7cb7': '빅데이터', '#f8864f': '인공지능', '#f46d43': '블록체인', '#f0f9a7': 'NTF',
                  '#3b92b9': '컨설팅', '#da464d': '클라우드', '#feec9f': '마켓팅', '#e6f598': '할리우드',
                  '#fdb768': '반도체', '#fff8b4': '친환경', '#fecc7b': '소셜네트워크', '#fee08b': '디자인', '#c9314c': '물리학',
                  '#9cd7a4': '건축학', '#e75948': '생체공학', '#50a9af': '철학', '#fafdb7': '화학',
                  '#fba05b': '조선업', '#81cda5': '신생에너지', '#cfec9d': '컨슈머'}


class GraphAPI(APIView):

    permission_classes = [AllowAny]
    serializer_class = Match_query

    @csrf_exempt
    def post(self, request):

        req = request.data
        print(req)
        serializer = Match_query(req)
        data = serializer.get_value(req)
        # print(data)

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


    def convert_first(self, data):

        color_category = COLOR_CATEGORY

        chart_data = []
        nodenum = []
        data = data["results"][0]["data"]

        for key in color_category:
            chart_data.append({"name": color_category[key], "color": key, "children": []})

        for row in data:
            node = row["graph"]
            for n in node["nodes"]:
                if n["id"] in nodenum:
                    continue
                else:
                    nodenum.append(n["id"])
                    capital = n["properties"]["capital"]
                    code = n["properties"]["code"]
                    size = n["properties"]["size"]
                    name = n["properties"]["name"]
                    color = n["properties"]["color"]
                    if color in color_category.keys():
                        category = color_category[color]
                        for data in chart_data:
                            if category == data["name"]:
                                data["children"].append({"name": name, "value": size, "color":color, "code":code, "capital":capital,})

        result_data = []
        for data in chart_data:
            if data["children"] != []:
                result_data.append(data)

        return result_data

    # def startup_query(self, query, params, other=False):



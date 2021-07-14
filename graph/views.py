from django.shortcuts import render

# Create your views here.
import os


from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from django.views.decorators.csrf import csrf_exempt
import requests
import json

class GraphAPI(APIView):

    def post(self, request):



        req = requests.data
        URL = 'http://neo4j:8525@localhost:7474/db/neo4j/tx/commit'
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            'Access-Control-Allow-Origin': '*',
        }
        data = {
            "statements": [{
                "statement": "MATCH p=(a:Startup)-[:LINKED]-(b:Startup) RETURN p",
                "resultDataContents": ["graph", "row"]
            }]
        }
        res = requests.post(URL, headers=headers, data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
        print(res.status_code)
        # # vis.js 데이터 형식으로 변환한다.
        # vis = self.convert(res.json())
        return Response(res)

    @csrf_exempt
    def get(self, request):
        # https://neo4j.com/docs/http-api/current/actions/return-results-in-graph-format/

        URL = 'http://neo4j:8525@localhost:7474/db/neo4j/tx/commit'
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            'Access-Control-Allow-Origin': '*',
        }
        query = "MATCH p=(a:Startup)-[:LINKED]-(b:Startup) RETURN p limit 100"
        query = "MATCH p=(a:Startup)-[:LINKED]-(b:Startup) where a.name='소셜빈' RETURN p"

        data = {
            "statements": [{
                "statement": query,
                "resultDataContents": ["graph"]
            }]
        }
        res = requests.post(URL, headers=headers, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
        data = res.json()
        print(data)
        am_data = self.convert(data)

        return Response(am_data)


    def convert(self, data):

        color_category = {'#b5e1a2': 'AI', '#3b7cb7': '빅데이터', '#f8864f': '인공지능', '#f46d43': '블록체인', '#f0f9a7': 'NTF',
                          '#3b92b9': '컨설팅', '#da464d': '클라우드', '#feec9f': '마켓팅', '#e6f598': '할리우드',
                          '#fdb768': '반도체', '#fff8b4': '친환경', '#fecc7b': '소셜네트워크', '#fee08b': '디자인', '#c9314c': '물리학',
                          '#9cd7a4': '건축학', '#e75948': '생체공학', '#50a9af': '철학', '#fafdb7': '화학',
                          '#fba05b': '조선업', '#81cda5': '신생에너지', '#cfec9d': '컨슈머'}

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
                                data["children"].append({"name": name, "value": size})

        result_data = []
        for data in chart_data:
            if data["children"] != []:
                result_data.append(data)

        return result_data




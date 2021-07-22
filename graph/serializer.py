import requests, json
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

COLOR_CATEGORY = {'#b5e1a2': 'AI', '#3b7cb7': '빅데이터', '#f8864f': '인공지능', '#f46d43': '블록체인', '#f0f9a7': 'NTF',
                  '#3b92b9': '컨설팅', '#da464d': '클라우드', '#feec9f': '마켓팅', '#e6f598': '할리우드',
                  '#fdb768': '반도체', '#fff8b4': '친환경', '#fecc7b': '소셜네트워크', '#fee08b': '디자인', '#c9314c': '물리학',
                  '#9cd7a4': '건축학', '#e75948': '생체공학', '#50a9af': '철학', '#fafdb7': '화학',
                  '#fba05b': '조선업', '#81cda5': '신생에너지', '#cfec9d': '컨슈머'}


class Match_query(serializers.Serializer):

    company = serializers.CharField(max_length=10, allow_blank=True, allow_null=True)
    industrial = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    phase = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    capital = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)

    def get_value(self, data):

        company = data["company"]
        industrial = data["industrial"]
        phase = data["phase"]
        capital = data["phase"]

        basic_query = "MATCH p=(a:Startup)-[:LINKED*0..1]-(b:Startup) "
        return_query = " return p"

        if company:
            basic_query = "MATCH p=(a:Startup)-[:LINKED*0..2]-(b:Startup) "
            #  실 데이터 들어오는 거 보고 기업정보 비교하는 코드 작성
            # where_query = "WHERE '{}' in a.keywords".format(company)
            if industrial:
                where_query ="WHERE a.name='{}' and b.color='{}'".format(company, industrial)
                query = basic_query + where_query + return_query
                data = self.get_neo4j(query)
                data = self.convert_one_category(data)
                return data
            elif phase:
                where_query = "WHERE a.name='{}' and b.phase='{}'".format(company, phase)
                query = basic_query + where_query + return_query
                data = self.get_neo4j(query)
                data = self.convert_one_category(data)
                return data
            elif capital:
                where_query = "WHERE a.name='{}'and a.capital <={}".format(company, capital)
            else:
                where_query = "WHERE a.name='{}'".format(company)
                query = basic_query + where_query + return_query
                data = self.get_neo4j(query)
                data = self.convert_one_category(data)
                return data
        elif industrial:
            where_query = "WHERE a.color='{}'".format(industrial)
        elif phase:
            where_query = "WHERE a.phase='{}'".format(phase)
        elif capital:
            where_query = "WHERE a.capital <='{}'".format(capital)

        query = basic_query+where_query+return_query

        data = self.get_neo4j(query)
        data = self.convert_one_category(data)

        return data

    def get_neo4j(self, query):
        '''neo4j 에서 데이터 값 가져오는 함수'''

        URL = 'http://neo4j:8525@localhost:7474/db/neo4j/tx/commit'
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            'Access-Control-Allow-Origin': '*',
        }

        data = {
            "statements": [{
                "statement": query,
                "resultDataContents": ["graph"]
            }]
        }
        res = requests.post(URL, headers=headers, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
        data = res.json()
        if data['results'][0]['data'] == []:
            raise ValidationError({"error": "검색 하신 결과가 없습니다."})
        return data

    def convert_one_category(self, data):

        color_category = COLOR_CATEGORY

        nodes = []
        edges = []
        nodenum = []

        data = data['results'][0]['data']

        for row in data:
            node = row["graph"]
            for n in node["nodes"]:
                if n["id"] in nodenum:
                    continue
                else:
                    id = n["id"]
                    nodenum.append(id)
                    capital = n["properties"]["capital"]
                    code = n["properties"]["code"]
                    size = n["properties"]["size"]
                    name = n["properties"]["name"]
                    color = n["properties"]["color"]
                    nodes.append(
                        {'id': id, "code": code, "value": size, "name": name, "color": color, "capital": capital})

                for r in node["relationships"]:
                    start_node = r["startNode"]
                    end_node = r["endNode"]
                    edges.append({"from":start_node, "to":end_node})
        for node in nodes:
            link_list = []

            for edge in edges:
                if node["id"] == edge["from"]:
                    link_list.append(edge["to"])
                elif node["id"] == edge["to"]:
                    link_list.append(edge["from"])
            node.update({"link":link_list})

        return nodes


    def convert_multy_data(self, data):

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




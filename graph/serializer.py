import requests, json
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import pprint

COLOR_CATEGORY = {'#b5e1a2': 'AI', '#3b7cb7': '빅데이터', '#f8864f': '인공지능', '#f46d43': '블록체인', '#f0f9a7': 'NTF',
                  '#3b92b9': '컨설팅', '#da464d': '클라우드', '#feec9f': '마켓팅', '#e6f598': '할리우드',
                  '#fdb768': '반도체', '#fff8b4': '친환경', '#fecc7b': '소셜네트워크', '#fee08b': '디자인', '#c9314c': '물리학',
                  '#9cd7a4': '건축학', '#e75948': '생체공학', '#50a9af': '철학', '#fafdb7': '화학',
                  '#fba05b': '조선업', '#81cda5': '신생에너지', '#cfec9d': '컨슈머'}

INDUSTRIAL_DICT = {'#771DAE': '0', '#67DC75': '1', '#2A1DBD': '2', '#F83F97': '3', '#F1B200': '4','#F30259': '5', '#009E4F': '6', '#0058FF': '7',
              '#FD7D20': '8', '#FF3100': '9', '#7151A5': '10', '#036174': '11', '#303173': '12','#ECA406': '13', '#5C33F6': '14',
              '#B8307C': '15', '#0C5C22': '16', '#0085FF': '17', '#FD7159': '18', '#6A75B3': '19','#A367DC': '20'}

PHASE_DICT = {'0': '전체선택', '1': '선택안함', '2': '투자 단계 비공개','3': '미입력','4': 'Series A','5': 'Series B','6': 'Series C',
              '7': 'Series D','8': 'Seed','9': 'Angel','10': 'Pre-IPO', '11': 'Pre-A'}


def get_neo4j(query):
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

    result = data['results'][0]['data']

    if result == []:
        raise ValidationError({"error": "검색 하신 결과가 없습니다."})
    return result





# 그래프 정보 가져오는 serializers
class Match_query(serializers.Serializer):

    company = serializers.CharField(max_length=10, allow_blank=True, allow_null=True)
    industrial = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    phase = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    capital = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    age = serializers.CharField(max_length=50, allow_null=True, allow_blank=True)

    def total_guery(self, match, where, return_query):
        result = match + where + return_query
        return result


    def make_multy_where(self,val_list):

        where_query = ""
        for index, val in enumerate(val_list):
            print(val)
            if index == (len(val_list) - 1):
                where_query += "(a.color='{}' and b.color='{}')".format(val, val)
            else:
                where_query += "(a.color='{}' and b.color='{}') or ".format(val, val)

        return where_query


    def make_limit_union_multy_query(self, val_list, category):
        """ union을 사용하여 여러 쿼리는 검색 하게 함"""
        query = ""
        for index, val in enumerate(val_list):
            if index == (len(val_list)-1):
                query += "match p=(a:Startup)-[:LINKED]-(b:Startup) where (a.{0}='{1}' and b.{0}='{1}') return p limit 30".format(category, val)
            else:
                query += "match p=(a:Startup)-[:LINKED]-(b:Startup) where (a.{0}='{1}' and b.{0}='{1}') return p limit 30 union ".format(category, val)

        return query


    def get_value(self, data):

        company = data["company"]
        industrial = data.getlist("industrial[]")
        phase = data.getlist("phase[]")
        match = "MATCH p=(a:Startup)-[:LINKED]-(b:Startup) "
        return_query = " return p"
        print(industrial, phase, company)
        print(len(industrial))
        # 회사나 키워드 값 선택시
        if company:
            if industrial != ['']:
                print("기업,키워드 와 산업분류")
                print("industrial:",industrial)
                color_list = []
                for i in industrial:
                    color_list.append([color for color, index in INDUSTRIAL_DICT.items() if index == i][0])
                where_query = "where ( a.name='{}' or '{}' in a.keywords) and ".format(company, company)
                color_where=self.make_multy_where(color_list)
                where_query = where_query+"("+color_where+")"
                return_query = ' return p'
                query = self.total_guery(match, where_query, return_query)
                noe4j_data = self.get_neo4j(query)
                result = self.convert_multy_query_company(noe4j_data, company)

                return result

            elif phase !=['1']:
                print("기업 + 투자단게")
                phase_list = []
                for i in phase:
                    phase_list.append(PHASE_DICT[i])
                with_query = "with {} as phases ".format(phase_list)
                match = "match p = (a:Startup)-[:LINKED]-(b:Startup) "
                where_query = "where ( a.name='{}' or '{}' in a.keywords) and (b.phase in phases) return b".format(company, company)
                query = with_query + match + where_query
                print(query)
                noe4j_data = get_neo4j(query)
                result = self.convert_multy_query_company(noe4j_data, company, "phase")

                return result
            else:
                print("기업 혹은 키워드만")
                # 키워드나, 회사만 검색하는 경우
                where_query = "where a.name='{}' or '{}' in a.keywords".format(company, company)
                query = self.total_guery(match, where_query, return_query)
                noe4j_data = self.get_neo4j(query)
                result = self.convert_one_category(noe4j_data)
                return result
            
        #  산업분류 선택시
        if industrial != ['']:
            if len(industrial) == 1:
                print("산업분류 하나일 경우")
                industrial = industrial[0]
                color = [color for color, index in INDUSTRIAL_DICT.items() if index == industrial]
                where_query = "where a.color='{}' and b.color='{}'".format(color[0], color[0])
                return_query = " return p"
                query = self.total_guery(match, where_query, return_query)
                noe4j_data = self.get_neo4j(query)
                result = self.convert_one_category(noe4j_data)
            else:
                print("산업분류 여러개일 경우")
                color_list =[]
                for i in industrial:
                    color_list.append([color for color, index in INDUSTRIAL_DICT.items() if index == i][0])

                query = self.make_limit_union_multy_query(color_list, "color")
                noe4j_data = self.get_neo4j(query)
                result = self.convert_multy_data(noe4j_data)

            return result

        if phase != ['1']:
            print("투자 단계")
            if len(phase) == 1:
                print("투자 단계만 선택시")
                phase = PHASE_DICT[phase[0]]
                return_query = " return p limit 150"
                try:
                    where_query = "where a.phase='{}' and b.phase='{}'".format(phase, phase)
                    query = self.total_guery(match, where_query, return_query)
                    noe4j_data = self.get_neo4j(query)
                except:
                    query = "MATCH p=(a:Startup)-[:LINKED]-(b:Startup) where a.phase='{}' return a limit 50".format(phase)
                    noe4j_data = self.get_neo4j(query)
                finally:
                    result = self.convert_one_category(noe4j_data)
                    return result
            else:
                print("여러 단계")
                phase_list = []
                for i in phase:
                    phase_list.append(PHASE_DICT[i])
                query = self.make_limit_union_multy_query(phase_list, "phase")
                noe4j_data = self.get_neo4j(query)
                result = self.convert_multy_data(noe4j_data, category="phase")
                return result

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
        return data['results'][0]['data']

    def convert_one_category(self, data):

        color_category = COLOR_CATEGORY
        nodes = []
        edges = []
        nodenum = []
        color_list = []


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
                    phase = n["properties"]["phase"]
                    color_list.append(color)
                    category = INDUSTRIAL_DICT[n["properties"]["color"]]
                    nodes.append(
                        {'id': id, "code": code, "value": size, "name": name, "color": color, "capital": capital, "category":category, "phase":phase})

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
        nodes.append({"color_list":list(set(color_list))})
        return nodes

    def convert_multy_query_company(self, data, company_name, category=None):

        chart_data = {"name": company_name, "value":"100", "color": "blue", "children": []}

        if category == "phase":
            data = self.convert_multy_data(data, company_name, category)
        else:
            data = self.convert_multy_data(data, company_name)
        chart_data["children"].extend(data[:len(data)-1])
        result = [chart_data]
        result.append(data[len(data)-1])
        return result

    def convert_multy_data(self, data, company_name=None, category=None):

        color_category = INDUSTRIAL_DICT
        node_category = INDUSTRIAL_DICT
        chart_data = []
        nodenum = []
        color_list = []
        # 검색 카테고리 별로 데이터 변경 형식이 달라짐
        if category == "phase":
            node_category = PHASE_DICT
        # 카테고리에 부모값을 미리 생성
        for key in node_category:
            chart_data.append({"name": node_category[key], "color": key, "children": [], "value": 50})
        for row in data:
            node = row["graph"]
            for n in node["nodes"]:
                if n["id"] in nodenum:
                    continue
                elif n["properties"]["name"] == company_name:
                    continue
                else:
                    nodenum.append(n["id"])
                    capital = n["properties"]["capital"]
                    code = n["properties"]["code"]
                    size = n["properties"]["size"]
                    name = n["properties"]["name"]
                    color = n["properties"]["color"]
                    phase = n["properties"]["phase"]
                    color_list.append(color)
                    if category == "phase":
                        if phase in node_category.values():
                            for data in chart_data:
                                if phase == data["name"]:
                                    data["children"].append(
                                        {"name": name, "value": size, "color": color, "code": code, "capital": capital,
                                         "phase": phase})
                    else:
                        if color in color_category.keys():
                            category = color_category[color]
                            for data in chart_data:
                                if category == data["name"]:
                                    data["children"].append({"name": name, "value": size, "color":color, "code":code, "capital":capital, "phase":phase})

        result_data = []

        for data in chart_data:
            if data["children"] != []:
                result_data.append(data)
        result_data.append({"color_list": list(set(color_list))})
        return result_data



class CategoryQuerySerializer(serializers.Serializer):

    company = serializers.CharField(max_length=10, allow_blank=True, allow_null=True)


    def get_value(self, data):

        company = data["company"]

        query = "match p = (a:Startup)-[:LINKED]-(b:Startup) where a.name='{}' or '{}' in a.keywords return p".format(company, company)
        data = get_neo4j(query)
        result = self.get_category(data)
        return result

    def get_category(self, data):

        nodenum = []
        color_list = []
        phase_list = []
        for row in data:
            node = row["graph"]
            for n in node["nodes"]:
                if n["id"] in nodenum:
                    continue
                else:
                    color = n["properties"]["color"]
                    phase = n["properties"]["phase"]
                    color_list.append(color)
                    phase_list.append(phase)

        color_list = list(set(color_list))
        phase_list = list(set(phase_list))
        result = {"color_list":color_list, "phase_list":phase_list}

        return result

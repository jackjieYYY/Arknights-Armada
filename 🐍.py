print("黄金🐍舰队 v3.5.3")  # 2020.1.20
import mitmproxy.http

from mitmproxy import ctx, http
import copy
import json

# 是否全员获得钢铁侠buff
allMight = True
# 自定义黄金舰队干员
customChar = {
    # "5": "char_2014_nian"
}

Debug = True
Servers = ["ak-gs.hypergryph.com", "gs.arknights.jp", "ak-gs-localhost.hypergryph.com",
           "ak-as-localhost.hypergryph.com"]


class Armada:
    def __init__(self):
        self.chars = json.loads(open('./character_table.json', 'r', encoding='UTF-8').read())
        self.squadFormation = {}
        self.squadFormationID = 0
        self.customChar = customChar

    def http_connect(self, flow: mitmproxy.http.HTTPFlow):
        print(flow.request.host)
        if flow.request.host not in Servers and False is Debug:
            flow.response = http.HTTPResponse.make(404)
        if flow.request.host == "ak-gs-localhost.hypergryph.com":
            flow.request.host = "ak-gs.hypergryph.com"
            flow.request.port = 8443
        elif flow.request.host == "ak-as-localhost.hypergryph.com":
            flow.request.host = "ak-as.hypergryph.com"
            flow.request.port = 9443

    def request(self, flow):
        if flow.request.host in Servers and flow.request.path.startswith("/quest/battleStart"):
            data = flow.request.get_content()
            print('战斗开始 >>>')
            j = json.loads(data)
            for i, d in enumerate(j['squad']['slots']):
                if d is not None:
                    d['skillIndex'] = 0
            flow.request.set_content(json.dumps(j).encode())
        elif flow.request.host in Servers and flow.request.path.startswith("/campaign/battleStart"):
            data = flow.request.get_content()
            print('🐉门战斗开始 >>>')
            j = json.loads(data)
            for i, d in enumerate(j['squad']['slots']):
                if d is not None:
                    d['skillIndex'] = 0
            flow.request.set_content(json.dumps(j).encode())
        elif flow.request.host in Servers and flow.request.path.startswith("/quest/squadFormation"):
            data = flow.request.get_content()
            # self.squadFormation = flow.request.headers['uid']

            j = json.loads(data)
            self.squadFormation = {flow.request.headers['uid']: {'slots': copy.deepcopy(j['slots']),
                                                                 'squadId': copy.deepcopy(j['squadId'])}}
            for i, d in enumerate(j['slots']):
                if j['slots'][i] is not None:
                    j['slots'][i]['skillIndex'] = 0
            flow.request.set_content(json.dumps(j).encode())
        elif flow.request.host not in Servers and Debug is False:
            flow.response = http.HTTPResponse.make(404)

    def response(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.host in Servers and flow.request.path.startswith("/account/syncData"):
            text = flow.response.get_text()
            j = json.loads(text)
            print('黄金舰队 ' + j['user']['status']['nickName'] + '#' + flow.request.headers['uid'] + ' 初始化...')
            j['user']['status']['secretary'] = 'char_103_angel'
            j['user']['status']['secretarySkinId'] = "char_103_angel#2"
            print(len(j['user']['troop']['chars']))

            if allMight:
                for lv in j['user']['troop']['chars']:
                    j['user']['troop']['chars'][lv]['potentialRank'] = 5
                    j['user']['troop']['chars'][lv]['mainSkillLvl'] = 10
                    j['user']['troop']['chars'][lv]['favorPoint'] = 240000
                    charId = j['user']['troop']['chars'][lv]['charId']
                    rarity = self.chars[charId]['rarity']

                    if rarity == 2:
                        j['user']['troop']['chars'][lv]['level'] = 55
                        j['user']['troop']['chars'][lv]['evolvePhase'] = 1
                        j['user']['troop']['chars'][lv]['defaultSkillIndex'] = 0
                    elif rarity == 3:
                        j['user']['troop']['chars'][lv]['level'] = 70
                        j['user']['troop']['chars'][lv]['evolvePhase'] = 2
                        j['user']['troop']['chars'][lv]['defaultSkillIndex'] = 1
                        j['user']['troop']['chars'][lv]['skin'] = j['user']['troop']['chars'][lv]['charId'] + "#2"
                    elif rarity == 4:
                        j['user']['troop']['chars'][lv]['level'] = 80
                        j['user']['troop']['chars'][lv]['evolvePhase'] = 2
                        j['user']['troop']['chars'][lv]['defaultSkillIndex'] = 1
                        j['user']['troop']['chars'][lv]['skin'] = j['user']['troop']['chars'][lv]['charId'] + "#2"
                    elif rarity == 5:
                        j['user']['troop']['chars'][lv]['level'] = 90
                        j['user']['troop']['chars'][lv]['evolvePhase'] = 2
                        j['user']['troop']['chars'][lv]['defaultSkillIndex'] = 2
                        j['user']['troop']['chars'][lv]['skin'] = j['user']['troop']['chars'][lv]['charId'] + "#2"

                    for e, skill in enumerate(j['user']['troop']['chars'][lv]['skills']):
                        j['user']['troop']['chars'][lv]['skills'][e]['unlock'] = 1

                    print('%s 号干员 %s' % (lv, self.chars[j['user']['troop']['chars'][lv]['charId']]['name']))

            print('')
            print('黄金舰队准备出航！')
            print('')
            flow.response.set_text(json.dumps(j))
        elif flow.request.host in Servers and flow.request.path.startswith("/quest/squadFormation"):
            text = flow.response.get_text()
            print('设置编队 >>>')
            j = json.loads(text)
            j['playerDataDelta']['modified']['troop']['squads'][
                self.squadFormation[flow.request.headers['uid']]['squadId']]['slots'] = \
                self.squadFormation[flow.request.headers['uid']]['slots']
            flow.response.set_text(json.dumps(j))
        elif flow.request.host not in Servers and Debug is False:
            flow.response = http.HTTPResponse.make(404)


addons = [
    Armada()
]

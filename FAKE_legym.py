import datetime
import time
import requests
import sys
import random
import json
import os


#注意，本脚本只是乐健fake RUn的最基础实现，仅仅提供一个示例或者思路，免除各位逆向过程，如果想要试用GUI版本，请联系我，GUI和路线干扰，循环上传等功能无开源计划且实现简单
#如果项目对你有帮助，请给我star，谢谢！有问题可以在issue提出，我们会尽力实现！
#我们注意到某🐟和🍑某等平台有人售卖里程，恳请手下留情，本脚本仅用于学习交流，请勿用于商业用途！


#跑步数据体自定义
upload_example={
    "appVersion":"3.10.0",
    "avePace":0,
    "calorie":0,
    "deviceType":"在下方修改机型",
    "effectiveMileage":0,
    "effectivePart":1,
    "endTime":"",
    "gpsMileage":0,
    "keepTime":481,
    "limitationsGoalsSexInfoId":"",
    "paceNumber":0,
    "paceRange":0,
    "routineLine":[],
    "scoringType":1,
    "semesterId":"",
    "signDigital":"",
    "signPoint":[],
    "startTime":"",
    "systemVersion":"14",
    "totalMileage":0,
    "totalPart":0.0,
    "type":"自由跑",
    "uneffectiveReason":""
    }



#导出参数定义
start_times=[]
id=[]
effectiveMileage=[]


#基础参数定义(可修改)
legym_ver="3.10.0"
fake_device="Redmi 22127RK46C" #尊贵的红米K60 Pro 用户您好！
fake_device_id="22127RK46C"
login_headers= {"Authorization": "", 
                     "Organization": "", 
                     "User-Agent": f"Mozilla/5.0 (Linux; Android 14; {fake_device} Build/UKQ1.230901.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/118.0.2.0 Mobile Safari/537.86 uni-app Html5Plus/1.0 (Immersed/34.282713)", 
                     "Content-Type": "application/json", 
                     "Content-Length": "118", 
                     "Host": "cpes.legym.cn", 
                     "Connection": "Keep-Alive", 
                     "Accept-Encoding": "gzip" }




def get_current_sign(rundata):
    respone=requests.post(url="http://116.198.207.78:10001/getsign", json=rundata)
    respone_json=respone.json()
    if respone_json['code']==0:
        return respone_json['sign']
    else:
        print("获取签名失败!")
        print("签名服务器返回：",respone_json['message'])
        return "error"

def upload_fakerun(a,c):
    #计算c的Content-Length
    CL=str(len(json.dumps(c)))
    hearders={
        "authorization": "Bearer "+a,
        "Host": "cpes.legym.cn",
        "charset": "UTF-8",
        "User-Agent": "okhttp/4.8.1",
        "Content-Type": "application/json",
        "Content-Length": CL,
        "Accept-Encoding": "gzip"  
    }
    url="https://cpes.legym.cn/running/app/v2/uploadRunningDetails"
    respone=requests.post(url=url,headers=hearders,data=json.dumps(c))
    respone_json=respone.json()
    if respone_json['code']==0:
        print("上传FAKE数据成功！")
        return "ok"
    else:
        print("上传失败！")
        print("服务器返回：",respone_json['message'])
        return "error"

    
def get_history(semesterId,cookies,accessToken,oi):
    post_json = {
    "page": 1,
    "semesterId": semesterId,
    "size": 100
    }
    his_headers = {
    'Authorization': 'Bearer '+accessToken,
    'Organization': semesterId,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 14; 22127RK46C Build/UKQ1.230804.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/118.0.0.0 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/34.285713)',
    'Content-Type': 'application/json',
    'Host': 'cpes.legym.cn',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Cookie': 'JSESSIONID=4DC9DF6AF3534F2DBAC331768F564B20'
    }

    response = requests.post('https://cpes.legym.cn/running/app/getDetails', cookies=cookies, headers=his_headers, json=post_json)
    data=response.json()
    #print(response.text)

    for item in data['data']['gradeDetails']:
        start_time_timestamp = int(item['startTime'])
        start_time_date = datetime.datetime.fromtimestamp(start_time_timestamp / 1000.0)  # 除以1000将毫秒转换为秒
        formatted_date = start_time_date.strftime('%Y-%m-%d')
        start_times.append(formatted_date)
        id.append(item['id'])
        effectiveMileage.append(item['effectiveMileage'])
    return 

def dump_main(semeid,accessToken,oi,userid):
    cookies = {
    'JSESSIONID': '34937AD34DBBD81E80CB710ACDD',
    }
    headers = {
    'Authorization': 'Bearer '+accessToken,
    'Organization': oi,
    'user-agent': 'Mozilla/5.0 (Linux; Android 14; 22127RK46C Build/UKQ1.230804.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/118.0.0.0 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/34.285713)',
    'Host': 'cpes.legym.cn',
}
    print("·乐健路线dump工具  2024/6/18   ver1.0fix·")
    print("·导出数据请配合定制版乐健赛博跑使用·")
    get_history(semeid,cookies,accessToken,oi)
    print("序号"+"  "+"时间"+"          "+"有效里程"+"\n")
    for i in range(len(id)):
        print(str(i)+"  "+start_times[i]+"    "+str(effectiveMileage[i]))

    targe=input("请输入采集目标序号:")
    json_detail={
        "id":id[int(targe)],
        "type":"3",
        "userId":userid

    }
    clear_screen()
    response2 = requests.post('https://cpes.legym.cn/running/back/getRunningDetailsAppeal', cookies=cookies, headers=headers, json=json_detail)
    original_json=response2.json()
    #$print(original_json.text)
    extracted_data = {
        "totalMileage": original_json["data"].get("totalMileage", None),
        "keepTime": original_json["data"].get("keepTime", None),
        "effectiveMileage": original_json["data"].get("effectiveMileage", None),
        "paceNumber": original_json["data"].get("detailsRoutineVO", {}).get("paceNumber", None),
        "calorie": original_json["data"].get("detailsRoutineVO", {}).get("calorie", None),
        "avePace": original_json["data"].get("detailsRoutineVO", {}).get("avePace", None),
        "gpsMileage": original_json["data"].get("detailsRoutineVO", {}).get("gpsMileage", None),
        "routineLine": original_json["data"].get("detailsRoutineVO", {}).get("routineLine", []),
        "type": original_json["data"].get("detailsRoutineVO", {}).get("type", None)
    }
    print(extracted_data["type"])
    with open('legym_way.txt', 'w',encoding="UTF-8") as file:
        json.dump(extracted_data, file, indent=4) 
    print("导出完成，导出数据位于当前目录下legym_way.txt")
#开始跑步
def legym_getRunningLimit(semesterId):
    limit_headers= login_headers
    limit_headers["Authorization"]="Bearer "+acessToken   
    limit_headers["Organization"]=organizationId
    limit_data={"semesterId":semesterId}
    limit=requests.post('https://cpes.legym.cn/running/app/getRunningLimit', headers=login_headers, json=limit_data)
    return limit.json()
    #limitationsGoalsSexInfoId=limit.json()["data"]["limitationsGoalsSexInfoId"]

def clear_screen():
    # 判断系统类型
    if os.name == 'nt':  # Windows系统
        os.system('cls')
    else:  # Mac和Linux系统
        os.system('clear')

def legym_getseme(az,oi):
    seme_headers = {
                'User-Agent': f"Mozilla/5.0 (Linux; Android 14; {fake_device} Build/UKQ1.230804.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/118.0.0.0 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/34.285713)",
                'Connection': "Keep-Alive",
                'Accept-Encoding': "gzip",
                'Authorization': f"Bearer {az}",
                'Organization': oi,
                'Content-Type': "application/json",
                'Cookie': "JSESSIONID=5AEC9EBD7C246AF4E8F66A29D5A46382"
                }
    #print(seme_headers)
    #response_seme = requests.get('https://cpes.legym.cn/education/semester/getCurrent', headers=seme_headers)
    url = "https://cpes.legym.cn/education/semester/getCurrent"
    response_seme = requests.get(url, headers=seme_headers)
    #print(response_seme.text)
    #if response_seme.json()["data"]["id"]!=None:
    try:
        return response_seme.json()["data"]["id"]
    except:
        print("获取学期失败，可能处于假期中···")
        exit()


def legym_login(userid,password):
    login_data={"entrance":"1","password":password,"userName":userid}
    response = requests.post('https://cpes.legym.cn/authorization/user/manage/login', headers=login_headers, json=login_data)
    if response.json()["code"] !=0:
        print(response.json()["message"])
        exit()
    print("登陆账户: "+response.json()["data"]['schoolName']+"  "+response.json()["data"]['realName'])
    with open ("legym_save.ini","w") as f:
        f.write(json.dumps({"name":response.json()["data"]['schoolName']+"  "+response.json()["data"]['realName'],"userid":userid,"password":password}))
    accessToken=response.json()["data"]['accessToken']
    organizationId=response.json()["data"]['organizationId']
    userid_another=response.json()["data"]['id']
    #print(accessToken)
    #print(organizationId)
    if accessToken != None and organizationId != None:
        return accessToken,organizationId,userid_another
    else:
        print("登录失败，accessToken或organizationId为空")
        exit()

def get_local_save():
    #不存在legym_save.ini则创建跳过
    if not os.path.exists("legym_save.ini"):
        return {'name':'', 'userid':'', 'password':''}
    with open ("legym_save.ini","r") as f:
        save_data=f.read()
        return save_data

save_json=json.loads(get_local_save())
if save_json['userid'] :
    choose=input(f"检测到本地保存的账户 : {save_json['name']}，是否使用？(y/n)")
    if choose == "y":
        name=save_json["name"]
        userid=save_json["userid"]
        password=save_json["password"]
    else:
        userid=input("请输入要账户:")
        password=input("请输入要密码:")
else:
    userid=input("请输入要账户:")
    password=input("请输入要密码:")





acessToken,organizationId,userid_another=legym_login(userid,password)

print("登录成功")
semesterId=legym_getseme(acessToken,organizationId)
print("获取学期成功")
#limit ＝ POST发送 (#乐健api ＋ “running/app/getRunningLimit”, 登录协议, 文本_替换 (#seme模板, 1, , , “模板”, seme))
limit=legym_getRunningLimit(semesterId)
limitationsGoalsSexInfoId=limit["data"]["limitationsGoalsSexInfoId"]
dailyMileage=limit["data"]["dailyMileage"]
effectiveMileageStart=limit["data"]["effectiveMileageStart"]    
weeklyMileage=limit["data"]["weeklyMileage"]
totalDayMileage=limit["data"]["totalDayMileage"]
totalWeekMileage=limit["data"]["totalWeekMileage"]
print("获取限制成功") 
#输出限制
if limitationsGoalsSexInfoId == "":
    print("获取限制失败，您的学期已结束或程序脚本异常。请检查更新或联系我们")   

if limitationsGoalsSexInfoId != "":
    print("每周限制："+str(weeklyMileage)+"每日限制："+str(dailyMileage)+"单次限制："+str(effectiveMileageStart))
    print("准备就绪，可以开始赛博乐健  O.O")
else:
    print("获取路线限制失败，您的学期已结束或程序脚本异常。请检查更新或联系我们")

way="路线信息"
print("########################################################")
print("FAKELEGYM PYTHON 实现")
print("请勿售卖本程序，仅供学习交流使用（未经测试，作者本人使用自编易语言版）")
while True:
    print("########################################################")
    print("请输入功能：\n1.选择路线\n2.导出路线\n3.开始跑步")
    func=input()
    if func == "1":
        #清屏
        clear_screen()
        print("路线选择：\n1.加载本目录下legym_way.txt\n2.输入路线\n3.返回")
        func=input()
        if func == "3":
            continue
        if func == "1":
            #判断路线是否存在
            if not os.path.exists("legym_way.txt"):
                print("未找到legym_way.txt，请检查文件是否存在")
                continue
            with open("legym_way.txt","r", encoding='utf-8') as f:
                way=f.read()
                clear_screen()
                print("路线已加载，请继续选择操作")
                #print(way)
        if func == "2":
            way=input("请输入路线：")
            print("路线已加载")
    elif func == "2":
        clear_screen()
        dump_main(accessToken=acessToken,semeid=semesterId,oi=organizationId,userid=userid_another)
        continue
    elif func == "3":
        clear_screen()
        print("正在开始跑步····")
        try:
            way_temp=json.loads(way)
            #upload_example=json.dumps(way_temp)
            #
            upload_example["avePace"]=way_temp["avePace"]
            upload_example["calorie"]=way_temp["calorie"]
            upload_example["effectiveMileage"]=way_temp["effectiveMileage"]
            upload_example["totalMileage"]=way_temp["totalMileage"]
            upload_example["keepTime"]=way_temp["keepTime"]
            upload_example["deviceType"]=fake_device
            upload_example["gpsMileage"]=way_temp["gpsMileage"]
            upload_example["paceNumber"]=way_temp["paceNumber"]
            upload_example["limitationsGoalsSexInfoId"]=limitationsGoalsSexInfoId
            upload_example["semesterId"]=semesterId
            upload_example["type"]=way_temp["type"]
            upload_example["routineLine"]=way_temp["routineLine"]
            #way_json=upload_example
            way_json=upload_example
        except Exception as e:
            print(e)
            continue
        #取当前时间并转化为YYYY-MM-DD HH:MM:SS格式,并输出
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        print("当前时间："+now)
        #开始跑步

        while(True):
            try:
                print("请输入开始时间，格式为2024-09-01 00:00:00,输入1为取当前时间为结束时间，自动计算开始时间")
                start_time=input()
                if start_time == "1":
                    #t_endtime为当前时间，t_starttime为t_endtime减去way_json["keepTime"]秒
                    t_endtime=datetime.datetime.now()
                    t_starttime=t_endtime-datetime.timedelta(seconds=way_json["keepTime"])
                else:
                    t_starttime=datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                    keepTime=way_json["keepTime"]
                #结束时间=开始加持续时间（秒）
                    t_endtime=t_starttime+datetime.timedelta(seconds=keepTime)
            except ValueError: 
                print("时间格式错误，请重试")
                continue
            break
        clear_screen()
        print("信息确认：\n开始时间："+t_starttime.strftime("%Y-%m-%d %H:%M:%S"))
        print("持续时间："+str(way_json["keepTime"])+"秒")
        print("结束时间："+t_endtime.strftime("%Y-%m-%d %H:%M:%S"))
        print("卡路里："+str(way_json["calorie"]))
        print("GPS距离："+str(way_json["totalMileage"]))    
        print("有效距离："+str(way_json["effectiveMileage"]))
        print("###########################################################")   
        print("请确认信息无误，输入1为开始，输入2为重新输入")
        func=input()
        if func == "1":
            print("开始整理上传数据")
            way_json["startTime"]=t_starttime.strftime("%Y-%m-%d %H:%M:%S")
            way_json["endTime"]=t_endtime.strftime("%Y-%m-%d %H:%M:%S")
            signdigital=get_current_sign(way_json)
            if signdigital=="error":
                continue
            else:
                way_json["signDigital"]=signdigital
            result=upload_fakerun(acessToken,way_json)
            if result == "ok":
                exit()
            else:
                print("异常，请提出ISSUE并联系开发者")
                exit()
            #上传数据
        elif func == "2":
            continue
        else:
            print("输入错误，请重新输入")
            continue
        




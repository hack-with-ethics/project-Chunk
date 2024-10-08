from flask import Flask,render_template,request,url_for,session,abort,jsonify
from cryptography.fernet import Fernet
from datetime import *
import os
import hashlib
import json
from connectorapi import database_connector as db_connect

db = db_connect()
def write_csv_file(name,data):
    if os.path.exists(name):
        with open(name,'a') as file:
            file.write("\n" + data)
            file.close()
    else:
        with open(name,'w') as file:
            file.write("\n" + data)
            file.close()
    
isLogged = False
key = Fernet.generate_key()
App = Flask(__name__)
App.secret_key = key
App.permanent_session_lifetime = timedelta(minutes=30)

@App.route("/",methods=["GET","POST"])

def Login():
    global isLogged
    try:
        writeLogs(processRequest(request.headers,request.method,"login"))
    except:
        pass
    if request.method == "POST" and isLogged==False:
        username = request.form["user"]
        passwd = request.form["pass"]
        if username=="sankar" and getHash(passwd) == "e657a853a2c844561dfb6ed7927c12117267ac338056d33555918fe2753ab757561b0973bc44b908bf69997573adbbce79e49e0d440d429107df2e3bcbd7c78e":
            print("Access Granted [ ! ]")
            session.permanent = True
            session["user"] = username
            session["pass"] = passwd
            print("[ + ]username :",username)
            print("[ + ] Password :",passwd)
            isLogged = True
            return render_template("login.html")
        return render_template("index.html",error='❌ login Error 🚨')
    
    else:
        if "user" in session:
            
            return render_template("login.html")
        isLogged = False

        return render_template("index.html",error="")
    
@App.route("/reports")

def report_genrate():
    return render_template("report.html")    

@App.route("/logout")

def logout():
    print(request.data)
    print(request.referrer)
    print(request.authorization)
    print(request.cookies)
    writeLogs(processRequest(request.headers,request.method,"logout"))
    global isLogged
    session.pop("user",None)
    isLogged = False
    return render_template("index.html")

@App.route("/patient")
def patient():
    global isLogged
    writeLogs(processRequest(request.headers,request.method,"Pateint Details"))
    if "user" in session:
        return render_template("patient.html")
    else:
        isLogged = False
        return abort(404)
@App.route("/vendor")

def vendormanage():
    
    global isLogged
    writeLogs(processRequest(request.headers,request.method,"vendor Management "))
    if "user" in session:
        return render_template("Vendor.html")
    else:
        isLogged = False
        return render_template("index.html")

@App.route("/genreport",methods=["Post"]) 
def getreport():
    data = request.json
    val = data.split()
    total = 0

    Format = "\nName,test,amount,date"
    file_Name =val[2]+ ".csv"
    print(getTimeInfo().strftime("%M-%D"))
    write_csv_file(file_Name,Format)
    lst = db.console(f'select * from {val[2]+"_det"} where (date between "{val[0]}" and "{val[1]}" )')

    for assets in lst:
        total += int(assets[3])
        Format=f"{assets[1]},{assets[2]},{assets[3]},{assets[4]}"
        write_csv_file(file_Name,Format)
    Format = f"Total,,{total}"
    write_csv_file(file_Name,Format)
    print(total)
    # lst = db.console("select * from lalpathlabs")
    # print(lst)
    # for i in lst:
    #     if i[-1].split("-")[1] == val[0] and val[1] == i[5]:
    #         total+=int(i[6])
    #         if os.path.exists(f"{val[1]}.csv"):
    #             with open(f"{val[1]}.csv",'a') as file:
    #                 file.write(f"\n{i[0]},{i[2]},{i[5]},{i[6]},{i[7]}")
    #                 file.close()
    #         else:
    #             with open(f"{val[1]}.csv",'w') as file:
    #                 file.write("\nName,Barcode,Head,Cost,Date")
    #                 file.close() 
    # with open(f"{val[1]}.csv",'a') as file:
    #     file.write(f"\ntotal,{total}")
    #     file.close()
    # os.system()
        
    return jsonify(f"Generated : {os.getcwd()}")
@App.route("/info",methods=["Post"])

def getInfo():
    
    object = request.get_json()
    print(object)
    # id_counter = db.console("select count(id) from lalpathlab")
    # db.console(f'insert into lalpathlab values("{str(int(id_counter[0][0])+1)}","{object["pat_name"]}","{object["contact_info"]}","{object["long"]}","{object["age_det"]}","{object["gender_info"]}","{object["long1"]}","{object["head_info"]}","{object["dis"].split(".")[1].strip()}")')
    # # if "user" in session: 2,sanjai,4545,9487887880,34,Male,Yuvan,Sanker,5
    counter = db.console("select count(sno) from daily_sales")
    if(len(counter) == 0):
        counter = 1
    else:
        counter = int(counter[0][0]) + 1
    data = f'{counter},'
    keys = object.keys()
    inc = 0
    for i in keys:
        if i == "dis":
            final = f'"{object[i].split(".")[1].strip()}"'
        elif i == "header":
            continue
        else:
            final = f'"{object[i]}"'
        # if i == "dis":
        #     data += f'"{object[i].split(".")[1].strip()}",'
        # elif i == "header":
        #     pass
        # else:
        #     if i == "date":
        #         data += f'"{object[i]}"'
        #     else:
        #         data += f'"{object[i]}",'
        if inc == len(keys) - 2:
            data += final
        else:
            data += final+","
        inc+=1
    data = data.split(",")
    swap = data[len(data) - 1]
    data[len(data) - 1] = data[len(data) - 2]
    data[len(data) - 2] = swap
    data = ",".join(data) 
    print(data)
    db.console(f'insert into daily_sales values({data})')
    header_Dict = object["header"] 
    lst = [i[0] for i in db.console("show tables")]
    print(lst)
    for header in header_Dict:
        
        
        if header+"_det" in lst:
            counter = db.console(f'select count(sno) from {header+"_det"}')
            counter = int(counter[0][0])
            f = header_Dict[header].split(",")
            header = header+"_det"
            for i in range(len(f)-1):
                if i%2 == 0:
                    test = f[i]
                    if test!="":
                        cost = f[i+1]

                        print("test : ",test)
                        print("cost :",cost)
                        db.console(f'insert into {header} values("{counter+1}","{object["pat_name"]}","{test.strip()}","{cost.strip()}","{object["date"]}")')
        
        else:
            print(f"Creating {header+'_det'}")
            db.console(f'create table {header+"_det"}(sno varchar(10),Name varchar(200),test varchar(200),cost varchar(200),date varchar(200))')
            counter = 1
            f = header_Dict[header].split(",")
            print(f)
            for i in range(len(f)-1):
                if i%2==0:
                    test = f[i]
                    if test!="":
                        cost = f[i+1]
                        print("test : ",test)
                        print("cost :",cost)
                        lst.append(f"{header+'_det'}")
                        db.console(f'insert into {header+"_det"} values("{counter}","{object["pat_name"]}","{test}","{cost}","{object["date"]}")')
                    
    print(object)
    
    return render_template("patient.html")

@App.route("/getvendor",methods=["POST"])
def vendorInfo():
    
    object = request.get_json()
    object = object.split()
    print(object)
    if len(object) == 2:
        print(object)
        lst = db.console(f'select test,cost from {object[1]}')
        return jsonify(lst)
    elif len(object) == 4 and object[0].lower().strip() == "add":
        db.console(f'insert into {object[2]} values("{object[1]}","{object[3]}")')
        return "Added"
    elif len(object) == 4 and object[0].lower().strip() == "acchead":
        lst = db.console("show tables")
        found = 0
        for tabs in lst:
            if tabs[0].lower() == object[1]:
                found = 1
                details = db.console(f'select cost from {object[1]} where test="{object[2]}" and vendor="{object[3]}"')
                if len(details)!=0:
                    return jsonify(details)
                else:
                    return jsonify(len(details))
        if found == 0:
            db.console(f'create table {object[1]} (test varchar(225),cost varchar(225),vendor varchar(225))')
            return jsonify(len([]))
    elif len(object) == 5 and object[0].lower().strip() == "acchead":
        db.console(f'insert into {object[1]} values("{object[2]}","{object[3]}","{object[4]}")')

    # elif len(object) == 3 and object[0].lower().strip() == "acchead":
    #     ops = object[0]
    #     if ops.lower() =="add":
    #         db.console(f'insert into {object[2]} values("{object[1]}","{object[3]}")')
    #     elif ops.lower() == "acchead":
    #         print(object)
    #         lst = db.console("show tables")
    #         flag = 0
    #         for i in lst:
    #             if i[0].lower() == object[1]:
    #                 flag = 1
                    
    #                 details = db.console(f'select cost from {object[1]} where test="{object[2]}"')
    #                 if len(details)!=0:
    #                     return jsonify(details)
    #                 else:
    #                     return jsonify(len(details))
    # elif len(object) == 4 and object[0].lower() == "acchead":
    #     print(object)
    #     db.console(f'insert into {object[1]} values("{object[2]}","{object[3]}")')
    # elif len(object) == 4 and object[0].lower() == "add":
    #     db.console(f'insert into {object[2]} values("{object[1]}","{object[3]}")')
    return jsonify("added")
@App.route("/crud",methods=["POST"])
def crudops():
    if "user" in session:
        ops = request.get_json()
        Arr = ops.split()
        print(Arr)
        if Arr[0].lower().strip() == "create":
            print("[ + ] Create Operation")
            db.console(f'create table {Arr[1]}(test varchar(225),cost varchar(225))')
        elif Arr[0].lower().strip() =="update":
            db.console(f'{Arr[0]} {Arr[len(Arr) - 1]} set cost="{Arr[1]}" where test="{Arr[2]}"')
        else:
            db.console(f'{Arr[0]} into {Arr[len(Arr) - 1]} values("{Arr[1]}","{Arr[2]}")')
        return jsonify("Inserted !")
    else:
        return render_template("index.html")

@App.route("/console",methods=["GET"])
def console():
    return abort(404)

# Functions Python Based [ * ] ============================================= [ * ]

def getHash(p):
    return hashlib.sha512(p.encode()).hexdigest()

def writeLogs(data):
    log_file = getTimeInfo().strftime("%D").split("/")
    log_file = "-".join(log_file)
    if os.path.exists(f"{log_file}.txt"):
        with open(f"{log_file}.txt",'a') as file:
            file.write(f"{getTimeInfo().strftime('%I:%M')} - "+data + "\n")
            file.close()
    else:
        with open(f"{log_file}.txt",'w') as f:
            f.write(f"{getTimeInfo().strftime('%I:%M')} - " + data + "\n")
            f.close()
    
def processRequest(request,code,nav):
    lst = ["host","Referer","Sec-Ch-Ua-Platform","Sec-Ch-Ua","Sec-Ch-Ua-Mobile"]
    time = getTimeInfo().strftime("%I:%M")
    Logs = f'[Info] Method : {code}\n'
    Logs+= f'To : {nav}\n'
    for i in lst:
        try:
            if i == "host":
                Logs+= f"Host_data:{request[i]} \n"
            elif i == "Referer":
                Logs+= f"Request_From : {request[i]} \n"

            elif i == "Sec-Ch-Ua-Platform":
                if request[i].lower() == "windows":
                    
                    Logs+="Device Info Windows"
                else:
                    Logs+=f"Request Made form : {request[i]}"
                if request["Sec-Ch-Ua-Mobile"].split("?")[1] == "0":
                    Logs+= "[ Desktop ]\n"
                else:
                    Logs+= "(Mobile)\n"
            elif i == "Sec-Ch-Ua":
                Logs+= f"User Agent Info {request[i]}\n"
        except:
            continue
    if "user" in session:
        Logs+="Session : True\n"
    else:
        Logs+= "Session : False\n"
    return Logs

def getTimeInfo():
     return datetime.now()                #.strftime("%I:%M - %D")

#=======================================================
# =====

App.run(debug=True)
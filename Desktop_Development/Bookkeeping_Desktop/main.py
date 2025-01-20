import json
import datetime
import PySimpleGUI as sg

# d = '[{"时间": "2024/08/07 22:24:56", "项目": "收到货款", "金额": 200, "分类": "收入"}]'
# with open(r"data.txt",'w') as f:
#     f.write(d)

def readData():
    with open(r"data.txt","r") as f:
        jsonData = f.read()
        dataList = json.loads(jsonData)
        return dataList

def writeData(dataList):
    jsonData = json.dumps(dataList, ensure_ascii=False)
    with open(r"data.txt","w") as f:
        f.write(jsonData)
    sg.popup("账户录入成功！")

# print(readData())

def showData():
    data = readData()
    dataLists = []
    for d in data:
        if d["分类"] == "收入":
            dataList = [d["时间"],d["项目"],d["金额"],d["分类"]]
            dataLists.append(dataList)
        else:
            dataList = [d["时间"],d["项目"],d["金额"] * -1,d["分类"]]
            dataLists.append(dataList)
    return dataLists

# print(showData())

def sumin():
    sumin=0
    data = readData()
    for d in data:
        if d["分类"]=="收入":
            sumin+=d["金额"]
    return sumin

def sumout():
    sumout = 0
    data = readData()
    for d in data:
        if d["分类"]=="支出":
            sumout+=d["金额"]
    return sumout

def addData(content,amount,cla):
    dataList = readData()
    t=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    data={"时间":t,"项目":content,"金额":amount,"分类":cla}
    dataList.append(data)
    writeData(dataList)

def deleteData(content):
    dataList = readData()
    # print(content,readData(),type(content))
    # return
    for item in dataList:
        if item['项目'] == content:
            dataList.remove(item)
    # dataStr=str(dataList)
    # return
    jsonData = json.dumps(dataList, ensure_ascii=False)
    with open(r"data.txt","w") as f:
        f.write(jsonData)
    sg.popup("账户删除成功！")



def main():
    list = showData()
    sin = sumin()
    sout = sumout()
    layout=[
        [sg.T("账目清单：")],
        [sg.Table(list,headings=["时间","项目","金额","分类"],
                  key="-show-",
                  justification="c",
                  auto_size_columns=False,
                  def_col_width=15

                  )],
        [sg.T("总收入"+str(sin)+"元，总支出"+str(sout)+"元，结余"+str(sin-sout)+"元",key="-text-")],
        [sg.T("请输入账单项目："),sg.In(key="-content-")],
        [sg.T("请输入账单金额："),sg.In(key="-amount-")],
        [sg.T("请输入账单分类：")],
        [sg.T("请输入账单分类：")]+[sg.Radio(i,group_id=1,key=i) for i in ["收入","支出"]],

        [sg.HorizontalSeparator ()],
        [sg.T("请输入删除内容："),sg.In(key="-delete-")],
        [sg.HorizontalSeparator ()],


        [sg.Column([[
            sg.B("确认提交"),
            sg.Text(""),
            sg.Text(""),
            sg.Text(""),
            sg.Text(""),
            sg.Text(""),
            sg.Text(""),
            sg.Text(""),
            sg.Text(""),
            sg.Text(""),
            sg.Text(""),
            sg.Text(""),
            sg.Text(""),
            sg.Button("确认删除"),
        ]],justification='c')],
    ]
    window = sg.Window("记账本", layout)
    while True:

        event, values = window.read()
        # print(values.items())
        if event == sg.WINDOW_CLOSED: break
        if event == "确认提交":
            content, amount = values["-content-"], float(values["-amount-"])
            cla = None
            for k,v in values.items():
                # print(k,v)
                if v == True:
                    cla=k
                    addData(content,amount,cla)
                    list=showData()
                    sout=sumout()
                    text="总收入"+str(sin)+"元，总支出"+str(sout)+"元，结余"+str(sin-sout)+"元"
                    window["-show-"].update(values=list)
                    window["-text-"].update(value=text)
                    window["-content-"].update("")
                    window["-amount-"].update("")

        if event == "确认删除":
            delete_data = values["-delete-"]
            deleteData(delete_data)
            list = showData()
            sout = sumout()
            text = "总收入" + str(sin) + "元，总支出" + str(sout) + "元，结余" + str(sin - sout) + "元"
            window["-show-"].update(values=list)
            window["-text-"].update(value=text)
            window["-content-"].update("")
            window["-amount-"].update("")
    window.close()
main()

# print(showData())
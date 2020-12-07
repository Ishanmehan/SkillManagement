import pandas
import numpy as np
import time

class ReadInput:

    def __init__(self, filepath):

        self.ex_df = ""
        self.divisions = []
        self.fetchdataframe(filepath)
        self.ex_heading = self.fetchheading()
        self.Division = 0
        self.UserID = 1
        self.Primary_skillset = 2
        self.Knowledge_Area = 4
        self.Category= 5
        self.Skill_Name = 6
        self.Current_Level = 7
        self.Target_Level = 8
        self.rowData = {}
        self.excel_create()
        self.userDictFunc()
        print("Class initialized")
        
    def runUsecase(self,usecase,label = None):
        self.label = label
        if usecase == "usecase1":
            self.updatenearnessmatrix([2,6], "usecase1")
        elif usecase == "usecase2":
            self.updatenearnessmatrix([6,1], "usecase2")
        elif usecase == "usecase3":
            self.updatenearnessmatrix3var([0, 6, 2],"usecase3")
            
    def updateLabel(self,max,cur):
        com = int((cur/max)*100)
        if self.label != None:
            if com == 100:
                self.label["text"] = ""
            else:
                self.label["text"] = "Completed :" + str(com) + "%"

            
    def fetchdataframe(self, filepath):
        self.ex_df = pandas.read_excel(open(filepath, 'rb'))

    def fetchheading(self):
        ex_heading = []
        for head in self.ex_df:
            ex_heading.append(head)
        return ex_heading

    def fetchdivision(self):
        if "Division" in self.ex_heading:
            self.divisions = set(self.ex_df["Division"])

    def fetch_division_userid(self):
        list_id_details = dict()
        if "Division" in self.ex_heading and "User ID" in self.ex_heading:
            for index in range(len(self.ex_df)):
                for di in self.divisions:
                    list_id_details.setdefault(di, [])
                    if self.ex_df.loc[index, "Division"] == di:
                        list_id_details.setdefault(di, []).append(self.ex_df.loc[index, "User ID"]) \
                            if self.ex_df.loc[index, "User ID"] not in list_id_details[di] else []

        print(list_id_details)
        for num in list_id_details:
            print(num, len(list_id_details[num]))
        return list_id_details

    def fetch_skillsets(self):
        skill_set_details = dict()
        if "Division" in self.ex_heading and "Primary skillset" in self.ex_heading:
            for index in range(len(self.ex_df)):
                for di in self.divisions:
                    skill_set_details.setdefault(di, [])
                    if self.ex_df.loc[index, "Division"] == di:
                        skill_set_details.setdefault(di, []).append(self.ex_df.loc[index, "Primary skillset"]) \
                            if self.ex_df.loc[index, "Primary skillset"] not in skill_set_details[di] else []

        print(skill_set_details)
        for num in skill_set_details:
            print(num, len(skill_set_details[num]))
        return skill_set_details
    
    
    def userDictFunc(self):
        self.userDict = {}
        for index in range(len(self.ex_df)):
            currId = self.ex_df.loc[index, "User ID"]
            updateList = [self.ex_df.loc[index, "Division"],
                          self.ex_df.loc[index, "SpotOn Role"],
                          self.ex_df.loc[index, "Primary skillset"],
                          self.ex_df.loc[index, "Other skillsets"],
                          self.ex_df.loc[index, "Knowledge Area"],
                          self.ex_df.loc[index, "Category"],
                          self.ex_df.loc[index, "Skill Name"],
                          self.ex_df.loc[index, "Current Level"],
                          self.ex_df.loc[index, "Target Level"]]
            if currId not in self.userDict.keys():
                self.userDict.update({currId: [updateList]})
            else:
                self.userDict[currId].append(updateList)
    def intersection(self, *args):

        x = "list("
        for i in range(len(args)):
            x = x + "set(args[" + str(i) + "]) &"
        x = x[:-1] + ")"
        li = eval(x)
        return li
    
    def updatenearnessmatrix(self,indexes ,usecase, listParse =[]):
        fullskillsetNearnessList = []
        skillsetNearnessList = []
        rowskillset = []
        for index in indexes:    
            self.updatecolvariables(index)

        
        rowskillset = self.rowData[indexes[0]]
        rowskillset = list(set(rowskillset))
        if len(listParse) != 0:
            rowskillset = listParse
        for i,row in enumerate(rowskillset):
            self.updateLabel(len(rowskillset),i+1)
            skillsetNearnessList = []
            for column in rowskillset:
                skillsetNearnessList.append(self.skillsetNearness(row, column,indexes[0], indexes[1]))
                
            fullskillsetNearnessList.append(skillsetNearnessList)
        print(fullskillsetNearnessList)
        print(rowskillset)
        self.excel_create()
        numpy_data = np.array(fullskillsetNearnessList)
        df = pandas.DataFrame(data=numpy_data, index=rowskillset, columns=rowskillset)
        self.excel_create()
        df.to_excel(self.writer, sheet_name=usecase)
        self.writer.save()
    
    def updatecolvariables(self,index):

        if index not in self.rowData.keys():
            self.rowData.update({index:[]})
            for i in self.userDict:#3000
                for j in self.userDict[i]:#40000
                    self.rowData[index].append(j[index])

    
    def updatenearnessmatrix3var(self,indexes,usecase,listParse = []):
        fullskillsetNearnessList = []
        skillsetNearnessList = []
        rowskillset = []
        for index in indexes:    
            self.updatecolvariables(index)
        self.excel_create()
        rowskillset = self.rowData[indexes[0]]
        rowskillset = list(set(rowskillset))
        startRow = 0
        startRowlen = len(rowskillset)
        if len(listParse) == 0:
            listParse = self.rowData[indexes[2]]
        listParse = list(set(listParse))
        for i,var in enumerate(listParse):
            fullskillsetNearnessList = []
            self.updateLabel(len(listParse),i+1)
            for row in rowskillset:
                skillsetNearnessList = []
                for column in rowskillset:
                    print(var,row,column)
                    skillsetNearnessList.append(self.skillsetNearness3var(row, column,var,indexes[0], indexes[1],indexes[2]))
    
                fullskillsetNearnessList.append(skillsetNearnessList)

            numpy_data = np.array(fullskillsetNearnessList)
            df = pandas.DataFrame(data=numpy_data, index=rowskillset, columns=rowskillset)
            df1 = pandas.DataFrame({var:[]})
            df1.to_excel(self.writer, sheet_name=usecase,startrow = startRow,index =False)
            df.to_excel(self.writer, sheet_name=usecase,startrow = startRow)
            startRow = startRow+startRowlen+3

        self.writer.save()
        
    def updateskillNearnessMatrix(self):
        mean_skill_dict={}
        if not self.rowskill:
            self.updaterowvariables()
        self.rowskill = list(set(self.rowskill))
        for row in self.rowskill:
            mean_skill_dict[row] = self.mean_current_target_level(value=row)
        self.excel_create()
        print(mean_skill_dict)
        df = pandas.DataFrame.from_dict(mean_skill_dict, orient='index').T
        x = df.corr(method='pearson')
        print(type(x))
        x.to_excel(self.writer, sheet_name="use-case2")
        self.writer.save()
        

    def mean_current_target_level(self, section="Skill Name", value="ASPICE"):
        val = []
        for index in range(len(self.ex_df)):
            if self.ex_df.loc[index,section] == value:
                val.append([self.ex_df.loc[index, "Current Level"],self.ex_df.loc[index, "Target Level"]])
            print(val)
    
        a = np.array(val)
        print(np.nanmean(a,axis=1))
        return np.nanmean(a,axis=1) 
 

    def fetchskillsetintersetcion(self):
        sl = self.fetch_skillsets()
        divisions = list(self.divisions)
        division_num = len(self.divisions)
        dyn_var = {}
        f = open("D:\\interssction.txt", "w+")
        for i in range(division_num):
            print(i)
            print(divisions[i])
            for j in range(i+1, division_num):
                f.write(divisions[i]+"_"+divisions[j]+"\n")
                f.write(str(self.intersection(sl[divisions[i]], sl[divisions[j]])))
                dyn_var[divisions[i]+"_"+divisions[j]] = self.intersection(sl[divisions[i]], sl[divisions[j]])

        # print(dyn_var)
        full_divisions_inter = ""
        paramter = ""
        for i in divisions:
            full_divisions_inter = full_divisions_inter +str(i)+"_"
            paramter = paramter + "sl["+i+"] ,"
        print(full_divisions_inter[:-1])
        print(paramter[:-1])
        # f.write(str(eval(self.intersection(paramter)))
        # dyn_var[full_divisions_inter[:-1]] = self.intersection(eval(paramter))
        f.close()
        
 

    def excel_create(self):
        try:
            self.writer = pandas.ExcelWriter("Skill_Mangement.xlsx",mode="a", engine = "openpyxl")
        except Exception as e:
            self.writer = pandas.ExcelWriter("Skill_Mangement.xlsx", engine = "openpyxl")

    def skillsetNearness3var(self, inp1, inp2,inp3, index1, index2, index3):
        s1 = []
        s2 = []

        if inp2 == inp1:
            return 1
        for id in self.userDict:
            for details in self.userDict[id]:
                # print(details)
                # print(inp1)
                # print(inp2)
                if details[index1] == inp1 and details[index3] == inp3:
                    s1.append(details[index2])
                elif details[index1] == inp2 and details[index3] == inp3:
                    s2.append(details[index2])
            # print(s1)
            # print(s2)
        s1 = list(dict.fromkeys(s1))
        s2 = list(dict.fromkeys(s2))
        intersection = [value for value in s1 if value in s2]
        if len(set(s1 + s2)) == 0:
            return 0
        res = len(intersection) / len(set(s1 + s2))
        print(round(res,2))
        return round(res,2)
    
    def skillsetNearness(self, inp1, inp2, index1, index2):
        s1 = []
        s2 = []
#        print(inp2,inp1)
        if inp2 == inp1:
            return 1
        for id in self.userDict:
            for details in self.userDict[id]:
                # print(details)
                # print(inp1)
                # print(inp2)
                if details[index1] == inp1:
                    s1.append(details[index2])
                elif details[index1] == inp2:
                    s2.append(details[index2])
#            print(s1)
#            print(s2)
        s1 = list(dict.fromkeys(s1))
        s2 = list(dict.fromkeys(s2))
        intersection = [value for value in s1 if value in s2]
        if len(set(s1 + s2)) == 0:
            return 0
        res = len(intersection) / len(set(s1 + s2))
        print(round(res,2))
        return round(res,2)

    def updaterowvariables(self):
        self.rowskillset = []
        self.rowskill = []
        for i in self.userDict:#3000
            for j in self.userDict[i]:#40000
                self.rowskillset.append(j[self.Primary_skillset])
                self.rowskill.append(j[self.Skill_Name])

    def updateskillsetnearnessmatrix(self):
        fullskillsetNearnessList = []
        skillsetNearnessList = []
        self.excel_create()
        if not self.rowskillset:
            self.updaterowvariables()

        self.rowskillset = list(set(self.rowskillset))

        for row in self.rowskillset:
            skillsetNearnessList = []
            for column in self.rowskillset:
                skillsetNearnessList.append(self.skillsetNearness(row, column, self.Primary_skillset, Skill_Name ))
            fullskillsetNearnessList.append(skillsetNearnessList)
        print(fullskillsetNearnessList)
        print(self.rowskillset)

        numpy_data = np.array(fullskillsetNearnessList)
        df = pandas.DataFrame(data=numpy_data, index=self.rowskillset, columns=self.rowskillset)
        self.excel_create()
        df.to_excel(self.writer, sheet_name="use-case1")
        self.writer.save()



    def updateskillNearnessMatrix(self):
        fullskillNearnessList = []
        skillNearnessList = []
        self.excel_create()
        if not self.rowskill:
            self.updaterowvariables()

        self.rowskill = list(set(self.rowskill))

        for row in self.rowskill:
            skillNearnessList = []
            for column in self.rowskill:
                skillNearnessList.append(self.skillsetNearness(row, column, self.Skill_Name, self.Primary_skillset))
            fullskillNearnessList.append(skillNearnessList)
        print(fullskillNearnessList)
        print(self.rowskill)

        numpy_data = np.array(fullskillNearnessList)
        df = pandas.DataFrame(data=numpy_data, index=self.rowskill, columns=self.rowskill)
        # self.excel_create()
        df.to_excel(self.writer, sheet_name="use-case2")
        self.writer.save()

    def check_employee_skill_nearness(self, empid, skill , area = "Skill Name"):

        current_skill_list = []
        matched_skill = []
        nearness = -1
        future_skill_list = []
        for item in skill.split(","):
            future_skill_list.append(item.strip())
        print(future_skill_list)
        for index in range(len(self.ex_df)):
            if str(self.ex_df.loc[index, "User ID"]) == empid:
                print(self.ex_df.loc[index, area])
                current_skill_list.append(self.ex_df.loc[index, area])
        print(current_skill_list)
        if len(current_skill_list) > 0 and len(future_skill_list) > 0:
            current_skill_list = list(set(current_skill_list))
            future_skill_list = list(set(future_skill_list))
            matched_skill = [value for value in current_skill_list if value.strip() in future_skill_list]
            print(matched_skill)
            nearness = len(matched_skill) / len(future_skill_list)
            nearness = round(nearness,2)
        return (nearness , matched_skill)

if __name__ == "__main__":
    filepath = r"C:\Users\lul3kor\Desktop\Sample_Data_SkillManagement.xlsx"#Sample_Data_SkillManagement.xlsx"
#    filepath = r"D:\SkillManagement\Sample_Data_SkillManagement.xlsx"
    ReadInput = ReadInput(filepath)
#    ReadInput.fetchdivision()
#    print(ReadInput.divisions)
#    print(ReadInput.ex_heading)
#    print(ReadInput.fetch_division_userid())
#    ReadInput.fetch_skillsets()
#    ReadInput.excel_create()
#    ReadInput.excel_create()
#    ReadInput.userDictFunc()
#    print(ReadInput.userDict)
#    ReadInput.updateskillNearnessMatrix()
    # ReadInput.fetchskillsetintersetcion()
#    ReadInput.updatenearnessmatrix([2, 6],"usecase1")
#    ReadInput.updaterowvariables1(2)
    # ReadInput.updatenearnessmatrix([6,1],"usecase6")#,["EV and Hybrid Systems","Design and Estimation"])
    ReadInput.updatenearnessmatrix3var([0,6,2],"usecase3")
#    print(ReadInput.check_employee_skill_nearness("7","Skill Name","abc,cde"))


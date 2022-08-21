import re
import os
import getpass


class SnippetData:
    def __init__(self, File_Name='', SnippetType='', Title='', Description='', Shortcut='', Language='', codes=''):
        self.File_Name = File_Name
        self.SnippetType = SnippetType
        self.Title = Title
        self.Description = Description
        self.Shortcut = Shortcut
        self.Language = Language
        self.codes = codes


# 处理特殊符号
def conversCode(code):
    code = code.replace('\n', '|_|')  # 换行
    code = code.replace('$end$', '|-|')  # 终止符
    code = code.replace('$', '')  # 删掉$
    return code


# 将单个snippet输出到对应整合文件
def writeToDevC(obj):
    if obj.SnippetType == "SurroundsWith":
        print("暂不支持 SurroundsWith 类型 : " + obj.File_Name)
        return
    with open('./Out/codeinsertion.ini', 'a+', encoding='utf-8') as file_obj:
        prefix = obj.Shortcut
        body = obj.codes.replace("|_|", "$_").replace("|-|", "*|*")
        description = obj.Description.replace("\n", "").replace(" ", "")
        passage = (
            "[{}]\nDesc={}\nLine={}\nSep=1\n".format(prefix, description, body))
        file_obj.write(passage)


# 检索整合数据
def getDatas(path, file_name):
    passage = ''
    fo = open(path + file_name, encoding='utf-8')
    for lines in fo.readlines(): passage += lines
    fo.close()
    start = '[\s\S]*<CodeSnippet Format="1\.0\.0">'
    type = '[\s\S]*<SnippetType>([\s\S]*)</SnippetType>'
    titel = '[\s\S]*<Title>([\s\S]*)</Title>'
    descriptiom = '[\s\S]*<Description>([\s\S]*)</Description>'
    shortcut = '[\s\S]*<Shortcut>([\s\S]*)</Shortcut>'
    codes = '[\s\S]*<Code Language="([\s\S]*)" Delimiter="\$"><!\[CDATA\[([\s\S]*)]]></Code>'
    end = '[\s\S]*</CodeSnippets>'
    searchObj = re.search(start + type + titel + descriptiom + shortcut + codes + end, passage, re.M)
    if searchObj:
        code = conversCode(searchObj.group(6))
        obj = SnippetData(file_name, searchObj.group(1), searchObj.group(2), searchObj.group(3), searchObj.group(4),
                          searchObj.group(5), code)
        writeToDevC(obj)
    else:
        print("Not Find!! " + file_name + '\n')


# 遍历snippet输出到对应整合文件
def readFile():
    if not os.path.exists('Snippets'):
        os.mkdir('Snippets')
        print('请将VS的snippet放到本目录中的Snippets文件夹中')
        return
    print('转化为DevC++Snippet')
    if not os.path.exists('Out'): os.mkdir('Out')
    with open('./Out/codeinsertion.ini', 'w+', encoding='utf-8') as file_obj:
        pass
    path = './Snippets/'
    files = os.listdir(path)
    for file_name in files:
        getDatas(path, file_name)
    print("Successful Operation!")
    print(r"请将./Out中的codeinsertion.ini 放到 C:\Users\{}\AppData\Roaming\Dev-Cpp中".format(getpass.getuser()))


if __name__ == "__main__":
    readFile()

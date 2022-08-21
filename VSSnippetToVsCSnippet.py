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
def writeToVSC(obj):
    if obj.SnippetType == "SurroundsWith":
        print("暂不支持 SurroundsWith 类型 : " + obj.File_Name)
        return
    with open('./Out/vscode.code-snippets', 'a+', encoding='utf-8') as file_obj:
        name = obj.File_Name
        scope = obj.Language
        prefix = obj.Shortcut
        body = obj.codes.replace("\\", "\\\\").replace("\"", "\\\"") \
            .replace("|_|", "\",\n\t\t\t\t\"").replace("|-|", "$0").replace("\t", "   ")
        description = obj.Description.replace("\n", "").replace(" ", "")
        passage = ("\t\"{name_}\": {{\n"
                   "\t\t\"scope\": \"{scope_}\",\n"
                   "\t\t\"prefix\": \"{prefix_}\",\n"
                   "\t\t\"body\": [\n"
                   "\t\t\t\"{body_}\"\n"
                   "\t\t],\n"
                   "\t\t\"description\": \"{description_}\"\n"
                   "\t}},\n".format(name_=name, scope_=scope, prefix_=prefix, body_=body, description_=description))
        file_obj.write(passage)


# 检索整合数据
def getDatas(file_name):
    passage = ''
    fo = open('./Snippets/' + file_name, encoding='utf-8')
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
        writeToVSC(obj)
    else:
        print("Not Find!! " + file_name + '\n')


# 遍历snippet输出到对应整合文件
def readFile():
    if not os.path.exists('Snippets'):
        os.mkdir('Snippets')
        print('请将VS的snippet放到本目录中的Snippets文件夹中')
        return
    print('转化为VsCodeSnippet')
    if not os.path.exists('Out'): os.mkdir('Out')
    with open('./Out/vscode.code-snippets', 'w+', encoding='utf-8') as file_obj:
        file_obj.write("{\n")
    files = os.listdir('./Snippets/')
    for file_name in files:
        getDatas(file_name)
    with open('./Out/vscode.code-snippets', 'a+', encoding='utf-8') as file_obj:
        file_obj.write("}")
    print("Successful Operation!")
    print(r"请将./Out中的vscode.code-snippets放到 C:\Users\{}\AppData\Roaming\Code\User\snippets中".format(getpass.getuser()))

if __name__ == "__main__":
    readFile()
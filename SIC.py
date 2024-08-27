import math

# 十六進位轉換字典
HexDict = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}

def Dec2Hex(Dec):
    Hex = ''
    # 將十進位轉換為十六進位
    while (Dec >= 16):
        Hex = (HexDict[Dec % 16] + Hex)
        Dec //= 16

    Hex = (HexDict[Dec] + Hex)
    return Hex

# 十六進位轉換字典（反向）
DecDict = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,'8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}

def Hex2Dec(Hex):
    Dec = 0
    times = 0
    # 將十六進位轉換為十進位
    while (len(Hex) > 0):
        Dec += int(DecDict[Hex[-1]] * math.pow(16, times))
        Hex = Hex[:-1]#將十六進制字符串轉換為十進制時，需要從最低位開始逐位處理、並將最低位的字符去除，以便處理下一個更高位的數字。
        times += 1

    return Dec

# 處理BYTE指令
def BYTE(value):
    mode = value[0] 
        #獲取 value 字串的第一個字符，這是 BYTE 指令中的模式（C 或 X）
    data = value[2:-1]
    #截取 value 字串中從第三個字符到倒數第二個字符的子字串，value 進行截取的目的是去除可能存在的引號
    objCode = ''
    if (mode == 'C'):
        #將資料每一自轉換為ASCII碼，再轉乘16進制
        for i in data:
            objCode += (Dec2Hex(ord(i))).zfill(2)
            #將結果添加到 objCode，zfill(2)用以確保轉換後的十六進位表示都是兩位數
    elif (mode == 'X'):
        #當資料都為16進位時，不須再轉換成16進位
        objCode += data
        #將資料data加入opcode中
    else:#如果不是C或X時，印出錯誤訊息ERROR
        print('BYTE Error')

    index_add = (len(objCode)//2) #將OPCODE整數除法並加入index_add中
    return index_add, objCode

# 處理WORD指令
def WORD(value):
    if (int(value) >= 0):#檢查 value 的值是否為非負整數。
        objCode = Dec2Hex(int(value)).zfill(6)
        #如果value是非負整數，用Dex2Hex函數轉成16進位後，用zfill確保為長度六，不夠前方會補零
    else:
        full_hex = Hex2Dec('1000000')
        #值為16進位1000000轉換為十進位的結果，即一個24位的二進位數，用於處理負數的情況
        objCode = Dec2Hex(full_hex + int(value)).zfill(6)
        # 計算出實際的數值，然後將其轉換為十六進位表示，用zfill確保為長度六，不夠前方會補零
    index_add = (len(objCode)//2)
        #計算 objCode 的長度，並將其除以2，得到 index_add 的值
    return index_add, objCode

# 處理RESB指令，返回指定的空字串
def RESB(value):#RESB 指令用於為定義的變數分配指定數量的字節空間
    objCode = ''
    #初始化一個空字串 objCode，因為 RESB 指令不需要生成目的碼。
    index_add = int(value)
    #將 value 轉換為整數，為了分配字節數量
    return index_add, objCode

# 處理RESW指令
def RESW(value):
    objCode = ''
    #初始化一個空字串 objCode，因為 RESW 指令不需要生成機器碼
    index_add = (int(value) * 3)
    #轉換為整數，並乘以 3。這是因為每個字（word）通常占據3個字節的空間
    return index_add, objCode

# 指令集和虛指令的對應表
instruction_convert = {
    "ADD": "18", "ADDF": "58", "ADDR": "90", "AND": "40", "CLEAR": "B4", "COMP": "28", "COMPF": "88", "COMPR": "A0",
    "DIV": "24", "DIVF": "64", "DIVR": "9C", "FIX": "C4", "FLOAT": "C0", "HIO": "F4",
    "J": "3C", "JEQ": "30", "JGT": "34", "JLT": "38", "JSUB": "48",
    "LDA": "00", "LDB": "68", "LDCH": "50", "LDF": "70", "LDL": "08", "LDS": "6C", "LDT": "74", "LDX": "04", "LPS": "E0",
    "MUL": "20", "MULF": "60", "MULR": "98", "NORM": "C8", "OR": "44", "RD": "D8", "RMO": "AC", "RSUB": "4C",
    "SHIFTL": "A4", "SHIFTR": "A8", "SIO": "F0", "SSK": "EC", "STA": "0C", "STB": "78", "STCH": "54", "STF": "80", "STI": "D4",
    "STL": "14", "STS": "7C", "STSW": "E8", "STT": "84", "STX": "10", "SUB": "1C", "SUBF": "5C", "SUBR": "94", "SVC": "B0",
    "TD": "E0", "TIO": "F8", "TIX": "2C", "TIXR": "B8", "WD": "DC"}

# 虛指令
pseudo_instruction = ['START', 'BYTE', 'WORD', 'RESB', 'RESW', 'END']

#初始化結構
original_input = {}  # 儲存 location 的原始輸入
function_index = {}  # 儲存 function 所在位置
object_code = {}  # 儲存 location 的 object code

# 讀取輸入檔案
with open('Input.txt', 'r', encoding='utf-8') as inp:
    input = inp.readlines()
    #用 open 函數打開 Input.txt 文件，使用 readlines 函數讀取文件中的所有行，存儲在input

    start = input[0].replace('\n', '').split(' ')
    if (start[-2] != 'START'):
        print('Error START')
        #檢查打開的文本是否start在倒數第二位，這是指令位置，-則是起始位置，此處從1000開始

    else:
        index = [Dec2Hex(Hex2Dec(start[-1]))]
        #start-1為列表最後一位，即為開始位置

        for i in input: #解析輸入並處理虛指令和匯編指令
            if (i[0] == '.'):  
                continue#處理輸入的每一行，跳過以點（.）開頭的註釋行。

            now_input = []
            now = i.replace('\n', '').split(' ')
            #用來移除字符串 i 中的換行符號，然後 split(' ') 將這個去除換行符號的字符串按照空格分割為一個列表
            
            for j in range(len(now)):
                if ((now[j] in instruction_convert) or (now[j] in pseudo_instruction)):
                    #檢查它是否是有效的組合語言指令（在 instruction_convert 中）或虛指令。                
                    
                    if (now[j] != 'START'):
                        if (now[j] == 'BYTE'):
                            index_add, objCode = BYTE(now[j+1])
                            #now[j+1] 是 BYTE 指令後面的參數，BYTE 函數的功能是根據 C 或 X 模式，
                            #將字串轉換為對應的目的碼。
                        elif (now[j] == 'WORD'):
                            index_add, objCode = WORD(now[j+1])
                            #WORD 函數根據參數的值，將其轉換為對應的機器碼。
                            #如果整數值大於等於零，直接轉換為六位十六進位數字；否則進行2補述轉換
                        elif (now[j] == 'RESB'):
                            index_add, objCode = RESB(now[j+1])
                            #RESB(now[j+1]) 將這個字節數傳遞給 RESB 函數進行處理
                            #index_add 表示 RESB 指令佔用的位置數，即保留的字節數。
                            #objCode 是 RESB 指令的機器碼，這裡為空字串。
                        elif (now[j] == 'RESW'):
                            index_add, objCode = RESW(now[j+1])
                            #index_add 表示 RESW 指令佔用的位置數，即需要保留的字的數量乘以 3
                        elif (now[j] == 'END'):
                            index_add, objCode = 0, ''
                        else:
                            #如果當前指令不是 START、BYTE、WORD、RESB、RESW 和 END，則進入 else 部分
                            index_add = 3
                            try:
                                if (',X' in now[j+1]):        
                                    objCode = f'nx,{instruction_convert[now[j]]}{now[j+1]}'
                                    """nx: 表示該指令使用了 Indexed Addressing。
                                        {instruction_convert[now[j]]}: 表示該指令的操作碼（opcode）。
                                        {now[j+1]}: 表示該指令的運算數，通常是一個記憶體位址。"""
                                else:
                                    objCode = f'n,{instruction_convert[now[j]]}{now[j+1]}'
                                    #n: 表示該指令不使用 Indexed Addressing。
                            except:
                                objCode = f'{instruction_convert[now[j]]}0000'#標識該指令沒有運算數
            #根據不同的指令類型，調用相應的處理函數（例如 BYTE、WORD、RESB、RESW）來生成機器碼。
            #將相應的信息（位置、指令、機器碼）添加到 object_code 和 original_input 字典中。

                        next_index = Dec2Hex(Hex2Dec(index[-1]) + index_add)#index[-1] 取得目前位置的十六進位表示
                    else:
                        index_add, objCode = 0, ''     #不生成任何機器碼，所以 objCode 被設為空字串
                        next_index = index[0]          #指令並不佔用記憶體空間，所以 next_index 被設為 index[0]。
                        original_input['START'] = now  #將指令的相關資訊保存在 original_input 字典中

                    if (j == 1): #確保只有在一行的第二個詞（now[1]）時才會執行這段程式碼。
                        if now[0] not in function_index:
                            #檢查目前行的第一個詞（now[0]）是否已經存在於 function_index 字典中
                            function_index[now[0]] = index[-1]
                            #如果不存在，將該標籤（label）加入 function_index 字典，並將其對應的值設為目前指令的位置 index[-1]
                            #有些指令可能會引用其他位置的標籤，建立對照表比較好處理後續指令
                        else:
                            print('Function Error, line:', index[-1])
                            #印出一條錯誤訊息，訊息包括 "Function Error, line:" 字串以及引起錯誤的行號 index[-1]

                        now_input = [now[0]] + now[1:]
                        #將 now[0] 與 now[1:] 組合成一個新的列表 now_input，
                        #確保 now_input 列表的格式統一，始終包含第一個元素（通常是指令助詞或標籤）以及其餘的元素
                    else:
                        now_input = [''] + now
                        """如果 now 中的元素不是指令助詞或標籤，則 now_input 會被設置為 [''] + now，其中第一個元素是空字符串，
                        其餘元素是 now 中的元素。這樣做可能是為了確保 now_input 中始終有一個元素"""

                    if (len(now_input) == 2):
                        now_input.append('')
                        #為了確保 now_input 列表總是包含三個元素

                    object_code[index[-1]] = objCode
                    #將資料儲存於object_code
                    original_input[index[-1]] = now_input
                    #將資料儲存於object_input
                    index.append(next_index)
                    #將下一條指令的位置添加到 index 列表的末尾。

        for i in object_code.keys():
            #object_code.keys指令的位置
            if ('n' in object_code[i]):
                #檢查物件碼（object code）中是否包含 'n'，表示相對位址。
                objCode = object_code[i].split(',')[1]
                #從物件碼中獲取 'n' 部分，即相對位址的部分。
                address = function_index[objCode[2:]]
                #使用相對位址的部分查找對應的標籤（label）在 function_index 字典中的位置
                if (len(address) < 4):
                    address = ("0"*(4 - len(address)) + address)
                    #不足四位，前面補零
                if ('nx' in object_code[i]):
                    address = (Dec2Hex(int(address[0]) + 8) + address[1:])
                    #物件碼中包含 'nx'，則將位置增加 8。這似乎是處理相對位址的一種方式。
                object_code[i] = (objCode[:2] + address)
                    #將更新後的絕對位址替換物件碼中的相對位址。
# 輸出結果(;'行號、位置、原始輸入、目的碼)
print('\n\nLine'.ljust(15) + 'Location'.ljust(15) +'Original input'.ljust(45) + 'Object code'.rjust(15))
#印出表頭，包含每列的標題，使用 ljust 和 rjust 方法來進行左右對齊。
print('------------------------------------------------------------------------------------------')

print(str(5).ljust(15) + index[0].ljust(15) +original_input['START'][0].ljust(15) +original_input['START'][1].ljust(15) +original_input['START'][2].ljust(15) +''.rjust(15))
#印出第一行的表格內容，包括行數、位置、原始輸入和目標碼

for i, location in enumerate(index[1:-1]):
    #enumerate 函式遍歷 index 列表的子列表（從第二個元素到倒數第二個元素），其中 i 是索引，location 是元素值。
    line = (i+2)*5  #計算行數，以5的倍數增加，並存儲在 line 變數中
    print(str(line).ljust(15) +
          location.ljust(15) +
          original_input[location][0].ljust(15) +
          original_input[location][1].ljust(15) +
          original_input[location][2].ljust(15) +
          object_code[location].rjust(15))
    #使用 ljust 方法進行左對齊，接著列印原始輸入和目標碼。

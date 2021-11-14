import re
identifiers = '[_a-zA-Z][_a-zA-Z0-9]*'
integers = '[0-9][0-9]*'
float_val = '\d+\.\d*'
float_val1 = '\.\d+'
octal = '[0][0-7]{1,2}'
hexadecimal = '[0][x][0-9a-fA-f]{1,2}'
operations = {'=':'assign_op', '+':'add_op', '-':'sub_op', '*':'mul_op', '/':'div_op', '%':'mod_op', '\'':'single_quotes', '"':'double_quotes', '(':'left_paranthesis',')':'right_paranthesis', ';':'delimiter','{':'left_curly','}':'right_curly', '>':"GREATER_THAN", '<':"LESS_THAN", "!":"EXCLAMATION"}
keywords = {'auto':'AUTO_CODE','const':'CONST_CODE','double':'DOUBLE_CODE','float':'FLOAT_CODE','int':"INT_CODE",'short':'SHORT_CODE','struct':'STRUCT_CODE','unsigned':'UNSIGNED_CODE','break':"BREAK_CODE",'continue':'CONTINUE_CODE','else':'ELSE_CODE','for':'FOR_CODE','long':'LONG_CODE','signed':'SIGNED_CODE','switch':'SWITCH_CODE','void':'VOID_CODE','case':'CASE_CODE','default':'DEFAULT_CODE','enum':"ENUM_CODE",'goto':'GOTO_CODE','register':'REGISTER_CODE','sizeof':'SIZEOF_CODE','typedef':'TYPEDEF_CODE','volatile':'VOLATILE_CODE','char':'CHAR_CODE','do':'DO_CODE','extern':"EXTERN_CODE",'if':'IF_CODE','return':'RETURN_CODE','static':'STATIC_CODE','union':'UNION_CODE','while':'WHILE_CODE'}
delimiter = ';'
parsed_array = []
val_temp=''
with open('front.c','r') as file:
    while True:
        new_char = file.read(1)
        if new_char=="":
            break
        token = new_char
        identifier = re.fullmatch(identifiers, new_char)
        if identifier:
            val='IDENTIFIER'
        integer = re.fullmatch(integers, new_char)
        floats = re.fullmatch(float_val, new_char)
        if integer:
            val='INTEGER'
        if new_char == ".":
            while new_char!='':
                next_char = file.read(1)
                if next_char == "":
                    break
                if next_char == " ":
                    break
                temp_char = token + next_char
                float_dot = re.fullmatch(float_val1, temp_char)
                if float_dot:
                    token = temp_char
                    val = "FLOAT" 
                if next_char in operations.keys():
                    val_temp = operations[next_char]  
                else:
                    break
        if new_char!="" and new_char in operations.keys():
            val = operations[new_char]
            parsed_array.append((new_char, val))              
        while new_char!='' and identifier: 
            next_char = file.read(1)
            if next_char == "":
                break
            if next_char == " ":
                break
            temp_char = token + next_char
            identifier = re.fullmatch(identifiers, temp_char)
            if identifier:
                token = temp_char
                val="IDENTIFIER"
            if next_char in operations.keys():
                val_temp = operations[next_char]   
        while new_char!='' and integer or floats:
            next_char = file.read(1)
            if next_char == "":
                break
            if next_char == " ":
                break
            temp_char = token + next_char
            integer = re.fullmatch(integers, temp_char)
            floats = re.fullmatch(float_val, temp_char)
            if floats:
                token = temp_char
                val = "FLOAT"
            elif integer:
                token = temp_char
                val="INTEGER"
            if next_char in operations.keys():
                val_temp = operations[next_char]
        
        if val == "IDENTIFIER" or val == "INTEGER" or val=="FLOAT" or val=="OCTAL"and token != " " and token != "\n":
            if token != " ":
                parsed_array.append((token,val))
            token=''
            val=""
        if val_temp and next_char != " " and next_char != "\n":
            parsed_array.append((next_char, val_temp))
            val_temp=''
        token=''
        val=""
        if new_char=="":
            break 
for i in range(len(parsed_array)):
    if parsed_array[i][1] == 'IDENTIFIER':
        if parsed_array[i][0] in keywords.keys():
            temp_var = list([parsed_array[i][0],keywords[parsed_array[i][0]]])
            parsed_array[i] = tuple(temp_var)
i = 0
while i < len(parsed_array):
    if parsed_array[i][0] == "=" and parsed_array[i+1][0] == "=":
        parsed_array.pop(i+1)
        parsed_array[i] = ("==", 'EQUALITY_OPERATOR')
    else:
        i +=1
i = 0
while i < len(parsed_array):
    if parsed_array[i][0] == ">" and parsed_array[i+1][0] == "=":
        parsed_array.pop(i+1)
        parsed_array[i] = (">=", 'GREAT_EQUAL')
    else:
        i +=1
i = 0
while i < len(parsed_array):
    if parsed_array[i][0] == "<" and parsed_array[i+1][0] == "=":
        parsed_array.pop(i+1)
        parsed_array[i] = ("<=", 'LESS_EQUAL')
    else:
        i +=1
i = 0
while i < len(parsed_array):
    if parsed_array[i][0] == "!" and parsed_array[i+1][0] == "=":
        parsed_array.pop(i+1)
        parsed_array[i] = ("!=", 'NOT_EQUAL')
    else:
        i +=1
for i in parsed_array:
    print(i)

############################RDA Algorithm#################################################
def lex():
    global nextToken
    val = parsed_array.pop(0)
    val = val[1]
    nextToken = val
    
def error():
    print("Error Encountered. Please check the stack trace")

def expr():
    print("Enter <expr>")
    term()
    while (nextToken == 'add_op' or nextToken == 'sub_op'):
        lex()
        term()
    print("Exit <expr>")

def term():
    print("Enter <term>")
    factor()

    while(nextToken == 'mult_op' or nextToken == 'div_op' or nextToken == 'mod_op'):
        lex()
        factor()
    print("Exit <term>")

def factor():
    print("Enter <factor>")
    if (nextToken == 'IDENTIFIER' or nextToken == 'INTEGER' or nextToken == 'FLOAT'):
        lex()

    elif nextToken == 'left_paranthesis':
        lex()
        expr()
        if nextToken == 'right_paranthesis':
            lex()
        else:
            error()
    else:
        error()
    print("Exit <factor>")

lex()
expr()
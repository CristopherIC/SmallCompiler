from myparser import Node, root

tNodes = {}
lNodes = {}

tCount = 1
lCount = 1

f = open("tac.txt","w")

def tacFile(node):
    global tCount
    global lCount
    global f

    if node.type in ["block"]:
        for child in node.childs:
            tacFile(child)
    elif node.type == "dcl":
        varType = node.childs[0].type
        f.write(varType + "dcl("+node.childs[1].type+")\n")
        tNodes[node] = node.childs[1].type
    elif node.type == "asg":
        tacFile(node.childs[0])
        tacFile(node.childs[1])
        f.write(tNodes[node.childs[0]] + " := " + tNodes[node.childs[1]] + "\n")
    elif node.type in ["intToFloat"]:
        tacFile(node.childs[0])
        f.write("t" + str(tCount) + " := " + node.type + "("+tNodes[node.childs[0]]+")"+"\n")
        tNodes[node]="t"+str(tCount)
        tCount+=3
    elif node.type in ["+","-","/","*","^"]:
        tacFile(node.childs[0])
        tacFile(node.childs[1])
        f.write("t"+str(tCount) + " := " + tNodes[node.childs[0]] + " " + node.type + " " + tNodes[node.childs[1]]+"\n")
        tNodes[node]="t"+str(tCount)
        tCount+=1 
    elif node.type in ["!=","==","<",">","<=",">="]:
        tacFile(node.childs[0])
        tacFile(node.childs[1])
        f.write("(" + tNodes[node.childs[0]] + " " + node.type + " " + tNodes[node.childs[1]] +") IFGOTO L" + str(lCount)+"\n")
        f.write("GOTO L" + str(lCount+1) + "\n")
        tNodes[node]="t" + str(tCount)
    elif node.type in ["if"]:
        tacFile(node.childs[0])
        f.write("\nL" + str(lCount)+"\n")
        saveLCount = lCount
        lCount += 2
        tacFile(node.childs[1])
        saveLCount2=lCount
        if node.type == "if":
            f.write("GOTO L" + str(lCount)+"\n")
            lNodes[node] = str(lCount)
            lCount+=1
        else:
            lNodes[node]=lNodes[node.parent]
            f.write("GOTO L"+lNodes[node.parent]+"\n")
        f.write("\nL"+str(saveLCount+1)+"\n")
        if(len(node.childs) > 2):
            tacFile(node.childs[2])
        if(len(node.childs) > 3):
            tacFile(node.childs[3])
        if node.type == "if":
            f.write("\nL" + str(saveLCount2) + "\n")
    elif not node.childs:
            tNodes[node]=node.type

#tacFile(root)
from myparser import Node, root

variables={}

class Variable:
    def __init__(self,value,token):
        self.token = token
        self.value = value

def setVariables(r):
    if(r.type == "dcl"):
        if isDeclared(r,r.childs[0].type):
            print("\033[31m" + "La variable: " + r.childs[0].type + " " + r.childs[1].type + " ya está declarada en el scope." + '\033[0m')
        scopeNode = findScopeNode(r)
        if scopeNode in variables.keys():
            variables[scopeNode].append(Variable(r.childs[0].type,r.childs[1].type))
        else:
            variables[scopeNode]=[Variable(r.childs[0].type,r.childs[1].type)]
    if r.childs:
        for child in r.childs:
            setVariables(child)

#Revisa que una declaracion sea valida para el scope actual
def isDeclared(node, varName):
    if node in variables.keys() and varName in (o.value for o in variables[node]):
        return True
    if node.type == "if":
        currentNode = node
        while((currentNode.type == "if")):
            currentNode = currentNode.parent
            if currentNode == None:
                return False
        return isDeclared(currentNode, varName)
    if node.parent:
        return isDeclared(node.parent,varName)
    else:
        return False

#Revisa en que scope se encuentra el nodo que recibe
def findScopeNode(node):
    if(node.type in ["block","if"]):
        return node
    if(node.parent):
        return findScopeNode(node.parent)
    return Node('Self')

setVariables(root)
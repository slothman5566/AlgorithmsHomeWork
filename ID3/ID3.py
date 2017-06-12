#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys,argparse,math,string
from collections import Counter
from graphviz import Digraph


class Node(object):
    def __init__(self,name):
        # name =Wind
        # children={Weak:new Node,Strong:result}
        # header_set=(Wind)
        # result=cluster number
        self.name=name
        self.children={}
        self.header_set=set([name])
        
    def append_child(self,node,key):
        node.header_set.update(self.header_set)
        self.children[key]=node

    def append_end(self,name,result):
        self.children[name]=result

class Decison_tree(object):
    def __init__(self,file):
        # header={Humidity': 2, 'Wind': 3, 'Outlook': 0, 'Play ball?': 4, 'Temperature': 1}
        # subset=High,Normal
        # result=Play ball?
        # data=[{Humidity:High,Play ball?:yes}]
        
        self.init(file)
        self.make_tree(self.root,self.data)
        
        self.dot = Digraph(comment='Decision tree',format='png')
        self.charlist = iter([str(i) for i in range(0,10000)])
        label=(next(self.charlist))
        self.dot.node(label, self.root.name,shape='rect')
        self.write(label,self.root)
        self.dot.render('ID3_img/output')
        
    def init(self,file):
        self.data=[]
        with open(file) as t:
            self.header_line=t.readline().strip("\n").split(",")
            self.header_set=set(self.header_line[:-1])
            self.result=(self.header_line[-1])
            self.header_dict=dict((self.header_line[k],k) for k in range(len(self.header_line)))
            for line in t:
                self.data.append(line.strip().split(','))

        entropy = self.cal_entropy(
            Counter(map(lambda x: x[self.header_dict[self.result]], self.data)).values()
        )
        self.subset = {}
        for key in self.header_set:
            self.subset[key] = list(set(map(lambda x: x[self.header_dict[key]], self.data)))
        
        self.root=Node(self.creat_node(self.data,self.header_set,entropy))
    
    def write(self,label,node):
        for k,v in node.children.items():
            new_label=next(self.charlist)
            if isinstance(v,str):
                self.dot.node(new_label,v)
            else:
                self.dot.node(new_label,v.name,shape='rect')
                self.write(new_label,v)
            self.dot.edge(label,new_label,k)
            
    def creat_node(self,data,header,entropy):
        header_entropy={}
        for h in header:
            result,total=0,0
            for s in self.subset[h]:
                t = Counter(map(lambda x: x[self.header_dict[self.result]], filter(lambda x: x[self.header_dict[h]] == s, data))).values()
                result+=sum(t)*self.cal_entropy(t)
                total+=sum(t)
            header_entropy[h]=entropy-result/total
        
        return max(header_entropy.keys(),key=lambda x: header_entropy[x])
    
    def cal_entropy(self,data):
        entropy=0.0
        total=float(sum(data))
        for (p) in data:
            entropy-= (p/total) * math.log((p/total),2)
        return entropy
    
    def make_tree(self,node,data):
        for k in self.subset[node.name]:
            new_data = list(filter(lambda x: x[self.header_dict[node.name]] == k, data))
            total=Counter(map(lambda x: x[self.header_dict[self.result]],new_data)).values()
            if len(total)==1:
               
                node.append_end(k,new_data[0][self.header_dict[self.result]])
            elif not new_data==[]:
                entropy=self.cal_entropy(total)
                child=Node(self.creat_node(new_data,self.header_set.difference(node.header_set),entropy))
                node.append_child(child,k)
                self.make_tree(child,new_data)
            
    def cluster(self,node,data):
        
        if (data[node.name] in node.children.keys()):
            if isinstance(node.children[data[node.name]],str):
                print (node.children[data[node.name]])
            else:
                self.cluster(node.children[data[node.name]],data)
        else:
            print ("???")
            
        
    def cluster_input(self,file):
        data=[]
        with open(file) as t:
            for line in t:
                data.append(dict(zip(self.header_line[:-1], line.strip().split(','))))
        
        for d in data:
            print(d)
            print ("{0}'s cluster result is ".format(data.index(d)))
            self.cluster(self.root,d)    
        
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--file", help="read train csv file")
	parser.add_argument("-t", "--test", help="read test csv file")
	args=parser.parse_args()
	if args.file is None:
		parser.error("please input csv file")
	tree=Decison_tree(args.file)
	if args.test is not None:
	    tree.cluster_input(args.test)
	    
    

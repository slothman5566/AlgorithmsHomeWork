#!/usr/bin/env python
# coding=utf-8
from PIL import Image
import random,sys,math,operator,argparse

def Cal_distance(a,b):
    return math.sqrt( (a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)

def cluster(center,point):
    min,mark=9999,0
    for rgb,i in center.items():
        dis=Cal_distance(rgb,point)
        if(dis<min):
            min,mark=dis,i
    return mark
    
def main(args):
    name=args.file
    k=args.k
    im = Image.open(name) #Can be many different formats.
    print (im.size)
    pix = im.load()
    width,height=im.size
    center,new_center,count={},[],[]
    for i in range(k):
        while 1:
            tmp=pix[ random.randrange(0, width),random.randrange(0, height)]
            if not tmp in center:
                center[tmp]=i
                break   
    mark_list= [[0 for x in range(height)] for y in range(width)]
    
    while True:
        print (center)
        new_center=[(0,0,0) for x in range(k)]
        count=[0 for x in range(k)] 
        for w in range(0,width):
            for h in range(0,height):
                mark_list[w][h]=cluster(center,pix[w,h])
                i=mark_list[w][h]
                new_center[i]=tuple(map(operator.add, pix[w,h], new_center[i]))
                count[i]+=1
        for i in range(k):
            new_center[i]=tuple([x/(count[i]+1) for x in new_center[i]])
        print (new_center)
        n = {k: center[k] for k in new_center if k in center}
        if(len(n)==len(center)):break
        center=dict((new_center[i],i) for i in range(k))

    center = dict((v,k) for k,v in center.items())
    print (center)
    for w in range(0,width):
        for h in range(0,height):
            pix[w,h]=(center[mark_list[w][h]])
    im.save("output.png") # Save the modified pixels as png
    
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-k",type=int,help="cluster number")
	parser.add_argument("-f", "--file", help="input image file")
	args=parser.parse_args()
	print (args)
	if (args.file and args.k) is not None:
		main(args)
	else:
	    parser.error("please input image file and cluster number")
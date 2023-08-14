import cv2
import segaut as sa
import numpy as np

class Converter:
    
    def __init__(self,defaut_path = "./segaut_output/",tool = None):
        self.sat = tool if tool else sa.Tool(defaut_path)
        self.dst = defaut_path

    def find(self,img):
        contours,hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        return cnt
        
    def seg_trans_det(self,area):
        return [area[3] + area[1]/2,area[2] + area[0]/2,area[1],area[0]]


    def get_txt(self,cate,pos,h=100,w=100):
        '''
        将轮廓的坐标值保存为新标签的txt文件
        '''
        poss = cate + " "
        for i in pos :
            for y in i:
                new = self.sat.process_list_in_two(y,
                    lambda x: str(round(x/w,6)),
                    lambda x: str(round(x/h,6))
                )
                poss += " ".join(new) + " "
        poss = poss[:-1]
        return poss
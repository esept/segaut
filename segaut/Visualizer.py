import cv2
import segaut as sa
import numpy as np

WHITE = (255,255,255)
GREEN = (0,255,0)
YELLOW = (0,255,255)
RED = (0,0,255)
BLUE = (255,0,0)
GOLD = (0,215,255)

class Visualizer:
    def __init__(self,dest_path,sat = None):
        print("I'm watching ..")
        self.dst = dest_path
        self.sat = sat if sat else sa.Tool(defaut_path)
        self.saa = sa.Augmentor(self.dst,self.sat)

    def __vis_seg_label(self,label,image_path):
        seglabel = label.split(" ")[1:]
        src_img = cv2.imread(image_path)
        _w,_h = src_img.shape[:2]
        points_pos = self.sat.process_list_in_two(seglabel,
            lambda x : int(float(x) * _w), 
            lambda x : int(float(x) * _h), 
            lambda x1,x2 : [x1,x2]
        )
        cv2.polylines(src_img,np.int32([points_pos]),True,(0,0,255))
        return src_img


    def __vis_det_label(self,label,image_path):
        det_label = label.split(" ")[1:]
        detlabel = [float(i) for i in det_label]
        src_img = cv2.imread(image_path)
        _w,_h = src_img.shape[:2]
        centre_w = detlabel[0]
        centre_h = detlabel[1]
        hlength_w = detlabel[2]/2
        hlength_h = detlabel[3]/2
        max_w_r = (centre_w + hlength_w)* _w
        max_h_r = (centre_h + hlength_h)* _h
        min_w_r = (centre_w - hlength_w)* _w
        min_h_r = (centre_h - hlength_h)* _h
        cv2.rectangle(src_img,(int(min_w_r),int(min_h_r)),(int(max_w_r),int(max_h_r)),(0,255,255),3)
        return src_img



    
    def show_label(self,labels_path,img_path,Task = "seg"):
        this_dst = self.dst + "show_label_" + Task + "/"
        self.sat.verify_folder(this_dst)
        labels = self.sat.catch_ext_file(labels_path, "txt")
        length = len(labels)
        pp = self.sat.create_pgbar(length)
        for i in labels:
            this_label = self.sat.read_file(i)
            name = i.split("/")[-1].split(".")[0]
            image_name = img_path + name + ".jpg"
            if Task == "seg":
                fin_img = self.__vis_seg_label(this_label[0],image_name)
            else :
                fin_img = self.__vis_det_label(this_label[0],image_name)
            # elif Task == "point":
            #     fin_img = self.__draw_points(this_label[0],image_name)
            info = self.saa.save_img(fin_img, "show_label_" + name , this_dst)
            self.sat.show_pgbar(pp,f"{info:72}")
    
    def __draw_points(self,image_path,label):
        seglabel = label.split(" ")[1:]
        src_img = cv2.imread(image_path)
        _w,_h = src_img.shape[:2]
        pos = self.sat.process_list_in_two(seglabel,
            lambda x : int(float(x) * _w), 
            lambda x : int(float(x) * _h), 
            lambda x1,x2 : [x1,x2]
        )
        for p in pos :
            point = (p[0],p[1])
            cv2.circle(src_img,point,1,GREEN,4)
        return src_img


    


        

import os
import segaut as sa

class Saline:
    '''
    class saline use as pipeline
    
    '''
    def __init__(self,defaut_path = "./segaut_output/"):
        self.dst = defaut_path
        self.sat = sa.Tool(self.dst)
        self.sat.verify_folder(self.dst)
        self.sad = sa.Dataset(self.dst,self.sat)
        self.sac = sa.Converter(self.dst,self.sat)
        self.saa = sa.Augmentor(self.dst,self.sat,self.sac)
        self.sav = sa.Visualizer(self.dst,self.sat)
    
    def clean_output(self):
        dirs = os.listdir(self.dst)
        print(dirs)
        for i in dirs :
            folder = os.path.join(self.dst,i) + "/"
            if os.path.isdir(folder):
                self.sat.verify_folder(folder)

    def load_dataset(self,path):
        self.sad.load_json(path)
        self.sat.copy_file_by_name("./segaut_output/yolo_label/","./dataset_coco/JPEGImages/","txt","jpg")

    def cut_labeled(self,img_path = None,label_path = None):
        img_path = self.dst+"images/" if not img_path else img_path
        label_path = self.dst + "yolo_label/" if not label_path else label_path
        self.saa.cut(img_path,label_path)

    def merge_cut_to_new(self,new_imgs,cutted_img = None,nbs = 10):
        cutted_img = self.dst + "cutted/" if not cutted_img else cutted_img
        self.saa.merge(cutted_img,new_imgs,nbs)

    def run(self,dataset_path,new_img_path):
        self.clean_output()
        self.load_dataset(dataset_path)
        self.cut_labeled()
        self.merge_cut_to_new(new_img_path)

    def see(self,label_path = None,img_path = None,task = "seg"):
        label_path = self.dst + "merged_" + task + "/" if not label_path else label_path
        img_path = self.dst + "merged_imgs/" if not img_path else img_path
        self.sav.show_label(label_path,img_path,task)






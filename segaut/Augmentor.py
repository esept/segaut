import os
import cv2
import segaut as sa
import numpy as np


class Augmentor:
    '''
    data augment class
    '''
    def __init__(self,defaut_path = "./segaut_output/",tool = None,sac = None):
        self.dest = defaut_path
        self.sat = tool if tool else sa.Tool(self.dest)
        self.sac = sac if sac else sa.Converter(self.dest,self.sat)
        # self.sac = sa.Converter(defaut_path,self.sat)

    def save_img(self,img,name,path = "output_img/",ext=".jpg"):
        '''save image with path,name,extension,return path + name + ext'''
        # print(path,name)
        if path == "output_img/":
            info = self.dest + path + name + ext + " " + str(img.shape) + "\t"
            cv2.imwrite(self.dest + path + name + ext, img)
        else:
            info = path + name + ext + " " + str(img.shape)
            cv2.imwrite(path + name + ext, img)
        return info 

    def get_min_max_w_h(self,mylist):
        max_h = -1
        max_w = -1
        min_h = 10e5
        min_w = 10e5
        for i in mylist:
            num1 = i[0]
            num2 = i[1]
            if num1 > max_w :
                max_w = num1
            if num1 < min_w :
                min_w = num1
            if num2 > max_h :
                max_h = num2
            if num2 < min_h:
                min_h = num2
        return [min_h,max_h,min_w,max_w]

    def create_mask_with_shape(self,shape):
        '''
        create a black image with shape 
        '''
        return np.zeros(shape,np.uint8)

    def noir_2_transparent(self,src):
        '''
        将切割出黑色背景图片的黑色背景变为透明
        '''
        tmp = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
        _,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
        b,g,r = cv2.split(src)
        rgba = [b,g,r,alpha]
        # rgba = [b,g,r,alpha]
        res = cv2.merge(rgba,4)
        return res


    def __cut_with_label(self,img,label):
        '''
        cut a area in img by label
        '''
        w,h,c = img.shape
        pos = label.split(" ")[1:]
        point_pos = self.sat.process_list_in_two(pos,
            lambda x : np.int32(float(x) * w),
            lambda x : np.int32(float(x) * w),
            lambda x1,x2: [x1,x2]
        )
        al = self.get_min_max_w_h(point_pos)
        area_str = [str(i) for i in al]
        mask = self.create_mask_with_shape((w,h,c))
        cv2.polylines(mask,np.int32([point_pos]),True,(0,0,0))
        cv2.fillPoly(mask,np.int32([point_pos]),(255,255,255))
        # print(mask.shape,img.shape)
        dst = cv2.bitwise_and(img,mask)
        area_cut = dst[al[0]:al[1],al[2]:al[3]]
        return area_cut,area_str


    def cut(self,img_path,label_path):
        '''
        main function for cut 
        '''
        this_dst = self.dest + "cutted/"
        self.sat.verify_folder(this_dst)
        img_file = self.sat.catch_ext_file(img_path,"jpg")
        pbar = self.sat.create_pgbar(len(img_file))
        for i in img_file:
            img = cv2.imread(i)
            name = i.split("/")[-1].split(".")[0]
            # print("cutting " + name)
            w,h = img.shape[:2]
            labels = self.sat.read_file(label_path + name + ".txt")
            self.sat.show_pgbar(pbar,f"{label_path+name:32}")
            for j in labels:
                cate = j.split(" ")[0]
                res,area = self.__cut_with_label(img,j)
                fin = self.noir_2_transparent(res)
                self.save_img(fin,cate + "_" + name +"_"+ "_".join(area),this_dst,".png")
            #     break
            # break

    def get_binary_img(self,img,max_v=255):
        '''
        img : 图像
        max_v : 高阈值
        获取二值图
        '''
        tmp_mask = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        _,dst = cv2.threshold(tmp_mask,0,max_v,cv2.THRESH_BINARY)
        return dst

    def __merge_real_pic(self,obj,src_paste):
        obj_w,obj_h = obj.shape[:2]
        mask = np.ones((obj_w,obj_h),np.uint8)
        obj_b = self.get_binary_img(obj)
        mask2 = cv2.bitwise_not(obj_b,obj_b,mask=mask)
        mask4 = cv2.bitwise_and(src_paste,src_paste,mask=mask2)
        mask7 = cv2.add(obj,mask4)
        return mask7

    # def get_txt(self,cate,pos,h=100,w=100):
    #     '''
    #     将轮廓的坐标值保存为新标签的txt文件
    #     '''
    #     poss = cate + " "
    #     for i in pos :
    #         for y in i:
    #             new = self.sat.process_list_in_two(y,
    #                 lambda x: str(round(x/w,6)),
    #                 lambda x: str(round(x/h,6))
    #             )
    #             poss += " ".join(new) + " "
    #     poss = poss[:-1]
    #     return poss

    # def find(self,img):
    #     contours,hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #     cnt = contours[0]
    #     return cnt


    def __merge_bin_nor(self,obj,src):
        src_w,src_h = src.shape[:2]
        obj_w,obj_h = obj.shape[:2]
        rand_pos_h = self.sat.get_random_int(0,src_h)
        rand_pos_w = self.sat.get_random_int(0,src_w)
        src_b = self.get_binary_img(src,0)
        obj_b = self.get_binary_img(obj,255)
        if rand_pos_w + obj_w > src_w :
            rand_pos_w = src_w - obj_w
        if rand_pos_h + obj_h > src_h:
            rand_pos_h = src_h - obj_h
        src_paste = src[rand_pos_w:rand_pos_w + obj_w,rand_pos_h:rand_pos_h + obj_h]
        src_b_paste = src_b[rand_pos_w:rand_pos_w + obj_w,rand_pos_h:(rand_pos_h + obj_h)]
        src_b[rand_pos_w:rand_pos_w + obj_w,rand_pos_h:rand_pos_h + obj_h] = cv2.add(obj_b,src_b_paste)
        merged_area = self.__merge_real_pic(obj,src_paste)
        det_area = [obj_w,obj_h,rand_pos_w,rand_pos_h]
        src[rand_pos_w:rand_pos_w + obj_w,rand_pos_h:rand_pos_h + obj_h] = merged_area
        return [src_b,src,det_area]

    # def seg_trans_det(self,area):
    #     return [area[3] + area[1]/2,area[2] + area[0]/2,area[1],area[0]]


    def __preprocess_merge(self,obj_img,src_img):
        obj = cv2.imread(obj_img,cv2.IMREAD_UNCHANGED)
        src = cv2.imread(src_img)
        src = cv2.cvtColor(src,cv2.COLOR_BGR2BGRA)
        cate = obj_img.split("/")[-1].split("_")[0]
        src_w,src_h = src.shape[:2]
        merged = self.__merge_bin_nor(obj,src)
        pos = self.sac.find(merged[0])
        label_pos = self.sac.get_txt(cate,pos,src_w,src_h)
        det_pos = self.sac.seg_trans_det(merged[2])
        det_pos_r = self.sat.process_list_in_two(det_pos,
            lambda x: x/src_w,
            lambda x: x/src_h
        )
        det_pos_r.insert(0,str(cate))
        det = " ".join([str(i) for i in det_pos_r])
        return [merged[1],label_pos,det]


    def merge(self,cutted_path,paste_path,nbs = 100):
        this_dst = os.path.join(self.dest,"merged_")
        cclist = self.sat.catch_ext_file(cutted_path,"png")
        pplist = self.sat.catch_ext_file(paste_path,"jpg")
        self.sat.verify_folder(this_dst)
        self.sat.verify_folder(this_dst + "seg/")
        self.sat.verify_folder(this_dst + "det/")
        self.sat.verify_folder(this_dst+"imgs/")
        pp = self.sat.create_pgbar(nbs)
        for nb in range(nbs):
            random_cut = self.sat.get_random_int(0,len(cclist) - 1)
            random_paste = self.sat.get_random_int(0,len(pplist) - 1)
            merged = self.__preprocess_merge(cclist[random_cut],pplist[random_paste])
            nums = [random_cut,random_paste,nb]
            nums = [str(i) for i in nums]
            self.save_img(merged[0], "merged_"+"_".join(nums), this_dst+"imgs/")
            info = self.sat.write_file(this_dst + "seg/"+ "merged_" + "_".join(nums) + ".txt",merged[1])
            self.sat.write_file(this_dst + "det/"+ "merged_" + "_".join(nums) + ".txt",merged[2])
            self.sat.show_pgbar(pp,info)
            # break





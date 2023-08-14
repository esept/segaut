import streamlit as st
import segaut as sa
import os

class Stviz(sa.Augmentor):
    def __init__(self):
        self.sa = sa.Saline(stviz = self)

    def sidebar(self):
        sd = st.sidebar
        sd.title("Segaut's parameters")
        mode = sd.radio("select your mode,",["all","step"])
        json_path = sd.text_input("json file path",value="./dataset_coco/test.json")
        ori_img_path = sd.text_input("original image path",value="./dataset_coco/JPEGImages/")
        new_img_path = sd.text_input("background image path",value="./tt/test_i/")
        nbs = sd.slider("Nbs of new Image",10,300,100)
        show_seg = sd.checkbox("show seg image label")
        show_det = sd.checkbox("show det image label")
        return [mode,json_path,ori_img_path,new_img_path,show_seg,show_det]

    def run_saline_all(self,start,infos):
        if start:
            text = self.sa.run(*infos[:3])
            st.markdown("## "+text)
            if infos[3]:
                self.sa.see(task = "seg")
            if infos[4]:
                self.sa.see(task = "det")


    def run_saline_step(self, start, infos):
        if start:
            self.sa.sad.load_json(infos[0],"./segaut_output/yolo_label/")
            self.sa.sat.copy_file_by_name("./segaut_output/yolo_label/",infos[1],"txt","jpg")
            self.sa.cut_labeled()
            cutted_img = self.sa.dst + "cutted/"
            self.merge(cutted_img,infos[2],10)

    # def click_button(self):
    #     st.session_state.clicked = True


    def run_saline(self):
        infos = self.sidebar()
        st.title("Segaut Web")
        start = st.button("Run segaut")
        if infos[0] == "all":
            self.run_saline_all(start,infos[1:])
        else:
            self.run_saline_step(start,infos[1:])
        st.markdown("A tool for image segmentation and detection")
        st.markdown("Created by Hsu")

    @overwrite
    def merge(self,cutted_path,paste_path,nbs = 100):
        this_dst = os.path.join(self.sa.dst,"merged_")
        cclist = self.sa.sat.catch_ext_file(cutted_path,"png")
        pplist = self.sa.sat.catch_ext_file(paste_path,"jpg")
        self.sa.sat.verify_folder(this_dst)
        self.sa.sat.verify_folder(this_dst + "seg/")
        self.sa.sat.verify_folder(this_dst + "det/")
        self.sa.sat.verify_folder(this_dst+"imgs/")
        nb = 0
        while nb < nbs:
            random_cut = self.sa.sat.get_random_int(0,len(cclist) - 1)
            random_paste = self.sa.sat.get_random_int(0,len(pplist) - 1)
            merged = self.sa.saa.preprocess_merge(cclist[random_cut],pplist[random_paste])
            nums = [random_cut,random_paste,nb]
            nums = [str(i) for i in nums]
            # save_button = st.button("Save")
            # next_button = st.button("Next")
            col1,col2 = st.columns(2)
            nb += 1
            with col1:
                st.image(merged[0], channels="BGR")
            with col2:
                if st.button("Save",key = "save image" + str(nb)) :
                    self.sa.saa.save_img(merged[0], "merged_"+"_".join(nums), this_dst+"imgs/")
                    self.sa.sat.write_file(this_dst + "seg/"+ "merged_" + "_".join(nums) + ".txt",merged[1])
                    self.sa.sat.write_file(this_dst + "det/"+ "merged_" + "_".join(nums) + ".txt",merged[2])
                if st.button("Next",key = "Dont save image" + str(nb)) :
                    # nb += 1
                    pass

    def create_st_pbar(self,text):
        stbar = st.progress(0,text)
        return stbar

    def update_st_pbar(self,pbar,text,progress):
        pbar.progress(progress,text = text)


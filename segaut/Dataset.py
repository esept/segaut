# from .Tool import *
# from .Visualizer import *
import segaut as sa
import os
class Dataset:
    def __init__(self,dest_path = "./segaut_output/",tool = None):
        print("read origine label")
        self.sat = tool if tool else sa.Tool(defaut_path)
        self.dest = dest_path
        self.sat.verify_folder(dest_path)
        self.sav = sa.Visualizer(self.dest,self.sat)

    def write_categories(self,cates):
        nc = len(cates)
        infos = ""
        infos += "# Replace by datasets' path \n\n\n# Classes \n"
        infos += "nc: " + str(nc) + "  # number of classes \n"
        infos += "names:  # class names\n"
        for i in cates:
            thisid = i["id"]
            thisname = i["name"]
            infos += "\t" +str(thisid) +": " + thisname + "\n"
        self.sat.write_file(self.dest + "this_data.yaml",infos)

    def search_img_info(self,infos,this_id):
        for i in infos:
            if i["id"] == this_id:
                return i

    def load_json(self,json_path,store_folder = "yolo_label/"):
        this_dest = os.path.join(self.dest + store_folder)
        print(this_dest)
        self.sat.verify_folder(this_dest)
        data = self.sat.read_file(json_path)
        seg_info = data["annotations"]
        img_info = data["images"]
        cate_info = data["categories"]
        self.write_categories(cate_info)
        pbar = self.sat.create_pgbar(len(seg_info))
        for i in seg_info:
            seg = i["segmentation"][0]
            seg_img_id = i["image_id"]
            cate = i["category_id"]
            this_img_info = self.search_img_info(img_info,seg_img_id)
            new_seg = self.sat.process_list_in_two(seg,
                lambda x:str(int(x)/int(this_img_info["width"])),
                lambda x:str(int(x)/int(this_img_info["height"])),
            )
            txt_name = this_img_info["file_name"].split(".")[0]
            content = str(cate) + " " + " ".join(new_seg)
            info = self.sat.write_file(this_dest + txt_name + ".txt",content,"a+")
            self.sat.show_pgbar(pbar,f"{info:30}")



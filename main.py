import segaut as sa

if __name__ == "__main__":
    sas = sa.Saline()
    sas.run("./dataset_coco/test.json","./dataset/pv_0/images/train/")
    sas.see()
    sas.see(task="det")
    # sas.sat.copy_content("./segaut/")

# if __name__ == "__main__":
#     dest_path = "./segaut_output/"
#     sat = sa.Tool(dest_path)
#     sad = sa.Dataset(dest_path,sat)
#     saa = sa.Augmentor(dest_path,sat)
#     sat.copy_file_by_name("./segaut_output/yolo_label/","./dataset_coco/JPEGImages/","txt","jpg")
#     sad.load_json("./dataset_coco/test.json")
#     saa.cut(dest_path + "images/",dest_path + "yolo_label/")
#     saa.merge(dest_path + "cutted/","./dataset/pv_0/images/train/",10)

#     sav = sa.Visualizer(dest_path,sat)
#     sav.show_label(dest_path + "merged/det/",dest_path + "merged/imgs/","det")
#     sav.show_label("./dataset/pv_45/labels/val/","./dataset/pv_45/images/val/","det")
#     sat.copy_content("./segaut/")

import os
import glob
import json
import shutil 
import random 
import segaut as sa
from tqdm.auto import tqdm

'''
工具类
'''

class Tool:
    def __init__(self,dest_path):
        self.__author = "hsu"
        self.dest = dest_path
        print("This is " + self.__author)

    def catch_ext_file(self,path,ext):
        # print(path,ext)
        return glob.glob(path + "*." + ext)

    def __remove_ele(self,folder_path):
        '''
        folder_path: path to folder
        remove everything in the folder
        '''
        for file in glob.glob(folder_path+"*.*"):
            os.remove(file)

    def __test_dir_exist(self,path):
        '''
        folder_path: path to folder
        verify if the folder exist, if not, create it 
        '''
        if not os.path.exists(path):
            os.makedirs(path)
            return "create"
        else:
            return "exist"

    def verify_folder(self,folder_path):
        '''
        verify if the folder exist and is empty
        '''
        print(self.__test_dir_exist(folder_path) + ": " + folder_path)
        self.__remove_ele(folder_path)

    def get_random_int(self,vmin,vmax):
        '''
        get a random integer value from vmin to vmax 
        '''
        # print(vmin,vmax)
        return random.randint(vmin,vmax)

    def write_file(self,file_name,content,mode = "w"):
        '''
        write content in file
        '''
        with open(file_name,mode) as f :
            f.writelines(content)
        return file_name

    def read_file(self,file_name):
        '''
        read file's content
        '''
        ext = file_name.split(".")[-1]
        with open(file_name,"r") as f:
            if ext == "json":
                content = json.load(f)
            else:
                content = f.readlines()
        return content

    def copyto_files(self,ori_path,dest_path,ext):
        '''
        copy everything in ori_path end with ext and paste to dest_path
        '''
        self.__test_dir_exist(dest_path)
        self.__remove_ele(dest_path)
        num = 0
        for i in glob.glob(path + "*." + ext):
            num += 1
            name = i.split(".")
            print(name)
            shutil.copy(ori_path + name + "." + ext,dest_path)
        print("COPY_TO_FILES DONE " + str(num))


    def copy_file_by_name(self,ori_path,src_path,ori_ext,dst_ext,stviz = None):
        '''
        copy everything in ori_path end with ext and paste to dest_path
        '''
        this_dest = self.dest + "images/"
        self.verify_folder(this_dest)
        num = 0
        llist = glob.glob(ori_path + "*." + ori_ext)
        total_length = len(llist)
        pbar = self.create_pgbar(len(llist))
        if stviz :
            stbar = stviz.create_st_pbar("Move Image")
        for i in range(total_length):
            name = llist[i].split("/")[-1].split(".")[0]
            self.show_pgbar(pbar,f"{name:30}")
            shutil.copy(src_path + name + "." + dst_ext,this_dest)
            if stviz :
                stviz.update_st_pbar(stbar,name,i/total_length)
        info = "COPY_TO_FILES DONE " + str(total_length)
        print(info)
        if stviz:
            stviz.update_st_pbar(stbar,info,(i+1)/total_length,"red")




    def process_list_in_two(self,ori_list,add_op_1,add_op_2,add_op_3 = None):
        '''
        return [add_op_3(add_op_1(ori_list[0]),add_op_2(ori_list[1])),...]
        for ori_list, process 2 obj together, use add_op_1 in first obj, add_op_2 in second obj,and add_op_3 for both obj
        for add_op_*, use lambda as parameter
        '''
        new_list = []
        for i in range(0,len(ori_list),2):
            val1 = add_op_1(ori_list[i])
            val2 = add_op_2(ori_list[i + 1])
            if add_op_3 == None :
                new_list.append(val1)
                new_list.append(val2)
            else :
                new_list.append(add_op_3(val1,val2))
        return new_list

    def copy_content(self,path):
        content = []
        for i in glob.glob(path + "*.py"):
            with open(i,"r") as f:
                content.append(f.readlines())
        with open("content.py","w")as w:
            for i in content:
                w.writelines(i)
        


    '''
    添加进度条
    '''
    def create_pgbar(self,length):
        pbar = tqdm(total = length)
        return pbar

    def show_pgbar(self,pgbar,info,up_ = 1):
        pgbar.set_description(info)
        pgbar.update(up_)


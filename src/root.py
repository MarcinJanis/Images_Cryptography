import tkinter as tk
from tkinter import messagebox, PhotoImage, filedialog
from PIL import Image, ImageTk
import os 
import img_analyse as ia
import cv2
import shares
import cryptoXor

# Closes project
def close_project():
    root.destroy()  

# Import photo
def import_img():
    file_path = tk.filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    img_tmp = cv2.imread(file_path)
    full_file_name = os.path.basename(file_path)
    fileName, fileType = os.path.splitext(full_file_name)
    imgStorTmp = ia.ImageStorage(img_tmp, fileName, fileType)
    if imgStorTmp:
        print(f"{fileName} file imported succesfully!")
    ImgListbox.insert(tk.END, imgStorTmp.name)
    addPreview(img_tmp, fileName, 'In')

# InImgsCntr = 0 
# InImgsStorage = []
# OutImgCntr = 0
# OutImgsStorage = []
    
def addPreview(I, name, InOut):
    global InImgsStorage, OutImgsStorage, InImgsCntr, OutImgsCntr
    ImgWidth = 120
    
    yS = I.shape[0]
    xS = I.shape[1]
    NewHeight = int( yS * ImgWidth / xS)
    I = cv2.resize(I, (ImgWidth,NewHeight))
    I = cv2.cvtColor(I, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(I)
    tk_img = ImageTk.PhotoImage(pil_img)
    tmp = tk.Label(root, image=tk_img)
    tmp.image = tk_img
    if InOut == 'In':
        tmp.place(x=30 + (ImgWidth + 30)*(InImgsCntr % 4), y= 350, width=ImgWidth, height=NewHeight)
        InImgsCntr += 1
        InImgsStorage.append((name, tmp))
    elif InOut == 'Out':
        tmp.place(x=630 + (ImgWidth + 30)*(OutImgsCntr % 4), y= 350, width=ImgWidth, height=NewHeight)
        OutImgsCntr += 1
        OutImgsStorage.append((name, tmp))

def delPreview(name):
    global InImgsStorage, OutImgsStorage, InImgsCntr, OutImgsCntr
    for imgName , obj in InImgsStorage:
        if imgName == name:
            obj.destroy()
            InImgsStorage.remove((imgName, obj))
            InImgsCntr -= 1
            break
    for imgName , obj in OutImgsStorage:
        if imgName == name:
            obj.destroy()
            OutImgsStorage.remove((imgName, obj))
            OutImgsCntr -= 1
            break
        
def addFrameSelect(event):
    global InImgsStorage, OutImgsStorage
    select_idx = ImgListbox.curselection()
    SelectedNames = [ImgListbox.get(i) for i in select_idx]
    # for i in range(len(select_idx)):
    #     selectedName = ImgListbox.get(select_idx[i])
    for name, obj in InImgsStorage:
        if name in SelectedNames:
            obj.config(borderwidth=2, relief=tk.SOLID)
        else: 
            obj.config(borderwidth=0, relief=tk.FLAT)

    for name, obj in OutImgsStorage:
        if name in SelectedNames:
            obj.config(borderwidth=2, relief=tk.SOLID)
        else: 
            obj.config(borderwidth=0, relief=tk.FLAT)

def delete_img():
    selected_index = ImgListbox.curselection()
    if selected_index:
        selected_name = ImgListbox.get(selected_index)
        for instance in ia.ImageStorage.instances:
            if instance.name == selected_name:
                print(f'deleting: {instance.name}...')
                ImgListbox.delete(selected_index)
                instance.delete()
                delPreview(instance.name)
                print('deleted')
    else:
        messagebox.showinfo("Warning", "No image selected.")

def disp_img():
    selected_index = ImgListbox.curselection()
    if selected_index:
        selected_name = ImgListbox.get(selected_index)
        for instance in ia.ImageStorage.instances:
            if instance.name == selected_name:
                cv2.imshow(instance.name, instance.img)
    else:
        messagebox.showinfo("Warning", "Please, select image.")

def compare_img():
    if ImgListbox.size() == 2:
        selected_name = [ImgListbox.get(0), ImgListbox.get(1)]
        imgs = []
        for instance in ia.ImageStorage.instances:
            if instance.name in selected_name:
                imgs.append(cv2.cvtColor(instance.img,cv2.COLOR_BGR2GRAY))
        cv2.imshow('Comparision', cv2.absdiff(imgs[0],imgs[1]))

    else:
        messagebox.showinfo("Warning", "Only 2 images shall be imported to compare each others.")

def encrypt_img():
    algo_index = AlgoListbox.curselection()
    if len(algo_index) == 1:
        algo_name = AlgoListbox.get(algo_index)
        if (algo_name == '1. Shares'):
            print(f'Choosen algo: {algo_name}')
            if(len(ImgListbox.curselection()) == 1): #if one is selected
                print(f'Imported images: {ImgListbox.size()} - ok')
                #get photo 
                InputImgName = ImgListbox.get(ImgListbox.curselection())
                for instance in ia.ImageStorage.instances:
                    if instance.name == InputImgName:
                        InputImage = instance.img # cointinue here
                        break
                #call funtion
                n = int(param1_input.get())
                if n % 2 != 0: 
                    messagebox.showinfo("Warning", "n parameter is not even number!\nNon symetrical encryption may cause image distortion.")
                InputImage = cv2.cvtColor(InputImage, cv2.COLOR_BGR2GRAY)
                Result = shares.encrypt_shares(InputImage,n)
                if(len(Result) == n):
                    messagebox.showinfo("Complted!", "Algorytm complete ecryption correctly!")
                    file_path = filedialog.askdirectory(title="Save as")
                    InName, InExtension = os.path.splitext(InputImgName)
                    for i in range(n):
                        #cv2.imwrite(InName+f'_s{i+1}.png',Result[i])
                        cv2.imwrite(os.path.join(file_path, InName+f'_s{i+1}.png'), Result[i])
                        imgStorTmp = ia.ImageStorage(Result[i], InName+f'_s{i+1}', '.png')
                        ImgListbox.insert(tk.END, imgStorTmp.name)
                        addPreview(Result[i], InName+f'_s{i+1}', 'Out')
                    messagebox.showinfo("Complted!", f"Saved {n} ecrypted images!")
            else:
                messagebox.showinfo("Warning", "Select one photo!")
        elif (algo_name == '2. Xor'):
            #print(f'Choosen algo: {algo_name}')
            if(len(ImgListbox.curselection()) == 2): #if two images are selected
                #print(f'Imported images: {ImgListbox.size()} - ok')
                #get photo 
                InputImgNames = [ImgListbox.get(i) for i in ImgListbox.curselection()]
                #InputImgName = [ImgListbox.get(0),ImgListbox.get(1)]
                #print(InputImgName)
                InputImage = []
                for instance in ia.ImageStorage.instances:
                    if instance.name in InputImgNames:
                        InputImage.append(instance.img)
                    #print(len(InputImage))
                for i in range(2):
                    tmp = cv2.cvtColor(InputImage[i], cv2.COLOR_BGR2GRAY)
                    _, tmp = cv2.threshold(InputImage[i],120 ,255 , cv2.THRESH_BINARY)
                    (tmp, 120, 255, cv2.THRESH_BINARY)
                    InputImage[i] = tmp
                if len(InputImage)==2:
                    Result = cryptoXor.xor(InputImage[0],InputImage[1])
                else:
                    messagebox.showinfo("Error!", "Img doesn't exist!")
                if Result is not None:
                    messagebox.showinfo("Complted!", "Algorytm complete ecryption correctly!")
                    file_path = filedialog.askdirectory(title="Save as")
                    InName = InputImgNames[0]
                    # cv2.imshow('xD', Result)
                    # cv2.waitKey(1)
                    cv2.imwrite(os.path.join(file_path, InName+'_xor.png'), Result)
                    imgStorTmp = ia.ImageStorage(Result, InName+'_xor', '.png')
                    ImgListbox.insert(tk.END, imgStorTmp.name)
                    addPreview(Result, InName+'_xor', 'Out')
                    #cv2.imwrite(InName+'_xor.png',Result)

                    messagebox.showinfo("Complted!", f"Saved ecrypted images!")
            else:
                messagebox.showinfo("Warning", "Select two images!")
    else:
        messagebox.showinfo("Warning", "Select only one algorythm!")

#InputImgNames = [ImgListbox.get(i) for i in ImgListbox.curselection()]

def decrypt_img():
    algo_index = AlgoListbox.curselection()
    if len(algo_index) == 1:
        algo_name = AlgoListbox.get(algo_index)
        if (algo_name == '1. Shares'):
            #print(f'Choosen algo: {algo_name}')
            n = int(param1_input.get()) #get arguments
            if(len(ImgListbox.curselection()) == n): #if n imgs are selected
                #print(f'Imported images: {ImgListbox.size()} - ok')  
                #InputImgs = []
                tmpImgNames = [ImgListbox.get(i) for i in ImgListbox.curselection()]
                #for i in range(n):
                    #tempImg = ia.ImageStorage.instances[i].img
                    # print(tempImg.shape)
                    #InputImgs.append(cv2.cvtColor(tempImg, cv2.COLOR_BGR2GRAY))
                InputImgs = [obj.img for obj in ia.ImageStorage.instances if obj.name in tmpImgNames]
                InName = tmpImgNames[0]
                Result = shares.decrypt_shares(InputImgs,n)
                if Result is not None:
                    messagebox.showinfo("Complted!", "Algorytm complete ecryption correctly!")
                    file_path = filedialog.askdirectory(title="Save as")
                    #InName = ia.ImageStorage.instances[0].name
                    cv2.imwrite(os.path.join(file_path, InName+'_decrypted_shares.png'), Result)
                    imgStorTmp = ia.ImageStorage(Result, InName+'.png', '.png')
                    ImgListbox.insert(tk.END, imgStorTmp.name)
                    addPreview(Result, InName+'_decrypted_shares', 'Out')
                    #messagebox.showinfo("Complted!", f"Image saved")
                else:
                    print('Error: decryption algorythm failed.')
            else:     
                messagebox.showinfo("Warning", f"Select {n} images!")
        elif (algo_name == '2. Xor'):
            if(len(ImgListbox.curselection()) == 2): #if 2 imgs are selected

                tmpImgNames = [ImgListbox.get(i) for i in ImgListbox.curselection()]
                InputImgs = [obj.img for obj in ia.ImageStorage.instances if obj.name in tmpImgNames]
                InName = tmpImgNames[0]
                for i in range(2):
                    tmp = cv2.cvtColor(InputImgs[i], cv2.COLOR_BGR2GRAY)
                    _, tmp = cv2.threshold(tmp,120 ,255 , cv2.THRESH_BINARY)
                    InputImgs[i] = tmp
    
                Result = cryptoXor.xor(InputImgs[0],InputImgs[1])
                if Result is not None:
                    file_path = filedialog.askdirectory(title="Save as")
                    cv2.imwrite(os.path.join(file_path, InName+'_decrypted_xor.png'), Result)
                    imgStorTmp = ia.ImageStorage(Result, InName, '.png')
                    ImgListbox.insert(tk.END, imgStorTmp.name)
                    addPreview(Result, InName+'_decrypted_xor', 'Out')
                    messagebox.showinfo("Complted!", "Image Decrypted")
                else:
                    print('Error: decryption algorythm failed.')
            else:     
                messagebox.showinfo("Warning", "Select 2 images!")
    else:
        messagebox.showinfo("Warning", "Select only one algorythm!")

def listbox_select(event):
    algo_index = AlgoListbox.curselection()
    if len(algo_index) == 1:
        algo_name = AlgoListbox.get(algo_index)
        if (algo_name == '1. Shares'):
            InfoLabel.config(text=shares.encrypt_shares_description(), justify='left', anchor = 'w', wraplength = 300)
            param1_input.place(x=180, y=220, width=100, height=25) 
            param1_label.place(x=160, y=220, width=20, height=25) 
        elif (algo_name == '2. Xor'):
            InfoLabel.config(text=cryptoXor.encrypt_xor_description(), justify='left', anchor = 'w', wraplength = 300)
            param1_input.place(x=2000, y=220, width=100, height=25) 
            param1_label.place(x=1500, y=220, width=20, height=25) 


# Root - base
root = tk.Tk()
root.title("Images cryptography")
#root.geometry("1200x900")  # Width x height
root.attributes("-fullscreen", True)
root.configure(bg="lightgray")  # Tło okna na szary

# Root - buttons

# img list
ImgListbox = tk.Listbox(root,  height=6, width=60, font = ("Helvetica", 10), selectmode='multiple', exportselection=False)
ImgListbox.place(x=160, y=20) 

ImgListbox.bind("<<ListboxSelect>>", addFrameSelect)
# # out list
# OutListbox = tk.Listbox(root,  height=6, width=60, font = ("Helvetica", 10), selectmode='multiple')
# OutListbox.place(x=160, y=130) 

# algorythm list
AlgoListbox = tk.Listbox(root, height=3, width=30, font = ("Helvetica", 10), exportselection=False)
AlgoListbox.place(x=160, y=140) 

AlgoListbox.insert(tk.END, '1. Shares')
AlgoListbox.insert(tk.END, '2. Xor')

AlgoListbox.bind("<<ListboxSelect>>", listbox_select)

# Close program
button_close = tk.Button(root, text="Close", command=close_project, fg="black", font=("Arial", 12))
button_close.place(x=1100, y=650, width=100, height=30) 

# import img
button_importImg = tk.Button(root, text="Import image", command=import_img, fg="black", font=("Arial", 12))
button_importImg.place(x=20, y=20, width=100, height=30) 

# display img
button_show = tk.Button(root, text="Show", command=disp_img, fg="black", font=("Arial", 12))
button_show.place(x=20, y=650, width=100, height=30) 

# display img
button_show = tk.Button(root, text="Compare", command=compare_img, fg="black", font=("Arial", 12))
button_show.place(x=140, y=650, width=100, height=30) 

# delete img
button_delete = tk.Button(root, text="Delete", command=delete_img, fg="black", font=("Arial", 12))
button_delete.place(x=20, y=70, width=100, height=30) 

# encrypt img
button_encrypt = tk.Button(root, text="Encrypt", command=encrypt_img, fg="black", font=("Arial", 12))
button_encrypt.place(x=20, y=120, width=100, height=30) 

# decrypt img
button_decrypt = tk.Button(root, text="Decrypt", command=decrypt_img, fg="black", font=("Arial", 12))
button_decrypt.place(x=20, y=170, width=100, height=30) 

# Param 1 input box
param1_input = tk.Entry(root)

#param1_input.place(x=280, y=120, width=100, height=25) 
param1_input.place_forget()
param1_label = tk.Label(root, text='n:', justify='left')
param1_label.place_forget()

# Info label
InfoLabel = tk.Label(root, text='Please, choose algorythm.', justify='left', anchor = 'w', wraplength = 380, font = ("Arial", 10) )
InfoLabel.place(x=630, y=20, width=450, height=230) 

# Input Images label
InImgLabel = tk.Label(root, text='Imported images:', justify='left', anchor = 'w', wraplength = 380, font = ("Arial", 10) )
InImgLabel.place(x=30, y=290, width=120, height=20) 
InImgsCntr = 0 
InImgsStorage = []
# Output Images label
OutImgLabel = tk.Label(root, text='Output images:', justify='left', anchor = 'w', wraplength = 380, font = ("Arial", 10) )
OutImgLabel.place(x=630, y=290, width=120, height=20) 
OutImgsCntr = 0
OutImgsStorage = []
# Uruchomienie pętli
root.mainloop()
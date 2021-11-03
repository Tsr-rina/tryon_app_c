from django.shortcuts import render
from django.http import HttpResponse
from .models import Human_model_img
from .models import Cloth_img
from .models import made_cloth
# from django_app.gan import CallNetWork
import cv2
import numpy as np
from PIL import Image
import io
import base64
from django_app.senga import makecounter
from django_app.overlay import overlayImage
from django_app.image_processing import gan_preprocessing, to_white, synthetic, opencv_to_pil

def index(request):
    return render(request, 'index.html')

def select_model(request):
    if request.method == 'POST':
        images = Human_model_img.objects.all()
        context = {'images': images}
        return render(request, 'model_select.html', context)
    else:
        images = Human_model_img.objects.all()
        context = {'images': images}
        return render(request, 'model_select.html', context)       

def select_cloth(request):
    if request.method == 'POST':
        if (not request.POST.get("m_S")) and (not request.POST.get("m_M")) and (not request.POST.get("m_L")) and (not request.POST.get("fm_S")) and (not request.POST.get("fm_M")) and (not request.POST.get("fm_L")):
            images = Human_model_img.objects.all()
            context = {
                'message':'モデルを1つ選択してください',
                'images': images
            }  
            return render(request, "model_select.html", context)

        # if 'None' in request.POST:
        #     context = {
        #         'alert':'モデルを選択してください'
        #     }
        #     return render(request, 'index',context)

        elif 'm_S' in request.POST:
            keys_list = request.POST.keys()
            # print(keys_list)
            model_data = Human_model_img.objects.values()
            cloth_img = Cloth_img.objects.values()
            # model_data1 = Human_model_img.objects.only()
            # model_data2 = Human_model_img.objects.values('model_name').get(id=1)
            # model_data3 = Human_model_img.objects.get(id=1)
            # print('values()', model_data)
            # print('only()', model_data1)
            # print('get()', model_data2)
            # print('values()で指定してないver',model_data3.model_name)
            # print('request.POST：', list(request.POST.values())[1])

            img = model_data[0]['img']
            mask = model_data[0]['mask']
            context = {
                'img': img,
                'name':'m_S',
                'cloth_img':cloth_img,
            }
            return render(request, 'cloth_select.html', context)

        elif 'm_M' in request.POST:
            model_data = Human_model_img.objects.values()
            cloth_img = Cloth_img.objects.values()
            img = model_data[1]['img']
            context = {
                'img': img,
                'name':'m_M',
                'cloth_img':cloth_img
            }
            return render(request, 'cloth_select.html', context)
        
        elif 'm_L' in request.POST:
            model_data = Human_model_img.objects.values()
            cloth_img = Cloth_img.objects.values()
            img = model_data[2]['img']
            context = {
                'img': img,
                'name':'m_L',
                'cloth_img':cloth_img,
            }
            return render(request, 'cloth_select.html', context)

        elif 'fm_S' in request.POST:
            model_data = Human_model_img.objects.values()
            cloth_img = Cloth_img.objects.values()
            img = model_data[3]['img']
            context = {
                'img': img,
                'name':'fm_S',
                'cloth_img':cloth_img,
            }
            return render(request, 'cloth_select.html', context)

        elif 'fm_M' in request.POST:
            model_data = Human_model_img.objects.values()
            cloth_img = Cloth_img.objects.values()
            img = model_data[4]['img']
            context = {
                'img': img,
                'name':'fm_M',
                'cloth_img':cloth_img,
            }
            return render(request, 'cloth_select.html', context)
        
        elif 'fm_L' in request.POST:
            model_data = Human_model_img.objects.values()
            cloth_img = Cloth_img.objects.values()
            img = model_data[5]['img']
            context = {
                'img': img,
                'name':'fm_L',
                'cloth_img':cloth_img,
            }
            return render(request, 'cloth_select.html', context)

def try_on(request):
    # ganモジュールに送信→全身画像,マスク画像,洋服
    if request.method == 'POST': 
        keys_list = request.POST.keys()
        keys_list = list(keys_list)
        # 選択した洋服
        cloth_path = keys_list[2]
        # print("cloth_path:{}".format(cloth_path))
        cloth_path = "./media/"+str(cloth_path)

        # 選択した人体モデルのマスク画像取得
        hm_img_mask = Human_model_img.objects.values('mask').filter(model_name=keys_list[0])
        mask_path = list(list(hm_img_mask)[0].values())
        mask_path = "./media/"+str(mask_path[0])
        # print("mask_path:{}".format(mask_path))

        # 人体モデル
        hm_img = Human_model_img.objects.values('img').filter(model_name=keys_list[0])
        hm_path = list(list(hm_img)[0].values())
        hm_path = "./media/"+str(hm_path[0])



        # if (not request.POST.get("media/cloth_img/cloth1.jpg")) and (not request.POST.get("media/cloth_img/cloth2.jpg")) and (not request.POST.get("media/cloth_img/cloth3.jpg")) and (not request.POST.get("media/cloth_img/cloth4.jpg")) and (not request.POST.get("media/cloth_img/cloth5.jpg")) and (not request.POST.get("media/cloth_img/cloth6.jpg")):
        if (keys_list[2] != 'media/cloth_img/cloth1.jpg') and (keys_list[2] != 'media/cloth_img/cloth2.jpg') and (keys_list[2] != 'media/cloth_img/cloth3.jpg') and (keys_list[2] != 'media/cloth_img/cloth4.jpg') and (keys_list[2] != 'media/cloth_img/cloth5.jpg') and (keys_list[2] != 'media/cloth_img/cloth6.jpg'):
            
            keys_list = request.POST.keys()
            keys_list = list(keys_list)
            # print(keys_list)
            # # 選択した服
            # print(keys_list[2])

            # 人体モデル
            hm_img = Human_model_img.objects.values('img').filter(model_name=keys_list[0])
            img_path = list(list(hm_img)[0].values())
            # print(hm_img)
            # print(img_path[0])

            cloth_img = Cloth_img.objects.all()
            context = {
                'message':'洋服を1つ選択してください',
                'cloth_img': cloth_img,
                'img':img_path[0],
                'name':keys_list[0]
            }
            return render(request, "cloth_select.html", context)

        elif 'media/cloth_img/cloth1.jpg' in request.POST:
            # keys_list = request.POST.keys()
            # keys_list = list(keys_list)

            # gan_preprocessing→入力画像生成

            # GANの入力画像は線画
            # put_img = makecounter(cloth_path)
            # GANに入力
            # image_make = CallNetWork(str(img_path), str(mask_path), str(cloth_path))

            made_img = made_cloth.objects.values('made_cloth_img').filter(made_cloth_color="white")
            made_path = list(list(made_img)[0].values())
            made_path = "./media/"+str(made_path[0])
            # print("made_path:{}".format(made_path))
            put_made_img = cv2.imread(made_path,-1)
            put_made_img = cv2.resize(put_made_img, dsize=(192,256))

            if keys_list[0] == "m_S" or keys_list[0] == "fm_S" or keys_list[0] == "fm_M":
                top = 45
                bottom = 128 
                left = 57
                right = 130
            elif keys_list[0] == "fm_L":
                top = 35
                bottom = 150
                left = 15
                right = 160              
            else:
                top = 20
                bottom = 165
                left = 5
                right = 175
                


            # get_mask = resized_mask[45:128, 57:130]
            # put_imgにGANの出力結果を入力
            colored_image, get_mask_shape = gan_preprocessing(mask_path, put_made_img,top, bottom, left, right)
            # print("colored_image:{}".format(colored_image.shape))


            # GANの結果を受け取り
            # なのでcolored_imageが変更の可能性あり(image_makeかな)
            # 値を受け渡す
            # all_got_img = synthetic(to_whited,mask_path,hm_path)
            all_got_img = synthetic(get_mask_shape, colored_image,mask_path,hm_path,top,bottom, left,right)

            # OpenCV→PIL変換
            transfer_img = opencv_to_pil(all_got_img)

            context = {
                'hello': 'Hello World!',
                'cloth_path':'media/cloth_img/cloth1.jpg',
                'mask_path':mask_path,
                'transfer_img':transfer_img,
            }
            return render(request, 'result.html', context)

        elif 'media/cloth_img/cloth2.jpg' in request.POST:

            made_img = made_cloth.objects.values('made_cloth_img').filter(made_cloth_color="pink")
            made_path = list(list(made_img)[0].values())
            made_path = "./media/"+str(made_path[0])
            # print("made_path:{}".format(made_path))
            put_made_img = cv2.imread(made_path,-1)
            put_made_img = cv2.resize(put_made_img, dsize=(192,256))

            top = 5
            bottom = 175
            left = 5
            right = 190

            # put_img = makecounter(cloth_path)
            colored_image, get_mask_shape = gan_preprocessing(mask_path, put_made_img,top, bottom, left, right)
            # print("colored_image:{}".format(colored_image.shape))
            all_got_img = synthetic(get_mask_shape, colored_image,mask_path,hm_path,top,bottom, left,right)
            transfer_img = opencv_to_pil(all_got_img)

            context = {
                'transfer_img':transfer_img,  
            }
            return render(request, 'result.html', context)

        elif 'media/cloth_img/cloth3.jpg' in request.POST:
            made_img = made_cloth.objects.values('made_cloth_img').filter(made_cloth_color="orange")
            made_path = list(list(made_img)[0].values())
            made_path = "./media/"+str(made_path[0])
            # print("made_path:{}".format(made_path))
            put_made_img = cv2.imread(made_path,-1)
            put_made_img = cv2.resize(put_made_img, dsize=(192,256))
            top = 5
            bottom = 175
            left = 5
            right = 190        
            # put_img = makecounter(cloth_path)
            colored_image, get_mask_shape = gan_preprocessing(mask_path, put_made_img,top, bottom, left, right)
            # print("colored_image:{}".format(colored_image.shape))
            all_got_img = synthetic(get_mask_shape, colored_image,mask_path,hm_path,top,bottom, left,right)
            transfer_img = opencv_to_pil(all_got_img)

            context = {
                'transfer_img':transfer_img,  
            }
            return render(request, 'result.html', context)

        elif 'media/cloth_img/cloth4.jpg' in request.POST:
            made_img = made_cloth.objects.values('made_cloth_img').filter(made_cloth_color="green")
            made_path = list(list(made_img)[0].values())
            made_path = "./media/"+str(made_path[0])
            # print("made_path:{}".format(made_path))
            put_made_img = cv2.imread(made_path,-1)
            put_made_img = cv2.resize(put_made_img, dsize=(192,256))
            top = 5
            bottom = 175
            left = 5
            right = 190

            # put_img = makecounter(cloth_path)
            colored_image, get_mask_shape = gan_preprocessing(mask_path, put_made_img,top, bottom, left, right)
            # print("colored_image:{}".format(colored_image.shape))
            all_got_img = synthetic(get_mask_shape, colored_image,mask_path,hm_path,top,bottom, left,right)
            transfer_img = opencv_to_pil(all_got_img)

            context = {
                'transfer_img':transfer_img,  
            }
            return render(request, 'result.html', context)

        elif 'media/cloth_img/cloth5.jpg' in request.POST:
            made_img = made_cloth.objects.values('made_cloth_img').filter(made_cloth_color="light-blue")
            made_path = list(list(made_img)[0].values())
            made_path = "./media/"+str(made_path[0])
            # print("made_path:{}".format(made_path))
            put_made_img = cv2.imread(made_path,-1)
            put_made_img = cv2.resize(put_made_img, dsize=(192,256))
            top = 5
            bottom = 175
            left = 5
            right = 190

            # put_img = makecounter(cloth_path)
            colored_image, get_mask_shape = gan_preprocessing(mask_path, put_made_img,top, bottom, left, right)
            # print("colored_image:{}".format(colored_image.shape))
            all_got_img = synthetic(get_mask_shape, colored_image,mask_path,hm_path,top,bottom, left,right)
            transfer_img = opencv_to_pil(all_got_img)
            context = {
                'transfer_img':transfer_img,  
            }
            return render(request, 'result.html', context)

        elif 'media/cloth_img/cloth6.jpg' in request.POST:
            made_img = made_cloth.objects.values('made_cloth_img').filter(made_cloth_color="blue")
            made_path = list(list(made_img)[0].values())
            made_path = "./media/"+str(made_path[0])
            # print("made_path:{}".format(made_path))
            put_made_img = cv2.imread(made_path,-1)
            put_made_img = cv2.resize(put_made_img, dsize=(192,256))
            top = 5
            bottom = 175
            left = 5
            right = 190
            # put_img = makecounter(cloth_path)
            colored_image, get_mask_shape = gan_preprocessing(mask_path, put_made_img,top, bottom, left, right)
            # print("colored_image:{}".format(colored_image.shape))
            all_got_img = synthetic(get_mask_shape, colored_image,mask_path,hm_path,top,bottom, left,right)
            transfer_img = opencv_to_pil(all_got_img)
            context = {
                'transfer_img':transfer_img,  
            }
            return render(request, 'result.html', context)
 


    



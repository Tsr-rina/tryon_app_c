import cv2
from PIL import Image
import numpy as np
import io
import base64
from django_app.senga import makecounter
from django_app.overlay import overlayImage

def gan_preprocessing(mask_path, cloth,top, bottom, left, right):
    # ここに画像処理
    mask_img = cv2.imread(mask_path)
    # print("mask_img.shape:{}".format(mask_img.shape))
    resized_mask = cv2.resize(mask_img, dsize=(192,256))
    # print("resized_mask:{}".format(resized_mask.shape))

    # 画像抽出paste
    get_mask = resized_mask[top:bottom, left:right]
    get_mask_shape = get_mask.shape
    # print("get_mask:{}".format(get_mask.shape))
    get_mask = cv2.resize(get_mask, dsize=(192,256))
    # print("抽出後のリサイズ:{}".format(get_mask.shape))

    # 洋服の線画past
    # cloth = makecounter(cloth_path)
    # print("cloth.shape:{}".format(cloth.shape))
    # resized_cloth = cv2.resize(cloth, dsize=(192,256))
    # print("resized_cloth:{}".format(resized_cloth.shape))

    # オーバーレイ
    # black = [0, 0, 0]
    # hotpink = [255, 105, 180]
    # get_mask[np.where((get_mask == black).all(axis=2))] = hotpink
    get_mask = cv2.cvtColor(get_mask, cv2.COLOR_RGB2BGRA)
    get_mask[:, :,3] = np.where(np.all(get_mask == (255, 255,255,255), axis=-1), 0, 255)  # 白色のみTrueを返し、Alphaを0にする
    colored_image = overlayImage(cloth, get_mask, (0, 0))

    return colored_image, get_mask_shape

def to_white(want_white):
    white = [255, 255, 255]
    hotpink = [255, 105, 180]
    want_white[np.where((want_white == hotpink).all(axis=2))] = white
    return want_white


def synthetic(get_mask_shape, after_gan,mask_path,hm_path,top, bottom, left, right):
    made = cv2.resize(after_gan, dsize=(get_mask_shape[1], get_mask_shape[0]))
    made = cv2.cvtColor(made, cv2.COLOR_BGRA2BGR)
    # print("made.shape:{}".format(made.shape))
    mask = cv2.imread(mask_path)
    mask = cv2.resize(mask, dsize=(192, 256))
    # print("mask.shape:{}".format(mask.shape))
    made_plot = [[0,0],[0,get_mask_shape[0]],[get_mask_shape[1],get_mask_shape[0]], [get_mask_shape[1],0]]
    # mask_plot = [[57,45],[57,128],[130, 128],[130, 45]]
    mask_plot = [[left,top],[left,bottom],[right, bottom],[right, top]]

    # バウンディングボックスで切り出し
    src_pts_arr = np.array(made_plot, dtype=np.float32)
    dst_pts_arr = np.array(mask_plot, dtype=np.float32)

    src_rect = cv2.boundingRect(src_pts_arr)
    dst_rect = cv2.boundingRect(dst_pts_arr)

    # print("src_rect:{}".format(src_rect))
    # print("dst_rect:{}".format(dst_rect))

    made_crop = made[src_rect[1]:src_rect[1] + src_rect[3], src_rect[0]:src_rect[0] + src_rect[2]]
    mask_crop = mask[dst_rect[1]:dst_rect[1] + dst_rect[3]-1, dst_rect[0]:dst_rect[0] + dst_rect[2]-1]
    # print(made_crop.shape)
    # print(mask_crop.shape)
    made_pts_crop = src_pts_arr - src_rect[:2]
    mask_pts_crop = dst_pts_arr - dst_rect[:2]

    # print("made_crop:{}".format(made_pts_crop))
    # print("mask_crop:{}".format(mask_pts_crop))

    masker = np.zeros_like(mask_crop, dtype=np.float32)
    cv2.fillConvexPoly(masker, mask_pts_crop.astype(np.int), (1.0,1.0,1.0), cv2.LINE_AA)
    dst_crop_merge = mask_crop * made_crop + made_crop * (1 - mask_crop)

    # black = [0, 0, 0]
    # hotpink = [255, 105, 180]
    # dst_crop_merge[np.where((dst_crop_merge == hotpink).all(axis=2))] = black
    dst_crop_merge = cv2.cvtColor(dst_crop_merge,cv2.COLOR_RGB2BGR)

    mask[dst_rect[1]:dst_rect[1]+dst_rect[3]-1, dst_rect[0]:dst_rect[0]+dst_rect[2]-1] = dst_crop_merge

    # GAN済のマスク画像が生成できたら人体モデルと合成する
    mask = cv2.resize(mask, dsize=(192,256))
    for i in range(250):
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
        black = [i, i,i]
        smoke = [245, 245, 245]
        mask[np.where((mask == black).all(axis=2))] = smoke
    smoke = [245, 245, 245]
    hotpink = [255, 105, 180]
    mask[np.where((mask == smoke).all(axis=2))] = hotpink
    mask = cv2.cvtColor(mask, cv2.COLOR_RGB2BGRA)
    mask[:, :,3] = np.where(np.all(mask == (180,105,255,255), axis=-1), 0, 255)  # 白色のみTrueを返し、Alphaを0にする
    # 人体モデル読み込み
    hm = cv2.imread(hm_path)
    hm_shape = hm.shape
    hmed = cv2.resize(hm, dsize=(192,256))
    all_got = overlayImage(hmed, mask, (0, 0))
    all_got = cv2.resize(all_got, dsize=(hm_shape[1], hm_shape[0]))

    return all_got


def opencv_to_pil(all_got):

    image_cv = cv2.cvtColor(all_got, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_cv)
    image_pil = image_pil.convert('RGB')

    # 画像をhtmlに持っていく準備
    buffer = io.BytesIO()
    image_pil.save(buffer, format="PNG")

    base64Img = base64.b64encode(buffer.getvalue()).decode().replace("'","")

    return base64Img


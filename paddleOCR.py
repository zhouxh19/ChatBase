import datetime
import os
import fitz  # fitz就是pip install PyMuPDF
import os
import cv2
from paddleocr import PPStructure, save_structure_res, PaddleOCR
from paddleocr.ppstructure.recovery.recovery_to_doc import sorted_layout_boxes, convert_info_docx
from copy import deepcopy
from paddleocr import PaddleOCR, draw_ocr

# 中文测试图
table_engine = PPStructure(recovery=True, lang='ch')


def pdf2png(pdfPath, baseImagePath):
    imagePath = os.path.join(baseImagePath, os.path.basename(pdfPath).split('.')[0])
    startTime_pdf2img = datetime.datetime.now()  # 开始时间
    if not os.path.exists(imagePath):
        os.makedirs(imagePath)
    pdfDoc = fitz.open(pdfPath)
    totalPage = pdfDoc.page_count
    for pg in range(totalPage):
        page = pdfDoc[pg]
        rotate = int(0)
        zoom_x = 2
        zoom_y = 2
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        print(f'正在保存{pdfPath}的第{pg + 1}页，共{totalPage}页')
        pix.save(imagePath + '/' + f'images_{pg + 1}.png')
    endTime_pdf2img = datetime.datetime.now()
    print(f'{pdfDoc}-pdf2img-花费时间={(endTime_pdf2img - startTime_pdf2img).seconds}秒')


def pdf2text(pdf_path, save_txt_path):
    text = ''
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    result = ocr.ocr(pdf_path, cls=True)
    for idx in range(len(result)):
        res = result[idx]
        if res == None:  # 识别到空页就跳过，防止程序报错 / Skip when empty result detected to avoid TypeError:NoneType
            print(f"[DEBUG] Empty page {idx + 1} detected, skip it.")
            continue
        txts = [line[1][0] for line in res]
        text += "".join(txts)

    with open(save_txt_path, 'w', encoding='utf-8') as f:
        f.write(text)


# def imgs2text(imgs_folder, save_txt_path):
#     imgs = os.listdir(imgs_folder)
#     text = ""
#     total_imgs = len(imgs)
#     for index, img_name in enumerate(imgs):
#         full_img_path = os.path.join(imgs_folder, img_name)
#         text += img2text(full_img_path)
#         print(f"完成{full_img_path}的采集，还剩下{total_imgs - (index + 1)}张图片")
#
#     with open(save_txt_path, 'w', encoding='utf-8') as f:
#         f.write(text)


if __name__ == "__main__":
    pdfPath = '/Volumes/NBDATA/JobProjects/Tsinghua/李老师课件资料/数据库系统概论-第5版_完整版.pdf'
    # baseImagePath = '/Volumes/NBDATA/JobProjects/Tsinghua/李老师课件资料/pdf_imsges/'
    # pdf2png(pdfPath, baseImagePath)
    result = pdf2text(pdfPath, '/Volumes/NBDATA/JobProjects/Tsinghua/李老师课件资料/数据库系统概论-第5版-2024-05-15.txt')
    print(result)
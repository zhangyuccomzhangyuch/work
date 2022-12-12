import numpy as np
import streamlit as st
import cv2
from ocr import OCRDetector
from baike_crawler import parse_baike
import re
import time
ocr = OCRDetector()
st.title('食品添加剂自动识别系统')
uploaded_file = st.file_uploader("上传配料表", ['png', 'jpg', 'jpeg'])
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    st.image(uploaded_file)
    ocr_pred = ocr.predict(cv2_img)
    if not ocr_pred:
        st.warning('未识别出配料表，请重新上传', icon="⚠️")
    else:
        items = re.split('，|、|,|、', ocr_pred)
        st.success(f'识别出 {len(items)} 种配料，准备爬取详细信息', icon="✅")
        for i, item in enumerate(items):
            sub_title, desc = parse_baike(item)
            st.subheader(item)
            st.text(sub_title)
            if desc == '':
                st.caption('无详细信息')
            else:
                #desc = desc.replace('防腐剂', '<font color="#FF0000">防腐剂</font>')
                #desc = desc.replace('防腐', '<font color="#FF0000">防腐</font>')
                #desc = desc.replace('甜味剂', '<font color="#FF0000">甜味剂</font>')
                #desc = desc.replace('着色剂', '<font color="#FF0000">着色剂</font>')
                #desc = desc.replace('食品添加剂', '<font color="#FF0000">食品添加剂</font>')
                #desc = desc.replace('增稠剂', '<font color="#FF0000">增稠剂</font>')
                #desc = desc.replace('剂', '<font color="#FF0000">剂</font>')
                st.caption(desc, unsafe_allow_html=True)
            with st.spinner(f'配料爬取中，已完成 {i+1}/{len(items)}'):
                time.sleep(1)





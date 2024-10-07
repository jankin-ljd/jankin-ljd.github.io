# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 14:46:47 2024

@function:
    
@author: Jankin

"""
from flask import Flask, render_template, request, make_response
from flask_frozen import Freezer
from markupsafe import Markup
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import io
import os, sys
# import base64
import re
 
def remove_digits(s):
    return re.sub(r'\d+', '', s)

# def b64encode(s):
#     # 实现 base64 编码的逻辑
#     return Markup(base64.b64encode(s))  # 使用 Markup 确保安全的输出

app = Flask(__name__, static_url_path='/static', static_folder='static')
freezer = Freezer(app)
# app.jinja_env.filters['b64encode'] = b64encode

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # 获取用户提交的数据
        text = remove_digits(request.form.get('text'))   
        
        # 指定字体路径
        font_path = 'simkai.ttf'
        # 创建词云
        wordcloud = WordCloud(font_path=font_path, background_color="white", 
                              prefer_horizontal = 0.5, max_words=6000, 
                              width=600, height=600).generate(text)
        # wordcloud.to_file(r'D:\work\Code\Python\wordcloudtest\static\wordcloud.png')

        # 将词云转换为图像
        image_array = np.array(wordcloud.recolor(color_func=wordcloud.color_func))
        image = Image.fromarray(image_array.astype(np.uint8))
        
        # 将图像保存到内存中
        # buffer = io.BytesIO()
        # image.save(buffer, format="PNG")
        # buffer.seek(0)

        # 构建保存图像的路径    
        current_path = os.getcwd() + '\\static\\'
        file_name = 'wordcloud.png'
        save_path = os.path.join(current_path, file_name)
        print(save_path)
        image.save(save_path)
        

        # 将图片数据编码为Base64字符串
        # image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
        # 显示图像
        # image = Image.open(buffer)  # 从BytesIO对象中读取图像数据
        image.show()  # 展示图像

        # 关闭内存中的图片
        # buffer.close()

        # 返回带有词云图片的结果页面
        return render_template('result.html', image=image)
    
    # 如果是 GET 请求，则显示初始表单
    return render_template('index.html')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', port=1212, debug=True)

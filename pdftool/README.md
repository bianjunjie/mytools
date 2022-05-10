# 介绍
split\_pdf.py: 给定一份pdf文件，摘出需要的部分（按照页码）
join\_pdf.py: 将多个pdf文件合并成一个
需要安装PyPDF2这个库(pip install即可)

# 使用方法
给定某个pdf文件(input.pdf)，一共100页（页面从1开始），摘出其中第10 ~ 11 这两页, 并生成一份新的pdf文件(output.pdf)
```py
python split_pdf.py input.pdf 10 11 output.pdf
```

给定三个pdf文件， 1.pdf,2.pdf,3.pdf，合并成1个pdf all.pdf
```py
python join_pdf.py 1.pdf 2.pdf 3.pdf all.pdf
```




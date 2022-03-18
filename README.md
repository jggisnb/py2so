# py2so



## 参数说明 ##

* -ifd(--input_folder):转换文件输入路径,必填。
* -ef(--exclude_files):不转换文件, ","号隔开,必填,可以将入口文件名写入。
* -ofd(--output_folder):转换文件输出路径,必填。
* -suf(--suffix):转换文件的后缀,默认.py,默认值".py"
* -kcf(--keep_cfile):是否保留转换过程中的.c文件,默认不保留,默认值"0"
* -py(--python)执行转换的python解释器,默认python,默认值"python"


## 示例 ##
* (py37) [root@text onlp_predictV2]# python toso.py -ifd /opt/nlp_predictV2 \
                                                  -ef gunicorn_config.py,gunicorn_server.py,flask_server.py,start_redis_workers_forever.py \
                                                  -ofd /opt/onlp_predictV2

* [root@text onlp_predictV2]# pythonj toso.py -ifd /opt/nlp_predictV2 \
                                                  -ef gunicorn_config.py,gunicorn_server.py,flask_server.py,start_redis_workers_forever.py \
                                                  -ofd /opt/onlp_predictV2 \
                                                  -suf .py \
                                                  -kcf 0 \
                                                  -py pythonj
                                                  
                                                  
## 注意 ## 

* py文件中不能包含与c语言中关键字相同的变量名称或者参数名称

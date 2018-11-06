#-*- coding:utf-8 -*-

'''
上传到文件存储服务器
'''

import urllib2
import time
import sys
import os
import shutil
class uploadcovFile:
    def __init__(self):
        self.url = 'https://oss.mail.qq.com/cgi-bin/log_upload?inputc=utf-8&outputc=utf-8&func=PerformanceLogSaveLocal'
        self.boundary = '----------%s' % hex(int(time.time() * 1000))

    def getData(self,buildInfo,deviceInfo,zipfile):
        data = []
        data.append('--%s' % self.boundary)

        data.append('Content-Disposition: form-data; name="name"\r\n')
        data.append('UploadFile')
        data.append('--%s' % self.boundary)

        data.append('Content-Disposition: form-data; name="os"\r\n')
        data.append('Android')
        data.append('--%s' % self.boundary)

        data.append('Content-Disposition: form-data; name="device"\r\n')
        data.append('pcdevice')
        data.append('--%s' % self.boundary)

        data.append('Content-Disposition: form-data; name="deviceid"\r\n')
        data.append('deviceid')
        data.append('--%s' % self.boundary)

        data.append('Content-Disposition: form-data; name="platform"\r\n')
        data.append('5')
        data.append('--%s' % self.boundary)
	data.append('--%s' % self.boundary)
        #this is the meaning

        data.append('Content-Disposition: form-data; name="clitime"\r\n')
        data.append(str(int(time.time())))
        data.append('--%s' % self.boundary)
        data.append('Content-Disposition: form-data; name="filename"\r\n')
        data.append('result.coverage')
        data.append('--%s' % self.boundary)
        data.append('Content-Disposition: form-data; name="appid"\r\n')
        data.append('19')
        data.append('--%s' % self.boundary)
        data.append('Content-Disposition: form-data; name="authtype"\r\n')
        data.append('1')
        data.append('--%s' % self.boundary)
        data.append('Content-Disposition: form-data; name="appversion"\r\n')
        data.append('2.6.2')
        data.append('--%s' %  self.boundary)
        data.append('Content-Disposition: form-data; name="channelid"\r\n')
        data.append('1000')
        data.append('--%s' %  self.boundary)

        fr = open(zipfile, 'rb')
        data.append('Content-Disposition: form-data; name="UploadFile"; filename="%s"'%zipfile)
        data.append('Content-Type: %s\r\n' % 'application/octet-stream')
        data.append(fr.read())
        fr.close()
        data.append('--%s--\r\n' % self.boundary)
        return data


    def sendData(self,data,http_url='https://oss.mail.qq.com/cgi-bin/log_upload?inputc=utf-8&outputc=utf-8&func=PerformanceLogSaveLocal'):
        http_body = '\r\n'.join(data)
        sendCode = 0
        try:
            # buld http request
            req = urllib2.Request(http_url, data=http_body)
            # header
            req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % self.boundary)
            req.add_header('User-Agent', 'Mozilla/5.0')
            # post data to server
            resp = urllib2.urlopen(req, timeout=5)
            # get response
            qrcont = resp.read()
            if eval(qrcont).get('result').get('errCode') ==0:
                print u"上传文件成功",eval(qrcont).get('result')
                sendCode = 1
            else :
                print u"上传文件失败，错误信息：",qrcont
        except Exception, e:
            print 'http error',e
        finally:
            return sendCode

if __name__ == "__main__":
    upfile = uploadcovFile()
    paths=sys.argv[1][:-1]
    print paths
    pathlist=os.listdir(paths)
    for pathitem in pathlist:
        if pathitem.endswith('.coverage'):
            data = upfile.getData(buildInfo="",deviceInfo="",zipfile=paths+'\\'+pathitem)
            upfile.sendData(data)
            shutil.move(paths+'\\'+pathitem,paths+'\\'+pathitem+'.done')




#!/bin/sh
wget http://gosspublic.alicdn.com/ossutil/1.6.18/ossutil64
chmod 755 ossutil64

echo "endPoint:"${endPoint}
echo "path:"${productionPath}

formDate="`date +%Y%m%d%H%M`"

echo "备份文件夹："${formDate}

./ossutil64 config -e ${endPoint} -i ${accessKeyID} -k ${accessKeySecret} -L CH --loglevel debug -c ~/.ossutilconfig

./ossutil64 -c ~/.ossutilconfig cp -r oss://${mybucket}/${productionPath}/ oss://${mybucket}/${productionPath}backup/${formDate}/ --meta x-oss-object-acl:public-read-write -f
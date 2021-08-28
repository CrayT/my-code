#!/bin/sh
wget http://gosspublic.alicdn.com/ossutil/1.6.18/ossutil64
chmod 755 ossutil64
echo "endPoint:"${endPoint}
echo "path:"${developePath}
./ossutil64 config -e ${endPoint} -i ${accessKeyID} -k ${accessKeySecret} -L CH --loglevel debug -c ~/.ossutilconfig
./ossutil64 -c ~/.ossutilconfig cp -r ./myfiles oss://${mybucket}/${developePath}/ --meta x-oss-object-acl:public-read-write -f
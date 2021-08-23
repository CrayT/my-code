FROM  ubuntu:latest
#FROM  mcr.microsoft.com/dotnet/sdk:3.1

COPY ./ /dotnet

WORKDIR /dotnet

RUN yum install autoconf automake libtool freetype-devel fontconfig libXft libexif giflib libjpeg-turbo libpng giflib libtiff libexif glib2 cairo -y \
&& yum install dotnet-sdk-3.1 -y
#rpm -ivh https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/l/libgdiplus-6.0.4-3.el8.x86_64.rpm

RUN  yum install glib* -y \
        && yum install wget -y \
        && wget http://download.mono-project.com/sources/libgdiplus/libgdiplus0-6.0.4.tar.gz \
        && tar -zxvf libgdiplus0-6.0.4.tar.gz \
        && cd libgdiplus-6.0.4 \
        && ./configure --prefix=/usr \
        && make && make install
EXPOSE 5010

CMD ["dotnet", "YW.Services.FloorPlanService.dll"]





/**
 * svg，需要定义viewPort即height和width，即在html中的宽高，默认没有单位。另外需要定义viewBox={x y width height},viewBox定义了在viewPort中的起始位置，
 * 即x和y坐标，默认(0,0)左上角，width和height指定了截取viewPort中的哪一部分。svg中的绘制的元素显示在viewBox中，然后再被扩展或缩放至viewPort区域，
 * 所以绘制元素的大小与实际展示出的大小是不一样的，需要根据比例计算。
 */
export class SvgCreator {
    constructor(params) { //放大倍数，屏幕需要显示的高，...宽，扩散数量，中心点屏幕坐标，屏幕坐标点数组。
        this.scale = params.scale || 1.5;
        this.height = params.height;
        this.width = params.width;
        this.num = params.num;
        this.center = params.center;
        this.points = params.points;
        this.polygon = params.polygon;
        this.dur = params.dur || 1.2;
        this.svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg') // 创建带有标准svg命名空间的节点
    }
    init(){
        //中心化坐标点：
        let center = this.points[0]
        let pointList = []
        let offset = center.clone().sub(this.center) //boundingBox的中点与group的中点的偏差。

        let offestWidth = offset.x //坐标需要整体偏移
        let offestHeight = offset.y

        for(let i = 0; i < this.points[1].length; i++){
            let p = this.points[1][i].clone().sub(center)
            let x = offestWidth + (p.x)
            let y = -offestHeight - p.y
            pointList.push({x : x, y : y}) //屏幕坐标系和svg坐标系，y轴是相反的。坐标也需要缩放倍数
        }

        //viewBox偏移1/2距离，满足矩形框扩散要求。
        //因为计算polygon时阈值可能过大导致偏移外轮廓太大，所以viewBox设置在scale基础上大0.5倍
        let viewBoxWidthOffset =  (this.scale + 0.5) * this.width / 2
        let viewBoxHeightOffset =  (this.scale + 0.5) * this.height / 2

        // console.log(width, height, offset1, offset2)

        this.svg.setAttribute('width', this.width * (this.scale + 0.5))
        this.svg.setAttribute('height', this.height * (this.scale + 0.5))
        this.svg.setAttribute('style','overflow:visible')

        //将viewBox坐标设置为偏移后的坐标，宽高保持不变。
        let viewBox = "-" + viewBoxWidthOffset + " -" + viewBoxHeightOffset + " " + this.width * (this.scale + 0.5) + ' ' + this.height * (this.scale + 0.5);

        this.svg.setAttribute("viewBox", viewBox);

        let path = 'M ' + pointList[0].x + ',' + pointList[0].y
        for(let i = 1; i < pointList.length; i++){
            path += 'L' + pointList[i].x + ',' + pointList[i].y
        }
        path += 'z'
        for(let i = 0; i < this.num; i++){
            this.svg.appendChild(this.createPath(path,0.2 * i))
        }
    }
    createPath (path, begin){
        begin = begin || 0
        let pathSvg = document.createElementNS('http://www.w3.org/2000/svg', 'path')
        pathSvg.setAttribute('d', path)
        pathSvg.setAttribute('style','fill:#FFFFFF;stroke:#fff;stroke-width:1;fill-opacity:0.06;overflow:visible')

        let animate1 = document.createElementNS('http://www.w3.org/2000/svg', 'animateTransform')
        animate1.setAttribute('attributeName', 'transform')
        animate1.setAttribute('type', 'scale')
        animate1.setAttribute('from', "0.8")
        let scaleTo = this.scale - 0.4
        animate1.setAttribute('to', scaleTo)
        animate1.setAttribute('begin', begin)
        animate1.setAttribute('dur', this.dur)
        animate1.setAttribute('repeatCount', 'indefinite')

        let animate2 = document.createElementNS('http://www.w3.org/2000/svg', 'animate')
        animate2.setAttribute('attributeName', 'opacity')
        animate2.setAttribute('from', 1)
        animate2.setAttribute('to', 0)
        animate2.setAttribute('begin', begin)
        animate2.setAttribute('dur', this.dur)
        animate2.setAttribute('repeatCount', 'indefinite')

        pathSvg.appendChild(animate1)
        pathSvg.appendChild(animate2)

        return pathSvg
    }
    //创建简单的矩形：
    createRecAnimation(points, scale, dur) {
        //中心化坐标点：
        let center = points[4]
        let p1 = points[0].clone().sub(center)
        let p2 = points[1].clone().sub(center)
        let p3 = points[2].clone().sub(center)
        let p4 = points[3].clone().sub(center)

        // console.log(p1,p2,p3,p4)
        let height = p1.distanceTo(p2)
        let width = p2.distanceTo(p3)

        //viewBox偏移1/2距离，满足矩形框扩散要求。
        let viewBoxWidthOffset = width / 2
        let viewBoxHeightOffset = height / 2

        //偏移距离=实际宽度/缩放倍数/2
        let recOffestWidth = "-" + width / (2 * scale)
        let recOffestHeight = "-" + height / (2 * scale)

        // console.log(width, height, offset1, offset2)

        //因为要扩散1.5倍，所以需要将viewPort设置为1.5倍，不然超出边界。
        this.svg.setAttribute('width', width * scale)
        this.svg.setAttribute('height', height * scale)
        this.svg.setAttribute('style', 'overflow:visible')

        //将viewBox坐标设置为偏移后的坐标，宽高保持不变。
        let viewBox = "-" + viewBoxWidthOffset + " -" + viewBoxHeightOffset + " " + width + ' ' + height;

        this.svg.setAttribute("viewBox", viewBox);

        this.svg.appendChild(this.createRec(height, width, recOffestWidth, recOffestHeight, '0s', dur))
        this.svg.appendChild(this.createRec(height, width, recOffestWidth, recOffestHeight, '0.2s', dur))
        this.svg.appendChild(this.createRec(height, width, recOffestWidth, recOffestHeight, '0.4s', dur))
        this.svg.appendChild(this.createRec(height, width, recOffestWidth, recOffestHeight, '0.6s', dur))
    }
    createRec (height, width, recOffestWidth, recOffestHeight, begin, dur, rx, ry){
        rx = rx || 5
        ry = ry || 5
        let rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect')

        //偏移矩形框
        rect.setAttribute('x', recOffestWidth)
        rect.setAttribute('y', recOffestHeight)

        //圆角大小
        rect.setAttribute('rx', rx)
        rect.setAttribute('ry', ry)

        //viewBox中的宽高，缩小1.5倍，这样viewBox缩放至viewPort时等于实际宽高。
        rect.setAttribute('height', height / this.scale)
        rect.setAttribute('width', width / this.scale)

        rect.setAttribute('style','stroke:#fff;stroke-width:1;fill-opacity:0;overflow:visible')

        let animate1 = document.createElementNS('http://www.w3.org/2000/svg', 'animateTransform')
        animate1.setAttribute('attributeName', 'transform')
        animate1.setAttribute('type', 'scale')
        animate1.setAttribute('from', "1")
        let scaleTo = this.scale
        animate1.setAttribute('to', scaleTo)
        animate1.setAttribute('begin', begin)
        animate1.setAttribute('dur', dur)
        animate1.setAttribute('repeatCount', 'indefinite')

        let animate2 = document.createElementNS('http://www.w3.org/2000/svg', 'animate')
        animate2.setAttribute('attributeName', 'opacity')
        animate2.setAttribute('from', 1)
        animate2.setAttribute('to', 0)
        animate2.setAttribute('begin', begin)
        animate2.setAttribute('dur', this.dur)
        animate2.setAttribute('repeatCount', 'indefinite')

        rect.appendChild(animate1)
        rect.appendChild(animate2)

        return rect
    }
    createPolygon () {
        let polygon = this.polygon, scale = this.scale, dur = this.dur;
        // let viewBoxWidthOffset =  (this.scale + 0.5) * this.width / 2
        // let viewBoxHeightOffset =  (this.scale + 0.5) * this.height / 2
        // let viewBox = "-" + viewBoxWidthOffset + " -" + viewBoxHeightOffset + " " + this.width * (this.scale + 0.5) + ' ' + this.height * (this.scale + 0.5);
        //
        // this.svg.setAttribute("viewBox", viewBox);
        this.svg.setAttribute('width', this.width)
        this.svg.setAttribute('height', this.height)
        this.svg.setAttribute('style','overflow:visible')

        let polygonFrom = polygon.map(p => p.x + " " + p.y).join(' ');
        let pro = new RoomProcessorV2();
        let polygonTo = pro.offset([polygon.map(p=>({X: p.x, Y:p.y}))], scale)[0].map(p => p.X + " " + p.Y).join(' ');
        let polygonSvg = document.createElementNS('http://www.w3.org/2000/svg', 'polygon')
        polygonSvg.setAttribute('points', polygonFrom)
        polygonSvg.setAttribute('style','fill:#cccccc;stroke:#ff0000;stroke-width:2')

        let animate1 = document.createElementNS('http://www.w3.org/2000/svg', 'animate')
        animate1.setAttribute('attributeName', 'opacity')
        animate1.setAttribute('type', 'scale')
        animate1.setAttribute('from', "1")
        let scaleTo = scale + "";
        animate1.setAttribute('to', "0")
        animate1.setAttribute('begin', "0s")
        animate1.setAttribute('dur', dur+"s")
        animate1.setAttribute('repeatCount', 'indefinite')

        let animate2 = document.createElementNS('http://www.w3.org/2000/svg', 'animate')
        animate2.setAttribute('attributeName', 'points')
        // animate2.setAttribute('from', 1)
        animate2.setAttribute('to', polygonTo)
        animate2.setAttribute('begin', "0s")
        animate2.setAttribute('dur', dur+"s")
        animate2.setAttribute('repeatCount', 'indefinite')

        polygonSvg.appendChild(animate1)
        polygonSvg.appendChild(animate2)

        this.svg.appendChild(polygonSvg)

        return polygonSvg
    }
}

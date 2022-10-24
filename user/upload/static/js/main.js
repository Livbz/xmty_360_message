var alimap = new Vue({
    el: "#container",
    delimiters: ['${', '}'],
    data:{
        markers: [],
        idList: [],
        salesmanNum: 0,
        showLable: 0,
        readyMass: false,
        zoomed: 12,
        LngCenter: 0,
        LatCenter: 0,
        nameDict: {},
        isGeting: false,
    },
    methods:{
      setPointNum(x,checked,name){
        if(checked=='1'){
          console.log(checked)
          markerContent = '' +
          '<div class="custom-content-marker">' +
          '   <img src="/map/img?name=red.png">' +
          '   <div class="lable" >' + name + '</div>' +
          '   <div class="close-btn-check">'+ x +'</div>' +
          '</div>';
        }else{
          markerContent = '' +
          '<div class="custom-content-marker">' +
          '   <img src="/map/img?name=red.png">' +
          '   <div class="lable" >' + name + '</div>' +
          '   <div class="close-btn">'+ x +'</div>' +
          '</div>';
        }
        return markerContent
      },
      getGivenBySalesman(salesman){
        let vm = this
        if(!vm.isGeting){
          axios.get('/map/givenbysalesman?salesman='+salesman)
          .then(function (response) {
            vm.isGeting = false
            vm.showMarker(response.data.data.markers)
            var allCustom = document.getElementById('allCustom')
            allCustom.setAttribute('style', 'border: solid 2px #e1e1e1c2');
            var notCustom = document.getElementById('notCustom')
            notCustom.setAttribute('style', 'border: solid 2px #e1e1e1c2');
            var readyCustom = document.getElementById('readyCustom')
            readyCustom.setAttribute('style', 'border: solid 2px #fb7a7ac2');
          }) 
        }else{
          console.log('已在请求....')
        }

      },
      getGivenorNot(t){
        let vm = this
        map.clearMap()
        if(!vm.isGeting){
            vm.isGeting = true
            if(t==1){
              axios.get('/map/given?t=1',)
                .then(function (response) {
                  vm.isGeting = false
                  console.log('已分配数量：',response.data.data.markers.length)
                  vm.showMarker(response.data.data.markers,useRam=0)
                  var allCustom = document.getElementById('allCustom')
                  allCustom.setAttribute('style', 'border: solid 2px #e1e1e1c2');
                  var notCustom = document.getElementById('notCustom')
                  notCustom.setAttribute('style', 'border: solid 2px #e1e1e1c2');
                  var readyCustom = document.getElementById('readyCustom')
                  readyCustom.setAttribute('style', 'border: solid 2px #fb7a7ac2');
                })
            }else{
              axios.get('/map/given?t=0',)
                .then(function (response) {
                  vm.isGeting = false
                  vm.showMarker(response.data.data.markers,useRam=0)
                  var allCustom = document.getElementById('allCustom')
                  allCustom.setAttribute('style', 'border: solid 2px #e1e1e1c2');
                  var notCustom = document.getElementById('notCustom')
                  notCustom.setAttribute('style', 'border: solid 2px #fb7a7ac2');
                  var readyCustom = document.getElementById('readyCustom')
                  readyCustom.setAttribute('style', 'border: solid 2px #e1e1e1c2');
                })    
            }
        }else{
          console.log('已在请求....')
        }
      },
      massMarker(datas){
      var styleObject = {
          url: '/map/img?name=blue.png',  // 图标地址
          size: new AMap.Size(11,11),      // 图标大小
          anchor: new AMap.Pixel(5,5) // 图标显示位置偏移量，基准点为图标左上角
      }
      
      var massMarks = new AMap.MassMarks({
          zIndex: 999999,  // 海量点图层叠加的顺序
          zooms: [3, 19],  // 在指定地图缩放级别范围内展示海量点图层
          style: styleObject  // 设置样式对象
      });
      
      var massData = []

      for(i of datas){
        var item = {
          lnglat: i.position,
          name: i.extData.name,
          id:i.extData.id
        }
        massData.push(item)
      }

      console.log(massData.length)
      massMarks.setData(massData);
      // 将海量点添加至地图实例
      massMarks.setMap(map);
      console.log('getMap()', massMarks.getMap())
      console.log('getData()', massMarks.getData())
      massMarks.show()
  
      },
      showMarker(markers,useRam=1){
        map.clearMap()
        let vm = this
        vm.readyMass = false
        // 选取当前窗口范围的点
        // 根据缩放级别和中心点，计算窗口范围
        vm.zoomed = map.getZoom()
        center = map.getCenter()
        vm.LngCenter = center.lng
        vm.LatCenter = center.lat
        console.log('center:',vm.LngCenter,vm.LatCenter)
        console.log('zoomed:',vm.zoomed)
        let LngDelta = 1310.719999*Math.pow(2.71828, -0.693147 * vm.zoomed)
        let left = vm.LngCenter - LngDelta
        let right = vm.LngCenter + LngDelta
        // let LatDelta = 363.724800*Math.pow(2.71828, -0.693147 * vm.zoomed)
        let LatDelta = 550.724800*Math.pow(2.71828, -0.693147 * vm.zoomed)
        let top = vm.LatCenter - LatDelta
        let bottom = vm.LatCenter + LatDelta
        // console.log('center:', vm.LngCenter, vm.LatCenter,'\n', '左：', left, '\n', '右：', right, '\n', '上：', top, '\n', '下：', bottom, '\n')

        if(useRam==0){
          _markers = markers
        }else{
          _markers = vm.markers
        }
        _markers.forEach(function(marker) {

          if(marker.position[0] > right){
            return 0
          }else if(marker.position[0] < left){
            return 0
          }else if(marker.position[1] < top){
            return 0
          }else if(marker.position[1] > bottom){
            return 0
          }
          console.log('In the area')
          if(marker.extData.salesmanNum != 0){
            new AMap.Marker({
              map: map,
              content: vm.setPointNum(marker.extData.salesmanNum, marker.extData.check, marker.extData.name),
              position: [marker.position[0],marker.position[1]],
              extData: marker.extData,
              offset: new AMap.Pixel(-10, -28),
              label: marker.label
            });
          }else{
            markerContent = '' +
            '<div class="custom-content-marker" info="'+ marker.extData.elec +'" name="'+  marker.extData.name +'" onclick="showInfo(this)">' +
            '   <img src="/map/img?name=blue.png">' +
            '   <div class="lable" >'+marker.extData.name+'</div>' +
            '</div>';

            new AMap.Marker({
              map: map,
              content: markerContent,
              position: [marker.position[0],marker.position[1]],
              extData: marker.extData,
              label: marker.label
            });
          }
        });
      },
      showMassLayer(){
        let vm = this
        // 创建 AMap.LabelsLayer 图层
        var layer = new AMap.LabelsLayer({
          zooms: [3, 20],
          zIndex: 1000,
          collision: false
        });
        vm.layer = layer
        var markers = [];
        var icon = {
            type: 'image',
            image: 'https://application.companyservice.xmtyet.com/map/img?name=blue.png',
            size: [9, 13.5],
            anchor: 'bottom-center',
        };

        if(vm.markers.length > 0){
            console.log('数据已加载， 直接添加 layer')
            map.clearMap()
            // 将图层添加到地图
            map.add(layer);
            for(i of vm.markers){
              markerContent = '' +
              '<div class="custom-content-marker" info="'+ i.extData.elec +'" name="'+  i.extData.name +'" onclick="showInfo(this)">' +
              // '   <img src="/map/img?name=blue.png">' +
              '   <div class="lable" v-if="showLable">'+i.extData.name+'</div>' +
              '</div>';
              var curPosition = [i.position[0], i.position[1]];
              var curData = {
                  position: curPosition,
                  icon
              };
              var labelMarker = new AMap.LabelMarker(curData);
              markers.push(labelMarker);
            }
            // 一次性将海量点添加到图层
            layer.add(markers);
            vm.readyMass = true
            console.log('markers:',markers)
        }else{
          console.log('数据未加载， 请求再添加 layer')
          if(!vm.isGeting){
                vm.isGeting = true
                axios.get('https://application.companyservice.xmtyet.com/map/allmarkers?selected_id=')
                .then(function (response) {
                    vm.isGeting = false
                    map.clearMap()
                    // 将图层添加到地图
                    map.add(layer);
                    // var massData = []
                    var textStyle = {
                    fontSize: 0,
                    fontWeight: 'normal',
                    fillColor: '#22886f',
                    strokeColor: '#fff',
                    strokeWidth: 0,
                    fold: true,
                    padding: '2, 5',
                    };
                  vm.markers = response.data.data.markers
                  for(i of response.data.data.markers){
      
                          (i.position[0]+i.position[1]).toString
                          vm.nameDict[(i.position[0]+i.position[1]).toString()] = i.extData.name
                          var curPosition = [i.position[0], i.position[1]];
                          var curData = {
                              position: curPosition,
                              text:i.extData.name,
                              icon
                          };
          
                          var labelMarker = new AMap.LabelMarker(curData);
                          // 给marker绑定事件
                          labelMarker.on('mouseover', function(e){
                              // console.log(vm.nameDict)
                              // console.log((e.data.data.position[0]+e.data.data.position[1]).toString())
                              markerContent = '' +
                              '<div class="custom-content-marker" ' +
                              '   <div class="lable_layer" v-if="showLable">'+vm.nameDict[(e.data.data.position[0]+e.data.data.position[1]).toString()]+'</div>' +
                              '</div>';
                              var position = e.data.data && e.data.data.position;
                              if(position){
                                  normalMarker.setContent(markerContent);
                                  normalMarker.setPosition(position);
                                  map.add(normalMarker);
                              }
                          });
          
                          labelMarker.on('mouseout', function(){
                              map.remove(normalMarker);
                          });
                          markers.push(labelMarker);
                    }
                    // 一次性将海量点添加到图层
                    layer.add(markers);
                    vm.readyMass = true
                    console.log('markers:',markers)
                })
          }else{
            console.log('已在请求...')
          }
          
        }

        // 普通点
        var normalMarker = new AMap.Marker({
            anchor: 'bottom-center',
            offset: [0, -15],
        });
      },
      getAllMarker(e, get=1){  // 默认重新获取所有标记点
            let vm = this
            if(vm.markers.length > 0 && get==0){
              console.time('showMarker ready')
              vm.showMarker()  // 使用缓存的数据
              console.timeEnd('showMarker ready')
              var allCustom = document.getElementById('allCustom')
              allCustom.setAttribute('style', 'border: solid 2px #fb7a7ac2');
              var notCustom = document.getElementById('notCustom')
              notCustom.setAttribute('style', 'border: solid 2px #e1e1e1c2');
              var readyCustom = document.getElementById('readyCustom')
              readyCustom.setAttribute('style', 'border: solid 2px #e1e1e1c2');
            }else{
              if(!vm.isGeting){
                vm.isGeting = true
                axios.get('/map/allmarkers?selected_id=',e)
                .then(function (response) {
                  vm.isGeting = false
                  map.clearMap()
                  vm.markers = response.data.data.markers
                  console.log('vm.markers:',vm.markers.length)
                  console.time('showMarker new')
                  vm.showMarker() // 使用新获取的 缓存的数据
                  console.time('showMarker new')
                  var allCustom = document.getElementById('allCustom')
                  allCustom.setAttribute('style', 'border: solid 2px #fb7a7ac2');
                  var notCustom = document.getElementById('notCustom')
                  notCustom.setAttribute('style', 'border: solid 2px #e1e1e1c2');
                  var readyCustom = document.getElementById('readyCustom')
                  readyCustom.setAttribute('style', 'border: solid 2px #e1e1e1c2');
                })
                .catch(function (error) {
                  console.log(error);
                });
              }
              console.log('已在请求...')
            }
        },
      sendSelected(){  // 上传所选标记点
          let vm = this
          console.log('vm._idList:'+vm._idList)
          axios.post('/map/SelectMarkers', {
            idList: vm._idList,
            salesman: document.getElementById('salesman').value
          })
          .then(function (response) {
            console.log(response);
            let link__ = 'https://application.companyservice.xmtyet.com/map/part/?='+response.data.selected_id
            alert(link__)
            // clipBoardContent = link__
            // window.clipboardData.setData("Text",clipBoardContent);

            document.getElementById('link_').innerText = link__
            map.clearMap();
            vm.getAllMarker()
          })
          .catch(function (error) {
            console.log(error);
          });
        },
      drawToSelect(e){
        ele = document.getElementById('drawToSelect')
        ele.setAttribute('style','background-color: #a8deff')
        draw('polygon')
      },
      filterByElec(){
        let vm = this
        vm.elec_markers = vm.markers
        _markers = vm.markers
        _markers.forEach(function(marker) {})
        vm.markers
      }
    }
})

var map = new AMap.Map('container', {
    resizeEnable: true,
    center: [104.066547,30.659825],
    mapStyle: "amap://styles/whitesmoke",
    zoom: 13
});

image = 'https://a.amap.com/jsapi_demos/static/demo-center/icons/poi-marker-default.png'
// map.clearMap();  // 清除地图覆盖物

// 获取区域id
var url = window.location.href;
let id = url.split("selected_id")[1]
// alimap.getAllMarker(id)


var mouseTool = new AMap.MouseTool(map);
//监听draw事件可获取画好的覆盖物
var overlays = [];
var overlayPath = [];
var inner = [];

var icon_blue = new AMap.Icon({
  size: new AMap.Size(28, 38),    // 图标尺寸
  image: '/map/img?name=blue.png',  // Icon的图像
  // imageOffset: new AMap.Pixel(0, 0),  // 图像相对展示区域的偏移量，适于雪碧图等
  imageSize: new AMap.Size(19, 32)   // 根据所设置的大小拉伸或压缩图片
});

var icon_red = new AMap.Icon({
  size: new AMap.Size(28, 38),    // 图标尺寸
  image: '/map/img?name=red.png',  // Icon的图像
  imageOffset: new AMap.Pixel(0, 0),  // 图像相对展示区域的偏移量，适于雪碧图等
  imageSize: new AMap.Size(19, 32)   // 根据所设置的大小拉伸或压缩图片
});

function drawToSelect(){
  console.log('drawToSelect')
  mapoffALL()
  alimap.drawToSelect()
}

// 关键函数 配置项
mouseTool.on('draw',function(e){
  overlays.push(e.obj);  // e 是绘制结果，是一个多个点组成的path
  // console.log(e.obj.getPath())
  overlayPath = e.obj.getPath()  //  添加范围多边形，以框选 Marker
  // 根据上面所绘制的多边形区域为判断依据，对所有的marker遍历判断
  var allMarkers = map.getAllOverlays('marker');
  console.log('allMarkers.length:'+allMarkers.length)
  inner = []; // 清空
  for (let i = 0; i < allMarkers.length; i++) {  // 遍历全部标记点数据，3w个点，不知道耗时多少
      console.log('i: '+i)
      var point = allMarkers[i].getPosition();
      var isPointInRing = AMap.GeometryUtil.isPointInRing(
      point,
      overlayPath
      );
      if(isPointInRing){    //判断条件可以换成e.obj.contains(point)
          console.log('In the ring : ' + allMarkers[i].getExtData().id)
          allMarkers[i].setIcon('/map/img?name=red.png')
          console.log('getIcon: ' + allMarkers[i].getIcon())
          inner.push(allMarkers[i].getExtData().id); 
      }
  }
  alimap._idList = inner
  mouseTool.close(false)
  e.obj.on('click', function(){
    ele = document.getElementById('drawToSelect')
    ele.setAttribute('style','background-color: #f3f3f38f')
    if(alimap.salesmanNum==0){
      alert("请选择销售——")
      return 0
    }
    if (confirm("是否标记该区域？") == true) {
      alimap.sendSelected()
      maponALL()
    } else {
      maponALL()
      text = "You canceled!";
    }
  })
  // console.log(inner)
})


var showNum = 1

function showNumber(){
  var blockNmber = document.getElementsByClassName('close-btn')
  var checkNmber = document.getElementsByClassName('close-btn-check')
  if(showNum==1){
    for(lable of blockNmber){
      lable.setAttribute('style', 'display: none');
    }
    for(lable of checkNmber){
      lable.setAttribute('style', 'display: none');
    }
    showNum = 0
  }else{
    for(lable of blockNmber){
      lable.setAttribute('style', 'display: block');
    }
    for(lable of checkNmber){
      lable.setAttribute('style', 'display: block');
    }
    showNum = 1
  }
}

var showlable = 0

function showLable(){
  var allLable = document.getElementsByClassName('lable')
  ele = document.getElementById('showLable')
  if(showlable==1){
    ele.setAttribute('style','background-color: #e1e1e1c2')
    for(lable of allLable){
      lable.setAttribute('style', 'display: none');
    }
    showlable = 0
  }else{
    ele.setAttribute('style','background-color: #a8deff')
    for(lable of allLable){
      lable.setAttribute('style', 'display: block');
    }
    showlable = 1
  }
}

function showAll(){
  if(alimap.readyMass){
    alert('请缩小地图再查询')
  }else{
    alimap.getAllMarker(get=0)
  }

}

function showReady(){
  if(alimap.readyMass){
    alert('请缩小地图再查询')
  }else{
    alimap.getGivenorNot(1)
  }

}

function showNot(){
  if(alimap.readyMass){
    alert('请缩小地图再查询')
  }else{
    alimap.getGivenorNot(0)
  }
  
}


function draw(type){
  switch(type){
    case 'polygon':{
        mouseTool.polygon({
          fillColor:'#00b0ff',
          strokeColor:'#80d8ff'
          //同Polygon的Option设置
        });
        break;
    }
    case 'rectangle':{
        mouseTool.rectangle({
          fillColor:'#00b0ff',
          strokeColor:'#80d8ff'
          //同Polygon的Option设置
        });
        break;
    }
    case 'circle':{
        mouseTool.circle({
          fillColor:'#00b0ff',
          strokeColor:'#80d8ff'
          //同Circle的Option设置
        });
        break;
    }
  }
}
var radios = document.getElementsByName('func');
for(var i=0;i<radios.length;i+=1){
    radios[i].onchange = function(e){
      draw(e.target.value)
    }
}

// 销售切换
$("#salesman").off("change");
$("#salesman").on("change",function(){
    salesman = document.getElementById('salesman').value
    alimap.salesmanNum = salesman
    // if(salesman==0){  // 全部销售，即已分配
    //   alimap.getGivenorNot(1)
    // }else{
    //   alimap.getGivenBySalesman(salesman)
    // }
})

function showInfo(e){
  companyName = e.getAttribute('name')
  elec = e.getAttribute('info')  //电量
  alert(companyName+' 的预估全年电量是：'+elec)
}

function mapZoomend(){
  console.time('mapZoomend')
  // 隐藏标签
  ele = document.getElementById('showLable')
  ele.setAttribute('style','background-color: #e1e1e1c2')
  //

  zoomed = map.getZoom()
  center = map.getCenter()
  console.log('zoomend: ',zoomed)
  alimap.LngCenter = center.lng
  alimap.LatCenter = center.lat
  if(zoomed<16){
    if(!alimap.readyMass){
      console.log('未加载layer')
      map.clearMap()
      alimap.showMassLayer()
      alimap.readyMass = true
    }else{
      console.log('已经加载layer')
    }
  }else{
    // map.clearMap()
    alimap.readyMass = false
    alimap.layer.clear()
    console.time('getAllMarker')
    alimap.getAllMarker()
    console.timeEnd('getAllMarker')
 }
 console.timeEnd('mapZoomend')

}

function getExcel(){
  document.getElementById("get_excel").click();
}


mapZoomend() 

function maponALL(){
  map.on('zoomend', mapZoomend);
  map.on('dragstart', mapZoomend);
}

maponALL()

function mapoffALL(){
  map.off('zoomend', mapZoomend);
  map.off('dragstart', mapZoomend);
}


var placeSearch = {}

AMap.plugin(["AMap.PlaceSearch"], function() {
  //构造地点查询类
    placeSearch = new AMap.PlaceSearch({
      pageSize: 5, // 单页显示结果条数
      pageIndex: 1, // 页码
      city: "028", // 兴趣点城市
      citylimit: true,  //是否强制限制在设置的城市内搜索
      map: map, // 展现结果的地图实例
      panel: "panel", // 结果列表将在此容器中进行展示。
      autoFitView: true // 是否自动调整地图视野使绘制的 Marker点都处于视口的可见范围
  });
  //关键字查询
  // placeSearch.search('红牌楼');
});

function search(){
  let name = document.getElementById('search_').value
  placeSearch.search(name);
  zoomed = map.setZoom(16)
}


// document.getElementById('clear').onclick = function(){
//     map.remove(overlays)
//     overlays = [];
// }
// document.getElementById('close').onclick = function(){
//     mouseTool.close(true)//关闭，并清除覆盖物
//     for(var i=0;i<radios.length;i+=1){
//         radios[i].checked = false;
//     }
// }
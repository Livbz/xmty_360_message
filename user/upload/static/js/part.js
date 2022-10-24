
var alimap = new Vue({
    el: "#container",
    delimiters: ['${', '}'],
    data:{
        markers: [],
        curPosition: [],
        showORgoto: true,
        canDrag: false
    },
    methods:{
        showExdata(e){
          let vm = this
          vm.showORgoto = !vm.showORgoto
        },
        getAllMarker(e){  // 获取所有标记点
            let vm = this
            axios.get('/map/allmarkers/',{
              params: {
                selected_id: e
              }
            })
            .then(function (response) {
              vm.markers = response.data.data.markers
              console.log(response)
              // 点标记显示内容，HTML要素字符串
              // var markerContent = '' +
              // '<div class="custom-content-marker">' +
              // '   <img src="//a.amap.com/jsapi_demos/static/demo-center/icons/dir-via-marker.png">' +
              // '   <div class="close-btn">1</div>' +
              // '</div>';
              map.clearMap();
              function setContent(type, name){
                if(type == 'red'){
                  markerContent_checked = '' +
                  '<div class="custom-content-marker">' +
                  '   <img src="/map/img?name=red.png">' +
                  '   <div class="lable" >' + name + '</div>' +
                  '</div>'
                }else{
                  markerContent_checked = '' +
                  '<div class="custom-content-marker">' +
                  '   <img src="/map/img?name=blue.png">' +
                  '   <div class="lable" >' + name + '</div>' +
                  '</div>'                  
                }

                return markerContent_checked
              }


              vm.markers.forEach(function(marker) {
                if(marker.extData.check != 0){
                  console.log('red' + marker.extData.id)
                  new AMap.Marker({
                    map: map,
                    content: setContent('red', marker.extData.name),
                    // icon: '/map/img?name=red.png',
                    position: [marker.position[0],marker.position[1]],
                    extData: marker.extData,
                    offset: new AMap.Pixel(-10, -28),
                    label: marker.label
                  });
                }else{
                  console.log('blue' + marker.extData.id)
                  new AMap.Marker({
                    map: map,
                    // draggable: true,
                    content: setContent('blue', marker.extData.name),
                    position: [marker.position[0],marker.position[1]],
                    extData: marker.extData,
                    offset: new AMap.Pixel(-10, -28),
                    label: marker.label
                  });
                }
              });

              var allMarkers = map.getAllOverlays('marker');
              for (let i = 0; i < allMarkers.length; i++){  // 遍历全部标记点数据，3k个点，不知道耗时多少
                  allMarkers[i].on('click', function(e){

                    if(vm.showORgoto){
                      if(confirm('导航前往目的地？')){
                        vm.api_goto([e.lnglat.getLng(),e.lnglat.getLat()])  // 调用api在新开页面进行导航
                      }
                    }else{
                      console.log(e.target.getExtData().phone)
                      let msg = e.target.getExtData().name + '\n' +
                      '地址：' + e.target.getExtData().address + '\n联系电话:' + e.target.getExtData().phone
                      + '\n预计电量:' +e.target.getExtData().elec
                      alert(msg)
                    }
                      
                  })

              }
            })
            .catch(function (error) {
              console.log(error);
            });
        },
        goto(e){
          // 获取当前位置
          let vm = this
          vm.getPosition(e)
        },
        api_goto(dest){
          AMap.plugin('AMap.Geolocation', function() {
            var geolocation = new AMap.Geolocation({
              enableHighAccuracy: true,//是否使用高精度定位，默认:true
              timeout: 10000,          //超过10秒后停止定位，默认：5s
              buttonPosition:'RB',    //定位按钮的停靠位置
              buttonOffset: new AMap.Pixel(10, 20),//定位按钮与设置的停靠位置的偏移量，默认：Pixel(10, 20)
              zoomToAccuracy: true,   //定位成功后是否自动调整地图视野到定位点
            });
            geolocation.getCurrentPosition(function(status,result){
              if(status=='complete'){
                  console.log(result.position)
                  let curPosition = [result.position.lng,result.position.lat]
                  goto_url = 'https://uri.amap.com/navigation?from=' +
                              curPosition[0].toString() +','+ curPosition[1].toString() + 
                              ',startpoint&to=' +
                              dest[0].toString() +','+ dest[1].toString() + 
                              ',endpoint&mode=car&policy=1&src=mypage&coordinate=gaode&callnative=0'
                  
                  window.location.href = goto_url
              }else{
                  alert("定位失败，请开启手机定位")
              }
            } );

          })
        },
        getPosition(e){
            let vm = this
            AMap.plugin('AMap.Geolocation', function() {
              var geolocation = new AMap.Geolocation({
                  enableHighAccuracy: true,//是否使用高精度定位，默认:true
                  timeout: 10000,          //超过10秒后停止定位，默认：5s
                  buttonPosition:'RB',    //定位按钮的停靠位置
                  buttonOffset: new AMap.Pixel(10, 20),//定位按钮与设置的停靠位置的偏移量，默认：Pixel(10, 20)
                  zoomToAccuracy: true,   //定位成功后是否自动调整地图视野到定位点
      
              });
              map.addControl(geolocation);
              geolocation.getCurrentPosition(function(status,result){
                  if(status=='complete'){
                      // onComplete(result) 
                      console.log(result.position)
                      vm.curPosition = [result.position.lng,result.position.lat]
                      
                      //根据起、终点坐标查询公交换乘路线
                      AMap.plugin(['AMap.Transfer'],function(){//异步同时加载多个插件
                        var transferOption = {
                          map: map,
                          nightflag: true, // 是否计算夜班车
                          city: '成都市',
                          // panel: 'panel',
                          outlineColor: '#ffeeee',
                          autoFitView: true,
                          policy: AMap.TransferPolicy.LEAST_TIME // 其它policy取值请参照 https://lbs.amap.com/api/javascript-api/reference/route-search#m_TransferPolicy
                        }
                        var transfer = new AMap.Transfer(transferOption)
                        //test
                        console.log('start',vm.curPosition[0],vm.curPosition[1])
                        start = new AMap.LngLat(vm.curPosition[0],vm.curPosition[1])
                        a = new AMap.LngLat(104.11055,30.627273)
                        // b = new AMap.LngLat(104.10056,30.616261)
                        //test
                        transfer.search(start, e, function(status, result) {
                            // result即是对应的公交路线数据信息，相关数据结构文档请参考  https://lbs.amap.com/api/javascript-api/reference/route-search#m_TransferResult
                          if (status === 'complete') {
                              log.success('绘制公交路线完成')
                          } else {
                              // log.error('公交路线数据查询失败' + result)
                          }
                          
                        });
                      });
                  }else{
                      // onError(result)
                  }
              });
            });

            //解析定位结果
            function onComplete(data) {
                document.getElementById('status').innerHTML='定位成功'
                var str = [];
                str.push('定位结果：' + data.position);
                str.push('定位类别：' + data.location_type);
                if(data.accuracy){
                    str.push('精度：' + data.accuracy + ' 米');
                }//如为IP精确定位结果则没有精度信息
                str.push('是否经过偏移：' + (data.isConverted ? '是' : '否'));
                document.getElementById('result').innerHTML = str.join('<br>');
            }

            //解析定位错误信息
            function onError(data) {
                document.getElementById('status').innerHTML='定位失败'
                document.getElementById('result').innerHTML = '失败原因排查信息:'+data.message;
            }
        }
    }
})

var map = new AMap.Map('container', {
    resizeEnable: true,
    center: [104.066547,30.659825],
    zoom: 13
});

image = 'https://a.amap.com/jsapi_demos/static/demo-center/icons/poi-marker-default.png'
map.clearMap();  // 清除地图覆盖物

// 获取区域id
var url = window.location.href;
let id = url.split("=")[1]
alimap.getAllMarker(id)

function showInfo(){
  alimap.showExdata()
  ele = document.getElementById('showBotton')
  if(ele.innerHTML == '点击显示公司详情'){
    ele.innerHTML = '点击导航至公司'
  }else{
    ele.innerHTML = '点击显示公司详情'
  }
}

function visit(marker){
  if(confirm('已拜访' + marker.target.getExtData().name + '?')){
    axios.get('/map/check/',{
      params: {
        id: marker.target.getExtData().id
      }
    })
    .then(function (response) {
      console.log(response)
    }
    )
  }
  location.reload();
}

function canDrag(){
  var allMarkers = map.getAllOverlays('marker');
  for (let i = 0; i < allMarkers.length; i++){  // 遍历全部标记点数据，3k个点，不知道耗时多少
    allMarkers[i].setDraggable(true)
    allMarkers[i].on('dragstart', function(e){
      visit(e)
    })
  }
  ele = document.getElementById('infoSpan')
  ele.setAttribute('style', 'background-color: #03a9f4')
}










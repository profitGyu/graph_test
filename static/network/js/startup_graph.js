const ROOT_PATH = location.protocol + '//' + location.host
console.log(ROOT_PATH)




// 페이지 첫 시작시 생성 되어야하는 것들
$().ready(function(){

    $('.js-ion-range-slider').each(function () {
      $.HSCore.components.HSIonRangeSlider.init($(this));
    });
//  산업 분류 드롭다운
    var industrialClassList = $('#industrialClassList')
    industrialClassList.empty()
    color_list = Object.keys(INDUSTRIAL_DICT)
    color_list.forEach(color => makeIndustrialCheckbox(industrialClassList, color))

// 투자 단계 드롭다운
    var phaseCheckBox = $("#phaseCheckBox")
    phaseCheckBox.empty()
    phase_list = Object.keys(PHASE_DICT)
    phase_list.forEach(phase => makePhaseCheckbox(phaseCheckBox, phase))
});



//$.ajax({
//        url: ROOT_PATH+'/api/v1',
//        type:"GET",
//        data:{
//
//        },
//        dataType:'json',
//        success:function(data){
//            console.log("안녕~")
//        }
//
//    })

/*검색 하여 네트워크 그래프 생성*/
function getNetworkGraph(){

    var company = $('#company').val()
    var phase= $('input[name="phase"]:checked')
    var industrial = $("input[name='industrialDiv']:checked")
    var capital = $('#capital').val()
    var ageMin = $('#ageMin').val()
    var ageMax = $('#ageMax').val()
    var invMin = $('#invMin').val()
    var invMax = $('#invMax').val()

    var phase_list = []
    phase.each(function(){
        phase_list.push(this.value)
    })

    var industrial_list = []
    industrial.each(function(){
        industrial_list.push(this.value)
    })
    if(industrial_list.length===0){
        industrial_list.push('')
    }
    console.log(industrial_list)
    $.ajax({
    url: ROOT_PATH+'/api/v1/',
    type:"POST",
    data:{
        "company": company,
        "industrial": industrial_list,
        "phase": phase_list,
        "capital": capital
    },
    dataType:'json',
    success:function(data){
        console.log(data)
        data_count = data.length-1
         /*산업 분류 테그 생성 START*/
        var industrialTagFrom = $('#industrialTagFrom')
        var color_list = data[data_count]["color_list"]
        industrialTagFrom.empty()
        for(color in color_list){
            makeIndustrialTag(industrialTagFrom ,color_list[color])
        }
        /* 산업분류 태그 생성 END*/

        var networkCount = $('#networkCount')
        var IndustrialCount = $('#IndustrialCount')
        networkCount.empty()
        makeListFromCountTag(networkCount, data_count)
        IndustrialCount.empty()
        makeListFromCountTag(IndustrialCount, color_list.length)
        /*네트워크 그래프 생성*/
        data.pop()
        MakeStartupNetworkChart(data);

    },
    error: function(data){
        alert("검색결과가 없습니다.")
    }
    })
}


/* 산업 분류 책크박스 설정 하는 함수 */
function getCategoryList(){
    console.log("산업분류 클릭 확인:")
    var company = $('#company').val()
    var industrialClassList = $('#industrialClassList')
    $.ajax({
        url: ROOT_PATH+'/api/v1/category',
        type:"POST",
        data:{
            "company": company,
        },
        dataType:'json',
        success:function(data){
            /* 산업 분류 창 만들어주는 함수*/
            industrial_data = data["color_list"]
            var industrialClassList = $('#industrialClassList')
            industrialClassList.empty()
            color_list = Object.keys(INDUSTRIAL_DICT)
            color_list.forEach(color => makeIndustrialCheckbox(industrialClassList, color))
            var industrial = $(".industrialCheckbox")
            industrial.prop('disabled', true)
            exist_list = []
            industrial_data.forEach(val => exist_list.push(INDUSTRIAL_DICT[val]))

            for(i=0; i<industrial.length; i++){
                exist_list.forEach(function(val){
                    console.log(industrial[i].value)
                    if(val == industrial[i].value){
                        industrial[i].disabled = false;
                    }
                })
            }

            /* 검색시 존재하는 투자 단계만 보여주기 */
            phase_data = data["phase_list"]
            var phaseCheckbox = $(".phaseCheckbox")
            phaseCheckbox.prop('disabled', true)
            exist_phase_list = []
            phase_data.forEach(val => exist_phase_list.push(PHASE_DICT[val]))
              for(i=0; i<phaseCheckbox.length; i++){
                exist_phase_list.forEach(function(val){
                    if(val == phaseCheckbox[i].value){
                        phaseCheckbox[i].disabled = false;
                    }
                })
            }
        }
    })
}


function getCategoryList(category){
    console.log(category)
    console.log("산업분류 클릭 확인:")
    var company = $('#company').val()
    var industrialClassList = $('#industrialClassList')
    $.ajax({
        url: ROOT_PATH+'/api/v1/category',
        type:"POST",
        data:{
            "company": company,
        },
        dataType:'json',
        success:function(data){
            /* 산업 분류 창 만들어주는 함수*/
            if(category === "industrial"){
               industrial_data = data["color_list"]
                var industrialClassList = $('#industrialClassList')
                industrialClassList.empty()
                color_list = Object.keys(INDUSTRIAL_DICT)
                color_list.forEach(color => makeIndustrialCheckbox(industrialClassList, color))
                var industrial = $(".industrialCheckbox")
                industrial.prop('disabled', true)
                exist_list = []
                industrial_data.forEach(val => exist_list.push(INDUSTRIAL_DICT[val]))

                for(i=0; i<industrial.length; i++){
                    exist_list.forEach(function(val){
                        if(val == industrial[i].value){
                            industrial[i].disabled = false;
                        }
                    })
                }
            }else if(category === "phase"){
                   /* 검색시 존재하는 투자 단계만 보여주기 */
                var phaseCheckBox = $("#phaseCheckBox")
                phaseCheckBox.empty()
                phase_list = Object.keys(PHASE_DICT)
                phase_list.forEach(phase => makePhaseCheckbox(phaseCheckBox, phase))
                phase_data = data["phase_list"]
                var phaseCheckbox = $(".phaseCheckbox")
                phaseCheckbox.prop('disabled', true)
                exist_phase_list = []
                phase_data.forEach(val => exist_phase_list.push(PHASE_DICT[val]))
                  for(i=0; i<phaseCheckbox.length; i++){
                    exist_phase_list.forEach(function(val){
                        if(val == phaseCheckbox[i].value){
                            phaseCheckbox[i].disabled = false;
                        }
                    })
                }
                var noneSelect = $("#noneSelect")
                var all = $('#all')
                noneSelect.prop("checked", false)
                all.prop('disabled', false)
            }



        }
    })
}


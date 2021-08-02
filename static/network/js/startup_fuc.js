// 산업 분류 카테고리
const INDUSTRIAL_DICT = {'#771DAE': '0', '#67DC75': '1', '#2A1DBD': '2', '#F83F97': '3', '#F1B200': '4','#F30259': '5', '#009E4F': '6', '#0058FF': '7',
                        '#FD7D20': '8', '#FF3100': '9', '#7151A5': '10', '#036174': '11', '#303173': '12','#ECA406': '13', '#5C33F6': '14',
                        '#B8307C': '15', '#0C5C22': '16', '#0085FF': '17', '#FD7159': '18', '#6A75B3': '19','#A367DC': '20'}
// 투자 단계 카테고리
const PHASE_DICT = {'전체선택': '0','선택안함': '1', '투자 단계 비공개': '2', '미입력': '3', 'Series A': '4', 'Series B': '5',
                    'Series C': '6', 'Series D': '7', 'Seed': '8', 'Angel': '9', 'Pre-IPO': '10','Pre-A': '11'}

/* phase select 전체 선택 해주는 함수*/
async function phaseAllSelect(){
       phase=$('input:checkbox[name="phase"]');
       phase_test = $('.phaseCheckbox')
       if(phase_test.is(':disabled') == true){

       }
       if($('input:checkbox[id="all"]').is(":checked")==true){
        phase.prop('checked',true);
        $('input:checkbox[id="noneSelect"]').prop('checked', false);
       }else{
        phase.prop('checked',false);
        $('input:checkbox[id="noneSelect"]').prop('checked', true);
       }
    }

/* phase 전체선택 해재 함수*/
async function phaseAllNotSelect(){
        console.log("not 이벤트 되요")
        phase=$('input:checkbox[name="phase"]');
        if($('input:checkbox[id="noneSelect"]').is(":checked")==true){
            $('input:checkbox').prop('checked', false)
            $('input:checkbox[id="noneSelect"]').prop('checked',true)
        }
    }

/* #listFrom에 있는 산업분류 테그 생성 함수*/
async function makeIndustrialTag(id, color){
      var html = '';
      html += '<a class="btn icon-btn" href="#">'
      html += '<button type="button" class="btn btn-banger btn-circle btn-sm" style="background:'+color+'"></button>'
      html += INDUSTRIAL_DICT[color]+'</a>'
      id.append(html)
}

/* #listFrom에 있는 기업네트워크, 산업분류 창 만드는 함수*/
async function makeListFromCountTag(id,count){
        var html = '';
        html += '<span class="indus font-size-2">'+count+'개</span><span>의</span>'
        if(id[0]["id"] =="networkCount"){
            html += '<div class="font-size-1">기업네트워크</div>'
        }else if(id[0]["id"] =="IndustrialCount"){
            html += '<div class="font-size-1">산업분류</div>'
        }
        id.append(html)
}

/*산업 분류 책크박스 만들어주는 함수*/
async function makeIndustrialCheckbox(id, color){
        var industrial_id = INDUSTRIAL_DICT[color];
        var html =  "";
        html += '<div class="form-check btn icon-btn">'
        html += '<input class="industrialCheckbox form-check-input" type="checkbox" name="industrialDiv" value="'+industrial_id+'" id="industrialDiv'+industrial_id+'">'
        html += '<label class="form-check-label" for="all" value="0">'+color+'</label>'
        html += '</div>'
        id.append(html)
}

async function makePhaseCheckbox(id, phase){
        var value = PHASE_DICT[phase];
        phase_id= "test"+ value
        if(value == "0"){
            phase_id = "all"
        }else if(value == "1"){
            phase_id= "noneSelect"
        }
        var html = ""
        html += '<li class="list-group-item"><div class="form-check">'
        if(phase_id == "all"){
            html += '<input class="phaseCheckbox form-check-input" type="checkbox" name="phase" value="'+value+'" id="'+phase_id+'" onclick="phaseAllSelect();">'
        }else if(phase_id == "noneSelect"){
            html += '<input class="phaseCheckbox form-check-input" type="checkbox" name="phase" value="'+value+'" id="'+phase_id+'" onclick="phaseAllNotSelect();" checked>'
        }else{
            html += '<input class="phaseCheckbox form-check-input" type="checkbox" name="phase" value="'+value+'" id="'+phase_id+'">'
        }

        html += '<label class="form-check-label" for="'+phase_id+'" value="'+phase+'">'+phase+'</label>'
        html += '<div></li>'
        id.append(html)
}
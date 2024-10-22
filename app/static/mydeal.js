const changeStatusBtn = document.getElementById('changeStatusBtn');
const progressBar = document.getElementById('progressBar');
const steps = document.querySelectorAll('.step');

let currentStep = 0;  // 현재 단계 (0부터 시작)

changeStatusBtn.addEventListener('click', () => {
    // 거래 상태 창을 처음 버튼을 눌렀을 때만 표시
    if (progressBar.classList.contains('hidden')) {
        progressBar.classList.remove('hidden');
    }

    // 현재 단계 활성화
    if (currentStep < steps.length) {
        steps[currentStep].classList.add('active');
        currentStep++;
    }

    // 모든 단계가 활성화되면 버튼을 비활성화
    if (currentStep === steps.length) {
        changeStatusBtn.disabled = true;
        changeStatusBtn.innerText = "거래 완료";
    }
});


function changeButton() {
    var button = document.getElementById('statusButton');
    button.classList.add('gray');
    button.innerHTML = "완료됨";
    button.disabled = true;  // 버튼 비활성화
}




function addContent(contentId, productName, description) {
    const contentContainer = document.getElementById('content-container');
    
    // 새로운 content 요소 생성
    const newContent = document.createElement('div');
    newContent.classList.add('content');
    newContent.innerHTML = `
        <div class="product-section">
            <div class="aboutabout">
                <h4>${productName}</h4>
                <p>${description}</p>
            </div>
            <div style="display: flex; gap: 10px;">
                <button class="status-btn2 changeStatusBtn" data-id="${contentId}">현황 조회</button>
            </div>
        </div>
        <div class="progress-bar hidden" id="progressBar-${contentId}">
            <div class="step">
                <span><img src="loading.png" style="width:60px; height:60px;"></span>
                <p>거래 대기 중</p>
            </div>
            <div class="step">
                <span><img src="money.png" style="width:60px; height:60px;"></span>
                <p>수락 완료</p>
            </div>
            <div class="step">
                <span><img src="box.png" style="width:60px; height:60px;"></span>
                <p>사물함 크기 선택 완료</p>
            </div>
            <div class="step">
                <span><img src="puttt.png" style="width:60px; height:60px;"></span>
                <p>사물함 배치 완료</p>
            </div>
            <div class="step">
                <span><img src="check.png" style="width:60px; height:60px;"></span>
                <p>수령 완료</p>
            </div>
        </div>
    `;
    
    // 새 content를 컨테이너에 추가
    contentContainer.appendChild(newContent);
}

// 예시로 새 콘텐츠 추가
addContent('1', '상품 A', '상품 A의 설명입니다.');
addContent('2', '상품 B', '상품 B의 설명입니다.');


document.addEventListener('click', function(event) {
    // 클릭한 요소가 class="changeStatusBtn"을 가지고 있을 때만 동작
    if (event.target.classList.contains('changeStatusBtn')) {
        const contentId = event.target.getAttribute('data-id');
        const progressBar = document.getElementById(`progressBar-${contentId}`);
        progressBar.classList.toggle('hidden'); // 해당 콘텐츠의 상태 바를 숨기거나 보여줌
    }
});
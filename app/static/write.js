// 제목 입력 필드의 너비를 텍스트 길이에 따라 조정하는 함수
const titleField = document.getElementById('titlearea'); // 'titlearea'로 변경
if (titleField) {
  titleField.addEventListener('input', function() {
    this.style.width = 'auto'; // 너비 재설정
    this.style.width = this.scrollWidth + 'px'; // 텍스트 길이에 맞춰 확장
  });
}

// 가격 입력 필드에 숫자만 입력되도록 제한
const priceField = document.getElementById('pricearea'); // 'pricearea'로 변경
if (priceField) {
  priceField.addEventListener('input', function(e) {
    // 입력 값 중 숫자가 아닌 문자는 제거
    this.value = this.value.replace(/[^0-9]/g, ''); // 숫자가 아닌 문자 제거
  });
}


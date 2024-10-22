// 팝업을 보여주는 함수
function showPopup(message) {
    var popup = document.getElementById('popup');
    var popupMessage = document.getElementById('popup-message');
    popupMessage.textContent = message;
    popup.style.display = 'block';  // 팝업을 보이도록 설정
}

// 팝업을 닫는 함수
function closePopup() {
    var popup = document.getElementById('popup');
    popup.style.display = 'none';  // 팝업을 숨김
}

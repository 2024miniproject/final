<script>
  document.addEventListener('DOMContentLoaded', function() {
    fetchImages();

    // 주기적으로 이미지 목록을 갱신
    setInterval(fetchImages, 60000); // 60초마다 갱신

    function fetchImages() {
      fetch('/api/images') // 서버 API 호출
        .then(response => response.json())
        .then(data => {
          const columns = document.getElementById('columns');
          columns.innerHTML = ''; // 기존 내용을 비움
          
          data.forEach(item => {
            const figure = document.createElement('figure');
            const img = document.createElement('img');
            img.src = item.imageUrl; // 이미지 URL
            const figcaption = document.createElement('figcaption');
            figcaption.textContent = item.description; // 이미지 설명
            
            figure.appendChild(img);
            figure.appendChild(figcaption);
            columns.appendChild(figure);
          });
        })
        .catch(error => console.error('Error fetching images:', error));
    }
  });
</script>


///json api 응답

[
    {
      "imageUrl": "//s3-us-west-2.amazonaws.com/s.cdpn.io/4273/cinderella.jpg",
      "description": "Cinderella wearing European fashion of the mid-1860’s"
    },
    {
      "imageUrl": "//s3-us-west-2.amazonaws.com/s.cdpn.io/4273/rapunzel.jpg",
      "description": "Rapunzel, clothed in 1820’s period fashion"
    }
    // ... 추가 이미지
  ]


  //서버 측에서 /api/images 엔드포인트를 구현
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("upload-form");
  const fileInput = document.getElementById("pdf-file");
  const downloadSection = document.getElementById("download-section");
  const downloadLinks = document.getElementById("download-links");

  form.addEventListener("submit", async function (e) {
    e.preventDefault(); // 기본 폼 제출 방지

    const file = fileInput.files[0];
    if (!file) {
      alert("PDF 파일을 선택해주세요!");
      return;
    }

    const formData = new FormData();
    formData.append("pdf", file);

    try {
      // 서버로 POST 요청 보내기
      const response = await fetch("/convert", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("서버 오류: 변환 실패");
      }

      const data = await response.json();

      // 변환된 파일 링크 표시
      downloadLinks.innerHTML = "";
      data.images.forEach((imageUrl, index) => {
        const li = document.createElement("li");
        const link = document.createElement("a");
        link.href = imageUrl;
        link.download = `page_${index + 1}.png`;
        link.textContent = `📄 PNG 페이지 ${index + 1} 다운로드`;
        li.appendChild(link);
        downloadLinks.appendChild(li);
      });

      downloadSection.style.display = "block";
    } catch (error) {
      console.error("에러 발생:", error);
      alert("파일 변환 중 문제가 발생했습니다.");
    }
  });
});

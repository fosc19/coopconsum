// static/js/gallery.js

document.addEventListener("DOMContentLoaded", function () {
  const images = document.querySelectorAll(".image-gallery-img");
  const modal = document.getElementById("lightbox-modal");
  const modalImg = document.getElementById("modal-img");
  const closeBtn = document.querySelector(".gallery-modal-close");

  images.forEach(img => {
    img.addEventListener("click", () => {
      const fullSrc = img.getAttribute("data-full");
      modalImg.src = fullSrc;
      modal.classList.remove("hidden");
    });
  });

  closeBtn.addEventListener("click", () => {
    modal.classList.add("hidden");
    modalImg.src = "";
  });

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.classList.add("hidden");
      modalImg.src = "";
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      modal.classList.add("hidden");
      modalImg.src = "";
    }
  });
});
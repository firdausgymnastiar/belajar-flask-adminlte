function generateRandomNumber() {
  // Membuat angka acak antara 100000 dan 999999 (6 digit)
  var randomNumber = Math.floor(100000 + Math.random() * 900000);
  // Menampilkan angka acak di console
  console.log("Angka acak: " + randomNumber);
  // Menampilkan angka acak di halaman HTML
  document.getElementById("randomNumberDisplay").value = randomNumber;
}
// Deteksi apakah perangkat merupakan perangkat mobile
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

// Menangkap elemen input dan tombol
const cameraInput = document.getElementById("cameraInput");
const cameraButton = document.getElementById("cameraButton");
const preview = document.getElementById("preview");

// Menampilkan tombol hanya jika perangkat adalah perangkat mobile
if (isMobile) {
  cameraButton.style.display = "block";
}

// Menambahkan event listener untuk tombol
cameraButton.addEventListener("click", function () {
  // Membuka kamera saat tombol ditekan
  cameraInput.click();
});

// Menambahkan event listener ketika gambar dipilih
cameraInput.addEventListener("change", function () {
  // Memastikan ada file yang dipilih
  if (cameraInput.files && cameraInput.files[0]) {
    const reader = new FileReader();
    reader.onload = function (e) {
      // Menampilkan gambar yang dipilih sebagai preview
      preview.src = e.target.result;
    };
    // Membaca file gambar yang dipilih sebagai URL data
    reader.readAsDataURL(cameraInput.files[0]);
  }
});

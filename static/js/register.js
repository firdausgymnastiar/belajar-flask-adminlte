const formRegister = document.getElementById("formRegister");
// Deteksi apakah perangkat merupakan perangkat mobile
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

// Menangkap elemen input dan tombol
const gambarWajah = document.getElementById("gambarWajah");
const cameraButton = document.getElementById("cameraButton");
const ulangiCamera = document.getElementById("ulangiCamera");
const preview = document.getElementById("preview");

async function sendToServer() {
  const formData = new FormData(formRegister);

  const response = await fetch("/registerwajah", {
    method: "POST",
    body: formData,
  });
  try {
    if (response.ok) {
      // If the response is successful, show success message
      Swal.fire({
        icon: "success",
        title: "Success!",
        text: "berhasil di submit",
      }).then((result) => {
        // Redirect to a new page after clicking "OK"
        if (result.isConfirmed) {
          window.location.href = "/register"; // Ganti "/success-page" dengan URL halaman yang ingin Anda arahkan
        }
      });
    } else {
      // If there is an error in the response, show error message
      Swal.fire({
        icon: "error",
        title: "Error!",
        text: "respon dari server false. gagal di submit.",
      });
      window.location.href = "/register"; // Ganti "/success-page" dengan URL halaman yang ingin Anda arahkan
    }
  } catch (error) {
    // If there is an error in fetching or parsing the response, show error message
    Swal.fire({
      icon: "error",
      title: "Error!",
      text: "GAGAL MANGGIL API BE. gagal di submit.",
    });
    window.location.href = "/register"; // Ganti "/success-page" dengan URL halaman yang ingin Anda arahkan
  }
}

formRegister.addEventListener("submit", function (event) {
  event.preventDefault();
  sendToServer();
});

// Menambahkan event listener untuk tombol
cameraButton.addEventListener("click", function () {
  // Membuka kamera saat tombol ditekan
  gambarWajah.click();
});
// Menambahkan event listener untuk tombol
ulangiCamera.addEventListener("click", function () {
  // Membuka kamera saat tombol ditekan
  gambarWajah.click();
});
// Menambahkan event listener ketika gambar dipilih
gambarWajah.addEventListener("change", function () {
  // Memastikan ada file yang dipilih
  if (gambarWajah.files && gambarWajah.files[0]) {
    cameraButton.style.display = "none";
    ulangiCamera.style.display = "block";
    const reader = new FileReader();
    reader.onload = function (e) {
      // Menampilkan gambar yang dipilih sebagai preview
      preview.src = e.target.result;
    };
    // Membaca file gambar yang dipilih sebagai URL data
    reader.readAsDataURL(gambarWajah.files[0]);
  }
});

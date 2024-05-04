const emailAddress = document.getElementById("emailAddress");
const fullName = document.getElementById("fullName");
const nim = document.getElementById("nim");
const programStudi = document.getElementById("programStudi");
const angkatan = document.getElementById("angkatan");
const formRegister = document.getElementById("formRegister");

async function sendToServer() {
  const formData = new FormData();
  formData.append("emailAddress", emailAddress.value);
  formData.append("fullName", fullName.value);
  formData.append("programStudi", programStudi.value);
  formData.append("nim", nim.value);
  formData.append("angkatan", angkatan.value);

  const response = await fetch("/registerwajah", {
    method: "POST",
    body: formData,
  });
  try {
    const result = await response.json();
    if (response.ok) {
      // If the response is successful, show success message
      Swal.fire({
        icon: "success",
        title: "Success!",
        text: "berhasil di submit",
      });
    } else {
      // If there is an error in the response, show error message
      Swal.fire({
        icon: "error",
        title: "Error!",
        text: "respon dari server false. gagal di submit.",
      });
    }
  } catch (error) {
    // If there is an error in fetching or parsing the response, show error message
    Swal.fire({
      icon: "error",
      title: "Error!",
      text: "GAGAL MANGGIL API BE. gagal di submit.",
    });
  }
}

formRegister.addEventListener("submit", function (event) {
  event.preventDefault();

  const tes = fullName.value;
  console.log(tes);
  sendToServer();
});

// Deteksi apakah perangkat merupakan perangkat mobile
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

// Menangkap elemen input dan tombol
const gambarWajah = document.getElementById("gambarWajah");
const cameraButton = document.getElementById("cameraButton");
const ulangiCamera = document.getElementById("ulangiCamera");
const preview = document.getElementById("preview");

// Menampilkan tombol hanya jika perangkat adalah perangkat mobile
if (isMobile) {
  cameraButton.style.display = "block";
}
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

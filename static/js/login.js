const formLogin = document.getElementById("formLogin");
// Deteksi apakah perangkat merupakan perangkat mobile
// const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

// Menangkap elemen input dan tombol
const gambarWajah = document.getElementById("gambarWajah");
const cameraButton = document.getElementById("cameraButton");
const ulangiCamera = document.getElementById("ulangiCamera");
const preview = document.getElementById("preview");

async function sendToServer() {
  const formData = new FormData(formLogin);

  const response = await fetch("/loginkelas", {
    method: "POST",
    body: formData,
  });
  const responseData = await response.json();
  try {
    if (response.ok && responseData.success) {
      displayAlert(responseData);
    } else {
      // Jika permintaan gagal atau respons dari Flask menunjukkan kegagalan
      displayAlert(responseData.error_message || responseData.message);
    }
  } catch (error) {
    // Jika terjadi kesalahan dalam melakukan permintaan
    displayAlert("Terjadi kesalahan dalam mengirim permintaan");
    console.error("Error:", error);
  }
}

formLogin.addEventListener("submit", function (event) {
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

// Fungsi untuk menampilkan SweetAlert berdasarkan pesan dari server
function displayAlert(responseData) {
  let message = responseData.message; // Mengambil nilai dari kunci 'message'

  let alertTitle, alertIcon;

  // Menyesuaikan judul dan ikon berdasarkan pesan dari server
  switch (message) {
    case "Selamat Datang!":
      alertTitle = "Success!";
      alertIcon = "success";
      break;
    case "No file part":
    case "No selected file":
    case "Missing required data":
      alertTitle = "Error!";
      alertIcon = "error";
      break;
    default:
      alertTitle = "Error!";
      alertIcon = "error";
      message = "Terjadi kesalahan saat menyimpan data";
      break;
  }

  // Menampilkan SweetAlert
  Swal.fire({
    icon: alertIcon,
    title: alertTitle,
    text: message,
  }).then((result) => {
    // Setelah mengklik tombol "OK"
    if (result.isConfirmed) {
      window.location.href = "/table"; // Ganti '/redirect-page' dengan URL halaman yang ingin Anda arahkan

      // Redirect hanya pada case 'Data berhasil disimpan'
      // if (message === "Data berhasil disimpan") {
      //   window.location.href = "/register"; // Ganti '/redirect-page' dengan URL halaman yang ingin Anda arahkan
      // }
    }
  });
}

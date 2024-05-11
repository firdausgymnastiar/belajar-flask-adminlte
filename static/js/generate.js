const formGenerate = document.getElementById("formGenerate");

function generateRandomNumber() {
  // Membuat angka acak antara 100000 dan 999999 (6 digit)
  var randomNumber = Math.floor(100000 + Math.random() * 900000);
  // Menampilkan angka acak di console
  console.log("Angka acak: " + randomNumber);
  // Menampilkan angka acak di halaman HTML
  document.getElementById("randomNumberDisplay").value = randomNumber;
}

async function sendToServer() {
  const formData = new FormData(formGenerate);

  // Tampilkan overlay saat memulai submit form
  document.getElementById("overlay").style.display = "flex";

  const response = await fetch("/generatetoken", {
    method: "POST",
    body: formData,
  });
  const responseData = await response.json();
  try {
    if (response.ok && responseData.success) {
      displayAlert(responseData);
    } else {
      // Jika permintaan gagal atau respons dari Flask menunjukkan kegagalan
      displayAlert(responseData.error_message || responseData);
    }
  } catch (error) {
    // Jika terjadi kesalahan dalam melakukan permintaan
    console.log("ada error:");
    displayAlert("Terjadi kesalahan dalam mengirim permintaan");
    console.error("Error:", error);
  }
}

formGenerate.addEventListener("submit", function (event) {
  event.preventDefault();
  sendToServer();
});

// Fungsi untuk menampilkan SweetAlert berdasarkan pesan dari server
function displayAlert(responseData) {
  let message = responseData.message; // Mengambil nilai dari kunci 'message'
  let nim = responseData.nim; // Mengambil nilai dari kunci 'nim'

  let alertTitle, alertIcon, alertText;

  // Menyesuaikan judul dan ikon berdasarkan pesan dari server
  switch (message) {
    case "Missing required data":
      alertTitle = "Error!";
      alertIcon = "error";
      alertText = "Ada form yang kosong";
      break;
    case "Data berhasil disimpan":
      alertTitle = "Berhasil Diaktifkan!";
      alertIcon = "success";
      alertText = `Token Anda: ${nim}`;
      break;
    case "gagal pas di mysql":
      alertTitle = "Error!";
      alertIcon = "error";
      alertText = "gagal pas di mysql";
      break;
    case "Terjadi kesalahan dalam mengirim permintaan":
      alertTitle = "Error!";
      alertIcon = "error";
      alertText = "Terjadi kesalahan dalam mengirim permintaan";
      break;
    case "form kosong":
      alertTitle = "Error!";
      alertIcon = "error";
      alertText = "Form kosong, mohon ulangi!";
      break;
    default:
      alertTitle = "Error!";
      alertIcon = "error";
      alertText = "Terjadi kesalahan saat menyimpan data";
      break;
  }

  // Menampilkan SweetAlert
  Swal.fire({
    icon: alertIcon,
    title: alertTitle,
    text: alertText,
    allowOutsideClick: false,
  }).then((result) => {
    // Setelah mengklik tombol "OK"
    if (result.isConfirmed) {
      window.location.href = "/generate"; // Ganti '/redirect-page' dengan URL halaman yang ingin Anda arahkan

      // Redirect hanya pada case 'Data berhasil disimpan'
      // if (message === "Data berhasil disimpan") {
      //   window.location.href = "/register"; // Ganti '/redirect-page' dengan URL halaman yang ingin Anda arahkan
      // }
    }
  });
}

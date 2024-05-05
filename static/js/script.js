function generateRandomNumber() {
  // Membuat angka acak antara 100000 dan 999999 (6 digit)
  var randomNumber = Math.floor(100000 + Math.random() * 900000);
  // Menampilkan angka acak di console
  console.log("Angka acak: " + randomNumber);
  // Menampilkan angka acak di halaman HTML
  document.getElementById("randomNumberDisplay").value = randomNumber;
}

// ოთახის არჩევისას ვწერთ მის სახელს/ფასს input-ში
const roomRadios = document.querySelectorAll(".room-radio");
const selectedRoomDisplay = document.getElementById("selectedRoomDisplay");

roomRadios.forEach(function (radio) {
  radio.addEventListener("change", function () {
    const roomName = radio.dataset.name;
    const roomPrice = radio.dataset.price;
    selectedRoomDisplay.value = roomName + " — " + roomPrice + "$/ღამე";
  });
});

// ფორმის submit-ზე ვწერთ მარტივ სტატუსს
const bookingForm = document.getElementById("bookingForm");
const bookingStatus = document.getElementById("bookingStatus");

bookingForm.addEventListener("submit", function (event) {
  event.preventDefault(); // გვერდის გადატვირთვის თავიდან ასაცილებლად

  const selectedRoom = document.querySelector('input[name="selectedRoom"]:checked');
  const customerName = document.getElementById("customerName").value.trim();
  const budget = parseFloat(document.getElementById("budget").value);
  const nights = parseInt(document.getElementById("nights").value, 10);

  if (!selectedRoom) {
    bookingStatus.textContent = "გთხოვთ, აირჩიოთ ოთახი.";
    bookingStatus.className = "booking-status error";
    return;
  }

  const totalPrice = parseFloat(selectedRoom.dataset.price) * nights;

  if (budget < totalPrice) {
    bookingStatus.textContent =
      customerName + ", თქვენი ბიუჯეტი (" + budget + "$) არასაკმარისია " + totalPrice + "$ ღირებულების დაჯავშნისთვის.";
    bookingStatus.className = "booking-status error";
    return;
  }

  bookingStatus.textContent =
    "დაჯავშნა შესრულებულია! " + customerName + "-მა დაჯავშნა " + selectedRoom.dataset.name +
    " (" + nights + " ღამით), ჯამში " + totalPrice + "$-ად.";
  bookingStatus.className = "booking-status success";
});

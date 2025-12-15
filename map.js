// ✅ Wait until the page fully loads
document.addEventListener("DOMContentLoaded", function () {
  // 1️⃣ Initialize map — no marker yet
  const map = L.map('map').setView([30.7333, 76.7794], 10);

  // 2️⃣ Add base map tiles
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
  }).addTo(map);

  // 3️⃣ Prepare marker variable
  let marker = null;

  // 4️⃣ Function to show marker when valid coordinates exist
  function showMarker(lat, lng) {
    if (!lat || !lng) return; // stop if invalid
    if (marker) map.removeLayer(marker); // remove old one
    marker = L.marker([lat, lng]).addTo(map);
    map.setView([lat, lng], 11);
  }

  // 5️⃣ Function triggered when dropdown changes
  window.updateDistrict = function (value) {
    if (value === "") {
      if (marker) {
        map.removeLayer(marker);
        marker = null;
      }
      return;
    }
    const [lat, lng] = value.split(",");
    showMarker(parseFloat(lat), parseFloat(lng));
  };
});

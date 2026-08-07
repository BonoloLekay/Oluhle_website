// ===============================
// BOOKING WIZARD
// ===============================

const steps = document.querySelectorAll(".form-step");
const nextBtns = document.querySelectorAll(".next-btn");
const prevBtns = document.querySelectorAll(".prev-btn");
const progressBar = document.getElementById("progressBar");

let currentStep = 0;

// ===============================
// SHOW STEP
// ===============================

function showStep(index) {
  steps.forEach((step) => step.classList.remove("active"));

  steps[index].classList.add("active");

  updateProgress();

  updateServiceDetails();

  if (index === steps.length - 1) {
    buildSummary();
  }
}

// ===============================
// PROGRESS BAR
// ===============================

function updateProgress() {
  const percent = ((currentStep + 1) / steps.length) * 100;

  progressBar.style.width = percent + "%";
}

// ===============================
// NEXT
// ===============================

nextBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    // Get all required fields in the current step
    const currentFields = steps[currentStep].querySelectorAll(
      "input, select, textarea",
    );

    let valid = true;

    currentFields.forEach((field) => {
      if (!field.checkValidity()) {
        field.reportValidity();

        valid = false;
      }
    });

    if (!valid) {
      return;
    }

    currentStep++;

    showStep(currentStep);
  });
});

// ===============================
// PREVIOUS
// ===============================

prevBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    if (currentStep > 0) {
      currentStep--;

      showStep(currentStep);
    }
  });
});

// ===============================
// SERVICE DETAILS
// ===============================

const chalet = document.getElementById("chalet");
const conference = document.getElementById("conference");
const spa = document.getElementById("spa");

const chaletDetails = document.getElementById("chaletDetails");
const conferenceDetails = document.getElementById("conferenceDetails");
const spaDetails = document.getElementById("spaDetails");

function updateServiceDetails() {
  if (chalet) {
    chaletDetails.classList.toggle("d-none", !chalet.checked);
  }

  if (conference) {
    conferenceDetails.classList.toggle("d-none", !conference.checked);
  }

  if (spa) {
    spaDetails.classList.toggle("d-none", !spa.checked);
  }
}

[chalet, conference, spa].forEach((item) => {
  if (item) {
    item.addEventListener("change", updateServiceDetails);
  }
});

// ===============================
// REVIEW SUMMARY
// ===============================

function buildSummary() {
  const review = document.querySelector(".review-box");

  if (!review) return;

  const services = [];

  if (chalet.checked) {
    services.push("🏡 Standard Chalet");
  }

  if (conference.checked) {
    services.push("🏢 Conference Hall");
  }

  if (spa.checked) {
    services.push("💆 Spa Treatment");
  }

  review.innerHTML = `

        <h4 class="mb-4">

            Booking Summary

        </h4>

        <p>

            Please review your selected services before submitting your request.

        </p>

        <hr>

        <strong>Selected Services</strong>

        <ul>

            ${services.map((service) => `<li>${service}</li>`).join("")}

        </ul>

        <p class="mt-4">

            Our reception team will contact you to confirm availability.

        </p>

    `;
}

// ===============================
// INITIALISE
// ===============================

if (steps.length) {
  showStep(currentStep);
}

document.addEventListener("DOMContentLoaded", function () {
  const checkIn = document.getElementById("check_in");
  const checkOut = document.getElementById("check_out");

  if (!checkIn || !checkOut) return;

  const today = new Date().toISOString().split("T")[0];

  checkIn.min = today;

  checkIn.addEventListener("change", function () {
    const date = new Date(checkIn.value);

    date.setDate(date.getDate() + 1);

    const minCheckout = date.toISOString().split("T")[0];

    checkOut.min = minCheckout;

    if (checkOut.value < minCheckout) {
      checkOut.value = "";
    }
  });
});

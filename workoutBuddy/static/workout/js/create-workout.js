document.addEventListener("DOMContentLoaded", function () {
  const steps = Array.from(document.querySelectorAll(".form-step"));
  const nextBtn = document.getElementById("nextBtn");
  const prevBtn = document.getElementById("prevBtn");
  const submitBtn = document.getElementById("submitBtn");
  const form = document.getElementById("fitnessPlanForm"); // Changed to fitnessPlanForm
  const progressBar = document.getElementById("progress-bar");
  const progressText = document.getElementById("progress-text");
  const workoutDaysSlider = document.getElementById("workout_days_per_week");
  const workoutDaysOutput = document.getElementById("workout-days-output");

  let currentStep = 0;
  const totalSteps = steps.length;

  if (workoutDaysSlider) {
    workoutDaysSlider.addEventListener("input", () => {
      workoutDaysOutput.textContent = workoutDaysSlider.value;
    });
  }

  function updateFormSteps() {
    steps.forEach((step, index) => {
      step.classList.toggle("active", index === currentStep);
      step.classList.toggle("hidden", index !== currentStep);
    });

    const progress = ((currentStep + 1) / totalSteps) * 100;
    progressBar.style.width = `${progress}%`;
    progressText.textContent = `Step ${currentStep + 1} of ${totalSteps}`;

    prevBtn.classList.toggle("invisible", currentStep === 0);
    // Ensure nextBtn is visible unless on the very last step
    nextBtn.classList.toggle("hidden", currentStep === totalSteps - 1);
    // submitBtn is only visible on the very last step
    submitBtn.classList.toggle("hidden", currentStep !== totalSteps - 1);
  }

  function validateStep(stepIndex) {
    const currentStepElement = steps[stepIndex];
    // Select required inputs and textareas
    const inputs = currentStepElement.querySelectorAll(
      "input[required], textarea[required]"
    );
    let isValid = true;

    inputs.forEach((input) => {
      // Check for emptiness, but also for specific radio button group selection if applicable
      if (input.type === "radio") {
        const radioGroupName = input.name;
        const isRadioGroupSelected = currentStepElement.querySelector(
          `input[name="${radioGroupName}"]:checked`
        );
        if (!isRadioGroupSelected) {
          // Highlight the parent container or add a message for radio groups
          // For simplicity, we'll just set isValid to false
          isValid = false;
        }
      } else if (!input.value.trim()) {
        input.classList.add("border-red-500");
        isValid = false;
      } else {
        input.classList.remove("border-red-500");
      }
    });

    // Add specific validation for radio buttons if needed (e.g., for gender, activity_level, goal, workout_duration)
    // Since radio buttons often have a 'checked' attribute on initial load, ensure a selection is made
    // For radio groups, check if any option is selected.
    const radioGroups = [
      "gender",
      "activity_level",
      "goal",
      "workout_duration",
    ];
    radioGroups.forEach((groupName) => {
      const selectedRadio = currentStepElement.querySelector(
        `input[name="${groupName}"]:checked`
      );
      if (
        !selectedRadio &&
        currentStepElement.querySelector(`input[name="${groupName}"]`)
      ) {
        isValid = false;
        // You might want to add a visual indicator here
      }
    });

    return isValid;
  }

  nextBtn.addEventListener("click", () => {
    if (validateStep(currentStep)) {
      if (currentStep < totalSteps - 1) {
        currentStep++;
        updateFormSteps();
      }
    } else {
      alert("Please fill in all required fields before proceeding."); // Simple alert for missing fields
    }
  });

  prevBtn.addEventListener("click", () => {
    if (currentStep > 0) {
      currentStep--;
      updateFormSteps();
    }
  });

form.addEventListener("submit", function (event) {
  if (!validateStep(currentStep)) {
    event.preventDefault(); // Prevent actual form submission if validation fails
    return; // Stop further execution
  }

  // ✅ Only reached if validation passes
  submitBtn.disabled = true;
  submitBtn.textContent = "Generating...";
});


  updateFormSteps(); // Initial setup
});
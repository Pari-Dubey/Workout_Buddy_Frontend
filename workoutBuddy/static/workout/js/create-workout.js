 document.addEventListener('DOMContentLoaded', function () {
          const steps = Array.from(document.querySelectorAll('.form-step'));
          const nextBtn = document.getElementById('nextBtn');
          const prevBtn = document.getElementById('prevBtn');
          const submitBtn = document.getElementById('submitBtn');
          const form = document.getElementById('gymForm');
          const progressBar = document.getElementById('progress-bar');
          const progressText = document.getElementById('progress-text');
          const workoutDaysSlider = document.getElementById('workout_days_per_week');
          const workoutDaysOutput = document.getElementById('workout-days-output');

          let currentStep = 0;
          const totalSteps = steps.length;

          // Update workout days display
          if (workoutDaysSlider) {
              workoutDaysSlider.addEventListener('input', () => {
                  workoutDaysOutput.textContent = workoutDaysSlider.value;
              });
          }

          function updateFormSteps() {
              // Hide all steps
              steps.forEach((step, index) => {
                  if (index === currentStep) {
                      step.classList.add('active');
                      step.classList.remove('hidden');
                  } else {
                      step.classList.remove('active');
                      step.classList.add('hidden');
                  }
              });

              // Update progress bar
              const progress = ((currentStep + 1) / totalSteps) * 100;
              progressBar.style.width = `${progress}%`;
              progressText.textContent = `Step ${currentStep + 1} of ${totalSteps}`;

              // Update button visibility
              prevBtn.classList.toggle('invisible', currentStep === 0);
              nextBtn.classList.toggle('hidden', currentStep === totalSteps - 1);
              submitBtn.classList.toggle('hidden', currentStep !== totalSteps - 1);
          }

          function validateStep(stepIndex) {
              const currentStepElement = steps[stepIndex];
              const inputs = currentStepElement.querySelectorAll('input[required]');
              let isValid = true;
              inputs.forEach(input => {
                  if (!input.value.trim()) {
                      input.classList.add('border-red-500');
                      isValid = false;
                  } else {
                      input.classList.remove('border-red-500');
                  }
              });
              return isValid;
          }

          nextBtn.addEventListener('click', () => {
              if (validateStep(currentStep)) {
                  if (currentStep < totalSteps - 1) {
                      currentStep++;
                      updateFormSteps();
                  }
              }
          });

          prevBtn.addEventListener('click', () => {
              if (currentStep > 0) {
                  currentStep--;
                  updateFormSteps();
              }
          });

          form.addEventListener('submit', (e) => {
              e.preventDefault();
              const formData = new FormData(form);
              const data = {};

              // Process FormData
              for (let [key, value] of formData.entries()) {
                  // Handle textareas that might be empty
                  if (key === 'medical_conditions' || key === 'injuries_or_limitations') {
                      data[key] = value.trim() === '' ? ['None'] : value.split(',').map(s => s.trim());
                  } else {
                      data[key] = value;
                  }
              }

              // Convert numeric strings to numbers
              data.age = parseInt(data.age, 10);
              data.height_cm = parseInt(data.height_cm, 10);
              data.weight_kg = parseInt(data.weight_kg, 10);
              data.workout_days_per_week = parseInt(data.workout_days_per_week, 10);

              console.log('Form Submitted!');
              console.log(JSON.stringify(data, null, 2));

              // You can now send this 'data' object to your server
              alert('Your plan is ready! Check the console for the form data.');
              // Replace alert with a more sophisticated modal in a real application
          });

          // Initial call to set up the form
          updateFormSteps();
      });

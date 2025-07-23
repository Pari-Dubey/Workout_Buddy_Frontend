
  const formContainer = document.getElementById('form-container');
  const showSignupBtn = document.getElementById('show-signup');
  const showLoginBtn = document.getElementById('show-login');

  showSignupBtn.addEventListener('click', (e) => {
    e.preventDefault();
    formContainer.classList.add('flipped');
  });

  showLoginBtn.addEventListener('click', (e) => {
    e.preventDefault();
    formContainer.classList.remove('flipped');
  });

  // Monkey Animation Code
  const monkeyFace = document.querySelector('.monkey-face');
  const monkeyHand = document.querySelector('.monkey-hand');
  const monkeyThought = document.querySelector('.monkey-thought');
  const monkeyEyesBrows = document.querySelectorAll('.eye-brow');

  const loginEmail = document.getElementById('login-email');
  const signupEmail = document.getElementById('signup-email');

  const passwordInputs = document.querySelectorAll('.password-input');

  const mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

  let degree = 13;
  let inputPrevLenght = [];

  const showMonkeyHand = () => {
    monkeyHand.style.transform = 'translateY(35%)';
  }

  const hideMonkeyHand = () => {
    monkeyHand.style.transform = 'translateY(120%)';
  }

  // Click anywhere logic
  document.addEventListener('click', (e) => {
    if (e.target.type === 'password') {
      showMonkeyHand();
    } else {
      hideMonkeyHand();
    }

    if (e.target.type !== 'email') {
      monkeyFace.style.transform = `perspective(800px) rotateZ(0deg)`;
      monkeyEyesBrows.forEach((eyeBrow) => {
        eyeBrow.style.transform = 'translateY(-2px)';
      });
    }
  });

  // Eye tracking for email input
  const handleEmailInput = (emailInput) => {
    emailInput.addEventListener('input', (e) => {
      let currentInputLength = String(e.target.value).length;
      let decrementInInputValue = inputPrevLenght.includes(currentInputLength);

      if (!decrementInInputValue && degree >= -10) {
        degree -= 1;
        inputPrevLenght.push(currentInputLength);
      }
      if (decrementInInputValue && degree < 13) {
        degree += 1;
      }

      if (!emailInput.value.match(mailformat)) {
        monkeyThought.style.opacity = '1';
        monkeyEyesBrows.forEach((eyeBrow) => {
          eyeBrow.style.transform = 'translateY(3px)';
        });
      } else {
        monkeyThought.style.opacity = '0';
        monkeyEyesBrows.forEach((eyeBrow) => {
          eyeBrow.style.transform = 'translateY(-3px)';
        });
      }

      monkeyFace.style.transform = `perspective(800px) rotateZ(${degree}deg)`;
    });
  }

  if (loginEmail) handleEmailInput(loginEmail);
  if (signupEmail) handleEmailInput(signupEmail);

  // Password focus/blur for both forms
  passwordInputs.forEach((input) => {
    input.addEventListener('focus', showMonkeyHand);
    input.addEventListener('blur', hideMonkeyHand);
  });

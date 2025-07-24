document.addEventListener("DOMContentLoaded", () => {
  const flipContainer = document.getElementById("form-container");
  const showSignupBtn = document.getElementById("show-signup");
  const showLoginBtn = document.getElementById("show-login");

  const monkeyFace = document.querySelector(".monkey-face");
  const monkeyHand = document.querySelector(".monkey-hand");
  const monkeyThought = document.querySelector(".monkey-thought");
  const monkeyEyesBrows = document.querySelectorAll(".eye-brow");
  const loginEmail = document.getElementById("login-email");
  const signupEmail = document.getElementById("signup-email");
  const passwordInputs = document.querySelectorAll(".password-input");
  const mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  let degree = 13;
  let inputPrevLength = [];

  // Flip with route change
  if (showSignupBtn) {
    showSignupBtn.addEventListener("click", (e) => {
      e.preventDefault();
      flipContainer.classList.add("flipped");
      window.history.pushState(null, "", "/register");
    });
  }

  if (showLoginBtn) {
    showLoginBtn.addEventListener("click", (e) => {
      e.preventDefault();
      flipContainer.classList.remove("flipped");
      window.history.pushState(null, "", "/login");
    });
  }

  // Handle browser back/forward navigation
  window.addEventListener("popstate", () => {
    const path = window.location.pathname;
    if (path === "/register") {
      flipContainer.classList.add("flipped");
    } else {
      flipContainer.classList.remove("flipped");
    }
  });

  // Monkey hand logic
  const showMonkeyHand = () => {
    monkeyHand.style.transform = "translateY(35%)";
  };

  const hideMonkeyHand = () => {
    monkeyHand.style.transform = "translateY(120%)";
  };

  document.addEventListener("click", (e) => {
    if (e.target.type === "password") {
      showMonkeyHand();
    } else {
      hideMonkeyHand();
    }

    if (e.target.type !== "email") {
      monkeyFace.style.transform = `perspective(800px) rotateZ(0deg)`;
      monkeyEyesBrows.forEach((eyeBrow) => {
        eyeBrow.style.transform = "translateY(-2px)";
      });
    }
  });

  const handleEmailInput = (emailInput) => {
    emailInput.addEventListener("input", (e) => {
      const currentLength = String(e.target.value).length;
      const isDecrement = inputPrevLength.includes(currentLength);

      if (!isDecrement && degree >= -10) {
        degree -= 1;
        inputPrevLength.push(currentLength);
      } else if (isDecrement && degree < 13) {
        degree += 1;
      }

      if (!emailInput.value.match(mailformat)) {
        monkeyThought.style.opacity = "1";
        monkeyEyesBrows.forEach((eyeBrow) => {
          eyeBrow.style.transform = "translateY(3px)";
        });
      } else {
        monkeyThought.style.opacity = "0";
        monkeyEyesBrows.forEach((eyeBrow) => {
          eyeBrow.style.transform = "translateY(-3px)";
        });
      }

      monkeyFace.style.transform = `perspective(800px) rotateZ(${degree}deg)`;
    });
  };

  if (loginEmail) handleEmailInput(loginEmail);
  if (signupEmail) handleEmailInput(signupEmail);

  passwordInputs.forEach((input) => {
    input.addEventListener("focus", showMonkeyHand);
    input.addEventListener("blur", hideMonkeyHand);
  });

  // On initial load, flip based on current URL
  const path = window.location.pathname.replace(/\/$/, "");
  if (path === "/register") {
    flipContainer.classList.add("flipped");
  } else {
    flipContainer.classList.remove("flipped");
  }
});

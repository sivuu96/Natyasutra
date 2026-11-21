(function () {
  "use strict";

  function setFieldError(field, message) {
    var group = field.closest("[data-auth-field]");
    var error = group && group.querySelector("[data-auth-error]");
    field.setAttribute("aria-invalid", message ? "true" : "false");
    if (error) error.textContent = message || "";
  }

  function isEmail(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  }

  function passwordScore(value) {
    var score = 0;
    if (value.length >= 8) score += 1;
    if (/[A-Z]/.test(value)) score += 1;
    if (/[0-9]/.test(value)) score += 1;
    if (/[^A-Za-z0-9]/.test(value)) score += 1;
    return score;
  }

  function initPasswordToggle(button) {
    var field = document.getElementById(button.getAttribute("aria-controls"));
    if (!field) return;
    button.addEventListener("click", function () {
      var show = field.type === "password";
      field.type = show ? "text" : "password";
      button.textContent = show ? "Hide" : "Show";
      button.setAttribute("aria-label", show ? "Hide password" : "Show password");
    });
  }

  function initStrengthMeter(form) {
    var password = form.querySelector("[data-auth-password]");
    var meter = form.querySelector("[data-auth-strength-meter]");
    var label = form.querySelector("[data-auth-strength-label]");
    if (!password || !meter || !label) return;

    password.addEventListener("input", function () {
      var score = passwordScore(password.value);
      meter.setAttribute("data-score", String(score));
      label.textContent = ["Too weak", "Weak", "Fair", "Good", "Strong"][score];
    });
  }

  function validateForm(form) {
    var valid = true;
    var mode = form.getAttribute("data-auth-form");
    var fullName = form.querySelector("[name='fullName']");
    var email = form.querySelector("[name='email']");
    var password = form.querySelector("[name='password']");
    var confirmPassword = form.querySelector("[name='confirmPassword']");
    var terms = form.querySelector("[name='terms']");

    form.querySelectorAll("[data-auth-error]").forEach(function (error) {
      error.textContent = "";
    });
    form.querySelectorAll("[aria-invalid]").forEach(function (field) {
      field.setAttribute("aria-invalid", "false");
    });

    if (fullName && fullName.value.trim().length < 2) {
      setFieldError(fullName, "Please enter your full name.");
      valid = false;
    }

    if (!email || !isEmail(email.value.trim())) {
      if (email) setFieldError(email, "Enter a valid email address.");
      valid = false;
    }

    if (!password || password.value.length < 8) {
      if (password) setFieldError(password, "Password must be at least 8 characters.");
      valid = false;
    }

    if (mode === "signup" && confirmPassword && confirmPassword.value !== password.value) {
      setFieldError(confirmPassword, "Passwords do not match.");
      valid = false;
    }

    if (terms && !terms.checked) {
      setFieldError(terms, "Please accept the terms and conditions.");
      valid = false;
    }

    return valid;
  }

  function initAuthForm(form) {
    var feedback = form.querySelector("[data-auth-feedback]");
    var submit = form.querySelector("[type='submit']");

    initStrengthMeter(form);

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (feedback) {
        feedback.textContent = "";
        feedback.classList.remove("is-success", "is-error");
      }

      if (!validateForm(form)) {
        if (feedback) {
          feedback.textContent = "Please fix the highlighted fields and try again.";
          feedback.classList.add("is-error");
        }
        return;
      }

      if (submit) {
        submit.disabled = true;
        submit.classList.add("is-loading");
      }

      window.setTimeout(function () {
        if (submit) {
          submit.disabled = false;
          submit.classList.remove("is-loading");
        }
        if (feedback) {
          feedback.textContent = form.getAttribute("data-auth-form") === "signup"
            ? "Account created successfully. You can now sign in."
            : "Signed in successfully. Redirecting to your learning dashboard.";
          feedback.classList.add("is-success");
        }
      }, 700);
    });
  }

  function init() {
    document.querySelectorAll("[data-password-toggle]").forEach(initPasswordToggle);
    document.querySelectorAll("[data-auth-form]").forEach(initAuthForm);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

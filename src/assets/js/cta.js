const modalTriggers = document.querySelectorAll(".popup-trigger");
const modalCloseTrigger = document.querySelector(".modal__close");
const bodyBlackout = document.querySelector(".modal-background");

const closeModal = (popupModal) => {
  popupModal.classList.remove("is--visible");
  bodyBlackout.classList.remove("is-blacked-out");
};

const switchModal = (modal) => {
  const calendlyDiv = modal.querySelector(".calendly");
  const callbackDiv = modal.querySelector(".callback");
  if (calendlyDiv.style.display === "none") {
    calendlyDiv.style.display = "block";
    callbackDiv.style.display = "none";
  } else {
    calendlyDiv.style.display = "none";
    callbackDiv.style.display = "block";
  }
};

modalTriggers.forEach((trigger) => {
  trigger.addEventListener("click", () => {
    const { popupTrigger } = trigger.dataset;
    const popupModal = document.querySelector(`[data-modal="${popupTrigger}"]`);
    popupModal.classList.add("is--visible");
    bodyBlackout.classList.add("is-blacked-out");

    popupModal
      .querySelectorAll(".modal__close")
      .forEach((m) =>
        m.addEventListener("click", () => closeModal(popupModal))
      );

    popupModal
      .querySelectorAll(".modal__switchButton")
      .forEach((m) =>
        m.addEventListener("click", () => switchModal(popupModal))
      );

    bodyBlackout.addEventListener("click", () => closeModal(popupModal));
  });
});

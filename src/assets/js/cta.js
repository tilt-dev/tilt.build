const modalTriggers = document.querySelectorAll(".popup-trigger");
const modalCloseTrigger = document.querySelector(".popup-modal__close");
const bodyBlackout = document.querySelector(".body-blackout");

const closeModal = (popupModal) => {
  popupModal.classList.remove("is--visible");
  bodyBlackout.classList.remove("is-blacked-out");
};

modalTriggers.forEach((trigger) => {
  trigger.addEventListener("click", () => {
    const { popupTrigger } = trigger.dataset;
    const popupModal = document.querySelector(
      `[data-popup-modal="${popupTrigger}"]`
    );
    popupModal.classList.add("is--visible");
    bodyBlackout.classList.add("is-blacked-out");

    popupModal
      .querySelector(".popup-modal__close")
      .addEventListener("click", () => closeModal(popupModal));

    bodyBlackout.addEventListener("click", () => closeModal(popupModal));
  });
});

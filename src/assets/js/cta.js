const modalTriggers = document.querySelectorAll(".popup-trigger");
const modalCloseTrigger = document.querySelector(".popup-modal__close");
const bodyBlackout = document.querySelector(".body-blackout");
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
      .addEventListener("click", () => {
        popupModal.classList.remove("is--visible");
        bodyBlackout.classList.remove("is-blacked-out");
      });

    bodyBlackout.addEventListener("click", () => {
      popupModal.classList.remove("is--visible");
      bodyBlackout.classList.remove("is-blacked-out");
    });
  });
});

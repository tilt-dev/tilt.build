const modalTriggers = document.querySelectorAll(".popup-trigger");
const modalCloseTrigger = document.querySelector(".modal-close");
const bodyBlackout = document.querySelector(".modal-background");

const closeModal = (popupModal) => {
  popupModal.classList.remove("is--visible");
  bodyBlackout.classList.remove("is-blacked-out");
};

modalTriggers.forEach((trigger) => {
  trigger.addEventListener("click", () => {
    const { popupTrigger } = trigger.dataset;
    const popupModal = document.querySelector(`[data-modal="${popupTrigger}"]`);
    popupModal.classList.add("is--visible");
    bodyBlackout.classList.add("is-blacked-out");

    popupModal
      .querySelectorAll(".modal-close")
      .forEach((m) =>
        m.addEventListener("click", () => closeModal(popupModal))
      );

    bodyBlackout.addEventListener("click", () => closeModal(popupModal));
  });
});

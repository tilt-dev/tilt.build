const modalTriggers = document.querySelectorAll(".popup-trigger");
const modalCloseTrigger = document.querySelector(".modal-close");
const bodyBlackout = document.querySelector(".modal-background");

const closeModal = (popupModal) => {
  popupModal.setAttribute('aria-hidden', 'true');
  popupModal.classList.remove("is--visible");
  bodyBlackout.classList.remove("is-blacked-out");
  popupModal.style.display = '';
};

modalTriggers.forEach((trigger) => {
  trigger.addEventListener("click", () => {
    const { popupTrigger } = trigger.dataset;
    const popupModal = document.querySelector(`[data-modal="${popupTrigger}"]`);
    popupModal.style.display = 'block';
    popupModal.getBoundingClientRect(); // force layout

    popupModal.removeAttribute('aria-hidden');
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

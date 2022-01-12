(function() {
    // NOTE(milas): this is not great but SVGs need to be inlined so they can be styled and we don't have something
    //  like Webpack for a real asset pipeline to do ES6 style imports on static files
    const copySVG = '<svg width="24" height="24" viewBox="0 0 24 24" role="presentation" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M16.3859 5.04492V6.17725H18.0707H18.072V6.18018C18.6041 6.18164 19.0865 6.41016 19.4347 6.78076C19.7803 7.14844 19.9959 7.65674 19.9972 8.21924H20V8.22217V18.9551V18.9565H19.9972C19.9959 19.519 19.7803 20.0303 19.4306 20.4009C19.0837 20.7671 18.6041 20.9956 18.0734 20.9971V21H18.0707H9.54341H9.54202V20.9971C9.01132 20.9956 8.5276 20.7671 8.17932 20.3965C7.83381 20.0288 7.61821 19.5205 7.61683 18.958H7.61406V18.9551V16.5513H5.92934H5.92796V16.5483C5.39725 16.5469 4.91354 16.3184 4.56526 15.9478C4.21975 15.5801 4.00415 15.0718 4.00276 14.5093H4V14.5063V5.04492V5.04346H4.00276C4.00415 4.47949 4.22113 3.96826 4.5694 3.59912C4.9163 3.23291 5.39587 3.00439 5.92658 3.00293V3H5.92934H14.4566H14.458V3.00293C14.9901 3.00439 15.4724 3.23291 15.8207 3.60352C16.1662 3.97119 16.3818 4.47949 16.3832 5.04199H16.3859V5.04492V5.04492ZM14.9237 6.17725V5.04492V5.04199H14.9265C14.9265 4.90869 14.8726 4.78564 14.7869 4.69482C14.7026 4.60547 14.5851 4.54834 14.4594 4.54834V4.55127H14.458H5.93072H5.92796V4.54834C5.80219 4.54834 5.6861 4.60547 5.60041 4.69629C5.51611 4.78564 5.46221 4.91016 5.46221 5.04346H5.46497V5.04492V14.5063V14.5093H5.46221C5.46221 14.6426 5.51611 14.7656 5.6018 14.8564C5.6861 14.9458 5.80358 15.0029 5.92934 15.0029V15H5.93072H7.61544V8.22217V8.2207H7.61821C7.61959 7.65674 7.83657 7.14551 8.18485 6.77637C8.53174 6.41016 9.01132 6.18164 9.54202 6.18018V6.17725H9.54479H14.9237ZM18.5364 18.9551V8.22217V8.21924H18.5392C18.5392 8.08594 18.4853 7.96289 18.3996 7.87207C18.3153 7.78271 18.1978 7.72559 18.072 7.72559V7.72852H18.0707H9.54341H9.54064V7.72559C9.41487 7.72559 9.29878 7.78271 9.2131 7.87354C9.12879 7.96289 9.07489 8.0874 9.07489 8.2207H9.07765V8.22217V18.9551V18.958H9.07489C9.07489 19.0913 9.12879 19.2144 9.21448 19.3052C9.29878 19.3945 9.41626 19.4517 9.54202 19.4517V19.4487H9.54341H18.0707H18.0734V19.4517C18.1992 19.4517 18.3153 19.3945 18.401 19.3037C18.4853 19.2144 18.5392 19.0898 18.5392 18.9565H18.5364V18.9551V18.9551Z" /></svg>';
    const clipboardSVG = '<svg width="24" height="24" viewBox="0 0 24 24" role="presentation" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M8 2H7.5V2.5V5.5C7.5 6.32843 8.17157 7 9 7H15C15.8284 7 16.5 6.32843 16.5 5.5V2.5V2H16H8ZM8.5 5.5V3H15.5V5.5C15.5 5.77614 15.2761 6 15 6H9C8.72386 6 8.5 5.77614 8.5 5.5ZM5 4H7V5H5L5 21.0027H19.0024V5H17V4H19.0024C19.5547 4 20.0024 4.44772 20.0024 5V21.0027C20.0024 21.555 19.5547 22.0027 19.0024 22.0027H5C4.44771 22.0027 4 21.555 4 21.0027V5C4 4.44771 4.44772 4 5 4Z" /></svg>';

    const eventListener = () => {
        if (document.readyState !== "complete") {
            return
        }

        const copyHTML = copySVG + 'Copy';
        const copyLabel = 'Copy to clipboard';

        const codeBlocks = document.querySelectorAll('.highlight');
        codeBlocks.forEach((wrapperEl, i) => {
            // find the <pre> element and assign it an ID for the button to reference
            const codeEl = wrapperEl.querySelector('pre');
            if (!codeEl) {
                return;
            }
            if (!codeEl.id) {
                codeEl.id = 'codeblock-' + i.toString();
            }

            // create a button and insert it inside the wrapper element
            const copyBtn = document.createElement('button');
            copyBtn.dataset.clipboardTarget = '#' + codeEl.id;
            copyBtn.innerHTML = copyHTML;
            copyBtn.classList.add('copy-to-clipboard');
            copyBtn.setAttribute('aria-label', copyLabel)
            wrapperEl.append(copyBtn);
        });

        const clipboard = new ClipboardJS('button.copy-to-clipboard');
        clipboard.on('success', (e) => {
            e.trigger.innerHTML = clipboardSVG + 'Copied!';
            e.trigger.removeAttribute('aria-label');
            e.clearSelection();

            // restore the button state after a few seconds
            setTimeout((target) => {
                target.innerHTML = copyHTML;
                target.setAttribute('aria-label', copyLabel);
            }, 3000, e.trigger);
        });

        document.removeEventListener('readystatechange', eventListener);
    }

    document.addEventListener('readystatechange', eventListener);
})()

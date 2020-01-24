// Adapted from https://codepen.io/gabrieleromanato/pen/pKrny

(function() {

    function Slideshow( element ) {
        this.el = document.querySelector( element );
        this.init();
    }

    Slideshow.prototype = {
        init: function() {
            this.wrapper = this.el.querySelector( ".slider-wrapper" );
            this.slides = this.el.querySelectorAll( ".slide" );
            this.previous = this.el.querySelector( ".slider-previous" );
            this.next = this.el.querySelector( ".slider-next" );
            this.nav = this.el.querySelector( ".slider-nav" );
            this.index = 0;
            this.total = this.slides.length;

            this.setup();
            this.actions();
        },
        _adjustIndex: function( iSlide ) {
            var adjusted = iSlide % this.slides.length;
            if ( adjusted < 0 ) {
                adjusted = adjusted + this.slides.length;
            }
            return adjusted;
        },
        _slideTo: function() {
            var iSlide = this.index;
            var currentSlide = this.slides[iSlide];
            currentSlide.style.opacity = 1;

            for( var i = 0; i < this.slides.length; i++ ) {
                var iSlide = this.slides[i];
                if( iSlide !== currentSlide ) {
                    iSlide.style.opacity = 0;
                }
            }
        },
        _setIndexAndSlide: function( i ) {
            this.index = this._adjustIndex(i);
            this._slideTo();
        },
        setup: function() {
            var slides = this.slides,
                len = slides.length,
                i;
            for( i = 0; i < len; ++i ) {
                var slide = slides[i],
                    src = slide.getAttribute( "data-image" );

                slide.style.backgroundImage = "url(" + src + ")";
            }
        },
        actions: function() {
            var self = this;

            self.next.addEventListener( "click", function() {
                var i = self.index + 1;
                self.previous.style.display = "block";

                self._setIndexAndSlide( i );

            }, false);

            self.previous.addEventListener( "click", function() {
                var i = self.index - 1;
                self.next.style.display = "block";

                self._setIndexAndSlide( i );

            }, false);

            document.body.addEventListener( "keydown", function( e ) {
                var code = e.keyCode;
                var evt = new Event( "click" );

                if( code == 39 ) {
                    self.next.dispatchEvent( evt );
                }
                if( code == 37 ) {
                    self.previous.dispatchEvent( evt );
                }

            }, false);
        }


    };

    document.addEventListener( "DOMContentLoaded", function() {

        var slider = new Slideshow( "#main-slider" );

    });


})();

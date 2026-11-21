(function () {
  "use strict";

  function withAutoplay(src) {
    if (!src) return "";
    var separator = src.indexOf("?") === -1 ? "?" : "&";
    return src.indexOf("autoplay=1") === -1 ? src + separator + "autoplay=1" : src;
  }

  function initFreeVideoPlayer(root) {
    var iframe = root.querySelector("[data-free-video-iframe]");
    if (!iframe) return;

    var grid = root.closest(".page-free-video-detail-grid");
    var playlist = grid ? grid.querySelector("[data-free-video-playlist]") : null;
    var track = playlist ? playlist.querySelector("[data-video-thumbs]") : null;
    var viewport = playlist ? playlist.querySelector("[data-free-video-playlist-viewport]") : null;
    var prevBtn = playlist ? playlist.querySelector("[data-free-video-playlist-prev]") : null;
    var nextBtn = playlist ? playlist.querySelector("[data-free-video-playlist-next]") : null;
    var thumbButtons = track
      ? Array.prototype.slice.call(track.querySelectorAll("button[data-video-index]"))
      : [];

    if (!thumbButtons.length) return;

    var currentVideoIndex = Math.max(
      0,
      thumbButtons.findIndex(function (btn) {
        return btn.classList.contains("is-active");
      })
    );
    var currentScrollIndex = 0;

    function maxIndex() {
      if (!viewport || !track) return Math.max(0, thumbButtons.length - 1);
      var maxScroll = Math.max(0, track.scrollHeight - viewport.clientHeight);
      var itemStep = getItemStep();
      return itemStep ? Math.ceil(maxScroll / itemStep) : 0;
    }

    function getItemStep() {
      if (!thumbButtons.length) return 0;
      var first = thumbButtons[0];
      var second = thumbButtons[1];
      if (second) return second.offsetTop - first.offsetTop;
      return first.offsetHeight;
    }

    function updateCarousel() {
      if (!track) return;
      var itemStep = getItemStep();
      currentScrollIndex = Math.max(0, Math.min(currentScrollIndex, maxIndex()));
      var offset = Math.min(currentScrollIndex * itemStep, Math.max(0, track.scrollHeight - (viewport ? viewport.clientHeight : 0)));
      track.style.transform = "translateY(-" + offset + "px)";
      if (prevBtn) prevBtn.disabled = currentScrollIndex <= 0;
      if (nextBtn) nextBtn.disabled = currentScrollIndex >= maxIndex();
    }

    function setActiveThumb(index) {
      thumbButtons.forEach(function (btn) {
        var idx = parseInt(btn.getAttribute("data-video-index"), 10);
        btn.classList.toggle("is-active", idx === index);
      });
    }

    function loadVideo(index, shouldPlay) {
      if (index < 0 || index >= thumbButtons.length) return;
      currentVideoIndex = index;
      currentScrollIndex = Math.min(index, maxIndex());

      var btn = thumbButtons[index];
      var src = btn.getAttribute("data-youtube-src") || "";
      var title = btn.getAttribute("data-video-title") || "Bharatanatyam Free Video";

      if (src) iframe.src = shouldPlay ? withAutoplay(src) : src;
      iframe.title = title;
      setActiveThumb(index);
      updateCarousel();
    }

    thumbButtons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        loadVideo(parseInt(btn.getAttribute("data-video-index"), 10), true);
      });
    });

    if (prevBtn) {
      prevBtn.addEventListener("click", function () {
        currentScrollIndex = Math.max(0, currentScrollIndex - 1);
        updateCarousel();
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        currentScrollIndex = Math.min(maxIndex(), currentScrollIndex + 1);
        updateCarousel();
      });
    }

    window.addEventListener("resize", updateCarousel);
    loadVideo(currentVideoIndex, false);
  }

  function init() {
    document.querySelectorAll("[data-free-video-player]").forEach(initFreeVideoPlayer);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

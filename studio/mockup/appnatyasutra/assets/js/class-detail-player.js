(function () {
  "use strict";

  var STORAGE_PREFIX = "natyasutra-class-progress:";

  function formatTime(seconds) {
    if (!isFinite(seconds) || seconds < 0) return "00:00";
    var mins = Math.floor(seconds / 60);
    var secs = Math.floor(seconds % 60);
    return String(mins).padStart(2, "0") + ":" + String(secs).padStart(2, "0");
  }

  function readStore(courseId) {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_PREFIX + courseId) || "{}");
    } catch (e) {
      return {};
    }
  }

  function writeStore(courseId, store) {
    localStorage.setItem(STORAGE_PREFIX + courseId, JSON.stringify(store));
  }

  function courseCompletion(store, total) {
    if (!total) return 0;
    var sum = 0;
    for (var i = 0; i < total; i++) {
      sum += Math.min(1, Math.max(0, store[String(i)] || 0));
    }
    return Math.round((sum / total) * 100);
  }

  function getThumbScrollLeft(track, thumb) {
    return thumb.getBoundingClientRect().left - track.getBoundingClientRect().left + track.scrollLeft;
  }

  function scrollThumbIntoView(track, thumb) {
    if (!track || !thumb) return;
    var thumbLeft = getThumbScrollLeft(track, thumb);
    var thumbRight = thumbLeft + thumb.offsetWidth;
    var viewLeft = track.scrollLeft;
    var viewRight = viewLeft + track.clientWidth;

    if (thumbLeft < viewLeft + 4) {
      track.scrollTo({ left: thumbLeft, behavior: "smooth" });
    } else if (thumbRight > viewRight - 4) {
      track.scrollTo({ left: thumbRight - track.clientWidth, behavior: "smooth" });
    }
  }

  function updateThumbCarouselNav(track, prevBtn, nextBtn) {
    if (!track) return;
    var maxScroll = Math.max(0, track.scrollWidth - track.clientWidth);
    var atStart = track.scrollLeft <= 2;
    var atEnd = track.scrollLeft >= maxScroll - 2;

    if (prevBtn) {
      prevBtn.disabled = atStart;
      prevBtn.classList.toggle("is-disabled", atStart);
    }

    if (nextBtn) {
      nextBtn.disabled = atEnd;
      nextBtn.classList.toggle("is-disabled", atEnd);
    }
  }

  function scrollThumbCarousel(track, thumbs, direction) {
    if (!track || !thumbs.length) return;
    var scrollLeft = track.scrollLeft;
    var target = null;

    if (direction < 0) {
      for (var i = thumbs.length - 1; i >= 0; i--) {
        if (getThumbScrollLeft(track, thumbs[i]) < scrollLeft - 4) {
          target = thumbs[i];
          break;
        }
      }
      if (!target) {
        track.scrollTo({ left: 0, behavior: "smooth" });
        return;
      }
    } else {
      var viewRight = scrollLeft + track.clientWidth;
      for (var j = 0; j < thumbs.length; j++) {
        var thumbLeft = getThumbScrollLeft(track, thumbs[j]);
        if (thumbLeft + thumbs[j].offsetWidth > viewRight + 4) {
          target = thumbs[j];
          break;
        }
      }
      if (!target) {
        track.scrollTo({ left: track.scrollWidth - track.clientWidth, behavior: "smooth" });
        return;
      }
    }

    track.scrollTo({ left: getThumbScrollLeft(track, target), behavior: "smooth" });
  }

  function withAutoplay(src) {
    if (!src) return "";
    var separator = src.indexOf("?") === -1 ? "?" : "&";
    return src.indexOf("autoplay=1") === -1 ? src + separator + "autoplay=1" : src;
  }

  function initClassDetailPlayer(root) {
    var video = root.querySelector("video");
    var iframe = root.querySelector("[data-class-detail-youtube], iframe");

    var courseId = root.getAttribute("data-course-id") || "default";
    var wrap = root.closest(".page-class-detail-player-wrap, .page-preview-detail-player-wrap");
    var thumbsRoot = wrap ? wrap.querySelector("[data-video-thumbs]") : null;
    var thumbButtons = thumbsRoot
      ? Array.prototype.slice.call(thumbsRoot.querySelectorAll("button[data-video-index]"))
      : [];
    var carousel = thumbsRoot ? thumbsRoot.closest("[data-class-detail-thumbs-carousel]") : null;
    var thumbsPrevBtn = carousel ? carousel.querySelector("[data-class-detail-thumbs-prev]") : null;
    var thumbsNextBtn = carousel ? carousel.querySelector("[data-class-detail-thumbs-next]") : null;

    if (!thumbButtons.length) return;

    if (iframe && !video) {
      var currentYoutubeIndex = 0;

      function setActiveYoutubeThumb(index) {
        thumbButtons.forEach(function (btn) {
          var idx = parseInt(btn.getAttribute("data-video-index"), 10);
          btn.classList.toggle("is-active", idx === index);
          if (idx === index) {
            scrollThumbIntoView(thumbsRoot, btn);
          }
        });
        updateThumbCarouselNav(thumbsRoot, thumbsPrevBtn, thumbsNextBtn);
      }

      function youtubeSrc(btn, shouldPlay) {
        var src = btn.getAttribute("data-youtube-src") || "";
        var id = btn.getAttribute("data-youtube-id") || "";
        if (!src && id) {
          src = "https://www.youtube.com/embed/" + encodeURIComponent(id) + "?rel=0&modestbranding=1&playsinline=1";
        }
        return shouldPlay ? withAutoplay(src) : src;
      }

      function loadYoutube(index, shouldPlay) {
        if (index < 0 || index >= thumbButtons.length) return;
        currentYoutubeIndex = index;
        var btn = thumbButtons[index];
        var src = youtubeSrc(btn, shouldPlay);
        if (src) iframe.src = src;
        iframe.title = btn.getAttribute("data-video-title") || "Payaliya Tarana";
        setActiveYoutubeThumb(index);
      }

      if (thumbsPrevBtn && thumbsRoot) {
        thumbsPrevBtn.addEventListener("click", function () {
          scrollThumbCarousel(thumbsRoot, thumbButtons, -1);
        });
      }

      if (thumbsNextBtn && thumbsRoot) {
        thumbsNextBtn.addEventListener("click", function () {
          scrollThumbCarousel(thumbsRoot, thumbButtons, 1);
        });
      }

      if (thumbsRoot) {
        thumbsRoot.addEventListener(
          "scroll",
          function () {
            updateThumbCarouselNav(thumbsRoot, thumbsPrevBtn, thumbsNextBtn);
          },
          { passive: true }
        );
        window.addEventListener(
          "resize",
          function () {
            updateThumbCarouselNav(thumbsRoot, thumbsPrevBtn, thumbsNextBtn);
            scrollThumbIntoView(thumbsRoot, thumbButtons[currentYoutubeIndex]);
          },
          { passive: true }
        );
      }

      thumbButtons.forEach(function (btn) {
        btn.addEventListener("click", function () {
          loadYoutube(parseInt(btn.getAttribute("data-video-index"), 10), true);
        });
      });

      var initialYoutubeActive = thumbButtons.findIndex(function (btn) {
        return btn.classList.contains("is-active");
      });
      currentYoutubeIndex = initialYoutubeActive >= 0 ? initialYoutubeActive : 0;
      loadYoutube(currentYoutubeIndex, false);
      updateThumbCarouselNav(thumbsRoot, thumbsPrevBtn, thumbsNextBtn);
      return;
    }

    if (!video) return;

    var playlist = thumbButtons.map(function (btn) {
      return {
        index: parseInt(btn.getAttribute("data-video-index"), 10),
        src: btn.getAttribute("data-video-src") || "",
        poster: btn.getAttribute("data-video-poster") || "",
        title: btn.getAttribute("data-video-title") || "",
      };
    });

    var source = video.querySelector("source");
    var playButtons = root.querySelectorAll("[data-video-play]");
    var prevBtn = root.querySelector("[data-video-prev]");
    var nextBtn = root.querySelector("[data-video-next]");
    var progress = root.querySelector("[data-video-progress]");
    var fill = root.querySelector("[data-video-progress-fill]");
    var timeCurrent = root.querySelector("[data-video-time-current]");
    var timeTotal = root.querySelector("[data-video-time-total]");
    var muteBtn = root.querySelector("[data-video-mute]");
    var fullscreenBtn = root.querySelector("[data-video-fullscreen]");
    var completionLabel = root.querySelector("[data-course-progress-label]");

    var currentIndex = 0;
    var store = readStore(courseId);
    var lastSaveAt = 0;

    function setPlaying(playing) {
      root.classList.toggle("is-playing", playing);
      playButtons.forEach(function (btn) {
        btn.setAttribute("aria-label", playing ? "Pause video" : "Play video");
      });
    }

    function setActiveThumb(index) {
      thumbButtons.forEach(function (btn) {
        var idx = parseInt(btn.getAttribute("data-video-index"), 10);
        btn.classList.toggle("is-active", idx === index);
        if (idx === index) {
          scrollThumbIntoView(thumbsRoot, btn);
        }
      });
      updateThumbCarouselNav(thumbsRoot, thumbsPrevBtn, thumbsNextBtn);
    }

    function updateCompletionLabel() {
      if (!completionLabel) return;
      var pct = courseCompletion(store, playlist.length);
      completionLabel.textContent = pct + "% complete";
    }

    function saveCurrentProgress() {
      if (!isFinite(video.duration) || video.duration <= 0) return;
      var fraction = video.currentTime / video.duration;
      if (fraction > 0.92) fraction = 1;
      var prev = store[String(currentIndex)] || 0;
      store[String(currentIndex)] = Math.max(prev, fraction);
      writeStore(courseId, store);
      updateCompletionLabel();
    }

    function updateTimeUI() {
      if (timeCurrent) timeCurrent.textContent = formatTime(video.currentTime);
      if (timeTotal) timeTotal.textContent = formatTime(video.duration);
      if (fill && isFinite(video.duration) && video.duration > 0) {
        fill.style.width = (video.currentTime / video.duration) * 100 + "%";
      }
    }

    function loadVideo(index, shouldPlay) {
      if (index < 0 || index >= playlist.length) return;
      saveCurrentProgress();
      currentIndex = index;
      var item = playlist[index];
      if (source && item.src) source.src = item.src;
      if (item.src) video.src = item.src;
      if (item.poster) video.poster = item.poster;
      setActiveThumb(index);
      video.load();
      var saved = store[String(index)];
      if (saved && saved > 0 && saved < 1) {
        video.addEventListener(
          "loadedmetadata",
          function restore() {
            if (isFinite(video.duration)) {
              video.currentTime = video.duration * saved;
            }
            video.removeEventListener("loadedmetadata", restore);
          },
          { once: true }
        );
      }
      if (shouldPlay) {
        var playWhenReady = function () {
          video.play().catch(function () {});
        };
        if (video.readyState >= 2) {
          playWhenReady();
        } else {
          video.addEventListener("canplay", playWhenReady, { once: true });
        }
      }
      if (prevBtn) prevBtn.disabled = currentIndex <= 0;
      if (nextBtn) nextBtn.disabled = currentIndex >= playlist.length - 1;
      updateCompletionLabel();
    }

    function togglePlay() {
      if (video.paused) {
        video.play().catch(function () {});
      } else {
        video.pause();
      }
    }

    playButtons.forEach(function (btn) {
      btn.addEventListener("click", togglePlay);
    });

    if (prevBtn) {
      prevBtn.addEventListener("click", function () {
        loadVideo(currentIndex - 1, true);
      });
      prevBtn.disabled = currentIndex <= 0;
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        loadVideo(currentIndex + 1, true);
      });
    }

    if (thumbsPrevBtn && thumbsRoot) {
      thumbsPrevBtn.addEventListener("click", function () {
        scrollThumbCarousel(thumbsRoot, thumbButtons, -1);
      });
    }

    if (thumbsNextBtn && thumbsRoot) {
      thumbsNextBtn.addEventListener("click", function () {
        scrollThumbCarousel(thumbsRoot, thumbButtons, 1);
      });
    }

    if (thumbsRoot) {
      thumbsRoot.addEventListener(
        "scroll",
        function () {
          updateThumbCarouselNav(thumbsRoot, thumbsPrevBtn, thumbsNextBtn);
        },
        { passive: true }
      );
      window.addEventListener(
        "resize",
        function () {
          updateThumbCarouselNav(thumbsRoot, thumbsPrevBtn, thumbsNextBtn);
          scrollThumbIntoView(thumbsRoot, thumbButtons[currentIndex]);
        },
        { passive: true }
      );
    }

    thumbButtons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var idx = parseInt(btn.getAttribute("data-video-index"), 10);
        loadVideo(idx, true);
      });
    });

    if (progress) {
      progress.addEventListener("click", function (e) {
        var rect = progress.getBoundingClientRect();
        var ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
        if (isFinite(video.duration)) {
          video.currentTime = ratio * video.duration;
        }
      });
    }

    if (muteBtn) {
      muteBtn.addEventListener("click", function () {
        video.muted = !video.muted;
        muteBtn.setAttribute("aria-label", video.muted ? "Unmute" : "Mute");
      });
    }

    if (fullscreenBtn) {
      fullscreenBtn.addEventListener("click", function () {
        var target = root.querySelector(".page-class-detail-video-stage, .page-preview-detail-video-stage") || video;
        if (target.requestFullscreen) target.requestFullscreen();
      });
    }

    video.addEventListener("timeupdate", function () {
      updateTimeUI();
      var now = Date.now();
      if (now - lastSaveAt > 2000) {
        lastSaveAt = now;
        if (isFinite(video.duration) && video.duration > 0) {
          var fraction = video.currentTime / video.duration;
          var prev = store[String(currentIndex)] || 0;
          store[String(currentIndex)] = Math.max(prev, fraction);
          writeStore(courseId, store);
          updateCompletionLabel();
        }
      }
      if (prevBtn) prevBtn.disabled = currentIndex <= 0;
      if (nextBtn) nextBtn.disabled = currentIndex >= playlist.length - 1;
    });

    video.addEventListener("loadedmetadata", updateTimeUI);
    video.addEventListener("play", function () {
      setPlaying(true);
    });
    video.addEventListener("pause", function () {
      setPlaying(false);
      saveCurrentProgress();
    });
    video.addEventListener("ended", function () {
      store[String(currentIndex)] = 1;
      writeStore(courseId, store);
      updateCompletionLabel();
      setPlaying(false);
      if (currentIndex < playlist.length - 1) {
        loadVideo(currentIndex + 1, true);
      }
    });

    var initialActive = thumbButtons.findIndex(function (btn) {
      return btn.classList.contains("is-active");
    });
    currentIndex = initialActive >= 0 ? initialActive : 0;
    setActiveThumb(currentIndex);
    updateCompletionLabel();
    updateTimeUI();
    if (prevBtn) prevBtn.disabled = currentIndex <= 0;
    if (nextBtn) nextBtn.disabled = currentIndex >= playlist.length - 1;
    updateThumbCarouselNav(thumbsRoot, thumbsPrevBtn, thumbsNextBtn);
  }

  function init() {
    document.querySelectorAll("[data-class-detail-player]").forEach(initClassDetailPlayer);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

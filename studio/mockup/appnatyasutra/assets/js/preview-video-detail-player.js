(function () {
  "use strict";

  function formatTime(seconds) {
    if (!isFinite(seconds) || seconds < 0) return "00:00";
    var mins = Math.floor(seconds / 60);
    var secs = Math.floor(seconds % 60);
    return String(mins).padStart(2, "0") + ":" + String(secs).padStart(2, "0");
  }

  function getThumbScrollLeft(track, thumb) {
    return thumb.getBoundingClientRect().left - track.getBoundingClientRect().left + track.scrollLeft;
  }

  function scrollToThumb(track, thumb) {
    if (!track || !thumb) return;
    track.scrollTo({
      left: getThumbScrollLeft(track, thumb),
      behavior: "smooth",
    });
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

  function updateVideoLabel(playerWrap, thumb) {
    if (!playerWrap || !thumb) return;
    var label = playerWrap.querySelector(".page-preview-detail-video-label");
    if (!label) return;
    var title = thumb.getAttribute("data-video-title") || (thumb.querySelector("img") ? thumb.querySelector("img").alt : "");
    label.innerHTML = title
      ? '<span class="page-preview-detail-video-kicker">' + title + "</span>"
      : "";
  }

  function updateCarouselNav(track, prevBtn, nextBtn) {
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

  function scrollCarouselPrev(track, thumbs) {
    var scrollLeft = track.scrollLeft;
    if (scrollLeft <= 2) return;

    for (var i = thumbs.length - 1; i >= 0; i--) {
      var thumbLeft = getThumbScrollLeft(track, thumbs[i]);
      if (thumbLeft < scrollLeft - 4) {
        scrollToThumb(track, thumbs[i]);
        return;
      }
    }

    track.scrollTo({ left: 0, behavior: "smooth" });
  }

  function scrollCarouselNext(track, thumbs) {
    var scrollLeft = track.scrollLeft;
    var viewportRight = scrollLeft + track.clientWidth;
    var maxScroll = track.scrollWidth - track.clientWidth;
    if (scrollLeft >= maxScroll - 2) return;

    for (var i = 0; i < thumbs.length; i++) {
      var thumbLeft = getThumbScrollLeft(track, thumbs[i]);
      var thumbRight = thumbLeft + thumbs[i].offsetWidth;
      if (thumbRight > viewportRight + 4) {
        scrollToThumb(track, thumbs[i]);
        return;
      }
    }

    track.scrollTo({ left: maxScroll, behavior: "smooth" });
  }

  function initThumbnailCarousel(wrap, onActiveChange) {
    var track = wrap.querySelector("[data-video-thumbs]");
    var prevBtn = wrap.querySelector("[data-preview-playlist-prev]");
    var nextBtn = wrap.querySelector("[data-preview-playlist-next]");
    if (!track) return null;

    var thumbs = Array.prototype.slice.call(track.querySelectorAll("button[data-video-index], button[data-youtube-id]"));

    function onScroll() {
      updateCarouselNav(track, prevBtn, nextBtn);
    }

    if (prevBtn) {
      prevBtn.addEventListener("click", function () {
        scrollCarouselPrev(track, thumbs);
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        scrollCarouselNext(track, thumbs);
      });
    }

    track.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });

    requestAnimationFrame(function () {
      onScroll();
    });

    return {
      thumbs: thumbs,
      track: track,
      scrollToThumb: function (thumb) {
        scrollThumbIntoView(track, thumb);
      },
      notifyActive: function (thumb) {
        if (thumb) {
          updateVideoLabel(wrap.closest(".page-preview-detail-player-wrap"), thumb);
          scrollThumbIntoView(track, thumb);
        }
        onScroll();
      },
    };
  }

  function initPreviewPlayer(playerWrap) {
    if (playerWrap.getAttribute("data-preview-player-ready") === "true") return;
    playerWrap.setAttribute("data-preview-player-ready", "true");

    var root = playerWrap.querySelector("[data-class-detail-player]") || playerWrap.querySelector(".page-preview-detail-player");
    var carouselWrap = playerWrap.querySelector("[data-preview-thumbnail-carousel]") || playerWrap.querySelector(".page-preview-detail-playlist-wrap");
    if (!root || !carouselWrap) return;

    var video = root.querySelector("video");
    var iframe = root.querySelector("iframe");

    var carousel = initThumbnailCarousel(carouselWrap);
    if (!carousel) return;

    var thumbs = carousel.thumbs;
    if (iframe && !video) {
      var currentYoutubePosition = Math.max(
        0,
        thumbs.findIndex(function (btn) {
          return btn.classList.contains("is-active");
        })
      );

      function youtubeSrc(thumb, shouldPlay) {
        var id = thumb.getAttribute("data-youtube-id");
        var src = thumb.getAttribute("data-youtube-src");
        if (!src && id) {
          src = "https://www.youtube.com/embed/" + encodeURIComponent(id) + "?rel=0&modestbranding=1&playsinline=1";
        }
        if (src && shouldPlay && src.indexOf("autoplay=1") === -1) {
          src += (src.indexOf("?") === -1 ? "?" : "&") + "autoplay=1";
        }
        return src || "";
      }

      function setActiveYoutubeThumb(position) {
        thumbs.forEach(function (btn, idx) {
          btn.classList.toggle("is-active", idx === position);
        });
        carousel.notifyActive(thumbs[position]);
      }

      function loadYoutube(position, shouldPlay) {
        if (position < 0 || position >= thumbs.length) return;
        currentYoutubePosition = position;
        var src = youtubeSrc(thumbs[position], shouldPlay);
        if (src) iframe.src = src;
        var img = thumbs[position].querySelector("img");
        iframe.title = thumbs[position].getAttribute("data-video-title") || (img ? img.alt : "Course Preview Video");
        setActiveYoutubeThumb(position);
      }

      thumbs.forEach(function (btn, position) {
        btn.addEventListener("click", function () {
          loadYoutube(position, true);
        });
      });

      loadYoutube(currentYoutubePosition, false);
      return;
    }

    if (!video) return;
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

    var playlist = thumbs.map(function (btn, position) {
      return {
        position: position,
        src: btn.getAttribute("data-video-src") || "",
        poster: btn.getAttribute("data-video-poster") || "",
        title: btn.getAttribute("data-video-title") || "",
      };
    });

    var currentPosition = 0;

    function setPlaying(playing) {
      root.classList.toggle("is-playing", playing);
      playButtons.forEach(function (btn) {
        btn.setAttribute("aria-label", playing ? "Pause video" : "Play video");
      });
    }

    function setActiveThumb(position) {
      thumbs.forEach(function (btn, idx) {
        btn.classList.toggle("is-active", idx === position);
      });
      carousel.notifyActive(thumbs[position]);
    }

    function updateTimeUI() {
      if (timeCurrent) timeCurrent.textContent = formatTime(video.currentTime);
      if (timeTotal) timeTotal.textContent = formatTime(video.duration);
      if (fill && isFinite(video.duration) && video.duration > 0) {
        fill.style.width = (video.currentTime / video.duration) * 100 + "%";
      }
    }

    function updatePlayerNav() {
      if (prevBtn) prevBtn.disabled = currentPosition <= 0;
      if (nextBtn) nextBtn.disabled = currentPosition >= playlist.length - 1;
    }

    function loadVideo(position, shouldPlay) {
      if (position < 0 || position >= playlist.length) return;

      currentPosition = position;
      var item = playlist[position];

      if (source && item.src) source.src = item.src;
      if (item.src) video.src = item.src;
      if (item.poster) video.poster = item.poster;

      setActiveThumb(position);
      video.load();

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

      updatePlayerNav();
      updateTimeUI();
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
        loadVideo(currentPosition - 1, true);
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        loadVideo(currentPosition + 1, true);
      });
    }

    thumbs.forEach(function (btn, position) {
      btn.addEventListener("click", function () {
        loadVideo(position, true);
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
        var target = root.querySelector(".page-preview-detail-video-stage") || video;
        if (target.requestFullscreen) target.requestFullscreen();
      });
    }

    video.addEventListener("loadedmetadata", updateTimeUI);
    video.addEventListener("timeupdate", updateTimeUI);
    video.addEventListener("play", function () {
      setPlaying(true);
    });
    video.addEventListener("pause", function () {
      setPlaying(false);
    });
    video.addEventListener("ended", function () {
      setPlaying(false);
      if (currentPosition < playlist.length - 1) {
        loadVideo(currentPosition + 1, true);
      }
    });

    var initialPosition = thumbs.findIndex(function (btn) {
      return btn.classList.contains("is-active");
    });
    currentPosition = initialPosition >= 0 ? initialPosition : 0;
    setActiveThumb(currentPosition);
    updatePlayerNav();
    updateTimeUI();
  }

  function init() {
    document
      .querySelectorAll(".preview-video-detail-page .page-preview-detail-player-wrap")
      .forEach(initPreviewPlayer);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

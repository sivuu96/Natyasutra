(function () {
  "use strict";

  var COMPACT_NAV_MQ = window.matchMedia("(max-width: 1023px)");
  var navDropdownBackdrop = null;

  function syncNavHeight() {
    var nav = document.querySelector("nav");
    if (!nav) return;
    document.documentElement.style.setProperty(
      "--site-nav-height",
      nav.getBoundingClientRect().height + "px"
    );
  }

  function ensureNavDropdownBackdrop() {
    if (navDropdownBackdrop) return navDropdownBackdrop;
    navDropdownBackdrop = document.createElement("div");
    navDropdownBackdrop.className = "nav-dropdown-backdrop";
    navDropdownBackdrop.setAttribute("aria-hidden", "true");
    navDropdownBackdrop.addEventListener("click", closeAllNavDropdowns);
    document.body.appendChild(navDropdownBackdrop);
    return navDropdownBackdrop;
  }

  function setNavDropdownBackdropVisible(visible) {
    if (!COMPACT_NAV_MQ.matches) visible = false;
    var backdrop = ensureNavDropdownBackdrop();
    backdrop.classList.toggle("is-visible", visible);
    backdrop.setAttribute("aria-hidden", visible ? "false" : "true");
    document.body.classList.toggle("nav-dropdown-open", visible);
  }

  function resetNavDropdownPosition(menu) {
    menu.style.position = "";
    menu.style.top = "";
    menu.style.right = "";
    menu.style.left = "";
    menu.style.width = "";
    menu.style.maxHeight = "";
    menu.style.transformOrigin = "";
  }

  function positionNavDropdown(menu, btn) {
    if (!COMPACT_NAV_MQ.matches) {
      resetNavDropdownPosition(menu);
      return;
    }

    syncNavHeight();
    var nav = document.querySelector("nav");
    if (!nav) return;

    var navRect = nav.getBoundingClientRect();
    var btnRect = btn.getBoundingClientRect();
    var gutter = Math.max(12, Math.min(16, window.innerWidth * 0.04));
    var isAccount = menu.classList.contains("nav-dropdown-panel--account");
    var maxWidth = isAccount ? 224 : 352;
    var width = Math.min(maxWidth, window.innerWidth - gutter * 2);
    var right = window.innerWidth - btnRect.right;
    right = Math.max(gutter, Math.min(right, window.innerWidth - width - gutter));
    var maxHeight = window.innerHeight - navRect.bottom - gutter - 8;

    menu.style.position = "fixed";
    menu.style.top = Math.round(navRect.bottom + 8) + "px";
    menu.style.right = Math.round(right) + "px";
    menu.style.left = "auto";
    menu.style.width = Math.round(width) + "px";
    menu.style.maxHeight = Math.max(180, Math.round(maxHeight)) + "px";
    menu.style.transformOrigin = "top right";
  }

  function initNavDropdown(btnId, menuId, wrapId) {
    var btn = document.getElementById(btnId);
    var menu = document.getElementById(menuId);
    var wrap = document.getElementById(wrapId);
    if (!btn || !menu || !wrap) return;

    function close() {
      menu.classList.remove("is-open");
      btn.setAttribute("aria-expanded", "false");
      resetNavDropdownPosition(menu);
      if (!document.querySelector(".nav-dropdown-panel.is-open")) {
        setNavDropdownBackdropVisible(false);
      }
    }

    function open() {
      positionNavDropdown(menu, btn);
      menu.classList.add("is-open");
      btn.setAttribute("aria-expanded", "true");
      setNavDropdownBackdropVisible(true);
    }

    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      document.querySelectorAll(".nav-dropdown-panel.is-open").forEach(function (panel) {
        if (panel !== menu) {
          panel.classList.remove("is-open");
          resetNavDropdownPosition(panel);
          var otherBtn = panel.parentElement && panel.parentElement.querySelector("button[aria-haspopup]");
          if (otherBtn) otherBtn.setAttribute("aria-expanded", "false");
        }
      });
      if (menu.classList.contains("is-open")) {
        close();
      } else {
        open();
      }
    });

    document.addEventListener("click", function (e) {
      if (!wrap.contains(e.target)) close();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });
  }

  function closeAllNavDropdowns() {
    document.querySelectorAll(".nav-dropdown-panel.is-open").forEach(function (panel) {
      panel.classList.remove("is-open");
      resetNavDropdownPosition(panel);
      var btn = panel.parentElement && panel.parentElement.querySelector("button[aria-haspopup]");
      if (btn) btn.setAttribute("aria-expanded", "false");
    });
    setNavDropdownBackdropVisible(false);
  }

  function initNavDropdowns() {
    initNavDropdown("cartDropdownBtn", "cartDropdownMenu", "cartDropdownWrap");
    initNavDropdown("avatarDropdownBtn", "avatarDropdownMenu", "avatarDropdownWrap");

    window.addEventListener(
      "resize",
      function () {
        syncNavHeight();
        document.querySelectorAll(".nav-dropdown-panel.is-open").forEach(function (panel) {
          var btn = panel.parentElement && panel.parentElement.querySelector("button[aria-haspopup]");
          if (!btn) return;
          if (COMPACT_NAV_MQ.matches) {
            positionNavDropdown(panel, btn);
          } else {
            resetNavDropdownPosition(panel);
            setNavDropdownBackdropVisible(false);
          }
        });
      },
      { passive: true }
    );

    window.addEventListener(
      "scroll",
      function () {
        if (!COMPACT_NAV_MQ.matches) return;
        document.querySelectorAll(".nav-dropdown-panel.is-open").forEach(function (panel) {
          var btn = panel.parentElement && panel.parentElement.querySelector("button[aria-haspopup]");
          if (btn) positionNavDropdown(panel, btn);
        });
      },
      { passive: true }
    );
  }

  function initMegaAndMobileMenu() {
    var megaMenuPairs = [
      ["danceClassesBtn", "megaMenu"],
      ["programmesBtn", "programmesMegaMenu"],
    ];
    var megaMenuEntries = megaMenuPairs
      .map(function (pair) {
        return {
          btn: document.getElementById(pair[0]),
          menu: document.getElementById(pair[1]),
        };
      })
      .filter(function (entry) {
        return entry.btn && entry.menu;
      });

    megaMenuEntries.forEach(function (entry) {
      entry.btn.addEventListener("click", function (e) {
        e.stopPropagation();
        var isHidden = entry.menu.classList.contains("invisible");
        megaMenuEntries.forEach(function (other) {
          if (other.menu !== entry.menu) {
            other.menu.classList.add("opacity-0", "invisible");
            other.menu.classList.remove("opacity-100", "visible");
          }
        });
        if (isHidden) {
          entry.menu.classList.remove("opacity-0", "invisible");
          entry.menu.classList.add("opacity-100", "visible");
        } else {
          entry.menu.classList.add("opacity-0", "invisible");
          entry.menu.classList.remove("opacity-100", "visible");
        }
      });
    });

    if (megaMenuEntries.length) {
      document.addEventListener("click", function (e) {
        megaMenuEntries.forEach(function (entry) {
          if (!entry.menu.contains(e.target) && !entry.btn.contains(e.target)) {
            entry.menu.classList.add("opacity-0", "invisible");
            entry.menu.classList.remove("opacity-100", "visible");
          }
        });
      });
    }

    var mobileBtn = document.getElementById("mobileMenuBtn");
    var mobileMenu = document.getElementById("mobileMenu");
    var closeMobileMenu = document.getElementById("closeMobileMenu");

    if (mobileBtn && mobileMenu) {
      mobileBtn.addEventListener("click", function () {
        closeAllNavDropdowns();
        mobileMenu.classList.remove("translate-x-full");
        document.body.style.overflow = "hidden";
      });
    }
    if (closeMobileMenu && mobileMenu) {
      closeMobileMenu.addEventListener("click", function () {
        mobileMenu.classList.add("translate-x-full");
        document.body.style.overflow = "";
      });
    }
  }

  // Matches index.html initCarousels behavior.
  function initCarousels() {
    document.querySelectorAll("[data-carousel]").forEach(function (root) {
      var track = root.querySelector(".carousel-track");
      var resolvedSlides = Array.prototype.slice.call(root.querySelectorAll(".carousel-slide"));
      var prevBtn = root.querySelector("[data-carousel-prev]");
      var nextBtn = root.querySelector("[data-carousel-next]");
      var dotsContainer = root.querySelector("[data-carousel-dots]");
      var useDots = root.dataset.dots === "true";
      var step = parseInt(root.dataset.step || "1", 10);

      if (!prevBtn || !nextBtn) {
        var carouselSection = root.closest(".page-section, section");
        if (carouselSection) {
          prevBtn = prevBtn || carouselSection.querySelector("[data-carousel-prev]");
          nextBtn = nextBtn || carouselSection.querySelector("[data-carousel-next]");
        }
      }

      if (!track || resolvedSlides.length === 0) return;

      var perViewConfig = { default: 1 };
      try {
        perViewConfig = JSON.parse(root.dataset.perView || '{"default":1}');
      } catch (e) {
        perViewConfig = { default: 1 };
      }

      var index = 0;

      function getPerView() {
        var w = window.innerWidth;
        if (w >= 1280 && perViewConfig.xl) return perViewConfig.xl;
        if (w >= 1024 && perViewConfig.lg) return perViewConfig.lg;
        if (w >= 768 && perViewConfig.md) return perViewConfig.md;
        if (w >= 640 && perViewConfig.sm) return perViewConfig.sm;
        return perViewConfig.default || 1;
      }

      function getMaxIndex() {
        return Math.max(0, resolvedSlides.length - getPerView());
      }

      function getPageCount() {
        var pv = getPerView();
        return Math.max(1, Math.ceil((resolvedSlides.length - pv) / step) + 1);
      }

      function getPageIndex() {
        return Math.floor(index / step);
      }

      function setSlideWidths() {
        var pv = getPerView();
        var widthPercent = 100 / pv;
        resolvedSlides.forEach(function (slide) {
          slide.style.flex = "0 0 " + widthPercent + "%";
          slide.style.width = widthPercent + "%";
        });
      }

      function renderDots() {
        if (!dotsContainer || !useDots) return;
        var pageCount = getPageCount();
        dotsContainer.innerHTML = "";
        dotsContainer.removeAttribute("role");
        for (var i = 0; i < pageCount; i++) {
          var dot = document.createElement("button");
          dot.type = "button";
          dot.className = "carousel-dot" + (i === getPageIndex() ? " is-active" : "");
          dot.setAttribute("aria-label", "Go to slide group " + (i + 1));
          dot.setAttribute("aria-current", i === getPageIndex() ? "true" : "false");
          (function (dotIndex) {
            dot.addEventListener("click", function () {
              index = Math.min(dotIndex * step, getMaxIndex());
              update();
            });
          })(i);
          dotsContainer.appendChild(dot);
        }
      }

      function update() {
        var maxIndex = getMaxIndex();
        index = Math.max(0, Math.min(index, maxIndex));
        var perView = getPerView();
        var offsetPercent = index * 100 / perView;
        track.style.transform = "translate3d(-" + offsetPercent + "%, 0, 0)";

        if (prevBtn) prevBtn.disabled = index <= 0;
        if (nextBtn) nextBtn.disabled = index >= maxIndex;

        if (dotsContainer && useDots) {
          Array.prototype.slice.call(dotsContainer.children).forEach(function (dot, i) {
            var isActive = i === getPageIndex();
            dot.classList.toggle("is-active", isActive);
            dot.setAttribute("aria-current", isActive ? "true" : "false");
          });
        }
      }

      setSlideWidths();
      renderDots();
      update();

      if (prevBtn) {
        prevBtn.addEventListener("click", function () {
          index = Math.max(0, index - step);
          update();
        });
      }

      if (nextBtn) {
        nextBtn.addEventListener("click", function () {
          index = Math.min(getMaxIndex(), index + step);
          update();
        });
      }

      var resizeTimer;
      window.addEventListener("resize", function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function () {
          setSlideWidths();
          renderDots();
          update();
        }, 150);
      });

      var touchStartX = 0;
      var touchDeltaX = 0;
      var viewport = root.querySelector(".carousel-viewport");
      if (viewport) {
        viewport.addEventListener(
          "touchstart",
          function (e) {
            touchStartX = e.touches[0].clientX;
            touchDeltaX = 0;
          },
          { passive: true }
        );
        viewport.addEventListener(
          "touchmove",
          function (e) {
            touchDeltaX = e.touches[0].clientX - touchStartX;
          },
          { passive: true }
        );
        viewport.addEventListener("touchend", function () {
          if (Math.abs(touchDeltaX) < 40) return;
          if (touchDeltaX < 0) {
            index = Math.min(getMaxIndex(), index + step);
          } else {
            index = Math.max(0, index - step);
          }
          update();
        });
      }
    });
  }

  function initTabs() {
    document.querySelectorAll("[data-tabs]").forEach(function (root) {
      var tabs = Array.prototype.slice.call(root.querySelectorAll(".page-tab"));
      var panels = root.parentElement.querySelectorAll(".page-tab-panel");
      if (!tabs.length || !panels.length) return;
      tabs.forEach(function (tab) {
        tab.addEventListener("click", function () {
          var id = tab.getAttribute("data-tab");
          tabs.forEach(function (item) {
            var isActive = item === tab;
            item.classList.toggle("is-active", isActive);
            item.setAttribute("aria-selected", isActive ? "true" : "false");
          });
          Array.prototype.forEach.call(panels, function (panel) {
            panel.classList.toggle("is-active", panel.getAttribute("data-tab-panel") === id);
          });
        });
      });
    });
  }

  function initPillTabs() {
    document.querySelectorAll("[data-pill-tabs]").forEach(function (root) {
      var tabs = Array.prototype.slice.call(
        root.querySelectorAll(".page-pill-tab, .page-programmes-lesson-tab")
      );
      tabs.forEach(function (tab) {
        tab.addEventListener("click", function () {
          tabs.forEach(function (item) {
            item.classList.toggle("is-active", item === tab);
          });
        });
      });
    });
  }

  function initProgrammesLessonTabs() {
    document.querySelectorAll("[data-programmes-lesson-tabs]").forEach(function (row) {
      var block = row.closest(".page-programmes-level-block");
      if (!block) return;
      var featured = block.querySelector("[data-programmes-featured]");
      if (!featured) return;
      var image = featured.querySelector("[data-featured-image]");
      var kicker = featured.querySelector("[data-featured-kicker]");
      var title = featured.querySelector("[data-featured-title]");
      var guru = featured.querySelector("[data-featured-guru]");
      var desc = featured.querySelector("[data-featured-desc]");
      var metricsRoot = featured.querySelector("[data-featured-metrics]");
      var tabs = Array.prototype.slice.call(row.querySelectorAll(".page-programmes-lesson-tab"));

      function metricHtml(label, value) {
        return (
          '<div class="page-programmes-metric"><span class="page-programmes-metric-label">' +
          label +
          '</span><strong class="page-programmes-metric-value">' +
          value +
          "</strong></div>"
        );
      }

      tabs.forEach(function (tab) {
        tab.addEventListener("click", function () {
          if (image) {
            image.src = tab.getAttribute("data-featured-img") || image.src;
            image.alt = tab.getAttribute("data-featured-title") || image.alt;
          }
          if (kicker) kicker.textContent = tab.getAttribute("data-featured-kicker") || "";
          if (title) title.textContent = tab.getAttribute("data-featured-title") || "";
          if (guru) guru.textContent = tab.getAttribute("data-featured-guru") || "";
          if (desc) desc.textContent = tab.getAttribute("data-featured-desc") || "";
          if (metricsRoot) {
            metricsRoot.innerHTML =
              '<div class="page-programmes-featured-metrics">' +
              metricHtml("Duration", tab.getAttribute("data-featured-duration") || "") +
              metricHtml("Lessons", tab.getAttribute("data-featured-lessons") || "") +
              metricHtml("Level", tab.getAttribute("data-featured-level") || "") +
              "</div>";
          }
        });
      });
    });
  }

  function initProgrammesFilter() {
    document.querySelectorAll("[data-programmes-filter]").forEach(function (root) {
      var pills = Array.prototype.slice.call(
        root.querySelectorAll(".page-programmes-category-pill")
      );
      pills.forEach(function (pill) {
        pill.addEventListener("click", function () {
          pills.forEach(function (item) {
            item.classList.toggle("is-active", item === pill);
          });
          var targetId = pill.getAttribute("data-programmes-target");
          if (!targetId) return;
          var section = document.getElementById("programmes-" + targetId);
          if (section) {
            section.scrollIntoView({ behavior: "smooth", block: "start" });
          }
        });
      });
    });
  }

  function initAccordion() {
    document.querySelectorAll("[data-accordion]").forEach(function (root) {
      var allowMulti = root.getAttribute("data-multi") === "true";
      var items = Array.prototype.slice.call(root.querySelectorAll("article"));
      items.forEach(function (item) {
        var trigger = item.querySelector("[data-accordion-trigger]");
        if (!trigger) return;
        trigger.addEventListener("click", function () {
          var open = item.classList.contains("is-open");
          if (!allowMulti) {
            items.forEach(function (other) {
              other.classList.remove("is-open");
            });
          }
          item.classList.toggle("is-open", !open);
        });
      });
    });
  }

  function formatTime(seconds) {
    if (!isFinite(seconds)) return "00:00";
    var mins = Math.floor(seconds / 60);
    var secs = Math.floor(seconds % 60);
    return String(mins).padStart(2, "0") + ":" + String(secs).padStart(2, "0");
  }

  function initVideoPlayers() {
    document.querySelectorAll("[data-video-player]:not([data-class-detail-player]):not([data-free-video-player])").forEach(function (root) {
      var video = root.querySelector("video");
      if (!video) return;
      var playButtons = root.querySelectorAll("[data-video-play]");
      var progress = root.querySelector("[data-video-progress]");
      var fill = root.querySelector("[data-video-progress-fill]");
      var time = root.querySelector("[data-video-time]");
      var timeCurrent = root.querySelector("[data-video-time-current]");
      var timeTotal = root.querySelector("[data-video-time-total]");
      var mute = root.querySelector("[data-video-mute]");
      var fullscreen = root.querySelector("[data-video-fullscreen]");

      function setPlaying(playing) {
        root.classList.toggle("is-playing", playing);
        playButtons.forEach(function (btn) {
          btn.setAttribute("aria-label", playing ? "Pause video" : "Play video");
        });
      }

      function updateTime() {
        var current = formatTime(video.currentTime);
        var total = formatTime(video.duration);
        if (time) {
          time.textContent = current + " / " + total;
        }
        if (timeCurrent) {
          timeCurrent.textContent = current;
        }
        if (timeTotal) {
          timeTotal.textContent = total;
        }
        if (fill && isFinite(video.duration) && video.duration > 0) {
          fill.style.width = (video.currentTime / video.duration) * 100 + "%";
        }
      }

      function togglePlay() {
        if (video.paused) {
          video.play();
          setPlaying(true);
        } else {
          video.pause();
          setPlaying(false);
        }
      }

      playButtons.forEach(function (play) {
        play.addEventListener("click", togglePlay);
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

      if (mute) {
        mute.addEventListener("click", function () {
          video.muted = !video.muted;
          mute.textContent = video.muted ? "Unmute" : "Mute";
        });
      }

      if (fullscreen) {
        fullscreen.addEventListener("click", function () {
          if (video.requestFullscreen) video.requestFullscreen();
        });
      }

      video.addEventListener("timeupdate", updateTime);
      video.addEventListener("loadedmetadata", updateTime);
      video.addEventListener("play", function () {
        setPlaying(true);
      });
      video.addEventListener("pause", function () {
        setPlaying(false);
      });
      video.addEventListener("ended", function () {
        setPlaying(false);
      });
      updateTime();
    });
  }

  function initVideoThumbs() {
    document.querySelectorAll("[data-video-thumbs]:not(.page-class-detail-thumbs):not(.page-free-video-detail-playlist)").forEach(function (root) {
      var buttons = Array.prototype.slice.call(root.querySelectorAll("button[data-video-src]"));
      if (!buttons.length) return;
      var player = root.closest(".page-video-hero, .page-video-player, section, div");
      var video = player ? player.querySelector("[data-video-player] video") : null;
      if (!video) return;
      var source = video.querySelector("source");

      buttons.forEach(function (btn) {
        btn.addEventListener("click", function () {
          var src = btn.getAttribute("data-video-src");
          var poster = btn.getAttribute("data-video-poster");
          if (source && src) source.src = src;
          if (src) video.src = src;
          if (poster) video.poster = poster;
          video.load();
          buttons.forEach(function (item) {
            item.classList.toggle("is-active", item === btn);
          });
        });
      });
    });
  }

  function initFilterForms() {
    document.querySelectorAll("[data-filter-toggle]").forEach(function (toggle) {
      var section = toggle.closest(".page-filter-bar");
      var content = section ? section.querySelector("[data-filter-content]") : null;
      if (!content) return;

      function setOpen(open) {
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
        content.classList.toggle("is-open", open);
        if (window.matchMedia("(min-width: 1024px)").matches) {
          content.style.maxHeight = "";
        } else {
          content.style.maxHeight = open ? content.scrollHeight + "px" : "0px";
        }
      }

      setOpen(false);

      toggle.addEventListener("click", function () {
        setOpen(toggle.getAttribute("aria-expanded") !== "true");
      });

      window.addEventListener(
        "resize",
        function () {
          if (window.matchMedia("(min-width: 1024px)").matches) {
            content.style.maxHeight = "";
          } else if (toggle.getAttribute("aria-expanded") === "true") {
            content.style.maxHeight = content.scrollHeight + "px";
          }
        },
        { passive: true }
      );
    });

    document.querySelectorAll("[data-filter-form]").forEach(function (form) {
      var applyBtn = form.querySelector("[data-filter-apply]");
      if (!applyBtn) return;
      applyBtn.addEventListener("click", function () {
        var cards = document.querySelectorAll(".page-class-card, .page-preview-card, .page-gallery-card");
        if (!cards.length) {
          alert("Filters applied");
          return;
        }
        var hidden = 0;
        cards.forEach(function (card, idx) {
          var show = idx < Math.ceil(cards.length * 0.66);
          card.style.display = show ? "" : "none";
          if (!show) hidden++;
        });
        if (hidden === 0) alert("No filters matched");
      });
    });
  }

  function initLearningPaths() {
    var pathData = {
      beginners: {
        pasyathi: {
          tag: "Beginners Path • Odissi",
          title: "Odissi Beginners Lessons",
          guru: "Guided by Sujata Mohapatra",
          desc: "Sujata Mohapatra gives an overview of Odissi Beginners Lessons.",
          duration: "4.5 Hours",
          lessons: "12 Lessons",
          level: "Beginner",
          img: "assets/images/classes/odissi-beginners-lessons.webp",
        },
        revathi: {
          tag: "Beginners Path • Kuchipudi",
          title: "Kuchipudi Beginners Lessons",
          guru: "Guided by Sreelakshmy Govardhanan",
          desc: "Sreelakshmy Govardhanan introduces the viewer to her journey in Kuchipudi.",
          duration: "3.5 Hours",
          lessons: "10 Lessons",
          level: "Beginner",
          img: "assets/images/classes/kuchipudi-beginners-lessons.webp",
        },
        ananthabhairavi: {
          tag: "Beginners Path • Kathak",
          title: "Beginners Lessons",
          guru: "Guided by Guru Dr Pali Chandra",
          desc: "An introduction to foundational Kathak technique, focusing on basic movements and gestures.",
          duration: "4.0 Hours",
          lessons: "14 Lessons",
          level: "Beginner",
          img: "assets/images/classes/beginners-lessons.webp",
        },
      },
    };

    pathData.master_class = pathData.beginners;
    pathData.composition = pathData.beginners;
    pathData.intermediate = pathData.beginners;
    pathData.technique = pathData.beginners;
    pathData.performance = pathData.beginners;

    document.querySelectorAll(".curated-learning-paths").forEach(function (section) {
      if (section.getAttribute("data-learning-paths-ready") === "true") return;

      var pathPanel = section.querySelector("#pathPanel, #guruPathPanel");
      var primaryTabsContainer = section.querySelector("#primaryTabsContainer, #guruPrimaryTabsContainer");
      var secondaryTabsContainer = section.querySelector("#secondaryTabsContainer, #guruSecondaryTabsContainer");
      var primaryTabs = Array.prototype.slice.call(section.querySelectorAll(".primary-path-tab"));
      var secondaryTabs = Array.prototype.slice.call(section.querySelectorAll(".secondary-path-tab"));
      var pathImg = section.querySelector("#pathImg, #guruPathImg");
      var pathTag = section.querySelector("#pathTag, #guruPathTag");
      var pathTitle = section.querySelector("#pathTitle, #guruPathTitle");
      var pathGuru = section.querySelector("#pathGuru, #guruPathGuru");
      var pathDesc = section.querySelector("#pathDesc, #guruPathDesc");
      var pathDuration = section.querySelector("#pathDuration, #guruPathDuration");
      var pathLessons = section.querySelector("#pathLessons, #guruPathLessons");
      var pathLevel = section.querySelector("#pathLevel, #guruPathLevel");

      if (!pathPanel || !primaryTabs.length || !secondaryTabs.length) return;
      section.setAttribute("data-learning-paths-ready", "true");

      var activePrimaryTab = (primaryTabs.find(function (tab) {
        return tab.classList.contains("text-brand-pink");
      }) || primaryTabs[0]).getAttribute("data-tab");
      var activeSecondaryTab = (secondaryTabs.find(function (tab) {
        return tab.classList.contains("bg-brand-pink");
      }) || secondaryTabs[0]).getAttribute("data-tab");

      function scrollTabIntoView(tab, container) {
        if (!tab || !container) return;
        tab.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
      }

      function updatePathPanel(animate) {
        if (animate === undefined) animate = true;
        var bucket = pathData[activePrimaryTab] || pathData.beginners;
        var data = bucket[activeSecondaryTab] || bucket.pasyathi;
        if (!data) return;

        function apply() {
          if (pathImg) {
            pathImg.src = data.img;
            pathImg.alt = data.title;
          }
          if (pathTag) pathTag.textContent = data.tag;
          if (pathTitle) pathTitle.textContent = data.title;
          if (pathGuru) pathGuru.textContent = data.guru;
          if (pathDesc) pathDesc.textContent = data.desc;
          if (pathDuration) pathDuration.textContent = data.duration;
          if (pathLessons) pathLessons.textContent = data.lessons;
          if (pathLevel) pathLevel.textContent = data.level;
          pathPanel.style.opacity = "1";
        }

        if (animate) {
          pathPanel.style.opacity = "0";
          window.setTimeout(apply, 150);
        } else {
          apply();
        }
      }

      function switchSecondaryTab(tabKey) {
        activeSecondaryTab = tabKey;
        var activeTabEl = null;
        secondaryTabs.forEach(function (tab) {
          var isActive = tab.getAttribute("data-tab") === tabKey;
          if (isActive) activeTabEl = tab;
          tab.classList.toggle("bg-brand-pink", isActive);
          tab.classList.toggle("text-white", isActive);
          tab.classList.toggle("shadow-sm", isActive);
          tab.classList.toggle("bg-white", !isActive);
          tab.classList.toggle("border", !isActive);
          tab.classList.toggle("border-gray-200", !isActive);
          tab.classList.toggle("text-gray-500", !isActive);
          tab.classList.toggle("hover:bg-brand-cream/50", !isActive);
          tab.classList.toggle("hover:text-brand-purple", !isActive);
        });
        scrollTabIntoView(activeTabEl, secondaryTabsContainer);
        updatePathPanel();
      }

      primaryTabs.forEach(function (tab) {
        tab.addEventListener("click", function () {
          primaryTabs.forEach(function (item) {
            var isActive = item === tab;
            item.classList.toggle("border-brand-pink", isActive);
            item.classList.toggle("text-brand-pink", isActive);
            item.classList.toggle("border-transparent", !isActive);
            item.classList.toggle("text-gray-400", !isActive);
          });
          activePrimaryTab = tab.getAttribute("data-tab");
          scrollTabIntoView(tab, primaryTabsContainer);
          updatePathPanel();
        });
      });

      secondaryTabs.forEach(function (tab) {
        tab.addEventListener("click", function () {
          switchSecondaryTab(tab.getAttribute("data-tab"));
        });
      });

      updatePathPanel(false);
    });
  }

  function initPagination() {
    document.querySelectorAll("[data-pagination]").forEach(function (root) {
      var buttons = Array.prototype.slice.call(root.querySelectorAll("[data-page]"));
      var next = root.querySelector("[data-page-next]");
      if (!buttons.length) return;

      function activate(btn) {
        buttons.forEach(function (b) {
          b.classList.toggle("is-active", b === btn);
        });
      }

      buttons.forEach(function (btn) {
        btn.addEventListener("click", function () {
          activate(btn);
        });
      });

      if (next) {
        next.addEventListener("click", function () {
          var activeIndex = Math.max(
            0,
            buttons.findIndex(function (btn) {
              return btn.classList.contains("is-active");
            })
          );
          var target = buttons[Math.min(buttons.length - 1, activeIndex + 1)];
          activate(target);
        });
      }
    });
  }

  function initScrollReveal() {
    var nodes = document.querySelectorAll(".page-reveal");
    if (!nodes.length) return;

    if (!("IntersectionObserver" in window)) {
      nodes.forEach(function (n) {
        n.classList.add("is-visible");
      });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.16, rootMargin: "0px 0px -10% 0px" }
    );

    nodes.forEach(function (node) {
      observer.observe(node);
    });
  }

  function initStickyShadow() {
    var sticky = document.querySelector(".page-sticky-nav");
    if (!sticky) return;
    function onScroll() {
      sticky.classList.toggle("is-shadow", window.scrollY > 16);
    }
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  function init() {
    syncNavHeight();
    window.addEventListener("resize", syncNavHeight, { passive: true });
    initNavDropdowns();
    initMegaAndMobileMenu();
    initCarousels();
    initTabs();
    initPillTabs();
    initProgrammesLessonTabs();
    initProgrammesFilter();
    initAccordion();
    initVideoPlayers();
    initVideoThumbs();
    initFilterForms();
    initLearningPaths();
    initPagination();
    initScrollReveal();
    initStickyShadow();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

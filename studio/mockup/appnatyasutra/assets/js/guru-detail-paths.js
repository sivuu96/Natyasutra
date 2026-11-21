(function () {
  "use strict";

  var pathPanel = document.getElementById("guruPathPanel");
  if (!pathPanel) return;

  var pathData = {
    beginners: {
      pasyathi: {
        tag: "Beginners Path • Kathak",
        title: "Payaliya Tarana - Beginners Foundation",
        guru: "Guided by Guru Dr Pali Chandra",
        desc: "Master foundational footwork, postures, and rhythmic patterns required for the expressive Tarana composition.",
        duration: "4.5 Hours",
        lessons: "12 Lessons",
        level: "Beginner",
        img: "assets/images/classes/odissi-beginners-lessons.webp",
      },
      revathi: {
        tag: "Beginners Path • Kathak",
        title: "Thumri Expressions - Beginners Guide",
        guru: "Guided by Guru Dr Pali Chandra",
        desc: "Learn basic abhinaya, gesture vocabulary, and introductory rhythmic patterns for lyrical Kathak repertoire.",
        duration: "3.5 Hours",
        lessons: "10 Lessons",
        level: "Beginner",
        img: "assets/images/classes/odissi-beginners-lessons.webp",
      },
      ananthabhairavi: {
        tag: "Beginners Path • Kathak",
        title: "Parayatti - Basics",
        guru: "Guided by Guru Dr Pali Chandra",
        desc: "An introduction to foundational Kathak technique with guided adavus, transitions, and theory notes.",
        duration: "4.0 Hours",
        lessons: "14 Lessons",
        level: "Beginner",
        img: "assets/images/classes/odissi-beginners-lessons.webp",
      },
    },
    master_class: {
      pasyathi: {
        tag: "Master Class • Kathak",
        title: "Payaliya Tarana - Master Class",
        guru: "Guided by Guru Dr Pali Chandra",
        desc: "Delve deep into fast footwork, chakkars, and performance-level precision in this signature Tarana.",
        duration: "6.0 Hours",
        lessons: "22 Lessons",
        level: "Advanced",
        img: "assets/images/classes/odissi-beginners-lessons.webp",
      },
      revathi: {
        tag: "Master Class • Kathak",
        title: "Parayatti (Kathak) Master Class",
        guru: "Guided by Guru Dr Pali Chandra",
        desc: "Refine your performance style, speed, and precision in executing complex compositions and stage repertoire.",
        duration: "5.5 Hours",
        lessons: "18 Lessons",
        level: "Advanced",
        img: "assets/images/classes/odissi-beginners-lessons.webp",
      },
      ananthabhairavi: {
        tag: "Master Class • Kathak",
        title: "Shringara Lahari - Choreography",
        guru: "Guided by Guru Dr Pali Chandra",
        desc: "Master choreographic structure, rhythmic complexity, and deep expressive patterns in this classic composition.",
        duration: "5.0 Hours",
        lessons: "20 Lessons",
        level: "Advanced",
        img: "assets/images/classes/odissi-beginners-lessons.webp",
      },
    },
    composition: {
      pasyathi: {
        tag: "Composition Path • Kathak",
        title: "Paayaliya Shubh Dinni - Full Composition Study",
        guru: "Guided by Guru Dr Pali Chandra",
        desc: "Complete choreography and song-length practice with audio guides, lyric meanings, and performance notes.",
        duration: "8.0 Hours",
        lessons: "28 Lessons",
        level: "Advanced",
        img: "assets/images/classes/odissi-beginners-lessons.webp",
      },
      revathi: {
        tag: "Composition Path • Kathak",
        title: "Mora Re Ang - Complete Choreography",
        guru: "Guided by Guru Dr Pali Chandra",
        desc: "Learn the full composition from initial pravesha to final mudras, ready for stage presentation.",
        duration: "7.0 Hours",
        lessons: "24 Lessons",
        level: "Advanced",
        img: "assets/images/classes/odissi-beginners-lessons.webp",
      },
      ananthabhairavi: {
        tag: "Composition Path • Kathak",
        title: "Lalitun Aranga - Complete Repertoire",
        guru: "Guided by Guru Dr Pali Chandra",
        desc: "Learn the entire composition combining rhythmic footwork and expressive abhinaya for full performance.",
        duration: "7.5 Hours",
        lessons: "26 Lessons",
        level: "Advanced",
        img: "assets/images/classes/odissi-beginners-lessons.webp",
      },
    },
  };

  pathData.intermediate = pathData.beginners;
  pathData.technique = pathData.master_class;
  pathData.performance = pathData.composition;

  var activePrimaryTab = "beginners";
  var activeSecondaryTab = "pasyathi";

  var primaryTabsContainer = document.getElementById("guruPrimaryTabsContainer");
  var secondaryTabsContainer = document.getElementById("guruSecondaryTabsContainer");
  var primaryTabs = document.querySelectorAll(".guru-detail-learning-paths .primary-path-tab");
  var secondaryTabs = document.querySelectorAll(".guru-detail-learning-paths .secondary-path-tab");

  var pathImg = document.getElementById("guruPathImg");
  var pathTag = document.getElementById("guruPathTag");
  var pathTitle = document.getElementById("guruPathTitle");
  var pathGuru = document.getElementById("guruPathGuru");
  var pathDesc = document.getElementById("guruPathDesc");
  var pathDuration = document.getElementById("guruPathDuration");
  var pathLessons = document.getElementById("guruPathLessons");
  var pathLevel = document.getElementById("guruPathLevel");

  function scrollTabIntoView(tab, container) {
    if (!tab || !container) return;
    tab.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
  }

  function switchSecondaryTab(tabKey) {
    activeSecondaryTab = tabKey;
    var activeTabEl = null;
    secondaryTabs.forEach(function (t) {
      var tKey = t.getAttribute("data-tab");
      if (tKey === tabKey) {
        activeTabEl = t;
        t.classList.remove("bg-white", "border", "border-gray-200", "text-gray-500", "hover:bg-brand-cream/50", "hover:text-brand-purple");
        t.classList.add("bg-brand-pink", "text-white", "shadow-sm");
      } else {
        t.classList.add("bg-white", "border", "border-gray-200", "text-gray-500", "hover:bg-brand-cream/50", "hover:text-brand-purple");
        t.classList.remove("bg-brand-pink", "text-white", "shadow-sm");
      }
    });
    if (activeTabEl) scrollTabIntoView(activeTabEl, secondaryTabsContainer);
    updatePathPanel();
  }

  function updatePathPanel(animate) {
    if (animate === undefined) animate = true;
    if (!activeSecondaryTab) return;
    var bucket = pathData[activePrimaryTab];
    if (!bucket) return;
    var data = bucket[activeSecondaryTab];
    if (!data || !pathPanel) return;

    function apply() {
      pathImg.src = data.img;
      pathImg.alt = data.title;
      pathTag.textContent = data.tag;
      pathTitle.textContent = data.title;
      pathGuru.textContent = data.guru;
      pathDesc.textContent = data.desc;
      pathDuration.textContent = data.duration;
      pathLessons.textContent = data.lessons;
      pathLevel.textContent = data.level;
      pathPanel.style.opacity = "1";
    }

    if (animate) {
      pathPanel.style.opacity = "0";
      setTimeout(apply, 150);
    } else {
      apply();
    }
  }

  primaryTabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      primaryTabs.forEach(function (t) {
        t.classList.remove("border-brand-pink", "text-brand-pink");
        t.classList.add("border-transparent", "text-gray-400");
      });
      tab.classList.add("border-brand-pink", "text-brand-pink");
      tab.classList.remove("border-transparent", "text-gray-400");
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
})();


        function closeAllNavDropdowns() {
            if (window.NatyaNavDropdowns) window.NatyaNavDropdowns.closeAll();
        }

        // Hero help modal triggers
        const heroHelpData = {
            'start-learning': {
                user: 'Which beginner course do you recommend?',
                bot: ['We recommend the Beginner Kathak Lessons by Guru Dr. Pali Chandra'],
                cta: { text: 'Start Beginner Course', href: 'class-detail-page.html' },
                time: '09:25 AM'
            },
            'legendary-gurus': {
                user: 'Who are the legendary gurus on Natyasutra?',
                bot: ['Explore masters like Guru Dr Pali Chandra, Madhavi Mudgal, and Dr Neena Prasad — all in one place.'],
                cta: { text: 'Browse Gurus', href: 'guru-listing-page.html' },
                time: '09:26 AM'
            },
            'child-classes': {
                user: 'Do you have classes suitable for children?',
                bot: ['Yes! Our curated programmes include gentle introductions to Bharatanatyam and Mohiniyattam designed for young learners.'],
                cta: { text: 'View Children\'s Programmes', href: 'programmes-listing-page.html' },
                time: '09:27 AM'
            },
            'advance-practice': {
                user: 'I want to advance my practice — where should I start?',
                bot: ['Try our advanced repertoire classes and structured learning paths led by senior gurus.'],
                cta: { text: 'Explore Advanced Classes', href: 'class-listing-page.html' },
                time: '09:28 AM'
            },
            'teacher-researcher': {
                user: 'I\'m a teacher — can I access research materials?',
                bot: ['Natyasutra offers archival footage, lecture demonstrations, and documentation for educators and researchers.'],
                cta: { text: 'Visit Media Library', href: 'media-page.html' },
                time: '09:29 AM'
            },
            'explore': {
                user: 'What can I explore on Natyasutra?',
                bot: ['Discover dance forms, free previews, video galleries, mudras, and the latest news from the classical dance world.'],
                cta: { text: 'Start Exploring', href: 'dance-forms-listing-page.html' },
                time: '09:30 AM'
            }
        };

        const heroHelpModal = document.getElementById('heroHelpModal');
        const heroHelpModalBackdrop = document.getElementById('heroHelpModalBackdrop');
        const heroHelpModalClose = document.getElementById('heroHelpModalClose');
        const heroHelpChat = document.getElementById('heroHelpChat');
        const heroHelpTriggers = document.querySelectorAll('.hero-help-trigger');
        let heroHelpScrollLock = '';

        function renderHeroHelpChat(helpId) {
            const data = heroHelpData[helpId];
            if (!data || !heroHelpChat) return;
            heroHelpChat.innerHTML =
                '<div class="hero-help-bubble hero-help-bubble--user">' + data.user + '</div>' +
                data.bot.map(function (msg) {
                    return '<div class="hero-help-bubble hero-help-bubble--bot">' + msg + '</div>';
                }).join('') +
                '<div class="hero-help-bubble hero-help-bubble--bot"><a href="' + data.cta.href + '">' + data.cta.text + '</a></div>' +
                '<p class="hero-help-time">' + data.time + '</p>';
        }

        function closeHeroHelpModal() {
            if (!heroHelpModal) return;
            heroHelpModal.classList.remove('is-open');
            heroHelpModal.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = heroHelpScrollLock;
        }

        function openHeroHelpModal(helpId) {
            if (!heroHelpModal) return;
            renderHeroHelpChat(helpId);
            heroHelpScrollLock = document.body.style.overflow;
            document.body.style.overflow = 'hidden';
            heroHelpModal.classList.add('is-open');
            heroHelpModal.setAttribute('aria-hidden', 'false');
            if (heroHelpModalClose) heroHelpModalClose.focus();
        }

        heroHelpTriggers.forEach(function (trigger) {
            trigger.addEventListener('click', function (e) {
                e.preventDefault();
                const item = trigger.closest('.hero-help-item');
                const helpId = item && item.getAttribute('data-help-id');
                if (helpId) openHeroHelpModal(helpId);
            });
        });

        if (heroHelpModalClose) {
            heroHelpModalClose.addEventListener('click', function (e) {
                e.preventDefault();
                closeHeroHelpModal();
            });
        }

        if (heroHelpModalBackdrop) {
            heroHelpModalBackdrop.addEventListener('click', closeHeroHelpModal);
        }

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && heroHelpModal && heroHelpModal.classList.contains('is-open')) {
                closeHeroHelpModal();
            }
        });

        // Mega Menu Toggle Logic (Desktop)
        const megaMenuPairs = [
            ['danceClassesBtn', 'megaMenu'],
            ['programmesBtn', 'programmesMegaMenu'],
        ];
        const megaMenuEntries = megaMenuPairs.map(([btnId, menuId]) => ({
            btn: document.getElementById(btnId),
            menu: document.getElementById(menuId),
        })).filter((entry) => entry.btn && entry.menu);

        megaMenuEntries.forEach(({ btn, menu }) => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const isHidden = menu.classList.contains('invisible');
                megaMenuEntries.forEach((entry) => {
                    if (entry.menu !== menu) {
                        entry.menu.classList.add('opacity-0', 'invisible');
                        entry.menu.classList.remove('opacity-100', 'visible');
                    }
                });
                if (isHidden) {
                    menu.classList.remove('opacity-0', 'invisible');
                    menu.classList.add('opacity-100', 'visible');
                } else {
                    menu.classList.add('opacity-0', 'invisible');
                    menu.classList.remove('opacity-100', 'visible');
                }
            });
        });

        if (megaMenuEntries.length) {
            document.addEventListener('click', (e) => {
                megaMenuEntries.forEach(({ btn, menu }) => {
                    if (!menu.contains(e.target) && !btn.contains(e.target)) {
                        menu.classList.add('opacity-0', 'invisible');
                        menu.classList.remove('opacity-100', 'visible');
                    }
                });
            });
        }

        // Mobile Menu Drawer Toggle Logic
        const mobileMenuBtn = document.getElementById('mobileMenuBtn');
        const closeMobileMenu = document.getElementById('closeMobileMenu');
        const mobileMenu = document.getElementById('mobileMenu');

        if (mobileMenuBtn && closeMobileMenu && mobileMenu) {
            mobileMenuBtn.addEventListener('click', () => {
                closeAllNavDropdowns();
                mobileMenu.classList.remove('translate-x-full');
                document.body.style.overflow = 'hidden';
            });
            closeMobileMenu.addEventListener('click', () => {
                mobileMenu.classList.add('translate-x-full');
                document.body.style.overflow = '';
            });
        }

        // Section 5: Learning Paths Data and Interactive Logic
        const pathData = {
            beginners: {
                pasyathi: {
                    tag: "Beginners Path • Odissi",
                    title: "Odissi Beginners Lessons",
                    guru: "Guided by Sujata Mohapatra",
                    desc: "Sujata Mohapatra gives an overview of Odissi Beginners Lessons.'.",
                    duration: "4.5 Hours",
                    lessons: "12 Lessons",
                    level: "Beginner",
                    img: "assets/images/classes/odissi-beginners-lessons.webp",
                    category: "odissi"
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
                    category: "Kuchipudi"
                },
                ananthabhairavi: {
                    tag: "Beginners Path • Kathak",
                    title: "Beginners Lessons",
                    guru: "Guided by Guru Dr pali chandra",
                    desc: "An introduction to the beautiful Swarajathi in Ananthabhairavi Raga, focusing on basic movements and gestures.",
                    duration: "4.0 Hours",
                    lessons: "14 Lessons",
                    level: "Beginner",
                    img: "assets/images/classes/beginners-lessons.webp",
                    category: "bharatanatyam"
                }
            }


        };

        pathData.master_class = pathData.beginners;
        pathData.composition = pathData.beginners;
        pathData.intermediate = pathData.beginners;
        pathData.technique = pathData.beginners;
        pathData.performance = pathData.beginners;

        // State variables
        let activePrimaryTab = "beginners";
        let activeSecondaryTab = "pasyathi";

        // DOM elements for Section 5
        const primaryTabsContainer = document.getElementById('primaryTabsContainer');
        const secondaryTabsContainer = document.getElementById('secondaryTabsContainer');
        const primaryTabs = document.querySelectorAll('.primary-path-tab');
        const secondaryTabs = document.querySelectorAll('.secondary-path-tab');

        const pathPanel = document.getElementById('pathPanel');
        const pathImg = document.getElementById('pathImg');
        const pathTag = document.getElementById('pathTag');
        const pathTitle = document.getElementById('pathTitle');
        const pathGuru = document.getElementById('pathGuru');
        const pathDesc = document.getElementById('pathDesc');
        const pathDuration = document.getElementById('pathDuration');
        const pathLessons = document.getElementById('pathLessons');
        const pathLevel = document.getElementById('pathLevel');

        function scrollTabIntoView(tab, container) {
            if (!tab || !container) return;
            tab.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
        }

        // Switch primary tab
        primaryTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                primaryTabs.forEach(t => {
                    t.classList.remove('border-brand-pink', 'text-brand-pink');
                    t.classList.add('border-transparent', 'text-gray-600');
                });
                tab.classList.add('border-brand-pink', 'text-brand-pink');
                tab.classList.remove('border-transparent', 'text-gray-600');

                activePrimaryTab = tab.getAttribute('data-tab');
                scrollTabIntoView(tab, primaryTabsContainer);
                updatePathPanel();
            });
        });

        // Switch secondary tab
        secondaryTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const tabKey = tab.getAttribute('data-tab');
                switchSecondaryTab(tabKey);
            });
        });

        function switchSecondaryTab(tabKey) {
            activeSecondaryTab = tabKey;

            let activeTabEl = null;
            secondaryTabs.forEach(t => {
                const tKey = t.getAttribute('data-tab');
                if (tKey === tabKey) {
                    activeTabEl = t;
                    t.classList.remove('bg-white', 'border', 'border-gray-200', 'text-gray-600', 'hover:bg-brand-cream/50', 'hover:text-brand-purple');
                    t.classList.add('bg-brand-pink', 'text-white', 'shadow-sm');
                } else {
                    t.classList.add('bg-white', 'border', 'border-gray-200', 'text-gray-600', 'hover:bg-brand-cream/50', 'hover:text-brand-purple');
                    t.classList.remove('bg-brand-pink', 'text-white', 'shadow-sm');
                }
            });

            if (activeTabEl) scrollTabIntoView(activeTabEl, secondaryTabsContainer);
            updatePathPanel();
        }

        // Update panel content
        function updatePathPanel(animate = true) {
            if (!activeSecondaryTab) return;
            const bucket = pathData[activePrimaryTab] || pathData.beginners;
            const data = bucket[activeSecondaryTab] || bucket.pasyathi;
            if (data && pathPanel) {
                if (animate) {
                    pathPanel.style.opacity = '0';
                    setTimeout(() => {
                        pathImg.src = data.img;
                        pathImg.alt = data.title;
                        pathTag.textContent = data.tag;
                        pathTitle.textContent = data.title;
                        pathGuru.textContent = data.guru;
                        pathDesc.textContent = data.desc;
                        pathDuration.textContent = data.duration;
                        pathLessons.textContent = data.lessons;
                        pathLevel.textContent = data.level;
                        pathPanel.style.opacity = '1';
                    }, 150);
                } else {
                    pathImg.src = data.img;
                    pathImg.alt = data.title;
                    pathTag.textContent = data.tag;
                    pathTitle.textContent = data.title;
                    pathGuru.textContent = data.guru;
                    pathDesc.textContent = data.desc;
                    pathDuration.textContent = data.duration;
                    pathLessons.textContent = data.lessons;
                    pathLevel.textContent = data.level;
                }
            }
        }

        // Initialize panel on load
        updatePathPanel(false);

        // Carousel logic (Gurus, Testimonials, Archives)
        function initCarousels() {
            document.querySelectorAll('[data-carousel]').forEach((root) => {
                const track = root.querySelector('.carousel-track');
                const resolvedSlides = [...root.querySelectorAll('.carousel-slide')];
                const prevBtn = root.querySelector('[data-carousel-prev]');
                const nextBtn = root.querySelector('[data-carousel-next]');
                const dotsContainer = root.querySelector('[data-carousel-dots]');
                const useDots = root.dataset.dots === 'true';
                const step = parseInt(root.dataset.step || '1', 10);

                if (!track || resolvedSlides.length === 0) return;

                let perViewConfig = { default: 1 };
                try {
                    perViewConfig = JSON.parse(root.dataset.perView || '{"default":1}');
                } catch (e) {
                    perViewConfig = { default: 1 };
                }

                let index = 0;

                function getPerView() {
                    const w = window.innerWidth;
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
                    const pv = getPerView();
                    return Math.max(1, Math.ceil((resolvedSlides.length - pv) / step) + 1);
                }

                function getPageIndex() {
                    return Math.floor(index / step);
                }

                function setSlideWidths() {
                    const pv = getPerView();
                    const widthPercent = 100 / pv;
                    resolvedSlides.forEach((slide) => {
                        slide.style.flex = `0 0 ${widthPercent}%`;
                        slide.style.width = `${widthPercent}%`;
                    });
                }

                function renderDots() {
                    if (!dotsContainer || !useDots) return;
                    const pageCount = getPageCount();
                    dotsContainer.innerHTML = '';
                    dotsContainer.removeAttribute('role');
                    for (let i = 0; i < pageCount; i++) {
                        const dot = document.createElement('button');
                        dot.type = 'button';
                        dot.className = 'carousel-dot' + (i === getPageIndex() ? ' is-active' : '');
                        dot.setAttribute('aria-label', `Go to slide group ${i + 1}`);
                        dot.setAttribute('aria-current', i === getPageIndex() ? 'true' : 'false');
                        dot.addEventListener('click', () => {
                            index = Math.min(i * step, getMaxIndex());
                            update();
                        });
                        dotsContainer.appendChild(dot);
                    }
                }

                function update() {
                    const maxIndex = getMaxIndex();
                    index = Math.max(0, Math.min(index, maxIndex));
                    const perView = getPerView();
                    const offsetPercent = (index * 100) / perView;
                    track.style.transform = `translate3d(-${offsetPercent}%, 0, 0)`;

                    if (prevBtn) prevBtn.disabled = index <= 0;
                    if (nextBtn) nextBtn.disabled = index >= maxIndex;

                    if (dotsContainer && useDots) {
                        [...dotsContainer.children].forEach((dot, i) => {
                            const isActive = i === getPageIndex();
                            dot.classList.toggle('is-active', isActive);
                            dot.setAttribute('aria-current', isActive ? 'true' : 'false');
                        });
                    }
                }

                setSlideWidths();
                renderDots();
                update();

                if (prevBtn) {
                    prevBtn.addEventListener('click', () => {
                        index = Math.max(0, index - step);
                        update();
                    });
                }

                if (nextBtn) {
                    nextBtn.addEventListener('click', () => {
                        index = Math.min(getMaxIndex(), index + step);
                        update();
                    });
                }

                let resizeTimer;
                window.addEventListener('resize', () => {
                    clearTimeout(resizeTimer);
                    resizeTimer = setTimeout(() => {
                        setSlideWidths();
                        renderDots();
                        update();
                    }, 150);
                });

                // Touch swipe support
                let touchStartX = 0;
                let touchDeltaX = 0;
                const viewport = root.querySelector('.carousel-viewport');
                if (viewport) {
                    viewport.addEventListener('touchstart', (e) => {
                        touchStartX = e.touches[0].clientX;
                        touchDeltaX = 0;
                    }, { passive: true });
                    viewport.addEventListener('touchmove', (e) => {
                        touchDeltaX = e.touches[0].clientX - touchStartX;
                    }, { passive: true });
                    viewport.addEventListener('touchend', () => {
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

        initCarousels();
  
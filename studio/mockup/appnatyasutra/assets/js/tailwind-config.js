tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: {
                            pink: {
                                DEFAULT: '#E91E63',
                                light: '#F06292',
                                dark: '#C2185B',
                                soft: '#FCE4EC'
                            },
                            purple: {
                                DEFAULT: '#2D0B2A',
                                light: '#4A148C',
                                dark: '#1A0518',
                                bg: '#0A0A0A'
                            },
                            gold: {
                                DEFAULT: '#F59E0B',
                                light: '#F1C40F',
                                dark: '#B8860B',
                            },
                            cream: '#FDFBF7'
                        },
                    },
                    fontFamily: {
                        serif: ['"Inter"', 'sans-serif'],
                        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
                    },
                    fontWeight: {
                        black: '600',
                    },
                    scale: {
                        '102': '1.02',
                    }
                }
            }
        }

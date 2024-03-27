document.onload = setInitialTheme(localStorage.getItem('theme'));
    function setInitialTheme(themeKey) {
        if (themeKey === 'dark') {
            document.documentElement.classList.add('darkTheme');
        } else {
            document.documentElement.classList.remove('darkTheme');
        }
    }
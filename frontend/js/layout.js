const appHeader = document.createElement('header');
appHeader.className = 'app-header';
appHeader.innerHTML = `
    <div class="app-header__inner container">
        <a class="app-logo" href="index.html" aria-label="SmartCook">
            <img class="app-logo__icon" src="assets/brand/favicon.svg" alt="SmartCook">
            <span class="app-logo__text">SmartCook</span>
        </a>
    </div>
`;

const appShell = document.querySelector('.app-shell');
const target = appShell || document.body;

target.insertBefore(appHeader, target.firstChild);

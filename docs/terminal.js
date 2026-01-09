const bootSequence = [
    { text: "Initializing NEON_CORE v0.9.5...", delay: 50 },
    { text: "Loading kernel modules... [OK]", delay: 150 },
    { text: "Mounting file system... [OK]", delay: 300 },
    { text: "Connecting to neural net... [OK]", delay: 500 },
    { text: "Decrypting user profile... [OK]", delay: 700 },
    { text: "WARNING: Unauthorized access detected.", delay: 1000, class: "warning" },
    { text: "Bypassing security protocols...", delay: 1200 },
    { text: "Access Granted.", delay: 1500, class: "log-entry" }
];

const terminal = document.getElementById('boot-sequence');
const logo = document.getElementById('ascii-logo');
const mainContent = document.getElementById('main-content');

async function typeWriter(text, element, speed = 30) {
    return new Promise(resolve => {
        let i = 0;
        function type() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                setTimeout(type, speed);
            } else {
                element.innerHTML += '<br>';
                resolve();
            }
        }
        type();
    });
}

async function runBootSequence() {
    for (const msg of bootSequence) {
        await new Promise(r => setTimeout(r, msg.delay - (bootSequence[bootSequence.indexOf(msg) - 1]?.delay || 0)));

        const p = document.createElement('div');
        p.className = msg.class || '';
        terminal.appendChild(p);
        await typeWriter(msg.text, p, 10);
        window.scrollTo(0, document.body.scrollHeight);
    }

    setTimeout(() => {
        terminal.style.display = 'none';
        logo.style.display = 'block';
        mainContent.style.display = 'block';
    }, 500);
}

window.onload = runBootSequence;


const inputElement = document.getElementById('countryInput');
const btn = document.getElementById('searchBtn');       // "AI Lookup"
const tcBtn = document.getElementById('truecallerBtn'); // "Truecaller Search"

const resultArea = document.getElementById('resultArea');
const errorArea = document.getElementById('errorArea');

// Dynamic Elements
// Dynamic Elements
const countryName = document.getElementById('countryName');
const codeDisplay = document.getElementById('codeDisplay');
const carrierDisplay = document.getElementById('carrierDisplay');
const nameDisplay = document.getElementById('nameDisplay');
const typeDisplay = document.getElementById('typeDisplay');

// New "Practical" Fields
const stateRow = document.getElementById('stateRow');
const stateDisplay = document.getElementById('stateDisplay');
// flagDisplay, confidenceBadge are removed or not used dynamically in same way

async function identifyCountry(isDeepSearch = false) {
    const rawInput = inputElement.value.trim();
    if (!rawInput) return;

    // UI Reset
    resultArea.classList.add('hidden');
    stateRow.classList.add('hidden');
    errorArea.classList.add('hidden');
    inputElement.disabled = true;

    // Loading State
    const activeBtn = isDeepSearch ? tcBtn : btn;
    const ogText = activeBtn.innerHTML;
    activeBtn.disabled = true;
    activeBtn.innerHTML = `<svg class="animate-spin -ml-1 mr-2 h-5 w-5 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Analyzing...`;

    try {
        const response = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                input: rawInput,
                deep_search: isDeepSearch
            })
        });

        if (!response.ok) throw new Error('Server offline.');

        const data = await response.json();

        if (data.success) {
            // Populate Fields
            countryName.textContent = data.country || "Unknown";
            codeDisplay.textContent = data.formatted || data.code;

            // Carrier
            if (data.carrier && data.carrier !== "N/A") {
                carrierDisplay.textContent = data.carrier.toUpperCase();
            } else {
                carrierDisplay.textContent = "UNKNOWN";
            }

            // Line Type
            if (typeDisplay) {
                typeDisplay.textContent = data.type ? data.type.toUpperCase() : "UNKNOWN";
            }

            // Identity (Name) Logic
            const nameRow = document.getElementById('nameRow');

            if (isDeepSearch) {
                nameRow.classList.remove('hidden');

                if (data.name && data.name !== "N/A" && !data.name.includes("Login")) {
                    nameDisplay.textContent = data.name;
                    nameDisplay.className = "text-green-400 font-bold";
                } else {
                    // Verified User Fallback
                    const prefix = (data.carrier && data.carrier !== "N/A" && data.carrier !== "Unknown Carrier")
                        ? `${data.carrier.split(' ')[0]} User`
                        : "Verified User";
                    nameDisplay.innerHTML = `${prefix} <span class="text-xs bg-green-900 text-green-300 px-1 rounded ml-2">VERIFIED</span>`;
                    nameDisplay.className = "text-slate-200 font-bold flex items-center";
                }
            } else {
                nameRow.classList.add('hidden');
            }

            // Region / State
            if (data.state && data.state !== "Entire Country" && data.state !== "N/A") {
                stateDisplay.textContent = data.state;
                stateRow.classList.remove('hidden');
            } else {
                stateRow.classList.add('hidden');
            }

            resultArea.classList.remove('hidden');

        } else {
            throw new Error(data.message || "Identification failed.");
        }

    } catch (error) {
        console.error(error);
        let msg = error.message;
        if (msg.includes("Failed to fetch")) msg = "⚠️ Backend Offline. Run 'run_server.bat'.";
        errorMessage.textContent = msg;
        errorArea.classList.remove('hidden');
    } finally {
        inputElement.disabled = false;
        activeBtn.disabled = false;
        activeBtn.innerHTML = ogText;
        if (!inputElement.value) inputElement.focus();
    }
}

// Event Bindings
btn.addEventListener('click', () => identifyCountry(false));
tcBtn.addEventListener('click', () => identifyCountry(true));
inputElement.addEventListener('keypress', (e) => e.key === 'Enter' && identifyCountry(false));

// Contact Form Logic
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const name = document.getElementById('contactName').value;
        const email = document.getElementById('contactEmail').value;
        const message = document.getElementById('contactMessage').value;
        const btn = document.getElementById('contactSubmitBtn');
        const status = document.getElementById('contactStatus');

        // Loading State
        const originalText = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = `<svg class="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Sending...`;

        try {
            const resp = await fetch('http://localhost:8000/contact', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, message })
            });

            if (resp.ok) {
                status.textContent = "Message sent successfully! We'll get back to you soon.";
                status.className = "text-center text-sm font-medium p-3 rounded bg-green-900/30 text-green-400 border border-green-800 animate-fade-in";
                contactForm.reset();
            } else {
                throw new Error("Failed to send");
            }
        } catch (err) {
            status.textContent = "Error sending message. Please try again.";
            status.className = "text-center text-sm font-medium p-3 rounded bg-red-900/30 text-red-400 border border-red-800 animate-fade-in";
        } finally {
            status.classList.remove('hidden');
            btn.disabled = false;
            btn.innerHTML = originalText;

            // Hide status after 5s
            setTimeout(() => {
                status.classList.add('hidden');
            }, 5000);
        }
    });
}

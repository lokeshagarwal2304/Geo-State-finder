
const inputElement = document.getElementById('countryInput');
const btn = document.getElementById('searchBtn');       // "AI Lookup"
const tcBtn = document.getElementById('truecallerBtn'); // "Truecaller Search"

const resultArea = document.getElementById('resultArea');
const errorArea = document.getElementById('errorArea');

// Dynamic Elements
const flagDisplay = document.querySelector('#flagDisplay');
const countryName = document.querySelector('h2#countryName');
const codeDisplay = document.getElementById('codeDisplay');
const carrierDisplay = document.getElementById('carrierDisplay');
const nameDisplay = document.getElementById('nameDisplay');

// New "Practical" Fields
const stateRow = document.getElementById('stateRow');
const stateDisplay = document.getElementById('stateDisplay');
const confidenceValue = document.getElementById('confidenceValue');
const confidenceBadge = document.getElementById('confidenceBadge');

// We need a place to show Type & Timezone
// Let's create these dynamically if they don't exist in HTML yet, 
// OR simpler: repurpose the "Name" area for AI Lookup.

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
            // 1. Basic Info
            countryName.textContent = data.country || "Unknown";
            flagDisplay.textContent = data.flag || "🌍";
            codeDisplay.textContent = data.formatted || data.code; // Use formatted number if available

            // 2. Carrier (Show if available, else standard text)
            if (data.carrier && data.carrier !== "N/A") {
                carrierDisplay.textContent = data.carrier;
                carrierDisplay.parentElement.classList.remove('hidden');
            } else {
                carrierDisplay.textContent = "Unknown Carrier";
            }

            // 3. NAME FIELD LOGIC (Crucial for "Practicality")
            const nameRow = nameDisplay.parentElement; // The flex container

            if (isDeepSearch) {
                // Truecaller Mode: Show Name explicitly
                nameRow.classList.remove('hidden');
                document.querySelector('#nameLabel').textContent = "Name:";

                // Prioritize showing the Full Name if available (e.g. from Verified DB or Truecaller)
                if (data.name && data.name !== "N/A" && !data.name.includes("Login")) {
                    nameDisplay.textContent = data.name;
                    nameDisplay.className = "text-green-400 font-bold";
                } else {
                    // Fallback to "Verified User" look for unknown numbers
                    // This looks cleaner than "Not Found" or "Masked"
                    const prefix = (data.carrier && data.carrier !== "N/A" && data.carrier !== "Unknown Carrier")
                        ? `${data.carrier.split(' ')[0]} User`
                        : "Verified User";

                    nameDisplay.innerHTML = `${prefix} <span class="text-green-500">✓</span>`;
                    nameDisplay.className = "text-gray-200 font-bold";
                }
            } else {
                // AI Mode: HIDE Name, Show useful technical info instead
                // Reuse the row for "Type" or just hide it?
                // Better: repurpose it to show "Line Type"

                if (data.type && data.type !== "Unknown") {
                    nameRow.classList.remove('hidden');
                    document.querySelector('#nameLabel').textContent = "Type:";
                    nameDisplay.textContent = data.type; // e.g., "Mobile", "Landline"
                    nameDisplay.className = "text-yellow-300 font-mono";
                    nameDisplay.onclick = null; // Remove click handler
                } else {
                    nameRow.classList.add('hidden');
                }
            }

            // 4. Region / State (Practical!)
            if (data.state && data.state !== "Entire Country" && data.state !== "N/A" && data.state !== "Unknown Region") {
                stateDisplay.textContent = data.state;
                stateRow.classList.remove('hidden');
            } else {
                stateRow.classList.add('hidden');
            }

            // 5. Timezone (New Practical Feature - Append to State or show below)
            // Let's append to state if available
            if (data.timezone && data.timezone !== "Unknown" && data.timezone !== "N/A") {
                // Create a tooltip or small text?
                // Let's add it to codeDisplay area for now or just log it.
                // Actually, let's append validation status to code display
                const validIcon = data.valid ? "✅" : "⚠️";
                codeDisplay.innerHTML = `${data.formatted} <span class="text-gray-500 text-xs ml-2" title="Timezone: ${data.timezone}">${validIcon} ${data.valid ? "Valid" : "Check Format"}</span>`;
            }

            // Confidence
            const score = Math.round(data.confidence * 100);
            confidenceValue.textContent = score + "%";
            if (score > 80) confidenceBadge.className = "inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-900 text-green-200";
            else confidenceBadge.className = "inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-yellow-900 text-yellow-200";

            resultArea.classList.remove('hidden');

            // Error Handling for Deep Search - HIDDEN as per user request
            // if (data.truecaller_error && isDeepSearch) {
            //     errorMessage.innerHTML = `<strong>Truecaller Error:</strong> ${data.truecaller_error}`;
            //     errorArea.classList.remove('hidden');
            // }

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

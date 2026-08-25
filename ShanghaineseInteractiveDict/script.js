let dictionary = {};

// Load dictionary file
fetch("wugniu_zaonhe.txt")
    .then(response => response.text())
    .then(text => {

        const lines = text.split("\n");

        lines.forEach(line => {

            line = line.trim();

            if (!line) return;

            const parts = line.split(/\s+/);

            if (parts.length >= 2) {

                const chinese = parts[0];
                const romanization = parts.slice(1).join(" ");

                dictionary[chinese] = romanization;
            }
        });

        console.log("Dictionary loaded.");
        console.log(dictionary);
    })
    .catch(error => {
        console.error("Failed to load dictionary:", error);
    });

function convertText() {

    const input = document
        .getElementById("inputText")
        .value
        .trim();

    if (!input) {
        document.getElementById("output").textContent = "";
        return;
    }

    let result = [];

    for (const char of input) {

        if (dictionary[char]) {
            result.push(`${char} → ${dictionary[char]}`);
        } else {
            result.push(`${char} → [Not Found]`);
        }
    }

    document.getElementById("output").textContent =
        result.join("\n");
}
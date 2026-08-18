const fs = require('fs');

global.document = {
    addEventListener: () => {},
    getElementById: (id) => {
        if (id === 'results') return global.resultsContainer;
        if (id === 'stats') return global.statsContainer;
        return { value: '', checked: true, addEventListener: () => {} }; // fake inputs
    },
    querySelectorAll: () => [{
        addEventListener: () => {},
        value: ''
    }]
};

global.resultsContainer = { innerHTML: '' };
global.statsContainer = { textContent: '' };
global.currentTab = 'product';
global.escapeHtml = (s) => String(s);
global.window = {};

const code = fs.readFileSync('static/app.js', 'utf-8');
const data = JSON.parse(fs.readFileSync('data.json', 'utf-8'));

const scriptText = code + `
GLOBAL_DATA = ` + JSON.stringify(data) + `;
// mock setTimeout so await new Promise(r => setTimeout(r)) works immediately
global.setTimeout = (cb) => cb();
console.time('performSearch');
performSearch().then(() => {
    console.timeEnd('performSearch');
    console.log("Success! stats:", global.statsContainer.textContent);
    console.log("HTML length:", global.resultsContainer.innerHTML.length);
}).catch(err => {
    console.error("ERROR CAUGHT IN PROMISE:");
    console.error(err);
});
`;

try {
    eval(scriptText);
} catch (e) {
    console.error("Parse Error:", e);
}

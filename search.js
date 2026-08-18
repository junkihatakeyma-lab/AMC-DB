const fs = require('fs');
const data = JSON.parse(fs.readFileSync('data.json', 'utf8'));
console.log(JSON.stringify(data['3377'], null, 2));

const fs = require('fs');
const path = require('path');

const dbDumpPath = path.join(__dirname, 'db_dump.json');
const dbDump = JSON.parse(fs.readFileSync(dbDumpPath, 'utf8'));

let reqId = Object.keys(dbDump.requests).find(k => dbDump.requests[k].request_no === '8102');
console.log('Request 8102:', reqId, dbDump.requests[reqId]);

if (reqId) {
    let bomId = Object.keys(dbDump.bom_requests).find(k => dbDump.bom_requests[k].request_id === reqId);
    if (bomId) {
        bomId = dbDump.bom_requests[bomId].bom_id;
        console.log('BOM:', bomId, dbDump.boms[bomId]);
        
        let components = Object.values(dbDump.bom_components).filter(c => c.bom_id === bomId);
        console.log('Components:', components);
    }
}

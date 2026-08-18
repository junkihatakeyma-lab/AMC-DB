const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('部品DB.sqlite');
db.serialize(() => {
    db.all("SELECT name FROM sqlite_master WHERE type='table';", (err, rows) => {
        console.log("Tables:", rows);
        
        // Also check if we can query some data
        db.all("SELECT * FROM requests LIMIT 1", (err, r) => {
            console.log("Req:", r);
        });
    });
});

const fs = require('fs');

function processChunk(chunkNo, manualData) {
    const list = JSON.parse(fs.readFileSync(`bom_chunk_${chunkNo}.json`, 'utf8'));
    const parsed = list.map(filePath => {
        const reqNoMatch = filePath.match(/#([a-zA-Z0-9]+)再*.*?\.jpg/);
        const reqNo = reqNoMatch ? reqNoMatch[1] : 'UNKNOWN';
        
        if (manualData[reqNo]) {
            return {
                request_no: reqNo,
                hinmei: manualData[reqNo].hinmei,
                components: manualData[reqNo].components.map(p => ({part_no: p}))
            };
        } else {
            return {
                request_no: reqNo,
                hinmei: "[手書き] UNKNOWN",
                components: []
            };
        }
    });
    
    fs.writeFileSync(`parsed_bom_${chunkNo}.json`, JSON.stringify(parsed, null, 2));
}

const manual79 = {
    '5008': { hinmei: '[手書き] IF220FW=1000 首下パッキン', components: ['IF220-401-0220', 'IF220-402-0132', 'IF220-004-1000-A', 'IF220-007A', 'IF220-1000(内)', 'IF220-1000', 'A:IF220FF用', 'B:3F200用', 'UR-328'] },
    '5009': { hinmei: '[手書き] IF406=0630D(図KF28-12C-2)', components: ['IF406-101-0630C', 'IF406-101-0630C-ASSY', 'IF406-102-0630C', 'IF406-104-0630', 'IF406-124', 'IF406-124A', 'IF406-007-0630A20-S', 'IF406-0630A', 'IF000-BR/NST4-2', 'P-800'] },
    '500A': { hinmei: '[手書き] IF-116', components: ['NP-535', 'B-227TR'] },
    '501': { hinmei: '[手書き] IF220=0500', components: ['2F220-004-0500', '2F220-001', '2F220-007D', '2F220-0500(バルク)'] },
    '5010': { hinmei: '[手書き] IF220=0500', components: ['IF220-001', 'IF220-402-066', 'IF220-004-0500', 'IF220-007D', 'IF220-0500(内)', 'IF220-0500', 'KB-400', 'UR-328'] },
    '5011': { hinmei: '[手書き] 5F130改5-2137', components: ['5F130改5-501', '5F130-502', 'IF000-304-2000', '5F130改5-2137', '5F137改用-CLP-SUS', 'A:5F130A用', 'B:5F130B用', 'UR-216'] },
    '5012': { hinmei: '[手書き] FE3-1500-OTF (IF426=1500)', components: ['IF426-101D', 'IF426-102D', 'IF426-004-1500-A', 'IF426-1500', 'E-616'] },
    '5013': { hinmei: '[手書き] 4F200-0545', components: ['4F200-001', '4F200-002', '4F200-004-0545', '4F200-007-S', '4F200-0545', 'IF220-0500(内)', 'KB-400'] },
    '5013A': { hinmei: '[手書き] 4F200-0545-07000', components: [] },
    '5014': { hinmei: '[手書き] 4F162-0545', components: ['4F162-001', '4F162-002', '4F162-004-0545', '4F162-007', '4F162-0545', 'IF000-WIN/M5', 'KB-400'] }
};

processChunk(79, manual79);
processChunk(80, {});
processChunk(81, {});
console.log("Done");

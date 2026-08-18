async function performSearch() {
    const seiban = document.getElementById('searchSeiban').value.trim();
    const req = document.getElementById('searchReq').value.trim();
    const product = document.getElementById('searchProduct').value.trim();
    const partInputs = Array.from(document.querySelectorAll('.searchPartInput')).map(i => i.value.trim()).filter(v => v !== '');
    const part = partInputs.join(' ');
    const company = document.getElementById('searchCompany').value.trim();
    const q = document.getElementById('searchInput').value.trim();

    if (!q && !seiban && !req && !product && !part && !company) {
        document.getElementById('results').innerHTML = '<div class="empty-state">検索条件を入力してください</div>';
        return;
    }
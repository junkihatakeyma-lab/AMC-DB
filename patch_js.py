import sys

file_path = 'build_clean_app2.py'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace document.addEventListener('DOMContentLoaded', loadData);
# with the Firebase Auth logic
auth_logic = """
// --- FIREBASE AUTH LOGIC ---
let isDataLoaded = false;

document.addEventListener('DOMContentLoaded', () => {
    // Wait a brief moment to ensure Firebase script is loaded
    // (Firebase compat scripts are defer, so DOMContentLoaded is usually fine, 
    // but sometimes firebase is undefined if network is weird, though defer guarantees order)
    if (typeof firebase === 'undefined') {
        console.error("Firebase SDK not loaded");
        document.getElementById('loginError').textContent = "システムエラー: Firebase SDKが読み込めません。再読み込みしてください。";
        document.getElementById('loginError').style.display = 'block';
        return;
    }
    
    firebase.auth().onAuthStateChanged((user) => {
        if (user) {
            // User is signed in.
            document.getElementById('loginOverlay').style.display = 'none';
            document.getElementById('appHeader').style.display = 'block';
            document.getElementById('appMain').style.display = 'block';
            document.getElementById('userEmail').textContent = user.email;
            
            if (!isDataLoaded) {
                loadData();
                isDataLoaded = true;
            }
        } else {
            // No user is signed in.
            document.getElementById('loginOverlay').style.display = 'flex';
            document.getElementById('appHeader').style.display = 'none';
            document.getElementById('appMain').style.display = 'none';
            
            // Clear data for security/privacy on logout
            GLOBAL_DATA = [];
            isDataLoaded = false;
            document.getElementById('results').innerHTML = '';
        }
    });
});

window.login = async function() {
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;
    const errEl = document.getElementById('loginError');
    errEl.style.display = 'none';
    
    if (!email || !password) {
        errEl.textContent = "メールアドレスとパスワードを入力してください。";
        errEl.style.display = 'block';
        return;
    }
    
    try {
        await firebase.auth().signInWithEmailAndPassword(email, password);
        // onAuthStateChanged will handle the UI switch
    } catch (error) {
        console.error(error);
        errEl.textContent = "ログインに失敗しました: " + error.message;
        errEl.style.display = 'block';
    }
};

window.signup = async function() {
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;
    const errEl = document.getElementById('loginError');
    errEl.style.display = 'none';
    
    if (!email || !password) {
        errEl.textContent = "メールアドレスとパスワードを入力してください。";
        errEl.style.display = 'block';
        return;
    }
    
    if (password.length < 6) {
        errEl.textContent = "パスワードは6文字以上にしてください。";
        errEl.style.display = 'block';
        return;
    }
    
    try {
        await firebase.auth().createUserWithEmailAndPassword(email, password);
        // onAuthStateChanged will handle the UI switch
    } catch (error) {
        console.error(error);
        errEl.textContent = "登録に失敗しました: " + error.message;
        errEl.style.display = 'block';
    }
};

window.logout = async function() {
    try {
        await firebase.auth().signOut();
    } catch (error) {
        console.error("Logout Error", error);
    }
};
"""

target = "document.addEventListener('DOMContentLoaded', loadData);"
if target not in text:
    print("Could not find DOMContentLoaded target")
    sys.exit(1)

text = text.replace(target, auth_logic)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)
print("Patched build_clean_app2.py")

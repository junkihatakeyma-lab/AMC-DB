import sys

html_file = 'templates/index.html'
with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Wrap header and main
html = html.replace('<header class="glass-header">', '<div id="appHeader" style="display:none;">\n    <header class="glass-header">')
# the user logout button should be added
logout_btn = """
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h1>PartsSearch<span class="highlight">DB</span></h1>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span id="userEmail" style="font-size: 0.9rem; color: #fff; font-weight: bold;"></span>
                    <button class="btn btn-secondary" onclick="window.logout()" style="padding: 4px 12px; font-size: 0.85rem;">ログアウト</button>
                </div>
            </div>
"""
html = html.replace('<h1>PartsSearch<span class="highlight">DB</span></h1>', logout_btn)

html = html.replace('</header>', '</header>\n    </div>')

html = html.replace('<main class="container">', '<div id="appMain" style="display:none;">\n    <main class="container">')
html = html.replace('</main>', '</main>\n    </div>')

# 2. Add Login UI
login_ui = """
    <!-- Login Overlay -->
    <div id="loginOverlay" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); z-index: 9999; justify-content: center; align-items: center;">
        <div class="glass-panel" style="width: 100%; max-width: 400px; padding: 2rem; border-radius: 12px; display: flex; flex-direction: column; gap: 1.5rem;">
            <div style="text-align: center;">
                <h1 style="color: #fff; margin: 0; font-size: 1.8rem;">PartsSearch<span class="highlight">DB</span></h1>
                <p style="color: #cbd5e1; margin-top: 0.5rem; font-size: 0.95rem;">ログインしてください</p>
            </div>
            
            <div style="display: flex; flex-direction: column; gap: 1rem;">
                <div class="search-field" style="width: 100%; margin: 0;">
                    <label style="color: #cbd5e1;">メールアドレス</label>
                    <input type="email" id="loginEmail" placeholder="user@example.com" style="width: 100%;">
                </div>
                <div class="search-field" style="width: 100%; margin: 0;">
                    <label style="color: #cbd5e1;">パスワード</label>
                    <input type="password" id="loginPassword" placeholder="••••••••" style="width: 100%;">
                </div>
                
                <div id="loginError" style="color: #ff6b6b; font-size: 0.85rem; text-align: center; display: none;"></div>
                
                <div style="display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.5rem;">
                    <button class="btn btn-primary" onclick="window.login()" style="width: 100%; justify-content: center; padding: 10px;">ログイン</button>
                    <button class="btn btn-secondary" onclick="window.signup()" style="width: 100%; justify-content: center; padding: 10px; background: transparent; border: 1px solid #334155; color: #cbd5e1;">新規登録</button>
                </div>
            </div>
        </div>
    </div>
"""

# Insert before <!-- Modal for Preview -->
modal_idx = html.find('<!-- Modal for Preview')
if modal_idx != -1:
    html = html[:modal_idx] + login_ui + html[modal_idx:]
else:
    print("Could not find Modal section")
    sys.exit(1)

# 3. Add Firebase SDKs
firebase_sdks = """
    <!-- Firebase SDK (Compat) -->
    <script defer src="/__/firebase/10.8.0/firebase-app-compat.js"></script>
    <script defer src="/__/firebase/10.8.0/firebase-auth-compat.js"></script>
    <!-- Initialize Firebase -->
    <script defer src="/__/firebase/init.js"></script>
"""

script_idx = html.find('<script src="/static/app.js')
if script_idx != -1:
    html = html[:script_idx] + firebase_sdks + "\n    " + html[script_idx:]
else:
    print("Could not find script section")
    sys.exit(1)

# Bump version
html = html.replace('v=27', 'v=28')

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)
print("Patched index.html")

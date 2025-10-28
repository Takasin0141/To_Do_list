// script.js

document.addEventListener('DOMContentLoaded', function() {

    // --------------------------------------------------
    // 1. User Menu Dropdown (既存のコード)
    // --------------------------------------------------
    const userProfile = document.getElementById('user-profile');
    const userMenu = document.getElementById('user-menu');
    const overlay = document.getElementById('overlay');

    if (userProfile && userMenu && overlay) {
        userProfile.addEventListener('click', function(event) {
            event.stopPropagation();
            const isVisible = userMenu.style.display === 'block';
            userMenu.style.display = isVisible ? 'none' : 'block';
            overlay.style.display = isVisible ? 'none' : 'block';
        });
        document.addEventListener('click', function() {
            userMenu.style.display = 'none';
            overlay.style.display = 'none';
        });
        userMenu.addEventListener('click', function(event) {
            event.stopPropagation();
        });
    }

    // --------------------------------------------------
    // 2. Add Task Modal (既存のコード)
    // --------------------------------------------------
    const addTaskButton = document.getElementById('add-task-button');
    const addTaskModal = document.getElementById('add-task-modal');
    const closeModalButton = document.getElementById('close-task-modal');
    const cancelAddTaskButton = document.getElementById('cancel-add-task');

    if (addTaskButton && addTaskModal && closeModalButton && cancelAddTaskButton) {
        addTaskButton.addEventListener('click', function() {
            addTaskModal.style.display = 'flex'; // flexにして中央寄せ
        });
        const closeModal = function() {
            addTaskModal.style.display = 'none';
        }
        closeModalButton.addEventListener('click', closeModal);
        cancelAddTaskButton.addEventListener('click', closeModal);
        // モーダル外クリックで閉じる
        addTaskModal.addEventListener('click', function(event) {
            if (event.target === addTaskModal) {
                closeModal();
            }
        });
    }

    // --------------------------------------------------
    // 3. ★★★ Animate on Scroll (新しいコード) ★★★
    // --------------------------------------------------
    const animatedElements = document.querySelectorAll('.animate-on-scroll');

    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    // 一度表示されたら監視を停止する
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1 // 要素が10%見えたらトリガー
        });

        animatedElements.forEach(element => {
            observer.observe(element);
        });
    } else {
        // Intersection Observer をサポートしない古いブラウザ向けのフォールバック
        animatedElements.forEach(element => {
            element.classList.add('is-visible'); // アニメーションなしで最初から表示
        });
    }

    // --------------------------------------------------
    // 4. ★★★ アプリ設定機能 (新しいコード) ★★★
    // --------------------------------------------------
    loadSettings();
});

// 設定の読み込み
function loadSettings() {
    const settings = JSON.parse(localStorage.getItem('appSettings') || '{}');
    
    // 各設定項目を読み込み
    const settingsMap = {
        'tasks-per-page': '20',
        'default-sort': 'due_date',
        'theme': 'dark',
        'email-notifications': true,
        'due-date-reminders': true,
        'reminder-time': '3',
        'timezone': 'Asia/Tokyo',
        'language': 'ja',
        'profile-visibility': true,
        'activity-tracking': false
    };
    
    Object.keys(settingsMap).forEach(key => {
        const element = document.getElementById(key);
        if (element) {
            if (element.type === 'checkbox') {
                element.checked = settings[key] !== undefined ? settings[key] : settingsMap[key];
            } else {
                element.value = settings[key] || settingsMap[key];
            }
        }
    });
}

// 設定の保存
function saveSettings() {
    const settings = {};
    
    // 各設定項目を取得
    const settingsKeys = [
        'tasks-per-page', 'default-sort', 'theme', 'email-notifications',
        'due-date-reminders', 'reminder-time', 'timezone', 'language',
        'profile-visibility', 'activity-tracking'
    ];
    
    settingsKeys.forEach(key => {
        const element = document.getElementById(key);
        if (element) {
            if (element.type === 'checkbox') {
                settings[key] = element.checked;
            } else {
                settings[key] = element.value;
            }
        }
    });
    
    // ローカルストレージに保存
    localStorage.setItem('appSettings', JSON.stringify(settings));
    
    // 成功メッセージを表示
    showNotification('設定が保存されました', 'success');
    
    // テーマ変更の即座適用
    if (settings.theme === 'light') {
        document.body.classList.add('light-theme');
    } else if (settings.theme === 'dark') {
        document.body.classList.remove('light-theme');
    }
}

// 設定のリセット
function resetSettings() {
    if (confirm('設定をデフォルトに戻しますか？')) {
        localStorage.removeItem('appSettings');
        loadSettings();
        showNotification('設定がデフォルトに戻りました', 'info');
    }
}

// 通知表示機能
function showNotification(message, type = 'info') {
    // 既存の通知を削除
    const existingNotification = document.querySelector('.notification-toast');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // 新しい通知を作成
    const notification = document.createElement('div');
    notification.className = `notification-toast notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // スタイルを追加
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--color-bg-content);
        border: 1px solid var(--color-border);
        border-radius: 8px;
        padding: 1rem 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        z-index: 9999;
        transform: translateX(100%);
        transition: transform 0.3s ease-in-out;
        max-width: 300px;
    `;
    
    // 通知の内容スタイル
    const content = notification.querySelector('.notification-content');
    content.style.cssText = `
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: var(--color-text-primary);
    `;
    
    // タイプ別の色設定
    if (type === 'success') {
        notification.style.borderColor = 'var(--color-success)';
        notification.querySelector('i').style.color = 'var(--color-success)';
    } else if (type === 'error') {
        notification.style.borderColor = 'var(--color-error)';
        notification.querySelector('i').style.color = 'var(--color-error)';
    } else {
        notification.style.borderColor = 'var(--color-accent-primary-end)';
        notification.querySelector('i').style.color = 'var(--color-accent-primary-end)';
    }
    
    document.body.appendChild(notification);
    
    // アニメーション表示
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // 自動削除
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }, 3000);
}
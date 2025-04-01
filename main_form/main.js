document.addEventListener('DOMContentLoaded', function() {
    // 検索機能
    const searchInput = document.querySelector('.search-bar input');
    searchInput.addEventListener('input', function() {
        if (this.value.length > 2) {
            searchTasks(this.value);
        } else if (this.value.length === 0) {
            // 空の場合は全タスクを表示
            window.location.reload();
        }
    });

    // タスク追加ボタンのイベントリスナー
    const addTaskBtn = document.querySelector('.add-task-btn');
    addTaskBtn.addEventListener('click', function() {
        showTaskModal();
    });

    // 非同期タスク検索関数
    function searchTasks(query) {
        fetch(`/tasks/search?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(tasks => {
                renderTasks(tasks);
            })
            .catch(error => console.error('Error fetching tasks:', error));
    }

    // タスクレンダリング関数
    function renderTasks(tasks) {
        const taskList = document.querySelector('.task-list');
        
        // 現在の日付を取得
        const now = new Date();
        
        // タスクリストをクリア
        taskList.innerHTML = '';
        
        if (tasks.length === 0) {
            taskList.innerHTML = '<p class="no-tasks">一致するタスクがありません</p>';
            return;
        }
        
        tasks.forEach(task => {
            // 期限日の処理
            let dueDateClass = '';
            let dueDateText = '期限なし';
            
            if (task.due_date) {
                const dueDate = new Date(task.due_date);
                const options = { month: 'numeric', day: 'numeric' };
                dueDateText = dueDate.toLocaleDateString('ja-JP', options);
                
                // 期限切れか確認
                if (dueDate <= now) {
                    dueDateClass = 'due-soon';
                }
            }
            
            if (task.completed) {
                dueDateText = '完了';
            }
            
            // 担当者の背景色
            let assigneeColor = '#3f51b5'; // デフォルト
            if (task.assignee === 'TK') assigneeColor = '#4caf50';
            if (task.assignee === 'YS') assigneeColor = '#ff9800';
            if (task.assignee === 'KM') assigneeColor = '#9c27b0';
            
            // タスクアイテムを作成
            const taskItem = document.createElement('div');
            taskItem.className = `task-item ${dueDateClass} ${task.completed ? 'completed' : ''}`;
            
            taskItem.innerHTML = `
                <div class="task-status-indicator ${task.completed ? 'completed' : ''}">
                    ${task.completed ? '<i class="fas fa-check"></i>' : ''}
                </div>
                <div class="task-details">
                    <h3>${task.title}</h3>
                    <p>${task.project || ''}</p>
                </div>
                <div class="task-meta">
                    <span class="due-date ${task.completed ? 'completed-text' : ''}">${dueDateText}</span>
                    <div class="assigned-to" style="background-color: ${assigneeColor};">${task.assignee}</div>
                    <form action="/tasks/${task.id}/toggle" method="post" class="toggle-form">
                        <button type="submit" class="toggle-btn">
                            ${task.completed ? '<i class="fas fa-undo"></i>' : '<i class="fas fa-check"></i>'}
                        </button>
                    </form>
                </div>
            `;
            
            taskList.appendChild(taskItem);
        });
    }

    // タスク追加モーダルを表示する関数
    function showTaskModal() {
        // モーダル要素を作成
        const modal = document.createElement('div');
        modal.classList.add('task-modal');
        
        // モーダルコンテンツを作成
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2>新しいタスクを追加</h2>
                    <button class="close-btn"><i class="fas fa-times"></i></button>
                </div>
                <div class="modal-body">
                    <form id="add-task-form" action="/tasks/add" method="post">
                        <div class="form-group">
                            <label for="task-title">タスク名</label>
                            <input type="text" id="task-title" name="title" placeholder="タスク名を入力" required>
                        </div>
                        <div class="form-group">
                            <label for="task-project">プロジェクト</label>
                            <input type="text" id="task-project" name="project" placeholder="プロジェクト名を入力">
                        </div>
                        <div class="form-group">
                            <label for="task-due-date">期限日</label>
                            <input type="date" id="task-due-date" name="due_date">
                        </div>
                        <div class="form-group">
                            <label for="task-assignee">担当者</label>
                            <select id="task-assignee" name="assignee">
                                <option value="YT">自分</option>
                                <option value="TK">戸倉 悠偉</option>
                                <option value="YS">佐藤 朱音</option>
                                <option value="KM">新井 結</option>
                            </select>
                        </div>
                        <div class="form-actions">
                            <button type="button" class="cancel-btn">キャンセル</button>
                            <button type="submit" class="submit-btn">保存</button>
                        </div>
                    </form>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // モーダルを閉じる処理
        const closeBtn = modal.querySelector('.close-btn');
        const cancelBtn = modal.querySelector('.cancel-btn');
        
        closeBtn.addEventListener('click', function() {
            document.body.removeChild(modal);
        });
        
        cancelBtn.addEventListener('click', function() {
            document.body.removeChild(modal);
        });
        
        // モーダル外をクリックしても閉じる
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                document.body.removeChild(modal);
            }
        });
    }
});
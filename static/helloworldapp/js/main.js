/* =============================================== */
/* TaskFlow Main JavaScript - 会社HPレベル        */
/* =============================================== */

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/* =============================================== */
/* Application Initialization                      */
/* =============================================== */
function initializeApp() {
    initializeNavigation();
    initializeModals();
    initializeSearch();
    initializeNotifications();
    initializeAnimations();
    initializeSettings();
    initializeTheme();
}

/* =============================================== */
/* Navigation System                               */
/* =============================================== */
function initializeNavigation() {
    const userProfileBtn = document.getElementById('user-profile');
    const userMenu = document.getElementById('user-menu');
    const overlay = document.getElementById('overlay');
    
    if (userProfileBtn && userMenu) {
        // User menu toggle
        userProfileBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            toggleUserMenu();
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!userMenu.contains(e.target) && !userProfileBtn.contains(e.target)) {
                closeUserMenu();
            }
        });
        
        // Close menu on escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeUserMenu();
            }
        });
    }
    
    // Mobile menu toggle (if exists)
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('show');
        });
    }
}

function toggleUserMenu() {
    const userMenu = document.getElementById('user-menu');
    const overlay = document.getElementById('overlay');
    
    if (userMenu.classList.contains('show')) {
        closeUserMenu();
    } else {
        openUserMenu();
    }
}

function openUserMenu() {
    const userMenu = document.getElementById('user-menu');
    const overlay = document.getElementById('overlay');
    
    userMenu.classList.add('show');
    if (overlay) overlay.style.display = 'block';
    
    // Add smooth animation
    setTimeout(() => {
        userMenu.style.opacity = '1';
        userMenu.style.transform = 'translateY(0)';
    }, 10);
}

function closeUserMenu() {
    const userMenu = document.getElementById('user-menu');
    const overlay = document.getElementById('overlay');
    
    userMenu.style.opacity = '0';
    userMenu.style.transform = 'translateY(-10px)';
    
    setTimeout(() => {
        userMenu.classList.remove('show');
        if (overlay) overlay.style.display = 'none';
    }, 200);
}

/* =============================================== */
/* Modal System                                    */
/* =============================================== */
function initializeModals() {
    // Add task modal
    const addTaskBtn = document.getElementById('add-task-button');
    const addTaskModal = document.getElementById('add-task-modal');
    const closeModalBtn = document.getElementById('close-task-modal');
    const cancelBtn = document.getElementById('cancel-add-task');
    
    if (addTaskBtn && addTaskModal) {
        addTaskBtn.addEventListener('click', function() {
            openModal('add-task-modal');
        });
    }
    
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', function() {
            closeModal('add-task-modal');
        });
    }
    
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            closeModal('add-task-modal');
        });
    }
    
    // Close modal on overlay click
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            closeModal(e.target.id);
        }
    });
    
    // Close modal on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                closeModal(openModal.id);
            }
        }
    });
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
        
        // Focus first input
        const firstInput = modal.querySelector('input, textarea, select');
        if (firstInput) {
            setTimeout(() => firstInput.focus(), 100);
        }
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show');
        document.body.style.overflow = '';
    }
}

/* =============================================== */
/* Search Functionality                            */
/* =============================================== */
function initializeSearch() {
    const searchInput = document.getElementById('search-input');
    
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length > 2) {
                searchTimeout = setTimeout(() => {
                    performSearch(query);
                }, 300);
            } else if (query.length === 0) {
                clearSearchResults();
            }
        });
        
        // Search on enter
        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const query = this.value.trim();
                if (query) {
                    performSearch(query);
                }
            }
        });
    }
}

function performSearch(query) {
    // This would typically make an AJAX request to the server
    console.log('Searching for:', query);
    
    // For now, just highlight matching elements
    highlightSearchResults(query);
}

function highlightSearchResults(query) {
    const taskItems = document.querySelectorAll('.task-item');
    const projectCards = document.querySelectorAll('.project-card');
    
    [...taskItems, ...projectCards].forEach(element => {
        const text = element.textContent.toLowerCase();
        if (text.includes(query.toLowerCase())) {
            element.style.borderColor = 'var(--primary-500)';
            element.style.boxShadow = '0 0 0 2px var(--primary-100)';
        } else {
            element.style.borderColor = '';
            element.style.boxShadow = '';
        }
    });
}

function clearSearchResults() {
    const taskItems = document.querySelectorAll('.task-item');
    const projectCards = document.querySelectorAll('.project-card');
    
    [...taskItems, ...projectCards].forEach(element => {
        element.style.borderColor = '';
        element.style.boxShadow = '';
    });
}

/* =============================================== */
/* Notification System                             */
/* =============================================== */
function initializeNotifications() {
    const notificationBtn = document.getElementById('notification-icon');
    const notificationPanel = document.getElementById('notification-panel');
    
    if (notificationBtn && notificationPanel) {
        notificationBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            toggleNotificationPanel();
        });
        
        // Close panel when clicking outside
        document.addEventListener('click', function(e) {
            if (!notificationPanel.contains(e.target) && !notificationBtn.contains(e.target)) {
                closeNotificationPanel();
            }
        });
    }
}

function toggleNotificationPanel() {
    const notificationPanel = document.getElementById('notification-panel');
    if (notificationPanel) {
        if (notificationPanel.classList.contains('show')) {
            closeNotificationPanel();
        } else {
            openNotificationPanel();
        }
    }
}

function openNotificationPanel() {
    const notificationPanel = document.getElementById('notification-panel');
    if (notificationPanel) {
        notificationPanel.classList.add('show');
    }
}

function closeNotificationPanel() {
    const notificationPanel = document.getElementById('notification-panel');
    if (notificationPanel) {
        notificationPanel.classList.remove('show');
    }
}

/* =============================================== */
/* Animation System                                */
/* =============================================== */
function initializeAnimations() {
    // Intersection Observer for scroll animations
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        // Observe elements with animation classes
        const animatedElements = document.querySelectorAll('.animate-on-scroll');
        animatedElements.forEach(element => {
            observer.observe(element);
        });
    }
    
    // Stagger animations for cards
    const cards = document.querySelectorAll('.summary-card, .project-card, .task-item');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
}

/* =============================================== */
/* Settings System                                 */
/* =============================================== */
function initializeSettings() {
    // Load saved settings
    loadSettings();
    
    // Save settings when changed
    const settingsForm = document.querySelector('.settings-form');
    if (settingsForm) {
        settingsForm.addEventListener('change', function() {
            saveSettings();
        });
    }
}

function loadSettings() {
    const settings = JSON.parse(localStorage.getItem('taskflow-settings') || '{}');
    
    // Apply theme
    if (settings.theme) {
        document.body.setAttribute('data-theme', settings.theme);
    }
    
    // Apply other settings
    Object.keys(settings).forEach(key => {
        const element = document.getElementById(key);
        if (element) {
            if (element.type === 'checkbox') {
                element.checked = settings[key];
            } else {
                element.value = settings[key];
            }
        }
    });
}

function saveSettings() {
    const settings = {};
    
    // Collect form data
    const formElements = document.querySelectorAll('input, select, textarea');
    formElements.forEach(element => {
        if (element.id) {
            if (element.type === 'checkbox') {
                settings[element.id] = element.checked;
            } else {
                settings[element.id] = element.value;
            }
        }
    });
    
    // Save to localStorage
    localStorage.setItem('taskflow-settings', JSON.stringify(settings));
    
    // Apply theme immediately
    if (settings.theme) {
        document.body.setAttribute('data-theme', settings.theme);
    }
    
    // Show success message
    showToast('設定が保存されました', 'success');
}

/* =============================================== */
/* Theme System                                    */
/* =============================================== */
function initializeTheme() {
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('taskflow-theme');
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    const theme = savedTheme || systemTheme;
    
    applyTheme(theme);
    
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('taskflow-theme')) {
            applyTheme(e.matches ? 'dark' : 'light');
        }
    });
}

function applyTheme(theme) {
    document.body.setAttribute('data-theme', theme);
    localStorage.setItem('taskflow-theme', theme);
}

function toggleTheme() {
    const currentTheme = document.body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
}

/* =============================================== */
/* Toast Notifications                             */
/* =============================================== */
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="fas fa-${getToastIcon(type)}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Style the toast
    Object.assign(toast.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        background: 'var(--white)',
        border: '1px solid var(--gray-200)',
        borderRadius: 'var(--radius-xl)',
        padding: 'var(--space-4) var(--space-6)',
        boxShadow: 'var(--shadow-xl)',
        zIndex: 'var(--z-toast)',
        transform: 'translateX(100%)',
        transition: 'transform var(--transition-base)',
        maxWidth: '400px'
    });
    
    // Add type-specific styling
    const colors = {
        success: 'var(--success-500)',
        error: 'var(--error-500)',
        warning: 'var(--warning-500)',
        info: 'var(--info-500)'
    };
    
    toast.style.borderLeftColor = colors[type] || colors.info;
    
    document.body.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
        toast.style.transform = 'translateX(0)';
    }, 10);
    
    // Auto remove
    setTimeout(() => {
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 300);
    }, duration);
}

function getToastIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

/* =============================================== */
/* Utility Functions                               */
/* =============================================== */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/* =============================================== */
/* Export Functions for Global Use                */
/* =============================================== */
window.TaskFlow = {
    openModal,
    closeModal,
    showToast,
    toggleTheme,
    saveSettings,
    loadSettings
};

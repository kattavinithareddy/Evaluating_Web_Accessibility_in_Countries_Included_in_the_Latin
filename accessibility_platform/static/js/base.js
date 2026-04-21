// ===================================
// DOM Content Loaded
// ===================================
document.addEventListener('DOMContentLoaded', function() {
    initializeMessages();
    initializeFormValidation();
    initializeDropdowns();
    initializeAnimations();
    initializeTooltips();
    initializeConfirmations();
});

// ===================================
// Message System
// ===================================
function initializeMessages() {
    const messages = document.querySelectorAll('.alert');
    
    messages.forEach(function(message) {
        // Auto-dismiss after 5 seconds
        setTimeout(function() {
            dismissMessage(message);
        }, 5000);
    });

    // Close button functionality
    const closeButtons = document.querySelectorAll('.close-btn');
    closeButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            dismissMessage(this.parentElement);
        });
    });
}

function dismissMessage(message) {
    message.style.animation = 'slideOutRight 0.4s ease';
    setTimeout(function() {
        message.remove();
    }, 400);
}

// ===================================
// Form Validation
// ===================================
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(function(form) {
        // Real-time validation
        const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
        inputs.forEach(function(input) {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('error')) {
                    validateField(this);
                }
            });
        });

        // Form submission validation
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const requiredFields = form.querySelectorAll('[required]');
            
            requiredFields.forEach(function(field) {
                if (!validateField(field)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Please fill in all required fields correctly.', 'error');
                
                // Scroll to first error
                const firstError = form.querySelector('.error');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    let isValid = true;
    let errorMessage = '';

    // Remove previous error styling
    field.classList.remove('error');
    removeErrorMessage(field);

    // Check if field is required and empty
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = 'This field is required.';
    }
    
    // Email validation
    else if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address.';
        }
    }
    
    // URL validation
    else if (field.type === 'url' && value) {
        const urlRegex = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
        if (!urlRegex.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid URL.';
        }
    }
    
    // Password confirmation
    else if (field.name === 'password2') {
        const password1 = document.querySelector('[name="password1"]');
        if (password1 && value !== password1.value) {
            isValid = false;
            errorMessage = 'Passwords do not match.';
        }
    }
    
    // Minimum length validation
    else if (field.minLength && value.length > 0 && value.length < field.minLength) {
        isValid = false;
        errorMessage = `Minimum ${field.minLength} characters required.`;
    }

    // Apply error styling if invalid
    if (!isValid) {
        field.classList.add('error');
        field.style.borderColor = '#d63031';
        showErrorMessage(field, errorMessage);
    } else {
        field.style.borderColor = '#dfe6e9';
    }

    return isValid;
}

function showErrorMessage(field, message) {
    const errorDiv = document.createElement('small');
    errorDiv.className = 'error-message';
    errorDiv.style.color = '#d63031';
    errorDiv.style.display = 'block';
    errorDiv.style.marginTop = '5px';
    errorDiv.style.fontSize = '0.85rem';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

function removeErrorMessage(field) {
    const existingError = field.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
}

// ===================================
// Dropdown Functionality
// ===================================
function initializeDropdowns() {
    const dropdowns = document.querySelectorAll('.user-dropdown');
    
    dropdowns.forEach(function(dropdown) {
        const button = dropdown.querySelector('.user-btn');
        const content = dropdown.querySelector('.dropdown-content');
        
        if (button && content) {
            // Toggle dropdown on click
            button.addEventListener('click', function(e) {
                e.stopPropagation();
                content.style.display = content.style.display === 'block' ? 'none' : 'block';
            });
            
            // Close dropdown when clicking outside
            document.addEventListener('click', function(e) {
                if (!dropdown.contains(e.target)) {
                    content.style.display = 'none';
                }
            });
        }
    });
}

// ===================================
// Animations
// ===================================
function initializeAnimations() {
    // Fade in cards on scroll
    const cards = document.querySelectorAll('.card');
    
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';
                
                setTimeout(function() {
                    entry.target.style.transition = 'all 0.5s ease';
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);
                
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    cards.forEach(function(card) {
        observer.observe(card);
    });
}

// ===================================
// Tooltips
// ===================================
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(function(element) {
        element.style.position = 'relative';
        element.style.cursor = 'pointer';
        
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');
            tooltip.style.cssText = `
                position: absolute;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                background: #2d3436;
                color: #ffffff;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 0.85rem;
                white-space: nowrap;
                margin-bottom: 8px;
                z-index: 1000;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                animation: fadeIn 0.2s ease;
            `;
            
            this.appendChild(tooltip);
        });
        
        element.addEventListener('mouseleave', function() {
            const tooltip = this.querySelector('.tooltip');
            if (tooltip) {
                tooltip.remove();
            }
        });
    });
}

// ===================================
// Confirmation Dialogs
// ===================================
function initializeConfirmations() {
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    
    confirmButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || 'Are you sure?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
}

// ===================================
// Notification System
// ===================================
function showNotification(message, type = 'info') {
    const container = document.querySelector('.messages-container') || createMessageContainer();
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        ${message}
        <button class="close-btn">&times;</button>
    `;
    
    container.appendChild(alert);
    
    // Add close functionality
    const closeBtn = alert.querySelector('.close-btn');
    closeBtn.addEventListener('click', function() {
        dismissMessage(alert);
    });
    
    // Auto dismiss after 5 seconds
    setTimeout(function() {
        dismissMessage(alert);
    }, 5000);
}

function createMessageContainer() {
    const container = document.createElement('div');
    container.className = 'messages-container';
    document.body.appendChild(container);
    return container;
}

// ===================================
// Loading Spinner
// ===================================
function showLoading(element) {
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    element.appendChild(spinner);
    return spinner;
}

function hideLoading(spinner) {
    if (spinner && spinner.parentNode) {
        spinner.remove();
    }
}

// ===================================
// Table Search/Filter
// ===================================
function initializeTableSearch(tableId, searchInputId) {
    const table = document.getElementById(tableId);
    const searchInput = document.getElementById(searchInputId);
    
    if (!table || !searchInput) return;
    
    searchInput.addEventListener('keyup', function() {
        const filter = this.value.toLowerCase();
        const rows = table.getElementsByTagName('tr');
        
        for (let i = 1; i < rows.length; i++) {
            const row = rows[i];
            const text = row.textContent.toLowerCase();
            
            if (text.includes(filter)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        }
    });
}

// ===================================
// Smooth Scroll
// ===================================
function smoothScrollTo(element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ===================================
// Copy to Clipboard
// ===================================
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() {
            showNotification('Copied to clipboard!', 'success');
        }).catch(function() {
            fallbackCopyToClipboard(text);
        });
    } else {
        fallbackCopyToClipboard(text);
    }
}

function fallbackCopyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    
    try {
        document.execCommand('copy');
        showNotification('Copied to clipboard!', 'success');
    } catch (err) {
        showNotification('Failed to copy!', 'error');
    }
    
    document.body.removeChild(textarea);
}

// ===================================
// Debounce Function (for search, etc.)
// ===================================
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

// ===================================
// Local Storage Helper
// ===================================
const Storage = {
    set: function(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (e) {
            console.error('Error saving to localStorage:', e);
            return false;
        }
    },
    
    get: function(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.error('Error reading from localStorage:', e);
            return null;
        }
    },
    
    remove: function(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (e) {
            console.error('Error removing from localStorage:', e);
            return false;
        }
    }
};

// ===================================
// AJAX Helper
// ===================================
function ajaxRequest(url, method = 'GET', data = null) {
    return fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: data ? JSON.stringify(data) : null
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred. Please try again.', 'error');
    });
}

// ===================================
// Get CSRF Token
// ===================================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ===================================
// Progress Bar
// ===================================
function updateProgressBar(progressBarId, percentage) {
    const progressBar = document.getElementById(progressBarId);
    if (progressBar) {
        progressBar.style.width = percentage + '%';
        progressBar.setAttribute('aria-valuenow', percentage);
    }
}

// ===================================
// Add slideOutRight animation to CSS dynamically
// ===================================
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    .btn:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        pointer-events: none;
    }
    
    .loading {
        pointer-events: none;
        opacity: 0.6;
    }
`;
document.head.appendChild(style);

// ===================================
// Export functions for global use
// ===================================
window.showNotification = showNotification;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.copyToClipboard = copyToClipboard;
window.smoothScrollTo = smoothScrollTo;
window.initializeTableSearch = initializeTableSearch;
window.Storage = Storage;
window.ajaxRequest = ajaxRequest;
window.debounce = debounce;

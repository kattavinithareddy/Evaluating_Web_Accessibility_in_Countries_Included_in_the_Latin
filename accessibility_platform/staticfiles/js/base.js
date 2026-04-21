document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss messages after 5 seconds
    const messages = document.querySelectorAll('.alert');
    messages.forEach(function(message) {
        setTimeout(function() {
            message.style.animation = 'slideOut 0.3s ease';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });

    // Close button for messages
    const closeButtons = document.querySelectorAll('.close-btn');
    closeButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            this.parentElement.remove();
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#f5576c';
                } else {
                    field.style.borderColor = '#e1e8ed';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });
});

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

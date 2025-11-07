// Simple JS for confirmation dialogs (already used in templates)
function confirmAction(message) {
    return confirm(message);
}

// Example: prevent form submission if needed
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Example validation (optional)
        });
    });
});

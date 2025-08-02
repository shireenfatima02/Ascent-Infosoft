document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contact-form');
    
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Clear previous errors
        document.querySelectorAll('.error-message').forEach(el => el.textContent = '');
        
        // Show processing notification immediately
        showNotification('processing');
        
        // Get form data
        const formData = new FormData(contactForm);
        
        try {
            const response = await fetch('/', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Reset form
                contactForm.reset();
                
                // Update to success notification
                updateNotification('success');
            } else {
                if (result.message) {
                    // Update to error notification
                    updateNotification('error');
                } else if (result.errors) {
                    // Hide processing notification first
                    hideNotification('processing');
                    
                    // Show field-specific errors
                    for (const [field, message] of Object.entries(result.errors)) {
                        const errorElement = document.getElementById(`${field}-error`);
                        if (errorElement) {
                            errorElement.textContent = message;
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Error:', error);
            // Update to error notification
            updateNotification('error');
        }
    });
    
    function showNotification(type) {
        const notification = document.getElementById(`${type}-message`);
        notification.style.display = 'block';
        
        if (type === 'processing') {
            const progressBar = notification.querySelector('.progress');
            // Reset progress bar
            progressBar.style.transition = 'none';
            progressBar.style.width = '0%';
            
            // Start animating immediately
            setTimeout(() => {
                progressBar.style.transition = 'width 3s linear';
                progressBar.style.width = '100%';
            }, 10);
        }
    }
    
    function updateNotification(type) {
        // Hide processing notification
        hideNotification('processing');
        
        // Show the final notification
        const notification = document.getElementById(`${type}-message`);
        const progressBar = notification.querySelector('.progress');
        
        notification.style.display = 'block';
        
        // Reset and animate progress bar
        progressBar.style.transition = 'none';
        progressBar.style.width = '0%';
        setTimeout(() => {
            progressBar.style.transition = 'width 3s linear';
            progressBar.style.width = '100%';
        }, 10);
        
        // Hide after 3 seconds
        setTimeout(() => {
            notification.style.display = 'none';
            progressBar.style.width = '0%';
            progressBar.style.transition = 'none';
        }, 3000);
    }
    
    function hideNotification(type) {
        const notification = document.getElementById(`${type}-message`);
        notification.style.display = 'none';
        
        // Reset progress bar
        const progressBar = notification.querySelector('.progress');
        if (progressBar) {
            progressBar.style.width = '0%';
            progressBar.style.transition = 'none';
        }
    }
});
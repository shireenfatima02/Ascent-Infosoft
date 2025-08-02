document.addEventListener('DOMContentLoaded', function() {
    // Country/State/City Dropdown Logic
    const countrySelect = document.getElementById('country');
    const stateSelect = document.getElementById('state');
    const citySelect = document.getElementById('city');

    // Only initialize if dropdowns exist
    if (countrySelect && stateSelect && citySelect) {
        // Load countries
        fetch('/api/countries')
            .then(response => response.json())
            .then(countries => {
                countries.forEach(country => {
                    const option = document.createElement('option');
                    option.value = country.id;
                    option.textContent = country.name;
                    countrySelect.appendChild(option);
                });
            });

        // Country change event
        countrySelect.addEventListener('change', function() {
            const countryId = this.value;
            stateSelect.disabled = !countryId;
            citySelect.disabled = true;
            
            // Clear previous options
            stateSelect.innerHTML = '<option value="" disabled selected>Select State</option>';
            citySelect.innerHTML = '<option value="" disabled selected>Select City</option>';

            if (countryId) {
                fetch(`/api/states/${countryId}`)
                    .then(response => response.json())
                    .then(states => {
                        states.forEach(state => {
                            const option = document.createElement('option');
                            option.value = state.id;
                            option.textContent = state.name;
                            stateSelect.appendChild(option);
                        });
                    });
            }
        });

        // State change event
        stateSelect.addEventListener('change', function() {
            const stateId = this.value;
            citySelect.disabled = !stateId;
            
            // Clear previous options
            citySelect.innerHTML = '<option value="" disabled selected>Select City</option>';

            if (stateId) {
                fetch(`/api/cities/${stateId}`)
                    .then(response => response.json())
                    .then(cities => {
                        cities.forEach(city => {
                            const option = document.createElement('option');
                            option.value = city.id;
                            option.textContent = city.name;
                            citySelect.appendChild(option);
                        });
                    });
            }
        });
    }

    // Form Submission Logic
    const contactForm = document.getElementById('contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.stopImmediatePropagation();
            e.preventDefault();
            
            // Clear previous errors
            document.querySelectorAll('.error-message').forEach(el => {
                el.textContent = '';
            });
            
            // Get selected names instead of IDs
            const countryName = countrySelect.options[countrySelect.selectedIndex].text;
            const stateName = stateSelect.options[stateSelect.selectedIndex].text;
            const cityName = citySelect.options[citySelect.selectedIndex].text;
            
            // Create a new FormData with text values
            const formData = new FormData(contactForm);
            formData.set('country', countryName);
            formData.set('state', stateName);
            formData.set('city', cityName);
            
            // Show processing notification
            showNotification('processing');
            
            try {
                // Submit to correct endpoint
                const response = await fetch('/contact-us/', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    // Reset form
                    contactForm.reset();
                    
                    // Reset dropdown states
                    if (stateSelect) stateSelect.disabled = true;
                    if (citySelect) citySelect.disabled = true;
                    
                    // Reset dropdown selections
                    countrySelect.selectedIndex = 0;
                    stateSelect.innerHTML = '<option value="" disabled selected>Select State</option>';
                    citySelect.innerHTML = '<option value="" disabled selected>Select City</option>';
                    
                    // Show success notification
                    updateNotification('success');
                } else {
                    if (result.message) {
                        // Show generic error notification
                        updateNotification('error');
                    } else if (result.errors) {
                        // Hide processing notification
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
                // Show error notification
                updateNotification('error');
            }
        });
    }

    // Notification Functions
    function showNotification(type) {
        const notification = document.getElementById(`${type}-message`);
        if (!notification) return;
        
        notification.style.display = 'block';
        
        if (type === 'processing') {
            const progressBar = notification.querySelector('.progress');
            if (progressBar) {
                // Reset progress bar
                progressBar.style.transition = 'none';
                progressBar.style.width = '0%';
                
                // Start animating
                setTimeout(() => {
                    progressBar.style.transition = 'width 3s linear';
                    progressBar.style.width = '100%';
                }, 10);
            }
        }
    }
    
    function updateNotification(type) {
        // Hide processing notification
        hideNotification('processing');
        
        // Show the final notification
        const notification = document.getElementById(`${type}-message`);
        if (!notification) return;
        
        const progressBar = notification.querySelector('.progress');
        notification.style.display = 'block';
        
        if (progressBar) {
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
    }
    
    function hideNotification(type) {
        const notification = document.getElementById(`${type}-message`);
        if (!notification) return;
        
        notification.style.display = 'none';
        
        // Reset progress bar
        const progressBar = notification.querySelector('.progress');
        if (progressBar) {
            progressBar.style.width = '0%';
            progressBar.style.transition = 'none';
        }
    }
});
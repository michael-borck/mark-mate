// Sample JavaScript for testing
'use strict';

class WebsiteController {
    constructor() {
        this.currentSection = 'home';
        this.isLoading = false;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadInitialData();
        console.log('Website controller initialized');
    }

    bindEvents() {
        // Navigation handling
        document.addEventListener('click', (e) => {
            if (e.target.matches('a[href^="#"]')) {
                e.preventDefault();
                this.navigateToSection(e.target.getAttribute('href').slice(1));
            }
        });

        // Form handling
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleFormSubmit(form);
            });
        });

        // Scroll handling
        window.addEventListener('scroll', this.throttle(() => {
            this.updateActiveSection();
        }, 100));
    }

    async loadInitialData() {
        try {
            this.isLoading = true;
            // Simulate API call
            const data = await this.fetchData('/api/initial');
            this.processData(data);
        } catch (error) {
            console.error('Failed to load initial data:', error);
            this.showNotification('Failed to load data', 'error');
        } finally {
            this.isLoading = false;
        }
    }

    async fetchData(endpoint) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                if (Math.random() > 0.1) {
                    resolve({ status: 'success', data: [] });
                } else {
                    reject(new Error('Network error'));
                }
            }, 1000);
        });
    }

    processData(data) {
        if (data && data.status === 'success') {
            console.log('Data processed successfully:', data.data);
        }
    }

    navigateToSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            section.scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
            this.currentSection = sectionId;
            this.updateUrl(sectionId);
        }
    }

    updateUrl(sectionId) {
        if (history.pushState) {
            history.pushState(null, null, `#${sectionId}`);
        }
    }

    updateActiveSection() {
        const sections = document.querySelectorAll('section[id]');
        const scrollPosition = window.scrollY + 100;

        sections.forEach(section => {
            if (section.offsetTop <= scrollPosition && 
                section.offsetTop + section.offsetHeight > scrollPosition) {
                this.currentSection = section.id;
            }
        });
    }

    handleFormSubmit(form) {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        if (this.validateForm(data)) {
            this.submitForm(data);
        } else {
            this.showNotification('Please fill in all required fields', 'warning');
        }
    }

    validateForm(data) {
        const requiredFields = ['name', 'email'];
        return requiredFields.every(field => data[field] && data[field].trim() !== '');
    }

    async submitForm(data) {
        try {
            this.isLoading = true;
            await this.fetchData('/api/submit');
            this.showNotification('Form submitted successfully!', 'success');
        } catch (error) {
            console.error('Form submission failed:', error);
            this.showNotification('Submission failed. Please try again.', 'error');
        } finally {
            this.isLoading = false;
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    throttle(func, limit) {
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

    // Utility functions
    static formatDate(date) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(date);
    }

    static debounce(func, wait) {
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
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const controller = new WebsiteController();
    
    // Global error handling
    window.addEventListener('error', (event) => {
        console.error('Global error:', event.error);
    });
    
    // Service worker registration (modern web app)
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => console.log('SW registered:', registration))
            .catch(error => console.log('SW registration failed:', error));
    }
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WebsiteController;
}
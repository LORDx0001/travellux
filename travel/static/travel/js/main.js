// Main JavaScript for TravelUX

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.style.display = 'none';
            }, 300);
        }, 5000);
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = '#dc3545';
                    isValid = false;
                } else {
                    field.style.borderColor = '#e9ecef';
                }
            });

            if (!isValid) {
                e.preventDefault();
                showMessage('Пожалуйста, заполните все обязательные поля', 'error');
            }
        });
    });

    // Add to cart animation
    const addToCartButtons = document.querySelectorAll('[action*="add-to-cart"]');
    addToCartButtons.forEach(form => {
        form.addEventListener('submit', function(e) {
            const button = form.querySelector('button[type="submit"]');
            const originalText = button.textContent;
            
            button.textContent = 'Добавлено!';
            button.style.background = '#28a745';
            
            setTimeout(() => {
                button.textContent = originalText;
                button.style.background = '';
            }, 2000);
        });
    });

    // Filter form auto-submit
    const filterInputs = document.querySelectorAll('.filter-form input, .filter-form select');
    filterInputs.forEach(input => {
        input.addEventListener('change', function() {
            // Auto-submit form after 500ms delay
            clearTimeout(window.filterTimeout);
            window.filterTimeout = setTimeout(() => {
                this.closest('form').submit();
            }, 500);
        });
    });

    // Tour card hover effects
    const tourCards = document.querySelectorAll('.tour-card');
    tourCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(-5px)';
        });
    });

    // Mobile menu toggle (if needed)
    const mobileMenuButton = document.querySelector('.mobile-menu-btn');
    const navMenu = document.querySelector('.nav');
    
    if (mobileMenuButton && navMenu) {
        mobileMenuButton.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }

    // Scroll to top button
    const scrollTopBtn = createScrollTopButton();
    document.body.appendChild(scrollTopBtn);

    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollTopBtn.style.display = 'block';
        } else {
            scrollTopBtn.style.display = 'none';
        }
    });

    // Loading states for async operations
    const asyncButtons = document.querySelectorAll('[data-async]');
    asyncButtons.forEach(button => {
        button.addEventListener('click', function() {
            showLoading(this);
        });
    });
});

// Utility functions
function showMessage(message, type = 'success') {
    const messageContainer = document.querySelector('.messages .container');
    if (!messageContainer) return;

    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="close" onclick="this.parentElement.style.display='none'">&times;</button>
    `;
    
    messageContainer.appendChild(alert);
    
    setTimeout(() => {
        alert.style.opacity = '0';
        setTimeout(() => {
            alert.remove();
        }, 300);
    }, 5000);
}

function createScrollTopButton() {
    const button = document.createElement('button');
    button.innerHTML = '<i class="fas fa-arrow-up"></i>';
    button.className = 'scroll-top-btn';
    button.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        background: #007bff;
        color: white;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        display: none;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
        transition: all 0.3s ease;
    `;
    
    button.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    button.addEventListener('mouseenter', function() {
        this.style.background = '#0056b3';
        this.style.transform = 'scale(1.1)';
    });
    
    button.addEventListener('mouseleave', function() {
        this.style.background = '#007bff';
        this.style.transform = 'scale(1)';
    });
    
    return button;
}

function showLoading(button) {
    const originalText = button.textContent;
    button.textContent = 'Загрузка...';
    button.disabled = true;
    
    // Reset after 3 seconds (adjust as needed)
    setTimeout(() => {
        button.textContent = originalText;
        button.disabled = false;
    }, 3000);
}

// Price formatting
function formatPrice(price) {
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB'
    }).format(price);
}

// Date formatting
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}

// Search functionality enhancement
function enhanceSearch() {
    const searchInput = document.querySelector('input[name="search"]');
    if (!searchInput) return;

    let searchTimeout;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            // Auto-submit search after 1 second of inactivity
            this.closest('form').submit();
        }, 1000);
    });
}

// Initialize enhanced search
document.addEventListener('DOMContentLoaded', enhanceSearch);

// Cart counter update
function updateCartCounter(count) {
    const cartCounter = document.querySelector('.cart-count');
    if (cartCounter) {
        cartCounter.textContent = count;
        
        // Animate counter
        cartCounter.style.transform = 'scale(1.3)';
        setTimeout(() => {
            cartCounter.style.transform = 'scale(1)';
        }, 200);
    }
}

// Tour comparison functionality (future feature)
let comparisonList = [];

function addToComparison(tourId) {
    if (comparisonList.length >= 3) {
        showMessage('Можно сравнить максимум 3 тура', 'error');
        return;
    }
    
    if (!comparisonList.includes(tourId)) {
        comparisonList.push(tourId);
        showMessage('Тур добавлен к сравнению', 'success');
        updateComparisonCounter();
    }
}

function removeFromComparison(tourId) {
    comparisonList = comparisonList.filter(id => id !== tourId);
    updateComparisonCounter();
}

function updateComparisonCounter() {
    const counter = document.querySelector('.comparison-counter');
    if (counter) {
        counter.textContent = comparisonList.length;
        counter.style.display = comparisonList.length > 0 ? 'block' : 'none';
    }
}

// Image lazy loading
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Initialize lazy loading if supported
if ('IntersectionObserver' in window) {
    document.addEventListener('DOMContentLoaded', initLazyLoading);
}

// Performance monitoring
function trackPageLoad() {
    window.addEventListener('load', function() {
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        console.log(`Page loaded in ${loadTime}ms`);
        
        // Send to analytics if needed
        if (typeof gtag !== 'undefined') {
            gtag('event', 'page_load_time', {
                value: loadTime,
                event_category: 'Performance'
            });
        }
    });
}

trackPageLoad();
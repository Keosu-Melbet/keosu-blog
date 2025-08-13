// Kèo Sư - Main JavaScript functionality
(function() {
    'use strict';

    // Initialize when DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        initializeComponents();
        initializeChatbot();
        initializeScrollEffects();
        initializeFormValidation();
        initializeLazyLoading();
        initializeTooltips();
    });

    // Initialize main components
    function initializeComponents() {
        // Active navigation highlighting
        highlightActiveNav();
        
        // Search form enhancements
        enhanceSearchForm();
        
        // Table responsive enhancements
        enhanceResponsiveTables();
        
        // Auto-refresh for live scores
        initializeLiveScoreRefresh();
    }

    // Chatbot functionality
    function initializeChatbot() {
        const chatbotToggle = document.getElementById('chatbot-toggle');
        const chatbotIframe = document.getElementById('chatbot-iframe');
        
        if (chatbotToggle && chatbotIframe) {
            chatbotToggle.addEventListener('click', function() {
                toggleChatbot();
            });
            
            // Close chatbot when clicking outside
            document.addEventListener('click', function(e) {
                if (!chatbotToggle.contains(e.target) && !chatbotIframe.contains(e.target)) {
                    if (!chatbotIframe.classList.contains('d-none')) {
                        // Only close if click is outside chatbot area
                        const rect = chatbotIframe.getBoundingClientRect();
                        if (e.clientX < rect.left || e.clientX > rect.right || 
                            e.clientY < rect.top || e.clientY > rect.bottom) {
                            closeChatbot();
                        }
                    }
                }
            });
        }
    }

    // Toggle chatbot visibility
    function toggleChatbot() {
        const chatbotToggle = document.getElementById('chatbot-toggle');
        const chatbotIframe = document.getElementById('chatbot-iframe');
        
        if (chatbotIframe.classList.contains('d-none')) {
            openChatbot();
        } else {
            closeChatbot();
        }
    }

    // Open chatbot
    function openChatbot() {
        const chatbotToggle = document.getElementById('chatbot-toggle');
        const chatbotIframe = document.getElementById('chatbot-iframe');
        
        chatbotIframe.classList.remove('d-none');
        chatbotToggle.innerHTML = '<i class="fas fa-times fa-lg"></i>';
        chatbotToggle.classList.add('btn-danger');
        chatbotToggle.classList.remove('btn-warning');
        
        // Add animation
        chatbotIframe.style.opacity = '0';
        chatbotIframe.style.transform = 'translateY(20px)';
        setTimeout(() => {
            chatbotIframe.style.transition = 'all 0.3s ease';
            chatbotIframe.style.opacity = '1';
            chatbotIframe.style.transform = 'translateY(0)';
        }, 10);
    }

    // Close chatbot
    function closeChatbot() {
        const chatbotToggle = document.getElementById('chatbot-toggle');
        const chatbotIframe = document.getElementById('chatbot-iframe');
        
        chatbotIframe.style.opacity = '0';
        chatbotIframe.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            chatbotIframe.classList.add('d-none');
            chatbotToggle.innerHTML = '<i class="fas fa-comments fa-lg"></i>';
            chatbotToggle.classList.remove('btn-danger');
            chatbotToggle.classList.add('btn-warning');
        }, 300);
    }

    // Highlight active navigation
    function highlightActiveNav() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
                link.classList.add('active');
                link.style.backgroundColor = 'rgba(255, 215, 0, 0.2)';
                link.style.color = '#ffd700';
            }
        });
    }

    // Enhance search form
    function enhanceSearchForm() {
        const searchInput = document.querySelector('input[name="q"]');
        if (searchInput) {
            // Add search suggestions
            const suggestions = [
                'kèo thơm hôm nay',
                'soi kèo Premier League',
                'mẹo cược tài xỉu',
                'Manchester United',
                'Barcelona vs Real Madrid',
                'Champions League'
            ];
            
            let suggestionsList = null;
            
            searchInput.addEventListener('focus', function() {
                if (!suggestionsList) {
                    createSearchSuggestions();
                }
            });
            
            searchInput.addEventListener('input', function() {
                const query = this.value.toLowerCase();
                if (suggestionsList && query.length > 0) {
                    filterSuggestions(query);
                }
            });
            
            function createSearchSuggestions() {
                suggestionsList = document.createElement('div');
                suggestionsList.className = 'search-suggestions position-absolute bg-dark border border-warning rounded mt-1 w-100';
                suggestionsList.style.zIndex = '1000';
                suggestionsList.style.maxHeight = '200px';
                suggestionsList.style.overflowY = 'auto';
                
                suggestions.forEach(suggestion => {
                    const item = document.createElement('div');
                    item.className = 'suggestion-item px-3 py-2 text-light cursor-pointer';
                    item.textContent = suggestion;
                    item.style.cursor = 'pointer';
                    
                    item.addEventListener('mouseenter', function() {
                        this.style.backgroundColor = 'rgba(255, 215, 0, 0.1)';
                    });
                    
                    item.addEventListener('mouseleave', function() {
                        this.style.backgroundColor = 'transparent';
                    });
                    
                    item.addEventListener('click', function() {
                        searchInput.value = suggestion;
                        suggestionsList.style.display = 'none';
                        searchInput.form.submit();
                    });
                    
                    suggestionsList.appendChild(item);
                });
                
                searchInput.parentNode.style.position = 'relative';
                searchInput.parentNode.appendChild(suggestionsList);
                
                // Hide suggestions when clicking outside
                document.addEventListener('click', function(e) {
                    if (!searchInput.contains(e.target) && !suggestionsList.contains(e.target)) {
                        suggestionsList.style.display = 'none';
                    }
                });
            }
            
            function filterSuggestions(query) {
                const items = suggestionsList.querySelectorAll('.suggestion-item');
                let hasVisible = false;
                
                items.forEach(item => {
                    if (item.textContent.toLowerCase().includes(query)) {
                        item.style.display = 'block';
                        hasVisible = true;
                    } else {
                        item.style.display = 'none';
                    }
                });
                
                suggestionsList.style.display = hasVisible ? 'block' : 'none';
            }
        }
    }

    // Enhance responsive tables
    function enhanceResponsiveTables() {
        const tables = document.querySelectorAll('.table-responsive table');
        tables.forEach(table => {
            // Add horizontal scroll indicator
            const wrapper = table.closest('.table-responsive');
            if (wrapper && table.scrollWidth > wrapper.clientWidth) {
                wrapper.classList.add('has-scroll');
                
                // Add scroll indicator
                const indicator = document.createElement('div');
                indicator.className = 'scroll-indicator text-warning small text-center mt-2';
                indicator.innerHTML = '<i class="fas fa-arrows-alt-h me-1"></i>Vuốt ngang để xem thêm';
                wrapper.appendChild(indicator);
            }
        });
    }

    // Live score auto-refresh
    function initializeLiveScoreRefresh() {
        const liveScoreIframe = document.querySelector('iframe[src*="flashscore"]');
        if (liveScoreIframe) {
            // Refresh every 30 seconds
            setInterval(() => {
                if (document.visibilityState === 'visible') {
                    refreshLiveScore();
                }
            }, 30000);
        }
    }

    // Refresh live score iframe
    function refreshLiveScore() {
        const iframe = document.querySelector('iframe[src*="flashscore"]');
        if (iframe) {
            const src = iframe.src;
            iframe.src = '';
            setTimeout(() => {
                iframe.src = src;
            }, 100);
        }
    }

    // Initialize scroll effects
    function initializeScrollEffects() {
        // Back to top button
        createBackToTopButton();
        
        // Smooth scroll for anchor links
        initializeSmoothScroll();
        
        // Navbar background on scroll
        initializeNavbarScroll();
    }

    // Create back to top button
    function createBackToTopButton() {
        const backToTop = document.createElement('button');
        backToTop.innerHTML = '<i class="fas fa-chevron-up"></i>';
        backToTop.className = 'btn btn-warning position-fixed rounded-circle';
        backToTop.style.cssText = `
            bottom: 100px;
            right: 20px;
            width: 50px;
            height: 50px;
            display: none;
            z-index: 999;
            box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
        `;
        
        backToTop.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
        
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTop.style.display = 'block';
            } else {
                backToTop.style.display = 'none';
            }
        });
        
        document.body.appendChild(backToTop);
    }

    // Initialize smooth scroll
    function initializeSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // Navbar scroll effect
    function initializeNavbarScroll() {
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            window.addEventListener('scroll', () => {
                if (window.pageYOffset > 50) {
                    navbar.style.backgroundColor = 'rgba(13, 13, 13, 0.95)';
                    navbar.style.backdropFilter = 'blur(10px)';
                } else {
                    navbar.style.backgroundColor = '';
                    navbar.style.backdropFilter = '';
                }
            });
        }
    }

    // Form validation
    function initializeFormValidation() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                if (!validateForm(this)) {
                    e.preventDefault();
                }
            });
            
            // Real-time validation
            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                input.addEventListener('blur', () => validateField(input));
                input.addEventListener('input', () => clearFieldError(input));
            });
        });
    }

    // Validate form
    function validateForm(form) {
        let isValid = true;
        const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
        
        inputs.forEach(input => {
            if (!validateField(input)) {
                isValid = false;
            }
        });
        
        return isValid;
    }

    // Validate individual field
    function validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let message = '';
        
        // Required validation
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            message = 'Trường này là bắt buộc';
        }
        
        // Email validation
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                message = 'Email không hợp lệ';
            }
        }
        
        // Phone validation
        if (field.type === 'tel' && value) {
            const phoneRegex = /^[\d\s\-\+\(\)]+$/;
            if (!phoneRegex.test(value)) {
                isValid = false;
                message = 'Số điện thoại không hợp lệ';
            }
        }
        
        // URL validation
        if (field.type === 'url' && value) {
            try {
                new URL(value);
            } catch {
                isValid = false;
                message = 'URL không hợp lệ';
            }
        }
        
        // Show/hide error
        if (isValid) {
            clearFieldError(field);
        } else {
            showFieldError(field, message);
        }
        
        return isValid;
    }

    // Show field error
    function showFieldError(field, message) {
        clearFieldError(field);
        
        field.classList.add('is-invalid');
        const error = document.createElement('div');
        error.className = 'invalid-feedback';
        error.textContent = message;
        field.parentNode.appendChild(error);
    }

    // Clear field error
    function clearFieldError(field) {
        field.classList.remove('is-invalid');
        const error = field.parentNode.querySelector('.invalid-feedback');
        if (error) {
            error.remove();
        }
    }

    // Lazy loading for images
    function initializeLazyLoading() {
        const images = document.querySelectorAll('img[data-src]');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });
            
            images.forEach(img => imageObserver.observe(img));
        } else {
            // Fallback for browsers without IntersectionObserver
            images.forEach(img => {
                img.src = img.dataset.src;
            });
        }
    }

    // Initialize tooltips
    function initializeTooltips() {
        // Enable Bootstrap tooltips if available
        if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
    }

    // Utility functions
    window.KeoSu = {
        // Copy to clipboard
        copyToClipboard: function(text) {
            if (navigator.clipboard) {
                navigator.clipboard.writeText(text).then(() => {
                    showNotification('Đã sao chép vào clipboard!', 'success');
                }).catch(() => {
                    fallbackCopyTextToClipboard(text);
                });
            } else {
                fallbackCopyTextToClipboard(text);
            }
        },
        
        // Share functionality
        share: function(title, text, url) {
            if (navigator.share) {
                navigator.share({
                    title: title,
                    text: text,
                    url: url
                });
            } else {
                // Fallback to copying URL
                this.copyToClipboard(url);
            }
        },
        
        // Show notification
        showNotification: function(message, type = 'info') {
            showNotification(message, type);
        },
        
        // Toggle chatbot
        toggleChatbot: toggleChatbot,
        
        // Refresh live score
        refreshLiveScore: refreshLiveScore
    };

    // Fallback copy function
    function fallbackCopyTextToClipboard(text) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
            showNotification('Đã sao chép vào clipboard!', 'success');
        } catch (err) {
            showNotification('Không thể sao chép', 'error');
        }
        
        document.body.removeChild(textArea);
    }

    // Show notification
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} position-fixed`;
        notification.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 1060;
            min-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        `;
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    // Performance monitoring
    window.addEventListener('load', function() {
        // Log page load time
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        console.log(`Page loaded in ${loadTime}ms`);
        
        // Monitor critical resources
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                list.getEntries().forEach((entry) => {
                    if (entry.duration > 1000) {
                        console.warn(`Slow resource: ${entry.name} took ${entry.duration}ms`);
                    }
                });
            });
            observer.observe({entryTypes: ['resource']});
        }
    });

    // Error handling
    window.addEventListener('error', function(e) {
        console.error('JavaScript Error:', e.error);
        // You could send this to an error tracking service
    });

    // Service Worker registration (for PWA features)
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            // Uncomment when you have a service worker
            // navigator.serviceWorker.register('/sw.js');
        });
    }

})();

// Global functions for template usage
function toggleChatbot() {
    if (window.KeoSu) {
        window.KeoSu.toggleChatbot();
    }
}

function copyToClipboard(text) {
    if (window.KeoSu) {
        window.KeoSu.copyToClipboard(text);
    }
}

function refreshLiveScore() {
    if (window.KeoSu) {
        window.KeoSu.refreshLiveScore();
    }
}

/**
 * SWILL ADULT STREAM - PREMIUM SCRIPTS
 * ФИОЛЕТОВЫЙ НЕОН • АВТООБНОВЛЕНИЕ • ЭФФЕКТЫ
 */

document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    // ============= ИНИЦИАЛИЗАЦИЯ =============
    console.log('⚡ SWILL STREAM ACTIVATED');
    
    // ============= ФИОЛЕТОВЫЙ КУРСОР =============
    const style = document.createElement('style');
    style.textContent = `
        *::selection {
            background: #6b21a8;
            color: white;
        }
        
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #0a0a0f;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #6b21a8;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #9333ea;
        }
    `;
    document.head.appendChild(style);

    // ============= ПЛАВНАЯ ЗАГРУЗКА =============
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);

    // ============= ЭФФЕКТЫ ДЛЯ КАРТОЧЕК =============
    const videoCards = document.querySelectorAll('.video-card');
    
    videoCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-12px)';
            this.style.boxShadow = '0 25px 40px -15px #a855f7';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });

    // ============= СЧЕТЧИК ПРИБЫЛИ =============
    function updateEarnings() {
        fetch('/api/earnings')
            .then(response => {
                if (!response.ok) throw new Error('Network error');
                return response.json();
            })
            .then(data => {
                // ОБНОВЛЯЕМ ВСЕ ЭЛЕМЕНТЫ С ПРИБЫЛЬЮ
                const todayEarnings = document.getElementById('today-earnings');
                const todayStat = document.getElementById('today-stat');
                
                if (todayEarnings) {
                    todayEarnings.textContent = '$' + data.today.toLocaleString();
                }
                
                if (todayStat) {
                    todayStat.textContent = '$' + data.today.toLocaleString();
                }
                
                // ОБНОВЛЯЕМ СТАТИСТИКУ
                const statValues = document.querySelectorAll('.stat-card .stat-value');
                if (statValues.length >= 3) {
                    statValues[0].textContent = '$' + data.total.toLocaleString();
                    statValues[1].textContent = '$' + data.week.toLocaleString();
                    statValues[2].textContent = '$' + data.today.toLocaleString();
                }
                
                // АНИМАЦИЯ ПРИ ОБНОВЛЕНИИ
                const earningsElement = document.querySelector('.live-earnings');
                if (earningsElement) {
                    earningsElement.style.animation = 'none';
                    earningsElement.offsetHeight;
                    earningsElement.style.animation = 'pulse 0.5s ease';
                }
            })
            .catch(error => console.error('Earnings update error:', error));
    }

    // ОБНОВЛЯЕМ КАЖДЫЕ 5 СЕКУНД
    setInterval(updateEarnings, 5000);

    // ============= ПРЕВЬЮ ФАЙЛОВ =============
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            if (this.files && this.files[0]) {
                const fileName = this.files[0].name;
                const fileSize = (this.files[0].size / 1024 / 1024).toFixed(2);
                
                // СОЗДАЕМ КАСТОМНЫЙ ИНДИКАТОР
                const indicator = document.createElement('div');
                indicator.className = 'file-indicator';
                indicator.style.cssText = `
                    margin-top: 10px;
                    padding: 10px;
                    background: #1e1e2a;
                    border-radius: 10px;
                    color: #d8b4fe;
                    font-size: 14px;
                    border-left: 4px solid #6b21a8;
                `;
                indicator.innerHTML = `📁 ${fileName} (${fileSize} MB)`;
                
                // УДАЛЯЕМ СТАРЫЙ ИНДИКАТОР
                const oldIndicator = this.parentNode.querySelector('.file-indicator');
                if (oldIndicator) oldIndicator.remove();
                
                this.parentNode.appendChild(indicator);
            }
        });
    });

    // ============= КНОПКА КОПИРОВАНИЯ =============
    window.copyToClipboard = function(text) {
        navigator.clipboard.writeText(text).then(() => {
            // СОЗДАЕМ ВСПЛЫВАЮЩЕЕ УВЕДОМЛЕНИЕ
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: #6b21a8;
                color: white;
                padding: 15px 30px;
                border-radius: 40px;
                font-weight: 600;
                z-index: 9999;
                animation: slideIn 0.3s ease;
                box-shadow: 0 0 30px #6b21a8;
            `;
            notification.textContent = '✅ СКОПИРОВАНО!';
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => notification.remove(), 300);
            }, 2000);
        });
    };

    // ============= АНИМАЦИИ =============
    const styleSheet = document.createElement('style');
    styleSheet.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(168, 85, 247, 0.7); }
            70% { box-shadow: 0 0 0 15px rgba(168, 85, 247, 0); }
            100% { box-shadow: 0 0 0 0 rgba(168, 85, 247, 0); }
        }
        
        .video-card {
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .btn {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
    `;
    document.head.appendChild(styleSheet);

    // ============= ЛЕНИВАЯ ЗАГРУЗКА =============
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => imageObserver.observe(img));
    }

    // ============= ПОДТВЕРЖДЕНИЕ ДЕЙСТВИЙ =============
    window.confirmAction = function(message) {
        return confirm(message);
    };

    // ============= ЗАЩИТА КОНТЕНТА =============
    document.addEventListener('contextmenu', function(e) {
        // ТОЛЬКО ДЛЯ ВИДЕО И ИЗОБРАЖЕНИЙ
        if (e.target.tagName === 'VIDEO' || e.target.tagName === 'IMG') {
            e.preventDefault();
            return false;
        }
    });

    // ============= ДИНАМИЧЕСКИЙ БЭКГРАУНД =============
    function createPurpleParticles() {
        const canvas = document.createElement('canvas');
        canvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
            opacity: 0.1;
        `;
        
        document.body.appendChild(canvas);
        
        // ТОЛЬКО ЕСЛИ НЕ НАГРУЖАЕТ ПРОИЗВОДИТЕЛЬНОСТЬ
        if (window.innerWidth > 768) {
            // АКТИВИРУЕМ ТОЛЬКО НА БОЛЬШИХ ЭКРАНАХ
        }
    }

    // ============= ИНИЦИАЛИЗАЦИЯ СТРАНИЦЫ =============
    console.log('✅ SWILL ready • Purple neon active');
});

// ============= ГЛОБАЛЬНЫЕ ФУНКЦИИ =============
window.SWILL = {
    version: '1.0.0',
    theme: 'dark_purple',
    earnings: null,
    
    refresh: function() {
        location.reload();
    },
    
    scrollToTop: function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
};
// Neumorphism Login Form JavaScript
class NeumorphismLoginForm {
    constructor() {
        this.form = document.getElementById('loginForm');

        // چک کردن وجود المان‌ها قبل از استفاده
        if (!this.form) {
            console.error('Login form not found!');
            return;
        }

        this.usernameInput = document.getElementById('username');
        this.passwordInput = document.getElementById('password');
        this.passwordToggle = document.getElementById('passwordToggle');
        this.submitButton = this.form.querySelector('.login-btn');
        this.successMessage = document.getElementById('successMessage');
        this.socialButtons = document.querySelectorAll('.neu-social');

        // چک کردن وجود المان‌های ضروری
        if (!this.usernameInput || !this.passwordInput) {
            console.error('Required form elements not found!');
            return;
        }

        this.init();
    }

    init() {
        if (!this.form) return;

        this.bindEvents();
        this.setupPasswordToggle();
        this.setupSocialButtons();
        this.setupNeumorphicEffects();
    }

    bindEvents() {
        // استفاده از arrow function برای حفظ context
        this.form.addEventListener('submit', (e) => {
            // Validate inputs
            const isUsernameValid = this.validateUsername();
            const isPasswordValid = this.validatePassword();

            if (!isUsernameValid || !isPasswordValid) {
                e.preventDefault();
                this.animateSoftPress(this.submitButton);
                return false;
            }

            // اگر validation موفق بود، اجازه بده فرم به Django submit بشه
            console.log('Form is valid, submitting to Django...');
            // فرم به صورت عادی submit می‌شه (preventDefault صدا نمی‌زنیم)
            return true;
        });

        if (this.usernameInput) {
            this.usernameInput.addEventListener('blur', () => this.validateUsername());
            this.usernameInput.addEventListener('input', () => this.clearError('username'));
        }

        if (this.passwordInput) {
            this.passwordInput.addEventListener('blur', () => this.validatePassword());
            this.passwordInput.addEventListener('input', () => this.clearError('password'));
        }

        // Add soft press effects to inputs
        const inputs = [];
        if (this.usernameInput) inputs.push(this.usernameInput);
        if (this.passwordInput) inputs.push(this.passwordInput);

        inputs.forEach(input => {
            input.addEventListener('focus', (e) => this.addSoftPress(e));
            input.addEventListener('blur', (e) => this.removeSoftPress(e));
        });
    }

    setupPasswordToggle() {
        if (!this.passwordToggle) return;

        this.passwordToggle.addEventListener('click', () => {
            const type = this.passwordInput.type === 'password' ? 'text' : 'password';
            this.passwordInput.type = type;

            const eyeOpen = this.passwordToggle.querySelector('.eye-open');
            const eyeClosed = this.passwordToggle.querySelector('.eye-closed');

            if (eyeOpen && eyeClosed) {
                if (type === 'text') {
                    eyeOpen.style.display = 'none';
                    eyeClosed.style.display = 'block';
                } else {
                    eyeOpen.style.display = 'block';
                    eyeClosed.style.display = 'none';
                }
            }

            this.animateSoftPress(this.passwordToggle);
        });
    }

    setupSocialButtons() {
        this.socialButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                this.animateSoftPress(button);
                this.handleSocialLogin('Social', button);
            });
        });
    }

    setupNeumorphicEffects() {
        // Add hover effects to all neumorphic elements
        const neuElements = document.querySelectorAll('.neu-icon, .neu-checkbox, .neu-social');
        neuElements.forEach(element => {
            element.addEventListener('mouseenter', () => {
                element.style.transform = 'scale(1.05)';
                element.style.transition = 'transform 0.3s ease';
            });

            element.addEventListener('mouseleave', () => {
                element.style.transform = 'scale(1)';
            });
        });

        // Add ambient light effect on mouse move
        const card = document.querySelector('.login-card');
        if (card) {
            document.addEventListener('mousemove', (e) => {
                this.updateAmbientLight(e);
            });
        }
    }

    updateAmbientLight(e) {
        const card = document.querySelector('.login-card');
        if (!card) return;

        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const angleX = (x - centerX) / centerX;
        const angleY = (y - centerY) / centerY;

        const shadowX = angleX * 30;
        const shadowY = angleY * 30;

        card.style.boxShadow = `
            ${shadowX}px ${shadowY}px 60px #bec3cf,
            ${-shadowX}px ${-shadowY}px 60px #ffffff
        `;
    }

    addSoftPress(e) {
        const inputGroup = e.target.closest('.neu-input');
        if (inputGroup) {
            inputGroup.style.transform = 'scale(0.98)';
            inputGroup.style.transition = 'transform 0.2s ease';
        }
    }

    removeSoftPress(e) {
        const inputGroup = e.target.closest('.neu-input');
        if (inputGroup) {
            inputGroup.style.transform = 'scale(1)';
        }
    }

    animateSoftPress(element) {
        if (!element) return;

        element.style.transform = 'scale(0.95)';
        element.style.transition = 'transform 0.15s ease';
        setTimeout(() => {
            element.style.transform = 'scale(1)';
        }, 150);
    }

    validateUsername() {
        if (!this.usernameInput) return false;

        const username = this.usernameInput.value.trim();

        if (!username) {
            this.showError('username', 'Username is required');
            return false;
        }

        if (username.length < 3) {
            this.showError('username', 'Username must be at least 3 characters');
            return false;
        }

        this.clearError('username');
        return true;
    }

    validatePassword() {
        if (!this.passwordInput) return false;

        const password = this.passwordInput.value;

        if (!password) {
            this.showError('password', 'Password is required');
            return false;
        }

        if (password.length < 3) {
            this.showError('password', 'Password must be at least 3 characters');
            return false;
        }

        this.clearError('password');
        return true;
    }

    showError(field, message) {
        const inputElement = document.getElementById(field);
        if (!inputElement) return;

        const formGroup = inputElement.closest('.form-group');
        const errorElement = document.getElementById(`${field}Error`);

        if (formGroup) formGroup.classList.add('error');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.classList.add('show');
        }

        // Add gentle shake animation
        inputElement.style.animation = 'gentleShake 0.5s ease-in-out';
        setTimeout(() => {
            inputElement.style.animation = '';
        }, 500);
    }

    clearError(field) {
        const inputElement = document.getElementById(field);
        if (!inputElement) return;

        const formGroup = inputElement.closest('.form-group');
        const errorElement = document.getElementById(`${field}Error`);

        if (formGroup) formGroup.classList.remove('error');
        if (errorElement) {
            errorElement.classList.remove('show');
            setTimeout(() => {
                errorElement.textContent = '';
            }, 300);
        }
    }

    async handleSocialLogin(provider, button) {
        console.log(`Initiating ${provider} login...`);

        if (!button) return;

        // Add loading state to button
        button.style.pointerEvents = 'none';
        button.style.opacity = '0.7';

        try {
            await new Promise(resolve => setTimeout(resolve, 1500));
            console.log(`Redirecting to ${provider} authentication...`);
            window.location.href = '/ref/home/';
        } catch (error) {
            console.error(`${provider} authentication failed: ${error.message}`);
        } finally {
            button.style.pointerEvents = 'auto';
            button.style.opacity = '1';
        }
    }

    setLoading(loading) {
        if (!this.submitButton) return;

        this.submitButton.classList.toggle('loading', loading);
        this.submitButton.disabled = loading;

        // Disable social buttons during login
        this.socialButtons.forEach(button => {
            if (button) {
                button.style.pointerEvents = loading ? 'none' : 'auto';
                button.style.opacity = loading ? '0.6' : '1';
            }
        });
    }
}

// Add custom animations
if (!document.querySelector('#neu-keyframes')) {
    const style = document.createElement('style');
    style.id = 'neu-keyframes';
    style.textContent = `
        @keyframes gentleShake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-3px); }
            75% { transform: translateX(3px); }
        }
        
        @keyframes successPulse {
            0% { transform: scale(0.8); opacity: 0; }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
}

// Initialize با چک کردن وجود فرم
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        new NeumorphismLoginForm();
        console.log('✅ Login form script loaded successfully');
    } else {
        console.log('ℹ️ Login form not found on this page');
    }
});
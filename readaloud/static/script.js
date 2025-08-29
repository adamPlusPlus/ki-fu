// ReadAloud Web Interface JavaScript

class ReadAloudInterface {
    constructor() {
        this.config = {};
        this.init();
    }

    async init() {
        await this.loadConfig();
        this.setupEventListeners();
        this.updateUI();
        this.checkStatus();
        
        // Debug: Check if loading modal exists
        this.checkModalElements();
        
        // Check status periodically
        setInterval(() => this.checkStatus(), 10000);
    }

    async loadConfig() {
        try {
            const response = await fetch('/api/config');
            this.config = await response.json();
        } catch (error) {
            console.error('Failed to load config:', error);
            this.showToast('Failed to load configuration', 'error');
        }
    }

    setupEventListeners() {
        // Configuration controls
        document.getElementById('ttsEngine').addEventListener('change', (e) => {
            this.config.tts_engine = e.target.value;
            this.updateUI();
        });

        document.getElementById('voice').addEventListener('change', (e) => {
            this.config.voice = e.target.value;
            this.updateUI();
        });

        // Sliders
        document.getElementById('temperature').addEventListener('input', (e) => {
            this.config.temperature = parseFloat(e.target.value);
            document.getElementById('tempValue').textContent = this.config.temperature;
        });

        document.getElementById('volume').addEventListener('input', (e) => {
            this.config.volume = parseFloat(e.target.value);
            document.getElementById('volValue').textContent = Math.round(this.config.volume * 100) + '%';
        });

        document.getElementById('speed').addEventListener('input', (e) => {
            this.config.speed = parseFloat(e.target.value);
            document.getElementById('speedValue').textContent = this.config.speed + 'x';
        });

        // Buttons
        document.getElementById('saveConfig').addEventListener('click', () => this.saveConfig());
        document.getElementById('resetConfig').addEventListener('click', () => this.resetConfig());
        
        // TTS Actions
        document.getElementById('readClipboard').addEventListener('click', () => this.readClipboard());
        document.getElementById('readSelection').addEventListener('click', () => this.readSelection());
        document.getElementById('stopAudio').addEventListener('click', () => this.stopAudio());
        document.getElementById('testTTS').addEventListener('click', () => this.testTTS());
        
        // Service Controls
        document.getElementById('startService').addEventListener('click', () => this.startService());
        document.getElementById('stopService').addEventListener('click', () => this.stopService());
    }

    updateUI() {
        // Update current values display
        document.getElementById('currentEngine').textContent = this.config.tts_engine || 'Not set';
        document.getElementById('currentVoice').textContent = this.config.voice || 'Not set';
        
        // Update form values
        if (this.config.tts_engine) {
            document.getElementById('ttsEngine').value = this.config.tts_engine;
        }
        if (this.config.voice) {
            document.getElementById('voice').value = this.config.voice;
        }
        if (this.config.temperature !== undefined) {
            document.getElementById('temperature').value = this.config.temperature;
            document.getElementById('tempValue').textContent = this.config.temperature;
        }
        if (this.config.volume !== undefined) {
            document.getElementById('volume').value = this.config.volume;
            document.getElementById('volValue').textContent = Math.round(this.config.volume * 100) + '%';
        }
        if (this.config.speed !== undefined) {
            document.getElementById('speed').value = this.config.speed;
            document.getElementById('speedValue').textContent = this.config.speed + 'x';
        }
    }

    async saveConfig() {
        try {
            const response = await fetch('/api/config', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.config)
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                this.showToast('Configuration saved successfully!', 'success');
            } else {
                this.showToast(result.message || 'Failed to save configuration', 'error');
            }
        } catch (error) {
            console.error('Failed to save config:', error);
            this.showToast('Failed to save configuration', 'error');
        }
    }

    async resetConfig() {
        if (confirm('Are you sure you want to reset all settings to defaults?')) {
            this.config = {
                tts_engine: 'higgs_audio',
                voice: 'default',
                temperature: 0.3,
                volume: 0.8,
                speed: 1.0,
                audio_output_path: './audio_output'
            };
            this.updateUI();
            this.showToast('Configuration reset to defaults', 'info');
        }
    }

    async readClipboard() {
        // Show loading modal
        this.showLoadingModal('Reading Clipboard...', 'Processing clipboard content for TTS...');

        try {
            const response = await fetch('/api/tts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ action: 'read_clipboard' })
            });

            const result = await response.json();
            
            // Hide loading modal
            this.hideLoadingModal();
            
            if (result.status === 'success') {
                this.showToast(result.message, 'success');
            } else {
                this.showToast(result.message, 'error');
            }
        } catch (error) {
            console.error('Failed to read clipboard:', error);
            this.hideLoadingModal();
            this.showToast('Failed to read clipboard', 'error');
        }
    }

    async readSelection() {
        // Show loading modal
        this.showLoadingModal('Reading Selection...', 'Processing selected text for TTS...');

        try {
            const response = await fetch('/api/tts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ action: 'read_selection' })
            });

            const result = await response.json();
            
            // Hide loading modal
            this.hideLoadingModal();
            
            if (result.status === 'success') {
                this.showToast(result.message, 'success');
            } else {
                this.showToast(result.message, 'error');
            }
        } catch (error) {
            console.error('Failed to read selection:', error);
            this.hideLoadingModal();
            this.showToast('Failed to read selection', 'error');
        }
    }

    async stopAudio() {
        try {
            const response = await fetch('/api/tts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ action: 'stop' })
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                this.showToast(result.message, 'success');
            } else {
                this.showToast(result.message, 'error');
            }
        } catch (error) {
            console.error('Failed to stop audio:', error);
            this.showToast('Failed to stop audio', 'error');
        }
    }

    async testTTS() {
        console.log('testTTS called!'); // Debug log
        const testText = document.getElementById('testText').value.trim();
        
        if (!testText) {
            this.showToast('Please enter some text to test', 'error');
            return;
        }

        console.log('Showing loading modal...'); // Debug log
        // Show loading modal
        this.showLoadingModal('Generating TTS Audio...', 'This may take up to 2 minutes for the first generation.');

        try {
            const response = await fetch('/api/tts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    action: 'test', 
                    text: testText 
                })
            });

            const result = await response.json();
            
            console.log('Hiding loading modal...'); // Debug log
            // Hide loading modal
            this.hideLoadingModal();
            
            if (result.status === 'success') {
                this.showToast(result.message, 'success');
            } else {
                this.showToast(result.message, 'error');
            }
        } catch (error) {
            console.error('Failed to test TTS:', error);
            this.hideLoadingModal();
            this.showToast('Failed to test TTS', 'error');
        }
    }

    async checkStatus() {
        try {
            const response = await fetch('/api/status');
            const result = await response.json();
            
            if (result.status === 'success') {
                this.updateStatusIndicator(true);
                this.updateHiggsStatus(result.higgs_audio);
                
                // Update service status if available
                if (result.higgs_service) {
                    this.updateServiceStatus(result.higgs_service);
                }
            } else {
                this.updateStatusIndicator(false);
            }
        } catch (error) {
            console.error('Failed to check status:', error);
            this.updateStatusIndicator(false);
        }
    }

    updateStatusIndicator(connected) {
        const indicator = document.getElementById('statusIndicator');
        const statusText = document.getElementById('statusText');
        
        if (connected) {
            indicator.classList.add('connected');
            statusText.textContent = 'Connected';
        } else {
            indicator.classList.remove('connected');
            statusText.textContent = 'Disconnected';
        }
    }

    updateHiggsStatus(available) {
        const higgsStatus = document.getElementById('higgsStatus');
        if (available) {
            higgsStatus.textContent = 'Available';
            higgsStatus.style.color = 'var(--vs-accent-green)';
        } else {
            higgsStatus.textContent = 'Not Available';
            higgsStatus.style.color = 'var(--vs-accent-red)';
        }
    }

    updateServiceStatus(serviceInfo) {
        const serviceStatus = document.getElementById('serviceStatus');
        const startServiceBtn = document.getElementById('startService');
        const stopServiceBtn = document.getElementById('stopService');
        const serviceDetails = document.getElementById('serviceDetails');
        
        if (serviceInfo.running) {
            if (serviceInfo.ready) {
                serviceStatus.textContent = 'Ready';
                serviceStatus.style.color = 'var(--vs-accent-green)';
                serviceDetails.textContent = 'AI model loaded and ready for fast TTS generation';
                startServiceBtn.disabled = true;
                stopServiceBtn.disabled = false;
            } else {
                serviceStatus.textContent = 'Loading...';
                serviceStatus.style.color = 'var(--vs-accent-orange)';
                serviceDetails.textContent = 'Loading AI model into memory...';
                startServiceBtn.disabled = true;
                stopServiceBtn.disabled = false;
            }
        } else {
            serviceStatus.textContent = 'Stopped';
            serviceStatus.style.color = 'var(--vs-accent-red)';
            serviceDetails.textContent = 'Service not running. TTS will use fallback mode (slower)';
            startServiceBtn.disabled = false;
            stopServiceBtn.disabled = true;
        }
    }

    async startService() {
        try {
            const response = await fetch('/api/service/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                this.showToast('Service started successfully!', 'success');
                this.checkStatus(); // Refresh status
            } else {
                this.showToast(result.message || 'Failed to start service', 'error');
            }
        } catch (error) {
            console.error('Failed to start service:', error);
            this.showToast('Failed to start service', 'error');
        }
    }

    async stopService() {
        try {
            const response = await fetch('/api/service/stop', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                this.showToast('Service stopped successfully!', 'success');
                this.checkStatus(); // Refresh status
            } else {
                this.showToast(result.message || 'Failed to stop service', 'error');
            }
        } catch (error) {
            console.error('Failed to stop service:', error);
            this.showToast('Failed to stop service', 'error');
        }
    }

    showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        const toastMessage = toast.querySelector('.toast-message');
        const toastIcon = toast.querySelector('.toast-icon');
        
        // Set message and icon
        toastMessage.textContent = message;
        
        // Set icon based on type
        let iconClass = 'fas fa-info-circle';
        if (type === 'success') iconClass = 'fas fa-check-circle';
        if (type === 'error') iconClass = 'fas fa-exclamation-circle';
        if (type === 'warning') iconClass = 'fas fa-exclamation-triangle';
        
        toastIcon.className = iconClass;
        
        // Set toast type class
        toast.className = `toast ${type}`;
        
        // Show toast
        toast.classList.add('show');
        
        // Hide after 3 seconds
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    checkModalElements() {
        console.log('Checking modal elements...'); // Debug log
        const modal = document.getElementById('loadingModal');
        const title = document.getElementById('loadingTitle');
        const message = document.getElementById('loadingMessage');
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        const step1 = document.getElementById('step1');
        const step2 = document.getElementById('step2');
        const step3 = document.getElementById('step3');
        
        console.log('Modal elements found:', {
            modal: !!modal,
            title: !!title,
            message: !!message,
            progressFill: !!progressFill,
            progressText: !!progressText,
            step1: !!step1,
            step2: !!step2,
            step3: !!step3
        });
        
        if (modal) {
            console.log('Modal current display style:', modal.style.display);
            console.log('Modal computed display style:', window.getComputedStyle(modal).display);
        }
    }

    showLoadingModal(title, message) {
        console.log('showLoadingModal called with:', title, message); // Debug log
        const modal = document.getElementById('loadingModal');
        const titleEl = document.getElementById('loadingTitle');
        const messageEl = document.getElementById('loadingMessage');
        
        if (!modal) {
            console.error('Loading modal not found!'); // Debug log
            return;
        }
        
        titleEl.textContent = title;
        messageEl.textContent = message;
        
        // Reset progress
        document.getElementById('progressFill').style.width = '0%';
        document.getElementById('progressText').textContent = '0%';
        
        // Reset steps
        document.querySelectorAll('.step').forEach(step => step.classList.remove('active'));
        
        console.log('Setting modal display to block'); // Debug log
        // Show modal
        modal.style.display = 'block';
        
        // Start progress simulation
        this.startProgressSimulation();
    }

    hideLoadingModal() {
        const modal = document.getElementById('loadingModal');
        modal.style.display = 'none';
        
        // Clear progress interval if it exists
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
        }
    }

    startProgressSimulation() {
        let progress = 0;
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90; // Don't go to 100% until complete
            
            progressFill.style.width = progress + '%';
            progressText.textContent = Math.round(progress) + '%';
            
            // Update steps based on progress
            if (progress > 20) {
                document.getElementById('step1').classList.add('active');
            }
            if (progress > 50) {
                document.getElementById('step2').classList.add('active');
            }
            if (progress > 80) {
                document.getElementById('step3').classList.add('active');
            }
            
            if (progress >= 90) {
                clearInterval(interval);
            }
        }, 500);
        
        // Store interval ID to clear it when hiding modal
        this.progressInterval = interval;
    }
}

// Initialize the interface when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new ReadAloudInterface();
});

// Add some nice animations and interactions
document.addEventListener('DOMContentLoaded', () => {
    // Smooth scrolling for anchor links
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

    // Add loading states to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function() {
            if (!this.classList.contains('btn-disabled')) {
                this.classList.add('btn-loading');
                setTimeout(() => {
                    this.classList.remove('btn-loading');
                }, 1000);
            }
        });
    });

    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl+Enter to test TTS
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            document.getElementById('testTTS').click();
        }
        
        // Ctrl+S to save config
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            document.getElementById('saveConfig').click();
        }
        
        // Escape to stop audio
        if (e.key === 'Escape') {
            document.getElementById('stopAudio').click();
        }
    });
});

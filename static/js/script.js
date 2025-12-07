// 1. THEME TOGGLE
const toggleBtn = document.getElementById('theme-toggle');
const icon = toggleBtn.querySelector('i');
const body = document.body;

if(localStorage.getItem('theme') === 'light'){
    body.classList.add('light-mode');
    icon.classList.remove('fa-sun');
    icon.classList.add('fa-moon');
}

toggleBtn.addEventListener('click', () => {
    body.classList.toggle('light-mode');
    if(body.classList.contains('light-mode')){
        icon.classList.remove('fa-sun'); icon.classList.add('fa-moon'); localStorage.setItem('theme', 'light');
    } else {
        icon.classList.remove('fa-moon'); icon.classList.add('fa-sun'); localStorage.setItem('theme', 'dark');
    }
});

// 2. SCROLL ANIMATION
const observerOptions = { threshold: 0.1, rootMargin: "0px 0px -50px 0px" };
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) { entry.target.classList.add('active'); }
    });
}, observerOptions);
document.querySelectorAll('.reveal').forEach((el) => { observer.observe(el); });

// 3. TYPEWRITER EFFECT
const textElement = document.getElementById('typewriter-text');
const phrases = ['Data Scientist', 'Machine Learning Engineer', 'AI Enthusiast'];
let phraseIndex = 0;
let charIndex = 0;
let isDeleting = false;

function type() {
    const currentPhrase = phrases[phraseIndex];
    
    if (isDeleting) {
        textElement.textContent = currentPhrase.substring(0, charIndex - 1);
        charIndex--;
    } else {
        textElement.textContent = currentPhrase.substring(0, charIndex + 1);
        charIndex++;
    }

    let typeSpeed = isDeleting ? 50 : 100;

    if (!isDeleting && charIndex === currentPhrase.length) {
        typeSpeed = 2000;
        isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        phraseIndex = (phraseIndex + 1) % phrases.length;
        typeSpeed = 500;
    }
    setTimeout(type, typeSpeed);
}
document.addEventListener('DOMContentLoaded', type);

// 4. BACK TO TOP
const backToTopBtn = document.getElementById('backToTop');
window.onscroll = function() {
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
        backToTopBtn.classList.add('show');
    } else {
        backToTopBtn.classList.remove('show');
    }
};
function scrollToTop() { window.scrollTo({ top: 0, behavior: 'smooth' }); }

// =========================================
// 6. AI CHATBOT LOGIC
// =========================================
const chatBox = document.getElementById('chat-box');
const messagesDiv = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');

function toggleChat() {
    if (chatBox.style.display === 'none' || chatBox.style.display === '') {
        chatBox.style.display = 'flex';
    } else {
        chatBox.style.display = 'none';
    }
}

function handleEnter(e) {
    if (e.key === 'Enter') sendMessage();
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    // 1. Tampilkan Pesan User
    appendMessage(text, 'user');
    userInput.value = '';

    // 2. Tampilkan Loading...
    const loadingId = appendMessage('Sedang berpikir...', 'bot', true);

    try {
        // 3. Kirim ke Python (Flask)
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        const data = await response.json();

        // 4. Ganti Loading dengan Jawaban AI
        removeMessage(loadingId);
        appendMessage(data.reply, 'bot');

    } catch (error) {
        removeMessage(loadingId);
        appendMessage("Maaf, terjadi kesalahan koneksi.", 'bot');
    }
}

function appendMessage(text, sender, isLoading = false) {
    const div = document.createElement('div');
    div.id = isLoading ? 'loading-msg' : '';
    div.style.marginBottom = '10px';
    div.style.textAlign = sender === 'user' ? 'right' : 'left';
    
    const span = document.createElement('span');
    span.style.padding = '8px 12px';
    span.style.display = 'inline-block';
    span.style.maxWidth = '80%';
    
    if (sender === 'user') {
        span.style.background = 'var(--accent)';
        span.style.color = '#fff';
        span.style.borderRadius = '10px 10px 0 10px';
    } else {
        span.style.background = 'var(--border)';
        span.style.color = 'var(--text-primary)';
        span.style.borderRadius = '10px 10px 10px 0';
    }
    
    // Render Markdown simpel (Bold) jadi HTML
    // Gemini suka pakai **bold**, kita ubah jadi <b>
    span.innerHTML = text.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');

    div.appendChild(span);
    messagesDiv.appendChild(div);
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // Auto scroll ke bawah
    return div.id;
}

function removeMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}
// =========================================
// 7. AUTO GREETING AI (SAPAAN OTOMATIS)
// =========================================
document.addEventListener("DOMContentLoaded", () => {
    // Tunggu 2.5 detik setelah website dimuat
    setTimeout(() => {
        const bubble = document.getElementById('chat-bubble');
        
        if (bubble && chatBox.style.display !== 'flex') {
            // Ubah teks bubble
            bubble.innerHTML = "Hai, Aku AI Agent milik Ian! 👋";
            
            // Tambahkan animasi muncul (pop up)
            bubble.style.animation = "popUpBubble 0.5s ease-out forwards";
            
            // Tampilkan bubble (jika sebelumnya tersembunyi di CSS)
            bubble.style.display = "block";

            // OPTIONAL: Hilangkan sapaan setelah 8 detik biar tidak mengganggu
            setTimeout(() => {
                 // Hanya hilangkan jika chat belum dibuka user
                 if (chatBox.style.display !== 'flex') {
                    bubble.style.opacity = '0'; // Fade out pelan2 (perlu transisi CSS)
                    setTimeout(() => { bubble.style.display = 'none'; }, 500);
                 }
            }, 8000);
        }
    }, 2500); // Waktu tunggu sebelum menyapa (2500ms = 2.5 detik)
});
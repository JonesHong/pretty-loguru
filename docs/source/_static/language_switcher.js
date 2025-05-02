document.addEventListener('DOMContentLoaded', function() {
    // 語言切換器 JavaScript
    function setupLanguageSwitcher() {
        // 獲取當前URL路徑
        const path = window.location.pathname;
        
        // 檢查當前是哪種語言
        const isEnglish = path.includes('/en/');
        
        // 獲取語言切換器中的連結
        const links = document.querySelectorAll('.language-switcher a');
        
        if (links.length > 0) {
            links.forEach(function(link) {
                if (link.textContent.trim() === 'English' && !isEnglish) {
                    // 修改英文連結
                    const basePath = path.replace('/zh_TW/', '/');
                    link.href = basePath.replace('/html/', '/html/en/');
                } else if (link.textContent.trim() === '繁體中文' && isEnglish) {
                    // 修改中文連結
                    const basePath = path.replace('/en/', '/');
                    link.href = basePath.replace('/html/', '/html/zh_TW/');
                }
            });
        }
    }
    
    // 執行語言切換器設置
    setupLanguageSwitcher();
});

// 語言切換器腳本
document.addEventListener('DOMContentLoaded', function() {
    // 創建語言切換器元素
    var switcher = document.createElement('div');
    switcher.className = 'language-switcher';
    switcher.style.cssText = 'text-align: right; padding: 10px 0; margin-bottom: 20px; border-bottom: 1px solid #e1e4e5;';
    
    // 獲取當前路徑
    var path = window.location.pathname;
    var inEnglishVersion = path.includes('/en/');
    
    // 創建語言切換器內容
    if (inEnglishVersion) {
        var chinesePath = path.replace('/en/', '/');
        switcher.innerHTML = '<a href="' + chinesePath + '">繁體中文</a> | English';
    } else {
        var englishPath = path.replace('/html/', '/html/en/');
        if (path.endsWith('/html/')) {
            englishPath = path + 'en/';
        }
        switcher.innerHTML = '繁體中文 | <a href="' + englishPath + '">English</a>';
    }
    
    // 將切換器添加到頁面
    var headerElem = document.querySelector('.wy-nav-content-wrap');
    if (headerElem) {
        headerElem.insertBefore(switcher, headerElem.firstChild);
    }
});

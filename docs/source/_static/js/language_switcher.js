document.addEventListener('DOMContentLoaded', () => {
    const links = document.querySelectorAll('.language-switcher a');
    // 從 URL path 擷取目前的語系（en 或 zh_TW）
    const current = window.location.pathname.match(/\/(en|zh_TW)\//)?.[1] || null;
  
    links.forEach(link => {
      const text = link.textContent.trim();
      // 目標語系
      const target = text === 'English' ? 'en' : 'zh_TW';
      let newPath;
      if (current) {
        // 只替換那段 /en/ 或 /zh_TW/
        newPath = window.location.pathname.replace(`/${current}/`, `/${target}/`);
      } else {
        // 如果在根目錄，直接帶到子目錄的 index.html
        newPath = `/${target}/index.html`;
      }
      link.setAttribute('href', newPath);
    });
  });
  
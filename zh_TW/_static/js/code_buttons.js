// document.addEventListener('DOMContentLoaded', () => {
//     document.querySelectorAll('div.highlight').forEach(block => {
//       // 建立 Edit 按鈕
//       const editBtn = document.createElement('button');
//       editBtn.className = 'edit-btn';
//       editBtn.innerText = 'Edit';
  
//       // 這裡示範用當前頁面的路徑去推算 RST 原檔位置，可依實際 Repo 結構調整
//       editBtn.addEventListener('click', () => {
//         // 假設你的 RST 檔對應到 GitHub 上 docs/source/<pagename>.rst
//         const path = window.location.pathname.replace(/\/$/, '/index');
//         const rstPath = path + '.rst';
//         const githubUrl = 'https://github.com/JonesHong/pretty-loguru/edit/master/docs/source' + rstPath;
//         window.open(githubUrl, '_blank');
//       });
  
//       // 插入到 code-block 右上
//       block.style.position = 'relative';
//       block.appendChild(editBtn);
//     });
//   });
  
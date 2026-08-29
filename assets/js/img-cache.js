/**
 * Image Cache - 浏览器内存级图片缓存
 * 
 * 参考 FBC 的 pdfCache 实现，在同一个 session 内跨页面导航时
 * 不再重复下载已加载过的图片，实现秒开体验。
 * 
 * 使用方式：
 *   1. 在 HTML 中引入此脚本（放在 </body> 前）
 *   2. 正常写 <img src="..."> 标签即可，缓存自动工作
 *   3. 或者手动预加载：ImgCache.preload(['url1', 'url2'])
 */

(function() {
    'use strict';

    // ──────────────────────────────────────────────────────
    // 配置
    // ──────────────────────────────────────────────────────
    const CONFIG = {
        // sessionStorage key 前缀
        storageKeyPrefix: 'lt_img_',
        // 最大缓存图片数量（超过后清理最久未使用的）
        maxSize: 50,
        // 单张图片最大尺寸（MB），超出则不缓存
        maxFileSizeMB: 2,
        // 是否启用（生产环境可设为 false 用于调试）
        enabled: true
    };

    // ──────────────────────────────────────────────────────
    // 核心数据结构
    // ──────────────────────────────────────────────────────

    /**
     * 内存缓存 Map
     * key: 图片 URL（已规范化）
     * value: { blob, url, lastAccess }
     */
    const cache = new Map();

    /**
     * 正在加载中的请求队列
     * key: 图片 URL
     * value: Promise | null
     */
    const pendingRequests = new Map();

    // ──────────────────────────────────────────────────────
    // 工具函数
    // ──────────────────────────────────────────────────────

    /**
     * 规范化图片 URL
     * - 去掉 query string 和 hash
     * - 统一大小写（部分服务器对大小写敏感）
     */
    function normalizeUrl(url) {
        try {
            const u = new URL(url, location.href);
            return u.origin + u.pathname;
        } catch {
            return url;
        }
    }

    /**
     * 获取存储 key
     */
    function storageKey(normalizedUrl) {
        // 用 base64 编码避免特殊字符问题
        const safeKey = btoa(normalizedUrl).replace(/=/g, '').substring(0, 30);
        return CONFIG.storageKeyPrefix + safeKey;
    }

    // ──────────────────────────────────────────────────────
    // 核心 API
    // ──────────────────────────────────────────────────────

    /**
     * 获取图片数据（优先从内存缓存，其次从 sessionStorage，最后网络请求）
     * @param {string} url - 图片 URL
     * @returns {Promise<string>} - data URL（含 MIME 类型前缀）
     */
    async function getImage(url) {
        if (!CONFIG.enabled) {
            return new Promise((resolve) => {
                resolve(url);
            });
        }

        const normalized = normalizeUrl(url);

        // 1. 先查内存缓存
        if (cache.has(normalized)) {
            const entry = cache.get(normalized);
            entry.lastAccess = Date.now();
            return entry.dataUrl;
        }

        // 2. 查正在加载中的请求
        if (pendingRequests.has(normalized)) {
            return pendingRequests.get(normalized);
        }

        // 3. 查 sessionStorage
        try {
            const key = storageKey(normalized);
            const stored = sessionStorage.getItem(key);
            if (stored) {
                const parsed = JSON.parse(stored);
                const dataUrl = parsed.dataUrl;
                const size = parsed.size;

                // 验证大小
                const bytes = atob(dataUrl.split(',')[1]).length;
                if (bytes > CONFIG.maxFileSizeMB * 1024 * 1024) {
                    sessionStorage.removeItem(key);
                    throw new Error('图片过大');
                }

                // 放入内存缓存
                cache.set(normalized, {
                    dataUrl,
                    lastAccess: Date.now()
                });

                return dataUrl;
            }
        } catch (e) {
            console.warn('[ImgCache] sessionStorage 读取失败:', e);
        }

        // 4. 发起网络请求
        const promise = fetchImage(normalized).then((dataUrl) => {
            // 存入内存缓存
            const bytes = atob(dataUrl.split(',')[1]).length;
            cache.set(normalized, {
                dataUrl,
                size: bytes,
                lastAccess: Date.now()
            });

            // 存入 sessionStorage（如果不太大）
            if (bytes <= CONFIG.maxFileSizeMB * 1024 * 1024) {
                try {
                    sessionStorage.setItem(
                        storageKey(normalized),
                        JSON.stringify({ dataUrl, size: bytes })
                    );
                } catch (e) {
                    // sessionStorage 满或不可用，忽略
                    console.debug('[ImgCache] sessionStorage 写入失败:', e);
                }
            }

            // 维护缓存大小
            evictCache();

            return dataUrl;
        }).finally(() => {
            pendingRequests.delete(normalized);
        });

        pendingRequests.set(normalized, promise);
        return promise;
    }

    /**
     * 从网络获取图片并转为 data URL
     */
    async function fetchImage(url) {
        const response = await fetch(url, {
            mode: 'cors',
            credentials: 'omit'
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${url}`);
        }

        const blob = await response.blob();
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        });
    }

    /**
     * 缓存淘汰：保留最近访问的 maxSize 个图片
     */
    function evictCache() {
        if (cache.size <= CONFIG.maxSize) return;

        // 按 lastAccess 排序，删除最老的
        const sorted = Array.from(cache.entries())
            .sort((a, b) => a[1].lastAccess - b[1].lastAccess);

        const toEvict = cache.size - CONFIG.maxSize;
        for (let i = 0; i < toEvict; i++) {
            const [url] = sorted[i];
            const key = storageKey(url);
            sessionStorage.removeItem(key);
            cache.delete(url);
        }
    }

    /**
     * 预加载一组图片
     * @param {string[]} urls - 图片 URL 数组
     */
    async function preload(urls) {
        if (!Array.isArray(urls) || urls.length === 0) return;
        await Promise.allSettled(urls.map(getImage));
    }

    /**
     * 清除所有缓存
     */
    function clear() {
        cache.clear();
        pendingRequests.clear();
        // 也清除 sessionStorage 中的图片
        Object.keys(sessionStorage).forEach((key) => {
            if (key.startsWith(CONFIG.storageKeyPrefix)) {
                sessionStorage.removeItem(key);
            }
        });
    }

    /**
     * 获取缓存统计信息
     */
    function stats() {
        return {
            memoryCount: cache.size,
            pendingCount: pendingRequests.size,
            storageCount: Object.keys(sessionStorage).filter(k => k.startsWith(CONFIG.storageKeyPrefix)).length
        };
    }

    // ──────────────────────────────────────────────────────
    // DOM 注入：自动缓存所有 <img> 标签
    // ──────────────────────────────────────────────────────

    /**
     * 处理单个 img 元素
     */
    function processImg(img) {
        const src = img.getAttribute('src');
        if (!src || src.startsWith('data:')) return;

        // 标记已处理
        if (img.dataset.imgCacheHandled) return;
        img.dataset.imgCacheHandled = 'true';

        // 替换 src 为 data URL
        getImage(src).then((dataUrl) => {
            if (img.src !== src) return; // 已经被其他机制处理过
            img.src = dataUrl;
        }).catch((err) => {
            // 失败时保持原样，不影响页面展示
            console.debug('[ImgCache] 图片加载失败，保持原 src:', err.message);
        });
    }

    /**
     * 扫描并处理页面上的所有 img 标签
     */
    function processAllImages() {
        if (!CONFIG.enabled) return;

        const imgs = document.querySelectorAll('img');
        imgs.forEach(processImg);
    }

    // ──────────────────────────────────────────────────────
    // MutationObserver：监听动态插入的图片
    // ──────────────────────────────────────────────────────

    function observeImages() {
        if (!CONFIG.enabled) return;

        const observer = new MutationObserver((mutations) => {
            let shouldProcess = false;
            for (const mutation of mutations) {
                for (const node of mutation.addedNodes) {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        if (node.tagName === 'IMG' || node.querySelector('img')) {
                            shouldProcess = true;
                            break;
                        }
                    }
                }
                if (shouldProcess) break;
            }

            if (shouldProcess) {
                processAllImages();
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // ──────────────────────────────────────────────────────
    // 初始化
    // ──────────────────────────────────────────────────────

    function init() {
        function start() {
            processAllImages();
            // 必须在 body 存在后再监听，否则 <head> 同步加载时 document.body 为 null
            observeImages();
        }
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', start);
        } else {
            start();
        }
    }

    // ──────────────────────────────────────────────────────
    // 暴露全局 API
    // ──────────────────────────────────────────────────────

    window.ImgCache = {
        get: getImage,
        preload,
        clear,
        stats,
        processImg,
        processAllImages,
        observeImages,
        init,
        CONFIG
    };

    // 自动初始化
    init();

})();

/* ===================== 站点增强：暗色模式 / 阅读进度条 / 文章目录 / 汉堡菜单 ===================== */
(function(){
  'use strict';
  function ready(fn){ if(document.readyState!=='loading') fn(); else document.addEventListener('DOMContentLoaded', fn); }

  /* 暗色模式 */
  function initTheme(){
    var root=document.documentElement;
    var saved=localStorage.getItem('lt-theme');
    if(saved==='dark') root.setAttribute('data-theme','dark');
    var nav=document.querySelector('.site-header .nav');
    if(!nav) return;
    var btn=document.querySelector('.theme-toggle');
    if(!btn){
      btn=document.createElement('button');
      btn.className='theme-toggle';
      btn.setAttribute('aria-label','切换深色模式');
      btn.innerHTML='<svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg><svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
      nav.parentNode.insertBefore(btn, nav);
    }
    btn.addEventListener('click',function(){
      var isDark=root.getAttribute('data-theme')==='dark';
      if(isDark){root.removeAttribute('data-theme');localStorage.setItem('lt-theme','light');}
      else{root.setAttribute('data-theme','dark');localStorage.setItem('lt-theme','dark');}
    });
  }

  /* 阅读进度条（仅长文） */
  function initProgress(){
    if(!document.querySelector('.article')) return;
    if(document.documentElement.scrollHeight < window.innerHeight*1.5) return;
    var bar=document.createElement('div');
    bar.className='read-progress';
    document.body.appendChild(bar);
    var ticking=false;
    function update(){
      var h=document.documentElement.scrollHeight-window.innerHeight;
      var y=window.scrollY||window.pageYOffset||0;
      var p=h>0?Math.min(100,Math.max(0,y/h*100)):0;
      bar.style.width=p+'%';
      ticking=false;
    }
    window.addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(update);}},{passive:true});
    update();
  }

  /* 文章目录高亮：复用模板自带的 .toc（如已有），不重复注入；仅做滚动高亮 */
  function initToc(){
    var main=document.querySelector('.article-main')||document.querySelector('.article');
    if(!main) return;
    var hs=main.querySelectorAll('h2');
    if(hs.length<2) return;

    // 模板已自带 TOC 时：复用并只挂滚动高亮；h2 没 id 的顺手补一个，便于跳转
    var aside=document.querySelector('.article-aside');
    var existingToc=aside && aside.querySelector('.toc');
    hs.forEach(function(h,i){ if(!h.id) h.id='sec-toc-'+i; });

    var links=(existingToc ? existingToc : null) && [].slice.call((existingToc).querySelectorAll('a'));
    if('IntersectionObserver' in window){
      var obs=new IntersectionObserver(function(entries){
        entries.forEach(function(en){
          if(en.isIntersecting){
            if(links) links.forEach(function(l){l.parentNode.classList.remove('active');});
            var sel='a[href="#'+en.target.id+'"]';
            if(existingToc){
              var cur=existingToc.querySelector(sel);
              if(cur) cur.parentNode.classList.add('active');
            }
          }
        });
      },{rootMargin:'-10% 0px -80% 0px'});
      hs.forEach(function(h){obs.observe(h);});
    }
  }

  /* 移动端汉堡菜单 */
  function initNavToggle(){
    var header=document.querySelector('.site-header .container');
    var nav=document.querySelector('.site-header .nav');
    if(!header||!nav) return;
    if(header.querySelector('.nav-toggle')) return;
    var btn=document.createElement('button');
    btn.className='nav-toggle';
    btn.setAttribute('aria-label','菜单');
    btn.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>';
    header.appendChild(btn);
    btn.addEventListener('click',function(e){e.stopPropagation();nav.classList.toggle('open');});
    nav.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){nav.classList.remove('open');});});
    document.addEventListener('click',function(e){if(!header.contains(e.target))nav.classList.remove('open');});
  }

  ready(function(){
    initTheme();
    initNavToggle();
    initProgress();
    initToc();
  });
})();

/* ===================== 站点增强：视觉气质升级 2026-08-29（B·有呼吸感） ===================== */
(function(){
  'use strict';
  function ready(fn){ if(document.readyState!=='loading') fn(); else document.addEventListener('DOMContentLoaded', fn); }
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 页面进场淡入标记（CSS 仅对 html.is-ready 触发，无 JS 不触发） */
  function initReady(){ document.documentElement.classList.add('is-ready'); }

  /* 头部离顶阴影 */
  function initHeaderScrolled(){
    var h=document.querySelector('.site-header'); if(!h) return;
    var ticking=false;
    function upd(){ h.classList.toggle('is-scrolled', (window.scrollY||window.pageYOffset||0) > 8); ticking=false; }
    window.addEventListener('scroll',function(){ if(!ticking){ ticking=true; requestAnimationFrame(upd); } },{passive:true});
    upd();
  }

  /* 滚动渐进揭示：内容默认可见，reduced-motion 或无 IO 时直接跳过，绝不隐藏内容 */
  function initReveal(){
    if(reduce || !('IntersectionObserver' in window)) return;
    var sel='.article-main > p, .article-main > h2, .article-main > h3, .article-main > ul, .article-main > ol, .article-main > blockquote, .article-main > .table-wrap, .card, .value-card, .bento-cell, .principle-card, .col-row, .tool-card, .section-head, .story, .feature-list li';
    var els=[].slice.call(document.querySelectorAll(sel));
    if(!els.length) return;
    els.forEach(function(el){ el.classList.add('reveal'); });
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if(en.isIntersecting){ en.target.classList.add('is-visible'); io.unobserve(en.target); }
      });
    },{rootMargin:'0px 0px -8% 0px', threshold:0.05});
    els.forEach(function(el){ io.observe(el); });
  }

  ready(function(){ initReady(); initHeaderScrolled(); initReveal(); });
})();

/* ===================== 站点增强：悬浮分类跳转条（跟随式浮标 + scrollspy 高亮） ===================== */
(function(){
  'use strict';
  function ready(fn){ if(document.readyState!=='loading') fn(); else document.addEventListener('DOMContentLoaded', fn); }
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function initJumpFab(){
    // 仅在存在三大分类区块的页面（articles.html）注入；其他页面不显示
    var defs=[
      {id:'cat-pingce',    label:'工具测评'},
      {id:'cat-jiaocheng', label:'使用教程'},
      {id:'cat-kepu',      label:'资讯科普'}
    ].map(function(s){ s.el=document.getElementById(s.id); return s; })
     .filter(function(s){ return s.el; });
    if(defs.length<2) return;

    var wrap=document.createElement('div');
    wrap.className='cat-jump';
    wrap.innerHTML=
      '<div class="cat-jump__panel" role="menu" aria-label="栏目快速跳转">'+
        '<div class="cat-jump__label">栏目跳转</div>'+
        defs.map(function(s){
          var cnt=''; var c=s.el.querySelector('.count');
          if(c) cnt=' <span class="cnt">'+c.textContent.replace(/\s/g,'')+'</span>';
          return '<div class="cat-jump__item" role="menuitem" data-target="'+s.id+'">'+s.label+cnt+'</div>';
        }).join('')+
      '</div>'+
      '<button class="cat-jump__btn" aria-label="栏目快速跳转" aria-expanded="false">'+
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>'+
      '</button>';
    document.body.appendChild(wrap);

    var btn=wrap.querySelector('.cat-jump__btn');
    var panel=wrap.querySelector('.cat-jump__panel');
    var items=[].slice.call(wrap.querySelectorAll('.cat-jump__item'));

    function open(v){
      wrap.classList.toggle('open', v);
      btn.setAttribute('aria-expanded', v?'true':'false');
    }
    btn.addEventListener('click',function(e){ e.stopPropagation(); open(!wrap.classList.contains('open')); });
    document.addEventListener('click',function(e){ if(!wrap.contains(e.target)) open(false); });

    items.forEach(function(it){
      it.addEventListener('click',function(){
        var t=document.getElementById(it.getAttribute('data-target'));
        if(t) t.scrollIntoView({behavior: reduce?'auto':'smooth', block:'start'});
        open(false);
      });
    });

    // scrollspy：高亮当前所在区块（展开面板时即显示你正在看哪一块）
    if('IntersectionObserver' in window){
      var spy=new IntersectionObserver(function(entries){
        entries.forEach(function(en){
          if(en.isIntersecting){
            var id=en.target.id;
            items.forEach(function(it){ it.classList.toggle('active', it.getAttribute('data-target')===id); });
          }
        });
      },{rootMargin:'-45% 0px -50% 0px', threshold:0});
      defs.forEach(function(s){ spy.observe(s.el); });
    }
  }

  ready(initJumpFab);
})();

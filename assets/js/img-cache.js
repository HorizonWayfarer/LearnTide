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
            const storageKey = storageKey(normalized);
            const stored = sessionStorage.getItem(storageKey);
            if (stored) {
                const parsed = JSON.parse(stored);
                const dataUrl = parsed.dataUrl;
                const size = parsed.size;

                // 验证大小
                const bytes = atob(dataUrl.split(',')[1]).length;
                if (bytes > CONFIG.maxFileSizeMB * 1024 * 1024) {
                    sessionStorage.removeItem(storageKey);
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
        // 页面加载完成后处理静态图片
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', processAllImages);
        } else {
            processAllImages();
        }

        // 开始监听动态插入的图片
        observeImages();
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

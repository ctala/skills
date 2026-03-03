/**
 * Sensitive Data Masker Hook
 * 
 * 在消息接收时自动脱敏敏感信息
 */

const { execSync } = require('child_process');
const path = require('path');

const MASKER_SCRIPT = path.join(__dirname, 'masker-wrapper.py');

/**
 * Hook handler
 * @param {Object} event - 事件对象
 */
async function handler(event) {
    // 只在消息接收时触发
    if (event.type !== 'message' || event.action !== 'received') {
        return;
    }

    try {
        const content = event.context.content || '';
        
        if (!content) {
            return;
        }

        // 调用 Python 脱敏脚本
        const escaped = content.replace(/"/g, '\\"').replace(/\n/g, '\\n');
        const result = execSync(
            `python3 "${MASKER_SCRIPT}" mask "${escaped}"`,
            { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'ignore'] }
        ).trim();

        // 如果脱敏后的内容不同，更新事件
        if (result) {
            const masked = JSON.parse(result);
            
            // 更新消息内容
            event.context.content = masked.masked;
            
            // 记录脱敏信息
            if (masked.count > 0) {
                console.log(`[sensitive-masker] 脱敏了 ${masked.count} 个敏感信息：${masked.types.join(', ')}`);
            }
        }
    } catch (error) {
        console.error('[sensitive-masker] 脱敏失败:', error.message);
        // 脱敏失败不影响消息处理，继续原始消息
    }
}

module.exports = handler;

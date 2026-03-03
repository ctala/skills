/**
 * Sensitive Data Masker Hook
 * 
 * Automatically mask sensitive data when messages are received
 */

const { execSync } = require('child_process');
const path = require('path');

const MASKER_SCRIPT = path.join(__dirname, 'masker-wrapper.py');

/**
 * Hook handler
 * @param {Object} event - Event object
 */
async function handler(event) {
    // Only trigger on message:received events
    if (event.type !== 'message' || event.action !== 'received') {
        return;
    }

    try {
        const content = event.context.content || '';
        
        if (!content) {
            return;
        }

        // Call Python masking script
        const escaped = content.replace(/"/g, '\\"').replace(/\n/g, '\\n');
        const result = execSync(
            `python3 "${MASKER_SCRIPT}" mask "${escaped}"`,
            { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'ignore'] }
        ).trim();

        // If masked content is different, update event
        if (result) {
            const masked = JSON.parse(result);
            
            // Update message content
            event.context.content = masked.masked;
            
            // Log masking information
            if (masked.count > 0) {
                console.log(`[sensitive-masker] Masked ${masked.count} sensitive items: ${masked.types.join(', ')}`);
            }
        }
    } catch (error) {
        console.error('[sensitive-masker] Masking failed:', error.message);
        // Masking failure doesn't affect message processing, continue with original message
    }
}

module.exports = handler;

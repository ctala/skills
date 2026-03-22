#!/bin/bash
# Generate English Daily Report PDF
# Usage: generate-pdf-html.sh "DATE" "ENGLISH_TITLE" "ENGLISH_CONTENT" "CHINESE_TRANSLATION" "WORD1:MEANING1" "WORD2:MEANING2" ...

cd ~/.openclaw/workspace

# Parse arguments
DATE="$1"
ENGLISH_TITLE="$2"
ENGLISH_CONTENT="$3"
CHINESE_TRANSLATION="$4"
shift 4
VOCAB_WORDS=("$@")

# Default values if not provided
DATE=${DATE:-$(date +%Y-%m-%d)}
PDF_FILE="/Users/fzzhao/.openclaw/workspace/uploads/english-daily-${DATE}.pdf"

# Build vocabulary HTML
VOCAB_HTML=""
for word in "${VOCAB_WORDS[@]}"; do
  WORD_NAME=$(echo "$word" | cut -d':' -f1)
  WORD_MEANING=$(echo "$word" | cut -d':' -f2-)
  VOCAB_HTML="${VOCAB_HTML}    <div class=\"vocab\"><span class=\"word\">${WORD_NAME}</span> - ${WORD_MEANING}</div>\n"
done

# Create HTML file with embedded CSS for print
cat > /Users/fzzhao/.openclaw/workspace/uploads/report-temp.html << HTMLEOF
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <style>
    @page { size: A4; margin: 2cm; }
    body { 
      font-family: "PingFang SC", "Microsoft YaHei", "SimSun", sans-serif; 
      max-width: 800px; 
      margin: 0 auto; 
      padding: 20px;
      line-height: 1.6;
    }
    .header { 
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
      color: white; 
      padding: 30px; 
      border-radius: 10px; 
      margin-bottom: 30px;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    .title { font-size: 28px; font-weight: bold; margin-bottom: 10px; }
    .date { font-size: 16px; opacity: 0.9; }
    .section { 
      margin: 25px 0; 
      padding: 20px; 
      background: #f8f9fa; 
      border-radius: 8px;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    .section-title { 
      font-size: 18px; 
      font-weight: bold; 
      color: #667eea; 
      margin-bottom: 15px; 
      border-bottom: 2px solid #667eea; 
      padding-bottom: 8px; 
    }
    .english { font-size: 16px; color: #333; white-space: pre-line; }
    .chinese { font-size: 16px; color: #555; margin-top: 15px; white-space: pre-line; }
    .vocab { 
      background: white; 
      padding: 15px; 
      border-radius: 5px; 
      margin: 10px 0;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    .word { font-weight: bold; color: #764ba2; }
    .footer { 
      text-align: center; 
      margin-top: 40px; 
      color: #999; 
      font-size: 12px; 
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="title">📰 English Daily Report</div>
    <div class="date">${DATE}</div>
  </div>

  <div class="section">
    <div class="section-title">📄 News Summary</div>
    <div class="english">
      <strong>${ENGLISH_TITLE}</strong><br><br>
${ENGLISH_CONTENT}
    </div>
  </div>

  <div class="section">
    <div class="section-title">📖 全文释义</div>
    <div class="chinese">
${CHINESE_TRANSLATION}
    </div>
  </div>

  <div class="section">
    <div class="section-title">📝 Vocabulary & Grammar</div>
$(echo -e "${VOCAB_HTML}")
  </div>

  <div class="footer">
    英语学习计划 · 每日推送 · Generated on ${DATE}
  </div>
</body>
</html>
HTMLEOF

echo "HTML created at /Users/fzzhao/.openclaw/workspace/uploads/report-temp.html"

# Convert to PDF with date in filename
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --print-to-pdf="${PDF_FILE}" /Users/fzzhao/.openclaw/workspace/uploads/report-temp.html 2>&1

echo "PDF created at ${PDF_FILE}"

# Audio file path (for reference, TTS will be called separately)
AUDIO_FILE="/Users/fzzhao/.openclaw/workspace/uploads/english-daily-${DATE}.mp3"
echo "Audio should be saved to: ${AUDIO_FILE}"

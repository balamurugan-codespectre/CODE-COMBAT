/**
 * CODE COMBAT Pro - Code Editor Enhancements
 * Line numbering, soft tabs, bracket auto-closing, font scaling, and fullscreen toggle.
 */

class CodeEditor {
  constructor(textareaId, lineNumbersId) {
    this.textarea = document.getElementById(textareaId);
    this.lineNumbers = document.getElementById(lineNumbersId);
    this.fontSize = 14;

    if (!this.textarea || !this.lineNumbers) return;

    this.initListeners();
    this.updateLineNumbers();
  }

  initListeners() {
    // 1. Line numbers syncing
    this.textarea.addEventListener('input', () => this.updateLineNumbers());
    this.textarea.addEventListener('scroll', () => {
      this.lineNumbers.scrollTop = this.textarea.scrollTop;
    });

    // 2. Keyboard shortcuts & Bracket Auto-closing
    this.textarea.addEventListener('keydown', (e) => this.handleKeyDown(e));
  }

  handleKeyDown(e) {
    const val = this.textarea.value;
    const start = this.textarea.selectionStart;
    const end = this.textarea.selectionEnd;

    // Tab key -> 4 spaces
    if (e.key === 'Tab') {
      e.preventDefault();
      const tabStr = '    ';
      this.textarea.value = val.substring(0, start) + tabStr + val.substring(end);
      this.textarea.selectionStart = this.textarea.selectionEnd = start + tabStr.length;
      this.updateLineNumbers();
      return;
    }

    // Bracket & Quote Auto-pairing
    const pairs = {
      '(': ')',
      '[': ']',
      '{': '}',
      '"': '"',
      "'": "'"
    };

    if (pairs[e.key]) {
      e.preventDefault();
      const openChar = e.key;
      const closeChar = pairs[e.key];
      const selectedText = val.substring(start, end);

      this.textarea.value = val.substring(0, start) + openChar + selectedText + closeChar + val.substring(end);
      this.textarea.selectionStart = start + 1;
      this.textarea.selectionEnd = end + 1;
      this.updateLineNumbers();
      return;
    }

    // Ctrl + Enter -> Run Sample Tests
    if (e.ctrlKey && e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (window.App) window.App.runCode();
      return;
    }

    // Ctrl + Shift + Enter -> Submit
    if (e.ctrlKey && e.shiftKey && e.key === 'Enter') {
      e.preventDefault();
      if (window.App) window.App.submitCode();
      return;
    }
  }

  updateLineNumbers() {
    const lines = this.textarea.value.split('\n');
    const lineCount = lines.length;
    let numsHtml = '';
    for (let i = 1; i <= lineCount; i++) {
      numsHtml += `<div>${i}</div>`;
    }
    this.lineNumbers.innerHTML = numsHtml;
  }

  setValue(val) {
    this.textarea.value = val || '';
    this.updateLineNumbers();
  }

  getValue() {
    return this.textarea.value;
  }

  changeFontSize(delta) {
    this.fontSize = Math.max(11, Math.min(24, this.fontSize + delta));
    this.textarea.style.fontSize = `${this.fontSize}px`;
    this.lineNumbers.style.fontSize = `${this.fontSize}px`;
    this.textarea.style.lineHeight = `${this.fontSize + 8}px`;
    this.lineNumbers.style.lineHeight = `${this.fontSize + 8}px`;
  }
}

window.CodeEditor = CodeEditor;

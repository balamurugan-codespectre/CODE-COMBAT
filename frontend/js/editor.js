/**
 * CODE COMBAT - Custom Offline Code Editor
 * Provides line numbering, auto-indentation, bracket completion, tab handling, and language template binding.
 */

class CodeEditor {
  constructor(textareaId, lineNumbersId, langSelectId) {
    this.textarea = document.getElementById(textareaId);
    this.lineNumbers = document.getElementById(lineNumbersId);
    this.langSelect = document.getElementById(langSelectId);

    this.currentLanguage = "python";
    this.currentProblem = null;
    this.codeCache = {}; // Key: `${problemId}_${language}` -> code string

    this.initEvents();
  }

  initEvents() {
    if (!this.textarea) return;

    // 1. Sync line numbers on typing & scrolling
    this.textarea.addEventListener("input", () => this.updateLineNumbers());
    this.textarea.addEventListener("scroll", () => {
      if (this.lineNumbers) {
        this.lineNumbers.scrollTop = this.textarea.scrollTop;
      }
    });

    // 2. Keyboard shortcuts & smart indentation
    this.textarea.addEventListener("keydown", (e) => this.handleKeyDown(e));

    // 3. Language Selector changed
    if (this.langSelect) {
      this.langSelect.addEventListener("change", (e) => {
        this.setLanguage(e.target.value);
      });
    }

    this.updateLineNumbers();
  }

  updateLineNumbers() {
    if (!this.lineNumbers || !this.textarea) return;
    const lines = this.textarea.value.split("\n").length;
    let numbers = "";
    for (let i = 1; i <= lines; i++) {
      numbers += i + "\n";
    }
    this.lineNumbers.innerText = numbers;
  }

  handleKeyDown(e) {
    const val = this.textarea.value;
    const start = this.textarea.selectionStart;
    const end = this.textarea.selectionEnd;

    // TAB Key -> Insert 4 spaces or indent block
    if (e.key === "Tab") {
      e.preventDefault();
      if (e.shiftKey) {
        // Shift + Tab: Dedent
        const before = val.substring(0, start);
        const lineStart = before.lastIndexOf("\n") + 1;
        const line = val.substring(lineStart, end);
        if (line.startsWith("    ")) {
          this.textarea.value = val.substring(0, lineStart) + val.substring(lineStart + 4);
          this.textarea.selectionStart = this.textarea.selectionEnd = Math.max(lineStart, start - 4);
        }
      } else {
        // Tab: Insert 4 spaces
        this.textarea.value = val.substring(0, start) + "    " + val.substring(end);
        this.textarea.selectionStart = this.textarea.selectionEnd = start + 4;
      }
      this.updateLineNumbers();
      this.saveDraft();
      return;
    }

    // ENTER Key -> Match indentation
    if (e.key === "Enter") {
      const lineStart = val.lastIndexOf("\n", start - 1) + 1;
      const currentLine = val.substring(lineStart, start);
      const match = currentLine.match(/^(\s+)/);
      let indent = match ? match[1] : "";

      // Add extra indent if previous line ends with : or {
      if (currentLine.trim().endsWith(":") || currentLine.trim().endsWith("{")) {
        indent += "    ";
      }

      if (indent.length > 0) {
        e.preventDefault();
        const insertText = "\n" + indent;
        this.textarea.value = val.substring(0, start) + insertText + val.substring(end);
        this.textarea.selectionStart = this.textarea.selectionEnd = start + insertText.length;
        this.updateLineNumbers();
        this.saveDraft();
        return;
      }
    }

    // Bracket & Quote Auto-closing
    const pairs = {
      "(": ")",
      "[": "]",
      "{": "}",
      '"': '"',
      "'": "'"
    };

    if (pairs[e.key] && start === end) {
      const char = e.key;
      const closeChar = pairs[char];
      e.preventDefault();
      this.textarea.value = val.substring(0, start) + char + closeChar + val.substring(end);
      this.textarea.selectionStart = this.textarea.selectionEnd = start + 1;
      this.updateLineNumbers();
      this.saveDraft();
      return;
    }

    // Trigger save draft on regular typing
    setTimeout(() => this.saveDraft(), 0);
  }

  loadProblem(problem, defaultLang = "python") {
    this.currentProblem = problem;
    this.currentLanguage = defaultLang;

    if (this.langSelect) {
      this.langSelect.value = defaultLang;
    }

    this.loadCodeForCurrentLanguage();
  }

  setLanguage(lang) {
    if (this.currentLanguage === lang) return;
    // Save draft for previous lang
    this.saveDraft();
    this.currentLanguage = lang;
    this.loadCodeForCurrentLanguage();
  }

  loadCodeForCurrentLanguage() {
    if (!this.currentProblem) return;

    const key = `${this.currentProblem.id}_${this.currentLanguage}`;
    const cached = localStorage.getItem(`codecombat_code_${key}`) || this.codeCache[key];

    if (cached) {
      this.textarea.value = cached;
    } else {
      const starter = this.currentProblem.starter_code?.[this.currentLanguage] || "// Write your code here";
      this.textarea.value = starter;
    }

    this.updateLineNumbers();
  }

  resetCurrentCode() {
    if (!this.currentProblem) return;
    const starter = this.currentProblem.starter_code?.[this.currentLanguage] || "";
    this.textarea.value = starter;
    this.updateLineNumbers();
    this.saveDraft();
  }

  saveDraft() {
    if (!this.currentProblem || !this.textarea) return;
    const key = `${this.currentProblem.id}_${this.currentLanguage}`;
    const code = this.textarea.value;
    this.codeCache[key] = code;
    try {
      localStorage.setItem(`codecombat_code_${key}`, code);
    } catch (e) {}
  }

  getCode() {
    return this.textarea ? this.textarea.value : "";
  }

  getLanguage() {
    return this.currentLanguage;
  }
}

from PyQt5.QtWidgets import QTextEdit

class TreeWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setStyleSheet("background-color: #1e1e2e; color: #50fa7b; font-family: Consolas, monospace; font-size: 13px; border: 1px solid #44475a;")
        self.depth = 0

    def add_node(self, var, value, is_fail=False, is_success=False):
        if is_success:
            indent = "    " * self.depth
            self.append(f"{indent}|\n{indent}SUCCESS 🎯")
            return
        indent = "    " * (self.depth - 1) if self.depth > 0 else ""
        branch = "+-- " if self.depth > 0 else ""
        prefix = f"{indent}|\n{indent}{branch}" if self.depth > 0 else ""
        status = " (Fail)" if is_fail else ""
        self.append(f"{prefix}{var}={value}{status}")

    def add_generic_log(self, text):
        self.append(text)

    def increase_depth(self):
        self.depth += 1

    def decrease_depth(self):
        self.depth = max(0, self.depth - 1)

    def clear_tree(self):
        self.clear()
        self.depth = 0
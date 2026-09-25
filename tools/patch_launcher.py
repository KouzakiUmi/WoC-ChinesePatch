# -*- coding: utf-8 -*-
"""Small Windows GUI wrapper for the standalone patch installer."""
import contextlib
import logging
import os
import platform
import queue
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

import patch_tool


APP_NAME = "Winds of Change 简体中文补丁"


def _log_path():
    base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    folder = os.path.join(base, "WoCChinesePatch", "logs")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "installer.log")


class _QueueWriter:
    def __init__(self, target):
        self.target = target

    def write(self, value):
        if value:
            self.target.put(value)
        return len(value)

    def flush(self):
        pass


class InstallerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("800x660")
        self.minsize(720, 600)
        self.events = queue.Queue()
        self.busy = False
        self.log_file = _log_path()
        logging.basicConfig(
            filename=self.log_file,
            filemode="a",
            encoding="utf-8",
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s %(message)s",
        )
        self.game_dir = tk.StringVar()
        self.status = tk.StringVar(value="就绪：选择游戏目录，或直接开始自动查找。")
        self._build_ui()
        self._append_log("WoC patch GUI started; Python %s; frozen=%s" % (
            platform.python_version(), bool(getattr(sys, "frozen", False))))
        self._append_log("Debug log: " + self.log_file)
        logging.debug("Platform: %s", platform.platform())
        logging.debug("Executable: %s", sys.executable)
        logging.debug("Resource root: %s", patch_tool.ROOT)
        self.after(100, self._drain_events)

    def _build_ui(self):
        style = ttk.Style(self)
        try:
            style.theme_use("vista")
        except tk.TclError:
            pass

        outer = ttk.Frame(self, padding=14)
        outer.pack(fill="both", expand=True)
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(6, weight=1)
        ttk.Label(outer, text=APP_NAME, font=("Microsoft YaHei UI", 16, "bold")).grid(
            row=0, column=0, sticky="w")
        ttk.Label(
            outer,
            text="一体化安装器，无需另外安装 Python。安装前会核对游戏版本并备份将被覆盖的文件。",
            wraplength=720,
        ).grid(row=1, column=0, sticky="w", pady=(4, 12))

        path_frame = ttk.LabelFrame(outer, text="游戏目录（可留空以自动查找 Steam 安装）", padding=8)
        path_frame.grid(row=2, column=0, sticky="ew")
        path_frame.columnconfigure(0, weight=1)
        ttk.Entry(path_frame, textvariable=self.game_dir).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ttk.Button(path_frame, text="浏览…", command=self._browse).grid(row=0, column=1)

        actions = ttk.Frame(outer)
        actions.grid(row=3, column=0, sticky="ew", pady=10)
        self.action_buttons = []
        for label, command in (
            ("安装中文补丁", lambda: self._run("install")),
            ("卸载并还原", self._confirm_uninstall),
            ("检查补丁", lambda: self._run("check")),
            ("验证已安装文件", lambda: self._run("verify")),
        ):
            button = ttk.Button(actions, text=label, command=command)
            button.pack(side="left", padx=(0, 8))
            self.action_buttons.append(button)

        ttk.Label(outer, textvariable=self.status).grid(row=4, column=0, sticky="w", pady=(0, 5))
        self.progress = ttk.Progressbar(outer, mode="indeterminate")
        self.progress.grid(row=5, column=0, sticky="ew", pady=(0, 8))
        log_frame = ttk.LabelFrame(outer, text="运行记录", padding=5)
        log_frame.grid(row=6, column=0, sticky="nsew")
        self.log_view = scrolledtext.ScrolledText(
            log_frame, height=8, state="disabled", wrap="word",
            font=("Microsoft YaHei UI", 9),
        )
        self.log_view.pack(fill="both", expand=True)
        footer = ttk.Frame(outer)
        footer.grid(row=7, column=0, sticky="ew", pady=(8, 0))
        ttk.Label(footer, text="遇到问题，请将 installer.log 发给补丁维护者。", wraplength=420).pack(side="left")
        ttk.Button(footer, text="打开调试日志", command=self._open_log).pack(side="right")

    def _append_log(self, text):
        self.log_view.configure(state="normal")
        self.log_view.insert("end", text)
        if not text.endswith("\n"):
            self.log_view.insert("end", "\n")
        self.log_view.see("end")
        self.log_view.configure(state="disabled")

    def _drain_events(self):
        try:
            while True:
                value = self.events.get_nowait()
                if isinstance(value, tuple) and value and value[0] == "__DONE__":
                    self._finish(value[1], value[2])
                else:
                    self._append_log(value)
                    logging.debug(value.rstrip())
        except queue.Empty:
            pass
        self.after(100, self._drain_events)

    def _browse(self):
        selected = filedialog.askdirectory(title="选择 Winds of Change 游戏目录")
        if selected:
            self.game_dir.set(os.path.abspath(selected))

    def _open_log(self):
        try:
            os.startfile(self.log_file)
        except Exception as exc:
            messagebox.showerror("无法打开日志", "%s\n\n日志路径：%s" % (exc, self.log_file))

    def _confirm_uninstall(self):
        if messagebox.askyesno("确认卸载", "将尝试还原安装前备份的游戏文件并删除补丁新增文件。继续吗？"):
            self._run("uninstall")

    def _run(self, command):
        if self.busy:
            return
        game_dir = self.game_dir.get().strip()
        argv = [command]
        if game_dir:
            argv.extend(["--game-dir", game_dir])
        self.busy = True
        self.status.set("正在执行：" + command + " …")
        self.progress.start(12)
        for button in self.action_buttons:
            button.state(["disabled"])
        self._append_log("\n=== %s ===" % command)
        logging.info("Starting command=%s game_dir=%r", command, game_dir)
        threading.Thread(target=self._worker, args=(argv,), daemon=True).start()

    def _worker(self, argv):
        result = 1
        old_argv = sys.argv
        try:
            sys.argv = [sys.argv[0]] + argv
            writer = _QueueWriter(self.events)
            with contextlib.redirect_stdout(writer), contextlib.redirect_stderr(writer):
                try:
                    patch_tool.main()
                except SystemExit as exc:
                    if isinstance(exc.code, int):
                        result = exc.code
                    elif exc.code:
                        print(str(exc.code))
                        result = 1
                    else:
                        result = 0
        except Exception:
            logging.exception("Unhandled installer error")
            self.events.put("未处理错误：\n" + __import__("traceback").format_exc())
            result = 1
        finally:
            sys.argv = old_argv
            self.events.put(("__DONE__", result, argv[0]))

    def _finish(self, result, command):
        self.busy = False
        self.progress.stop()
        for button in self.action_buttons:
            button.state(["!disabled"])
        if result == 0:
            message = {"install": "安装完成。现在可以启动游戏。", "uninstall": "卸载完成，已按可用备份还原。",
                       "check": "检查完成。", "verify": "文件验证完成。"}.get(command, "操作完成。")
            self.status.set(message)
            logging.info("Command completed successfully: %s", command)
            messagebox.showinfo("完成", message)
        else:
            self.status.set("操作未完成，请查看运行记录和调试日志。")
            logging.error("Command failed: %s (exit=%s)", command, result)
            messagebox.showerror("操作失败", "操作未能完成。请查看窗口中的运行记录，或点“打开调试日志”获取详细信息。")


def main():
    app = InstallerApp()
    app.mainloop()


if __name__ == "__main__":
    main()

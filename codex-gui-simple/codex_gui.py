#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Codex CLI 汉化工具
功能：检测、汉化 Codex CLI
"""

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import webbrowser
import subprocess
import os
import sys
import threading
import re
from pathlib import Path

class CodexCLIGUI:
    def __init__(self):
        # 设置CustomTkinter暗黑模式
        ctk.set_appearance_mode("dark")  # 暗黑模式
        ctk.set_default_color_theme("blue")  # 蓝色主题
        
        self.root = ctk.CTk()
        self.root.title("🚀 Codex CLI 汉化工具 1.0")
        self.root.geometry("850x580")
        self.root.resizable(True, True)
        self.root.minsize(800, 550)

        # 设置图标（如果存在）
        try:
            icon_path = Path(__file__).parent / "app_icon.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except:
            pass
        
        # 应用状态
        self.codex_status = {
            'installed': False,
            'version': '',
            'latest_version': '',
            'checked': False
        }
        
        self.npm_status = {
            'installed': False,
            'version': ''
        }
        
        # 支持的版本
        self.supported_versions = ["0.40.0"]
        self.max_supported_version = "0.40.0"
        
        # 初始化状态变量
        self.status_var = tk.StringVar(value="就绪")
        self.selected_version = tk.StringVar(value=self.max_supported_version)
        
        # 创建界面
        self.create_widgets()
        
        # 启动时检测
        self.root.after(1000, self.detect_installation)
    
    def create_widgets(self):
        """创建主界面组件"""
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # 标题区域
        title_frame = ctk.CTkFrame(self.root)
        title_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        title_frame.columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(title_frame, 
                                  text="🚀 Codex CLI 汉化工具", 
                                  font=ctk.CTkFont(family="微软雅黑", size=20, weight="bold"),
                                  text_color="#00D4FF")
        title_label.grid(row=0, column=0, pady=(12, 5))
        
        subtitle_label = ctk.CTkLabel(title_frame,
                                     text="一键汉化 OpenAI Codex CLI 界面",
                                     font=ctk.CTkFont(family="微软雅黑", size=12),
                                     text_color="#CCCCCC")
        subtitle_label.grid(row=1, column=0, pady=(0, 12))
        
        # 创建标签页
        notebook = ctk.CTkTabview(self.root)
        notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 5))
        
        # 添加标签页
        notebook.add("🏠 主要功能")
        notebook.add("ℹ️ 关于")
        
        # 创建标签页内容
        self.create_main_tab(notebook.tab("🏠 主要功能"))
        self.create_about_tab(notebook.tab("ℹ️ 关于"))
        
        # 状态栏
        status_bar = ctk.CTkLabel(self.root, textvariable=self.status_var,
                                 font=ctk.CTkFont(family="微软雅黑", size=11),
                                 text_color="#CCCCCC")
        status_bar.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 8))
        
    def create_main_tab(self, main_tab):
        """创建主要功能标签页"""
        main_tab.columnconfigure(0, weight=1)
        
        # 使用网格布局，将所有内容紧凑排列
        row = 0
        
        # Codex CLI 状态区域
        status_card = ctk.CTkFrame(main_tab)
        status_card.grid(row=row, column=0, sticky="ew", padx=10, pady=(8, 5))
        status_card.columnconfigure(1, weight=1)
        row += 1
        
        status_title = ctk.CTkLabel(status_card, text="📦 Codex CLI 状态",
                                   font=ctk.CTkFont(family="微软雅黑", size=14, weight="bold"),
                                   text_color="#00D4FF")
        status_title.grid(row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(10, 6))
        
        # 按钮容器
        button_container = ctk.CTkFrame(status_card, fg_color="transparent")
        button_container.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))
        
        detect_btn = ctk.CTkButton(button_container, text="🔍 检测安装", 
                                  command=self.detect_installation,
                                  font=ctk.CTkFont(family="微软雅黑", size=11, weight="bold"),
                                  width=90, height=30)
        detect_btn.grid(row=0, column=0, padx=(0, 8))
        
        self.check_update_btn = ctk.CTkButton(button_container, text="🔄 检测新版", 
                                             command=self.check_for_updates,
                                             font=ctk.CTkFont(family="微软雅黑", size=11, weight="bold"),
                                             width=90, height=30,
                                             state="disabled")
        self.check_update_btn.grid(row=0, column=1)
        
        # 状态显示区域
        self.status_frame = ctk.CTkFrame(status_card, fg_color="transparent")
        self.status_frame.grid(row=1, column=1, sticky="ew", padx=(8, 12), pady=(0, 8))
        self.status_frame.columnconfigure(0, weight=1)
        
        # 版本管理和汉化操作区域
        combined_frame = ctk.CTkFrame(main_tab, fg_color="transparent")
        combined_frame.grid(row=row, column=0, sticky="ew", padx=10, pady=(0, 5))
        combined_frame.columnconfigure(0, weight=1)
        combined_frame.columnconfigure(1, weight=1)
        row += 1
        
        # 版本管理区域
        version_card = ctk.CTkFrame(combined_frame)
        version_card.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        version_title = ctk.CTkLabel(version_card, text="🔢 版本管理",
                                    font=ctk.CTkFont(family="微软雅黑", size=14, weight="bold"),
                                    text_color="#00D4FF")
        version_title.grid(row=0, column=0, sticky="w", padx=12, pady=(8, 5))
        
        # 版本选择
        version_label = ctk.CTkLabel(version_card, text="支持版本:",
                                    font=ctk.CTkFont(family="微软雅黑", size=11, weight="bold"),
                                    text_color="#FFFFFF")
        version_label.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 3))
        
        # 当前版本显示（只读）
        self.version_label = ctk.CTkLabel(version_card, 
                                         text="0.40.0",
                                         font=ctk.CTkFont(family="微软雅黑", size=11, weight="bold"),
                                         text_color="#00D4FF",
                                         fg_color="#2B2B2B",
                                         corner_radius=6,
                                         width=130, height=26)
        self.version_label.grid(row=2, column=0, sticky="w", padx=12, pady=(0, 5))
        
        # 版本信息显示区域
        self.version_info_frame = ctk.CTkFrame(version_card, fg_color="transparent")
        self.version_info_frame.grid(row=3, column=0, sticky="ew", padx=12, pady=(5, 8))
        self.version_info_frame.columnconfigure(0, weight=1)
        
        # 汉化操作区域
        action_card = ctk.CTkFrame(combined_frame)
        action_card.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        action_title = ctk.CTkLabel(action_card, text="🌐 汉化操作",
                                   font=ctk.CTkFont(family="微软雅黑", size=14, weight="bold"),
                                   text_color="#00D4FF")
        action_title.grid(row=0, column=0, sticky="w", padx=12, pady=(8, 5))
        
        # 按钮组
        self.translate_btn = ctk.CTkButton(action_card, text="✨ 一键汉化", 
                                          command=self.start_translation,
                                          font=ctk.CTkFont(family="微软雅黑", size=12, weight="bold"),
                                          width=140, height=32,
                                          fg_color="#1DB954", hover_color="#1ED760")
        self.translate_btn.grid(row=1, column=0, padx=12, pady=(0, 5))
        
        self.restore_btn = ctk.CTkButton(action_card, text="🔄 恢复原版", 
                                        command=self.restore_original,
                                        font=ctk.CTkFont(family="微软雅黑", size=12, weight="bold"),
                                        width=140, height=32,
                                        fg_color="#FF6B6B", hover_color="#FF8E8E")
        self.restore_btn.grid(row=2, column=0, padx=12, pady=(0, 5))
        
        # 警告信息区域
        self.warning_frame = ctk.CTkFrame(action_card, fg_color="transparent")
        self.warning_frame.grid(row=3, column=0, sticky="ew", padx=12, pady=(5, 8))
        self.warning_frame.columnconfigure(0, weight=1)
        
        # 重要提示信息
        warning_info = ctk.CTkLabel(combined_frame, 
                                   text="⚠️ 本工具专为 Codex CLI 0.40.0 版本设计，请确保版本匹配",
                                   font=ctk.CTkFont(family="微软雅黑", size=9, weight="bold"),
                                   text_color="#FBBF24",
                                   wraplength=600)
        warning_info.grid(row=1, column=0, columnspan=2, sticky="ew", padx=12, pady=(5, 0))
        
        # 初始状态
        self.update_ui_state()
        
    def create_about_tab(self, about_tab):
        """创建关于标签页"""
        about_tab.columnconfigure(0, weight=1)
        
        # 主标题区域
        title_frame = ctk.CTkFrame(about_tab)
        title_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))
        title_frame.columnconfigure(0, weight=1)
        
        # 项目地址
        project_label = ctk.CTkLabel(title_frame, text="项目地址：",
                                    font=ctk.CTkFont(family="微软雅黑", size=12, weight="bold"),
                                    text_color="#FFFFFF")
        project_label.grid(row=0, column=0, pady=(15, 3))
        
        # GitHub链接（可点击）
        github_link = ctk.CTkLabel(title_frame, 
                                  text="https://github.com/396001000/codex-Chinese",
                                  font=ctk.CTkFont(family="微软雅黑", size=11, underline=True),
                                  text_color="#00D4FF",
                                  cursor="hand2")
        github_link.grid(row=1, column=0, pady=(0, 8))
        github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/396001000/codex-Chinese"))
        
        # 欢迎使用提示
        welcome_label = ctk.CTkLabel(title_frame, text="欢迎使用，请给项目一个小星星 ⭐",
                                    font=ctk.CTkFont(family="微软雅黑", size=12, weight="bold"),
                                    text_color="#FFD700")
        welcome_label.grid(row=2, column=0, pady=(0, 8))
        
        # 作者信息
        author_label = ctk.CTkLabel(title_frame, text="作者微信：chaojigeti520 支持软件开发定制。",
                                   font=ctk.CTkFont(family="微软雅黑", size=11),
                                   text_color="#4ADE80")
        author_label.grid(row=3, column=0, pady=(0, 15))
        
        # 内容区域
        content_frame = ctk.CTkFrame(about_tab)
        content_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        
        # 左侧：功能特点
        features_card = ctk.CTkFrame(content_frame)
        features_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=15)
        
        features_title = ctk.CTkLabel(features_card, text="✨ 功能特点",
                                     font=ctk.CTkFont(family="微软雅黑", size=14, weight="bold"),
                                     text_color="#00D4FF")
        features_title.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 8))
        
        features_text = """• 🔍 智能检测安装状态
• 🔄 自动检测最新版本
• 🌍 一键汉化CLI界面
• 🔄 快速恢复英文原版
• ⚡ 支持 0.40.0 版本
• 🎯 专业界面操作"""
        
        features_label = ctk.CTkLabel(features_card, text=features_text,
                                     font=ctk.CTkFont(family="微软雅黑", size=11),
                                     text_color="#FFFFFF",
                                     justify="left")
        features_label.grid(row=1, column=0, sticky="w", padx=25, pady=(0, 15))
        
        # 右侧：支持版本和技术信息
        version_card = ctk.CTkFrame(content_frame)
        version_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=15)
        
        version_title = ctk.CTkLabel(version_card, text="🔢 版本信息",
                                    font=ctk.CTkFont(family="微软雅黑", size=14, weight="bold"),
                                    text_color="#00D4FF")
        version_title.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 8))
        
        version_text = f"""• 支持版本: {', '.join(self.supported_versions)}
• 基于 Python + CustomTkinter
• MIT 开源许可证
• 跨平台兼容
• 实时状态监控
• 安全可靠操作"""
        
        version_label = ctk.CTkLabel(version_card, text=version_text,
                                    font=ctk.CTkFont(family="微软雅黑", size=11),
                                    text_color="#FFFFFF",
                                    justify="left")
        version_label.grid(row=1, column=0, sticky="w", padx=25, pady=(0, 15))
    
    def run_command(self, cmd, timeout=30):
        """运行命令并返回结果"""
        try:
            # 设置编码
            encoding = 'utf-8'
            if sys.platform.startswith('win'):
                encoding = 'gbk'
            
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=timeout,
                encoding=encoding,
                errors='ignore'
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "命令超时"
        except Exception as e:
            return False, "", str(e)
    
    def detect_installation(self):
        """检测 Node.js 和 Codex CLI 安装状态"""
        self.status_var.set("正在检测环境...")
        
        # 禁用按钮
        self.check_update_btn.configure(state="disabled")
        
        def detect_thread():
            # 检测 Node.js
            success, stdout, stderr = self.run_command("node --version")
            if success:
                self.npm_status['installed'] = True
                self.npm_status['version'] = stdout.strip()
            else:
                self.npm_status['installed'] = False
                self.npm_status['version'] = ''
            
            # 检测 Codex CLI
            success, stdout, stderr = self.run_command("codex --version")
            if success:
                # 提取版本号
                version_match = re.search(r'(\d+\.\d+\.\d+)', stdout)
                if version_match:
                    version = version_match.group(1)
                    self.codex_status['installed'] = True
                    self.codex_status['version'] = version
                    self.codex_status['checked'] = True
                else:
                    self.codex_status['installed'] = False
                    self.codex_status['version'] = ''
            else:
                self.codex_status['installed'] = False
                self.codex_status['version'] = ''
            
            # 更新UI
            def update_ui():
                self.update_detection_result()
                self.update_ui_state()
                # 启用检测新版按钮（如果已安装）
                if self.codex_status['installed']:
                    self.check_update_btn.configure(state="normal")
                else:
                    self.check_update_btn.configure(state="disabled")
            
            self.root.after(0, update_ui)
        
        threading.Thread(target=detect_thread, daemon=True).start()
    
    def check_for_updates(self):
        """检测Codex CLI新版本"""
        if not self.codex_status.get('installed', False):
            return
            
        self.status_var.set("正在检测新版本...")
        self.check_update_btn.configure(state="disabled", text="检测中...")
        
        def update_thread():
            try:
                self.detect_latest_version()
                
                # 更新UI
                def update_ui():
                    self.update_detection_result()
                    self.update_ui_state()
                    self.check_update_btn.configure(state="normal", text="🔄 检测新版")
                
                self.root.after(0, update_ui)
            except Exception as e:
                def update_ui():
                    self.status_var.set(f"检测新版本失败: {str(e)}")
                    self.check_update_btn.configure(state="normal", text="🔄 检测新版")
                
                self.root.after(0, update_ui)
        
        threading.Thread(target=update_thread, daemon=True).start()
    
    def detect_latest_version(self):
        """检测 Codex CLI 最新版本"""
        try:
            # 使用 npm view 获取最新版本信息
            success, stdout, stderr = self.run_command("npm view @openai/codex version")
            if success:
                latest_version = stdout.strip().strip('"')
                self.codex_status['latest_version'] = latest_version
                
                # 比较版本
                current_version = self.codex_status.get('version', '0.0.0')
                if self.compare_versions(latest_version, current_version) > 0:
                    self.codex_status['update_available'] = True
                else:
                    self.codex_status['update_available'] = False
            else:
                self.codex_status['latest_version'] = '未知'
                self.codex_status['update_available'] = False
        except Exception as e:
            self.codex_status['latest_version'] = '检测失败'
            self.codex_status['update_available'] = False
    
    def compare_versions(self, v1, v2):
        """比较版本号，返回 1 如果 v1 > v2，-1 如果 v1 < v2，0 如果相等"""
        def version_tuple(v):
            return tuple(map(int, v.split('.')))
        
        try:
            v1_tuple = version_tuple(v1)
            v2_tuple = version_tuple(v2)
            
            if v1_tuple > v2_tuple:
                return 1
            elif v1_tuple < v2_tuple:
                return -1
            else:
                return 0
        except:
            return 0
    
    def update_detection_result(self):
        """更新检测结果显示"""
        # 清空状态框架
        for widget in self.status_frame.winfo_children():
            widget.destroy()
        
        # Node.js 状态
        if self.npm_status['installed']:
            node_status = ctk.CTkLabel(self.status_frame, 
                                      text=f"✅ Node.js: {self.npm_status['version']}",
                                      font=ctk.CTkFont(family="微软雅黑", size=11),
                                      text_color="#4ADE80")
        else:
            node_status = ctk.CTkLabel(self.status_frame, 
                                      text="❌ Node.js: 未安装",
                                      font=ctk.CTkFont(family="微软雅黑", size=11),
                                      text_color="#F87171")
        node_status.grid(row=0, column=0, sticky="w", pady=(0, 3))
        
        # Codex CLI 状态
        if self.codex_status['installed']:
            codex_status = ctk.CTkLabel(self.status_frame, 
                                       text=f"✅ Codex CLI: v{self.codex_status['version']}",
                                       font=ctk.CTkFont(family="微软雅黑", size=11),
                                       text_color="#4ADE80")
            
            # 显示最新版本信息
            if 'latest_version' in self.codex_status and self.codex_status['latest_version'] != '':
                latest_version = self.codex_status['latest_version']
                if self.codex_status.get('update_available', False):
                    update_status = ctk.CTkLabel(self.status_frame, 
                                               text=f"🔄 最新版本: v{latest_version} (可更新)",
                                               font=ctk.CTkFont(family="微软雅黑", size=10),
                                               text_color="#FFA500")
                    update_status.grid(row=2, column=0, sticky="w")
                else:
                    update_status = ctk.CTkLabel(self.status_frame, 
                                               text=f"✅ 已是最新版本: v{latest_version}",
                                               font=ctk.CTkFont(family="微软雅黑", size=10),
                                               text_color="#4ADE80")
                    update_status.grid(row=2, column=0, sticky="w")
        else:
            codex_status = ctk.CTkLabel(self.status_frame, 
                                       text="❌ Codex CLI: 未安装",
                                       font=ctk.CTkFont(family="微软雅黑", size=11),
                                       text_color="#F87171")
        
        codex_status.grid(row=1, column=0, sticky="w")
        
        # 更新版本信息
        self.update_version_info()
    
    def update_version_info(self):
        """更新版本信息显示"""
        for widget in self.version_info_frame.winfo_children():
            widget.destroy()
        
        # 版本信息标题
        info_label = ctk.CTkLabel(self.version_info_frame, text="版本信息:",
                                 font=ctk.CTkFont(family="微软雅黑", size=12, weight="bold"),
                                 text_color="#FFFFFF")
        info_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        # 版本信息内容
        current_version = self.codex_status.get('version', '未检测')
        latest_version = self.codex_status.get('latest_version', '未知')
        selected_version = self.selected_version.get()
        
        version_text = f"当前: {current_version}"
        if current_version != '未检测':
            version_text += f"\n选择: {selected_version}"
            if latest_version != '未知':
                version_text += f"\n最新: {latest_version}"
        
        version_info_label = ctk.CTkLabel(self.version_info_frame, text=version_text,
                                         font=ctk.CTkFont(family="微软雅黑", size=11),
                                         text_color="#CCCCCC")
        version_info_label.grid(row=1, column=0, sticky="w")
        
        # 版本匹配状态和支持状态
        version_matched = (current_version == selected_version)
        is_supported = self.is_version_supported(current_version) if current_version != '未检测' else True
        
        # 向下兼容检查
        is_compatible = version_matched or (is_supported and self.is_version_supported(selected_version) and 
                                          self.compare_versions_for_compatibility(current_version, selected_version))
        
        if current_version != '未检测':
            if not is_supported:
                status_label = ctk.CTkLabel(self.version_info_frame, text="⚠️ 版本过高，不支持汉化",
                                           font=ctk.CTkFont(family="微软雅黑", size=11, weight="bold"),
                                           text_color="#FF6B6B")
            elif version_matched:
                status_label = ctk.CTkLabel(self.version_info_frame, text="✅ 版本匹配",
                                           font=ctk.CTkFont(family="微软雅黑", size=11, weight="bold"),
                                           text_color="#4ADE80")
            elif is_compatible:
                status_label = ctk.CTkLabel(self.version_info_frame, text="✅ 版本兼容",
                                           font=ctk.CTkFont(family="微软雅黑", size=11, weight="bold"),
                                           text_color="#4ADE80")
            else:
                status_label = ctk.CTkLabel(self.version_info_frame, text="❌ 版本不兼容",
                                           font=ctk.CTkFont(family="微软雅黑", size=11, weight="bold"),
                                           text_color="#F87171")
            status_label.grid(row=2, column=0, sticky="w", pady=(5, 0))
        
        # 更新按钮状态 - 版本支持且兼容就能汉化
        can_translate = self.codex_status.get('installed', False) and is_compatible and is_supported
        self.translate_btn.configure(state="normal" if can_translate else "disabled")
        self.restore_btn.configure(state="normal" if self.codex_status.get('installed', False) else "disabled")
        
        # 更新警告信息
        for widget in self.warning_frame.winfo_children():
            widget.destroy()
        
        if not can_translate and self.codex_status.get('installed', False):
            if not is_supported:
                warning_label = ctk.CTkLabel(self.warning_frame, 
                                            text=f"⚠️ v{current_version} 版本过高，不支持汉化\n最高支持版本：v{self.max_supported_version}",
                                            font=ctk.CTkFont(family="微软雅黑", size=11, weight="bold"),
                                            text_color="#FF6B6B")
                warning_label.grid(row=0, column=0)
            elif not is_compatible:
                selected_version = self.selected_version.get()
                warning_label = ctk.CTkLabel(self.warning_frame, 
                                            text=f"⚠️ 版本不兼容\n当前v{current_version}不兼容选择的v{selected_version}\n请选择v{current_version}或更低版本",
                                            font=ctk.CTkFont(family="微软雅黑", size=11, weight="bold"),
                                            text_color="#FBBF24")
                warning_label.grid(row=0, column=0)
    
    def is_version_supported(self, version):
        """检查版本是否支持"""
        if not version or version == '未检测':
            return True
        
        try:
            # 检查版本是否在支持列表中
            if version in self.supported_versions:
                return True
            
            # 检查是否高于最高支持版本
            if self.compare_versions(version, self.max_supported_version) > 0:
                return False
            
            # 检查是否在支持范围内（向下兼容）
            for supported_ver in self.supported_versions:
                if self.compare_versions(version, supported_ver) <= 0:
                    return True
            
            return False
        except:
            return True
    
    def compare_versions_for_compatibility(self, current, selected):
        """检查版本兼容性（向下兼容）"""
        try:
            # 当前版本应该 >= 选择版本（向下兼容）
            return self.compare_versions(current, selected) >= 0
        except:
            return True
    
    
    def update_ui_state(self):
        """更新界面状态"""
        # 根据检测结果更新按钮状态
        if not self.codex_status.get('installed', False):
            self.translate_btn.configure(state="disabled")
            self.restore_btn.configure(state="disabled")
            self.status_var.set("请先安装 Codex CLI")
        elif not self.npm_status.get('installed', False):
            self.translate_btn.configure(state="disabled")
            self.restore_btn.configure(state="disabled")
            self.status_var.set("请先安装 Node.js")
        else:
            # 根据版本兼容性更新按钮状态
            self.update_version_info()
            self.status_var.set("就绪")
    
    def get_script_path(self):
        """获取汉化脚本路径，支持打包后的环境"""
        script_name = "inject-chinese-final-dedup.js"
        
        # 尝试多个可能的路径
        possible_paths = []
        
        # 1. 如果是打包后的环境，检查临时目录
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller 打包后的临时目录
            possible_paths.append(Path(sys._MEIPASS) / "scripts" / script_name)
        elif hasattr(sys, 'frozen') and sys.frozen:
            # Nuitka 打包后，脚本在可执行文件同级的scripts目录
            exe_dir = Path(sys.executable).parent
            possible_paths.append(exe_dir / "scripts" / script_name)
        
        # 2. 开发环境路径
        current_dir = Path(__file__).parent
        possible_paths.extend([
            current_dir / "scripts" / script_name,  # 打包时复制到的scripts目录
            current_dir / script_name,              # 当前目录
            current_dir.parent / script_name        # 上级目录
        ])
        
        # 查找存在的脚本文件
        for path in possible_paths:
            if path.exists():
                return path
        
        return None
    
    def start_translation(self):
        """开始汉化过程"""
        if not self.codex_status.get('installed', False):
            messagebox.showwarning("警告", "请先安装 Codex CLI")
            return
        
        # 确认对话框
        result = messagebox.askyesno("确认汉化", 
                                   f"确定要汉化 Codex CLI v{self.codex_status['version']} 吗？\n\n" +
                                   f"选择版本: {self.selected_version.get()}\n" +
                                   "这将替换原有的英文界面。")
        if not result:
            return
        
        self.status_var.set("正在汉化...")
        self.translate_btn.configure(state="disabled", text="汉化中...")
        
        def translate_thread():
            try:
                # 获取汉化脚本路径
                script_path = self.get_script_path()
                if not script_path:
                    raise Exception("找不到汉化脚本文件 inject-chinese-final-dedup.js")
                
                # 执行汉化 - 切换到脚本所在目录
                script_dir = script_path.parent
                cmd = f'cd /d "{script_dir}" && node "{script_path.name}" inject'
                success, stdout, stderr = self.run_command(cmd, timeout=60)
                
                def update_ui():
                    self.translate_btn.configure(state="normal", text="✨ 一键汉化")
                    if success:
                        messagebox.showinfo("汉化成功", 
                                          "🎉 Codex CLI 汉化完成！\n\n" +
                                          "现在可以使用中文界面了。\n" +
                                          "如需恢复英文，请点击\"恢复原版\"。")
                        self.status_var.set("汉化完成")
                    else:
                        error_msg = stderr or "未知错误"
                        messagebox.showerror("汉化失败", f"汉化过程中出现错误：\n{error_msg}")
                        self.status_var.set("汉化失败")
                
                self.root.after(0, update_ui)
                
            except Exception as e:
                def update_ui():
                    self.translate_btn.configure(state="normal", text="✨ 一键汉化")
                    messagebox.showerror("汉化失败", f"汉化失败：\n{str(e)}")
                    self.status_var.set("汉化失败")
                
                self.root.after(0, update_ui)
        
        threading.Thread(target=translate_thread, daemon=True).start()
    
    def restore_original(self):
        """恢复原版"""
        if not self.codex_status.get('installed', False):
            messagebox.showwarning("警告", "请先安装 Codex CLI")
            return
        
        # 确认对话框
        result = messagebox.askyesno("确认恢复", 
                                   "确定要恢复 Codex CLI 英文原版吗？\n\n" +
                                   "这将移除所有汉化内容。")
        if not result:
            return
        
        self.status_var.set("正在恢复...")
        self.restore_btn.configure(state="disabled", text="恢复中...")
        
        def restore_thread():
            try:
                # 获取汉化脚本路径
                script_path = self.get_script_path()
                if not script_path:
                    raise Exception("找不到汉化脚本文件 inject-chinese-final-dedup.js")
                
                # 执行恢复 - 切换到脚本所在目录
                script_dir = script_path.parent
                cmd = f'cd /d "{script_dir}" && node "{script_path.name}" restore'
                success, stdout, stderr = self.run_command(cmd, timeout=60)
                
                def update_ui():
                    self.restore_btn.configure(state="normal", text="🔄 恢复原版")
                    if success:
                        messagebox.showinfo("恢复成功", 
                                          "✅ Codex CLI 已恢复为英文原版！\n\n" +
                                          "现在界面已恢复为英文显示。")
                        self.status_var.set("恢复完成")
                    else:
                        error_msg = stderr or "未知错误"
                        messagebox.showerror("恢复失败", f"恢复过程中出现错误：\n{error_msg}")
                        self.status_var.set("恢复失败")
                
                self.root.after(0, update_ui)
                
            except Exception as e:
                def update_ui():
                    self.restore_btn.configure(state="normal", text="🔄 恢复原版")
                    messagebox.showerror("恢复失败", f"恢复失败：\n{str(e)}")
                    self.status_var.set("恢复失败")
                
                self.root.after(0, update_ui)
        
        threading.Thread(target=restore_thread, daemon=True).start()

def main():
    app = CodexCLIGUI()
    app.root.mainloop()

if __name__ == "__main__":
    main()

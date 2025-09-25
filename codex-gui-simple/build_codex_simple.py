#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🚀 Codex CLI 汉化工具 - 简化版打包脚本
专注汉化功能，界面简洁
"""

import os
import sys
import shutil
import subprocess
import json
from pathlib import Path

class CodexSimpleBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.gui_dir = Path(__file__).parent
        self.release_dir = self.gui_dir / "release_codex_simple"
        
        print("🚀 Codex CLI 汉化工具 - 简化版打包脚本")
        print("=" * 65)
        print("🎯 目标：打包简化版GUI，专注汉化功能")
        print("")
        
    def check_nuitka(self):
        """检查Nuitka是否已安装"""
        try:
            result = subprocess.run(['python', '-m', 'nuitka', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip().split('\n')[0]
                print(f"✅ Nuitka: {version}")
                return True
            else:
                print("❌ Nuitka未安装，正在安装...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'nuitka'], check=True)
                print("✅ Nuitka安装完成")
                return True
        except Exception as e:
            print(f"❌ Nuitka检查失败: {e}")
            return False
    
    def check_scripts(self):
        """检查所有必要的汉化脚本文件"""
        print("\n" + "=" * 65)
        print("🔍 检查Codex CLI汉化脚本文件...")
        
        required_scripts = [
            "inject-chinese-final-dedup.js",
            "codex-translations-extended.json"
        ]
        
        found_count = 0
        missing_count = 0
        
        for script in required_scripts:
            script_path = self.project_root / script
            if script_path.exists():
                size = script_path.stat().st_size
                desc = self.get_script_description(script)
                print(f"   ✅ {script} ({size} bytes) - {desc}")
                found_count += 1
            else:
                print(f"   ❌ {script} - 文件缺失")
                missing_count += 1
        
        print(f"\n📊 统计: 找到 {found_count} 个文件，缺失 {missing_count} 个文件")
        
        if missing_count > 0:
            print("❌ 有汉化脚本文件缺失，无法继续打包")
            return False
        
        return True
    
    def get_script_description(self, script_name):
        """获取脚本描述"""
        descriptions = {
            "inject-chinese-final-dedup.js": "Codex CLI主汉化脚本",
            "codex-translations-extended.json": "Codex CLI扩展翻译文件"
        }
        return descriptions.get(script_name, "脚本文件")
    
    def prepare_data_files(self):
        """准备数据文件，复制到GUI目录以便Nuitka打包"""
        print("\n" + "=" * 65)
        print("📁 准备汉化脚本文件...")
        
        # 在GUI目录创建scripts子目录
        scripts_dir = self.gui_dir / "scripts"
        if scripts_dir.exists():
            shutil.rmtree(scripts_dir)
        scripts_dir.mkdir()
        
        required_scripts = [
            "inject-chinese-final-dedup.js",
            "codex-translations-extended.json"
        ]
        
        copied_count = 0
        for script in required_scripts:
            src_path = self.project_root / script
            dst_path = scripts_dir / script
            if src_path.exists():
                shutil.copy2(src_path, dst_path)
                print(f"   ✅ 复制: {script}")
                copied_count += 1
            else:
                print(f"   ❌ 缺失: {script}")
        
        print(f"\n📊 成功复制 {copied_count} 个脚本文件到 {scripts_dir}")
        return scripts_dir, copied_count == len(required_scripts)
    
    def build_with_nuitka(self, scripts_dir):
        """使用Nuitka构建EXE"""
        print("\n" + "=" * 65)
        print("🚀 开始Nuitka编译...")
        print("⏳ 编译为原生C++代码，包含所有汉化脚本...")
        
        # Nuitka编译命令
        nuitka_cmd = [
            sys.executable, '-m', 'nuitka',
            '--onefile',  # 单文件
            '--windows-disable-console',  # 无控制台窗口
            '--windows-icon-from-ico=app_icon.ico',  # 图标
            '--output-filename=Codex CLI汉化工具.exe',
            '--output-dir=dist_simple',
            '--remove-output',
            '--assume-yes-for-downloads',
            '--show-progress',
            '--enable-plugin=tk-inter',  # tkinter插件
            '--include-data-dir=scripts=scripts',  # 包含整个scripts目录
            '--include-data-file=scripts/inject-chinese-final-dedup.js=scripts/inject-chinese-final-dedup.js',  # 确保汉化脚本包含
            '--include-data-file=scripts/codex-translations-extended.json=scripts/codex-translations-extended.json',  # 确保翻译文件包含
            '--follow-imports',
            'codex_gui.py'
        ]
        
        try:
            # 切换到GUI目录
            os.chdir(self.gui_dir)
            
            print("🔧 执行Nuitka编译命令:")
            print(f"   {' '.join(nuitka_cmd)}")
            print("")
            
            # 执行Nuitka编译
            result = subprocess.run(nuitka_cmd, check=True)
            
            exe_path = self.gui_dir / "dist_simple" / "Codex CLI汉化工具.exe"
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print("✅ Nuitka编译成功！")
                print(f"📁 EXE位置: {exe_path}")
                print(f"📏 文件大小: {size_mb:.1f} MB")
                return exe_path
            else:
                print("❌ 编译完成但未找到EXE文件")
                return None
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Nuitka编译失败: {e}")
            return None
        except Exception as e:
            print(f"❌ 编译过程出错: {e}")
            return None
    
    def test_exe(self, exe_path):
        """测试EXE文件"""
        print("\n" + "=" * 65)
        print(f"🧪 测试简化版EXE: {exe_path}")
        
        try:
            print("   🔍 测试程序启动...")
            # 启动程序测试
            process = subprocess.Popen([str(exe_path)], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
            
            # 等待一小段时间
            import time
            time.sleep(3)
            
            if process.poll() is None:
                print("   ✅ 程序启动成功！")
                print("   📋 程序正在运行中，请手动测试功能...")
                process.terminate()
                return True
            else:
                stdout, stderr = process.communicate()
                print("   ❌ 程序启动失败")
                if stderr:
                    print(f"   错误: {stderr.decode('utf-8', errors='ignore')}")
                return False
                
        except Exception as e:
            print(f"   ❌ 测试失败: {e}")
            return False
    
    def create_release(self, exe_path):
        """创建发布包"""
        print("\n" + "=" * 65)
        print("📦 创建发布包...")
        
        # 创建发布目录
        target_dir = self.release_dir
        if target_dir.exists():
            try:
                shutil.rmtree(target_dir)
            except Exception:
                import datetime
                ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                target_dir = self.gui_dir / f"release_codex_simple_{ts}"
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # 复制EXE文件
        release_exe = target_dir / "Codex CLI汉化工具.exe"
        shutil.copy2(exe_path, release_exe)
        print(f"   ✅ EXE文件: {release_exe}")
        
        # 复制README文件
        readme_src = self.gui_dir / "README.md"
        if readme_src.exists():
            readme_dst = target_dir / "README.md"
            shutil.copy2(readme_src, readme_dst)
            print(f"   ✅ README文件: {readme_dst}")
        
        # 创建使用说明
        usage_text = """🚀 Codex CLI 汉化工具 使用说明

📋 系统要求:
   • Windows 操作系统
   • Node.js 已安装 (用于执行汉化脚本)
   • Codex CLI 0.40.0 版本 (npm install -g @openai/codex)

✨ 功能特点:
   • 🔍 智能检测 Node.js 和 Codex CLI 安装状态
   • 🔄 自动检测最新版本并提供更新提示  
   • 🌍 一键汉化 Codex CLI 界面为中文
   • 🔄 快速恢复英文原版界面
   • ⚡ 专为 Codex CLI 0.40.0 版本优化
   • 🎯 简洁界面，操作简便

🚀 使用步骤:
   1. 双击运行 "Codex CLI汉化工具.exe"
   2. 点击 "检测安装" 按钮检查 Codex CLI 状态
   3. 确保 Codex CLI 版本为 0.40.0
   4. 点击 "一键汉化" 开始汉化过程
   5. 如需恢复，点击 "恢复原版" 即可

⚠️ 重要提示:
   本工具专为 Codex CLI 0.40.0 版本设计，请确保版本匹配。

📞 联系方式:
   • 作者微信: chaojigeti520
   • 项目地址: https://github.com/396001000/codex-Chinese
   • 欢迎使用，请给项目一个小星星 ⭐

🎯 版本说明:
   简化版专注汉化功能，界面简洁，适合只需要汉化功能的用户。
   如果需要API配置功能，请使用完整版。

支持软件开发定制 - 有任何定制需求请联系作者微信
"""
        
        usage_file = target_dir / "使用说明.txt"
        with open(usage_file, 'w', encoding='utf-8') as f:
            f.write(usage_text)
        print(f"   ✅ 使用说明: {usage_file}")
        
        # 创建版本信息
        version_info = {
            "name": "Codex CLI汉化工具",
            "version": "1.0",
            "build_type": "简化版",
            "build_date": str(Path().cwd()),
            "compiler": "Nuitka -> C++",
            "features": [
                "Codex CLI 0.40.0汉化",
                "智能检测安装状态",
                "一键汉化操作",
                "快速恢复原版",
                "简洁界面设计",
                "原生C++编译",
                "单文件部署"
            ],
            "scripts_included": 2,
            "codex_version": "0.40.0",
            "supported_features": [
                "一键汉化",
                "恢复原版",
                "版本检测",
                "安装状态检测"
            ]
        }
        
        version_file = target_dir / "version.json"
        with open(version_file, 'w', encoding='utf-8') as f:
            json.dump(version_info, f, ensure_ascii=False, indent=2)
        print(f"   ✅ 版本信息: {version_file}")
        
        print(f"\n📁 发布包已创建: {target_dir}/")
        self.release_dir = target_dir
        return True
    
    def cleanup(self):
        """清理临时文件"""
        print("\n" + "=" * 65)
        print("🧹 清理临时文件...")
        
        scripts_dir = self.gui_dir / "scripts"
        if scripts_dir.exists():
            shutil.rmtree(scripts_dir)
            print(f"   ✅ 已删除临时目录: {scripts_dir}")
        
        return True
    
    def build(self):
        """执行完整构建流程"""
        if not self.check_nuitka():
            return False
            
        if not self.check_scripts():
            return False
        
        scripts_dir, success = self.prepare_data_files()
        if not success:
            return False
        
        exe_path = self.build_with_nuitka(scripts_dir)
        if not exe_path:
            return False
            
        if not self.test_exe(exe_path):
            print("⚠️ EXE测试失败，但编译已完成，请手动测试")
        
        if not self.create_release(exe_path):
            return False
        
        self.cleanup()
        
        print("\n" + "=" * 65)
        print("🎉 Codex CLI汉化工具 - 简化版构建完成！")
        print(f"📦 发布位置: {self.release_dir}/")
        print("🎯 专注功能: 汉化")
        print("✅ 支持版本: Codex CLI 0.40.0")
        print("\n🚀 简化版特点:")
        print("   ✅ 专注汉化功能")
        print("   ✅ 界面简洁美观")
        print("   ✅ 操作简单易用")
        print("   ✅ 体积小巧精悍")
        print("   ✅ 原生C++编译，性能优异")
        print("   ✅ 真正的单文件部署")
        print("\n✨ 简化版EXE已准备就绪！")
        print("\n🎊 简化版打包任务完成！")
        
        return True

if __name__ == "__main__":
    builder = CodexSimpleBuilder()
    success = builder.build()
    sys.exit(0 if success else 1)


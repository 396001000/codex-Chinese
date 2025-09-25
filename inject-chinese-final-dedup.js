#!/usr/bin/env node
/**
 * Codex CLI 最终去重版中文汉化注入脚本
 * 去除重复翻译，优化性能，包含所有用户界面文本
 */

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';
import { spawn } from "child_process";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 获取npm全局包路径
function getNpmGlobalPath() {
  try {
    const globalPath = execSync('npm root -g', { encoding: 'utf8' }).trim();
    return globalPath;
  } catch (error) {
    console.error('❌ 无法获取npm全局包路径:', error.message);
    process.exit(1);
  }
}

// 获取Codex CLI安装路径
function getCodexPath() {
  const globalPath = getNpmGlobalPath();
  const codexPath = path.join(globalPath, '@openai', 'codex');
  
  if (!fs.existsSync(codexPath)) {
    console.error('❌ 未找到全局安装的 @openai/codex 包');
    console.error('请先运行: npm install -g @openai/codex');
    process.exit(1);
  }
  
  return codexPath;
}

// 去重后的完全翻译映射
const finalTranslations = [
  // 基本界面
  ["Codex CLI", "Codex 命令行工具"],
  ["Usage:", "用法:"],
  ["Commands:", "命令:"],
  ["Arguments:", "参数:"],
  ["Options:", "选项:"],
  ["Print help", "打印帮助"],
  ["Print version", "打印版本"],
  ["Usage: codex [OPTIONS] [PROMPT]", "用法：codex [选项] [提示]"],
  ["If no subcommand is specified, options will be forwarded to the interactive CLI.", "如果未指定子命令，选项将转发给交互式CLI。"],
  
  // 欢迎界面和初始提示
  ["To get started, describe a task or try one of these commands:", "开始使用时，可以描述要做的任务或尝试以下命令："],
  ["  Welcome to Codex, OpenAI's command-line coding agent", "  欢迎使用 Codex，OpenAI 的命令行编程助手"],
  ["  Sign in with ChatGPT to use Codex as part of your paid plan", "  登录 ChatGPT 以在付费套餐中使用 Codex"],
  ["  or connect an API key for usage-based billing", "  或者连接 API 密钥以按使用量计费"],
  ["> 1. Sign in with ChatGPT", "> 1. 使用 ChatGPT 登录"],
  ["     Usage included with Plus, Pro, and Team plans", "     Plus、Pro、Team 套餐内含使用额度"],
  ["  2. Provide your own API key", "  2. 提供你自己的 API 密钥"],
  ["     Pay for what you use", "     按使用量付费"],
  ["  Press Enter to continue", "  按 Enter 键继续"],
  
  // 交互命令完整翻译
  ["/init - create an AGENTS.md file with instructions for Codex", "/init - 创建一个包含Codex指令的AGENTS.md文件"],
  ["/status - show current session configuration", "/status - 显示当前会话配置"],
  ["/approvals - choose what Codex can do without approval", "/approvals - 选择Codex可以在无需批准的情况下执行的操作"],
  ["/model - choose what model and reasoning effort to use", "/model - 选择要使用的模型和推理强度"],
  ["/review - review my current changes and find issues", "/review - 审查我当前的更改并查找问题"],
  ["/new - start a new chat during a conversation", "/new - 在对话中开始新的聊天"],
  ["/compact - summarize conversation to prevent hitting the context limit", "/compact - 总结对话以防止达到上下文限制"],
  ["/diff - show git diff (including untracked files)", "/diff - 显示git差异（包括未跟踪的文件）"],
  ["/mention - mention a file", "/mention - 提及文件"],
  ["/mcp - list configured MCP tools", "/mcp - 列出已配置的MCP工具"],
  ["/logout - log out of Codex", "/logout - 退出Codex登录"],
  ["/quit - exit Codex", "/quit - 退出Codex"],
  
  // 命令说明（不带斜杠前缀）
  ["create an AGENTS.md file with instructions for Codex", "创建一个包含Codex指令的AGENTS.md文件"],
  ["show current session configuration", "显示当前会话配置"],
  ["choose what Codex can do without approval", "选择Codex可以在无需批准的情况下执行的操作"],
  ["choose what model and reasoning effort to use", "选择要使用的模型和推理强度"],
  ["review my current changes and find issues", "审查我当前的更改并查找问题"],
  ["start a new chat during a conversation", "在对话中开始新的聊天"],
  ["summarize conversation to prevent hitting the context limit", "总结对话以防止达到上下文限制"],
  ["show git diff (including untracked files)", "显示git差异（包括未跟踪的文件）"],
  ["mention a file", "提及文件"],
  ["list configured MCP tools", "列出已配置的MCP工具"],
  ["log out of Codex", "退出Codex登录"],
  ["exit Codex", "退出Codex"],
  
  // 完整的命令行翻译（带格式）
  ["exec        Run Codex non-interactively [aliases: e]", "exec        非交互式运行Codex [别名: e]"],
  ["login       Manage login", "login       管理登录"],
  ["logout      Remove stored authentication credentials", "logout      删除存储的身份验证凭据"],
  ["mcp         [experimental] Run Codex as an MCP server and manage MCP servers", "mcp         [实验性] 将Codex作为MCP服务器运行并管理MCP服务器"],
  ["proto       Run the Protocol stream via stdin/stdout [aliases: p]", "proto       通过stdin/stdout运行协议流 [别名: p]"],
  ["completion  Generate shell completion scripts", "completion  生成shell自动补全脚本"],
  ["debug       Internal debugging commands", "debug       内部调试命令"],
  ["apply       Apply the latest diff produced by Codex agent as a", "apply       将Codex代理生成的最新差异作为"],
  ["to your local working", "应用到本地工作"],
  ["              tree [aliases: a]", "              目录 [别名: a]"],
  ["resume      Resume a previous interactive session (picker by default; use --last to continue the", "resume      恢复之前的交互式会话（默认使用选择器；使用--last继续"],
  ["              most recent)", "              最近的会话）"],
  ["help        Print this message or the help of the given subcommand(s)", "help        打印此消息或给定子命令的帮助"],
  
  // 命令说明（简化版本，去除重复）
  ["Run Codex non-interactively [aliases: e]", "非交互式运行Codex [别名: e]"],
  ["Run Codex non-interactively", "非交互式运行Codex"],
  ["Manage login", "管理登录"],
  ["Remove stored authentication credentials", "删除存储的身份验证凭据"],
  ["[experimental] Run Codex as an MCP server and manage MCP servers", "[实验性] 将Codex作为MCP服务器运行并管理MCP服务器"],
  ["Run the Protocol stream via stdin/stdout [aliases: p]", "通过stdin/stdout运行协议流 [别名: p]"],
  ["Run the Protocol stream via stdin/stdout", "通过stdin/stdout运行协议流"],
  ["Generate shell completion scripts", "生成shell自动补全脚本"],
  ["Internal debugging commands", "内部调试命令"],
  ["tree [aliases: a]", "目录 [别名: a]"],
  ["Resume a previous interactive session (picker by default; use --last to continue the", "恢复之前的交互式会话（默认使用选择器；使用--last继续"],
  ["most recent)", "最近的会话）"],
  ["Print this message or the help of the given subcommand(s)", "打印此消息或给定子命令的帮助"],
  
  // 参数说明
  ["Optional user prompt to start the session", "启动会话的可选用户提示"],
  ["          Optional user prompt to start the session", "          启动会话的可选用户提示"],
  
  // 详细选项说明
  ["Override a configuration value that would otherwise be loaded from `~/.codex/config.toml`.", "覆盖原本从 `~/.codex/config.toml` 加载的配置值。"],
  ["          Override a configuration value that would otherwise be loaded from `~/.codex/config.toml`.", "          覆盖原本从 `~/.codex/config.toml` 加载的配置值。"],
  ["Use a dotted path (`foo.bar.baz`) to override nested values. The `value` portion is parsed", "使用点分路径（`foo.bar.baz`）覆盖嵌套值。`value` 部分被解析"],
  ["          Use a dotted path (`foo.bar.baz`) to override nested values. The `value` portion is parsed", "          使用点分路径（`foo.bar.baz`）覆盖嵌套值。`value` 部分被解析"],
  ["as JSON. If it fails to parse as JSON, the raw string is used as a literal.", "为JSON。如果解析JSON失败，则将原始字符串用作字面值。"],
  ["          as JSON. If it fails to parse as JSON, the raw string is used as a literal.", "          为JSON。如果解析JSON失败，则将原始字符串用作字面值。"],
  
  ["Examples: - `-c model=\"o3\"` - `-c 'sandbox_permissions=[\"disk-full-read-access\"]'` - `-c", "示例：- `-c model=\"o3\"` - `-c 'sandbox_permissions=[\"disk-full-read-access\"]'` - `-c"],
  ["          Examples: - `-c model=\"o3\"` - `-c 'sandbox_permissions=[\"disk-full-read-access\"]'` - `-c", "          示例：- `-c model=\"o3\"` - `-c 'sandbox_permissions=[\"disk-full-read-access\"]'` - `-c"],
  ["shell_environment_policy.inherit=all`", "shell_environment_policy.inherit=all`"],
  ["          shell_environment_policy.inherit=all`", "          shell_environment_policy.inherit=all`"],
  
  ["Optional image(s) to attach to the initial prompt", "附加到初始提示的可选图像"],
  ["          Optional image(s) to attach to the initial prompt", "          附加到初始提示的可选图像"],
  ["Model the agent should use", "代理应使用的模型"],
  ["          Model the agent should use", "          代理应使用的模型"],
  ["Convenience flag to select the local open source model provider. Equivalent to -c", "选择本地开源模型提供商的便利标志。等价于-c"],
  ["          Convenience flag to select the local open source model provider. Equivalent to -c", "          选择本地开源模型提供商的便利标志。等价于-c"],
  ["model_provider=oss; verifies a local Ollama server is running", "model_provider=oss；验证本地Ollama服务器是否正在运行"],
  ["          model_provider=oss; verifies a local Ollama server is running", "          model_provider=oss；验证本地Ollama服务器是否正在运行"],
  ["Configuration profile from config.toml to specify default options", "来自config.toml的配置文件，用于指定默认选项"],
  ["          Configuration profile from config.toml to specify default options", "          来自config.toml的配置文件，用于指定默认选项"],
  ["Select the sandbox policy to use when executing model-generated shell commands", "选择执行模型生成的shell命令时使用的沙盒策略"],
  ["          Select the sandbox policy to use when executing model-generated shell commands", "          选择执行模型生成的shell命令时使用的沙盒策略"],
  ["Configure when the model requires human approval before executing a command", "配置模型在执行命令前何时需要人工批准"],
  ["          Configure when the model requires human approval before executing a command", "          配置模型在执行命令前何时需要人工批准"],
  ["Tell the agent to use the specified directory as its working root", "告诉代理使用指定目录作为其工作根目录"],
  ["          Tell the agent to use the specified directory as its working root", "          告诉代理使用指定目录作为其工作根目录"],
  ["Enable web search (off by default). When enabled, the native Responses `web_search` tool", "启用网络搜索（默认关闭）。启用时，原生响应 `web_search` 工具"],
  ["          Enable web search (off by default). When enabled, the native Responses `web_search` tool", "          启用网络搜索（默认关闭）。启用时，原生响应 `web_search` 工具"],
  ["is available to the model (no per‑call approval)", "对模型可用（无需每次调用批准）"],
  ["          is available to the model (no per‑call approval)", "          对模型可用（无需每次调用批准）"],
  ["Print help (see a summary with '-h')", "打印帮助（使用'-h'查看摘要）"],
  ["          Print help (see a summary with '-h')", "          打印帮助（使用'-h'查看摘要）"],
  ["          Print version", "          打印版本"],
  
  // 选项值和可能的值
  ["[possible values: read-only, workspace-write, danger-full-access]", "[可能的值：只读, 工作区写入, 危险-完全访问]"],
  ["          [possible values: read-only, workspace-write, danger-full-access]", "          [可能的值：只读, 工作区写入, 危险-完全访问]"],
  ["possible values:", "可能的值："],
  ["Possible values:", "可能的值："],
  ["          Possible values:", "          可能的值："],
  ["read-only", "只读"],
  ["workspace-write", "工作区写入"],
  ["danger-full-access", "危险-完全访问"],
  ["on-request", "按需批准"],
  ["untrusted", "不受信任"],
  ["on-failure", "失败时"],
  ["never", "从不"],
  
  // 详细的批准策略说明
  ["- untrusted:  Only run \"trusted\" commands (e.g. ls, cat, sed) without asking for user", "- 不受信任：仅运行 \"受信任\"的命令（如 ls、cat、sed）而不询问用户"],
  ["          - untrusted:  Only run \"trusted\" commands (e.g. ls, cat, sed) without asking for user", "          - 不受信任：仅运行 \"受信任\"的命令（如 ls、cat、sed）而不询问用户"],
  ["approval. Will escalate to the user if the model proposes a command that is not in the", "批准。如果模型提出不在"],
  ["            approval. Will escalate to the user if the model proposes a command that is not in the", "            批准。如果模型提出不在"],
  ["\"trusted\" set", "\"受信任\"集合中的命令，将升级给用户"],
  ["            \"trusted\" set", "            \"受信任\"集合中的命令，将升级给用户"],
  ["- on-failure: Run all commands without asking for user approval. Only asks for approval if", "- 失败时：运行所有命令而不询问用户批准。仅在以下情况下询问批准："],
  ["          - on-failure: Run all commands without asking for user approval. Only asks for approval if", "          - 失败时：运行所有命令而不询问用户批准。仅在以下情况下询问批准："],
  ["a command fails to execute, in which case it will escalate to the user to ask for", "命令执行失败，在这种情况下将升级给用户询问"],
  ["            a command fails to execute, in which case it will escalate to the user to ask for", "            命令执行失败，在这种情况下将升级给用户询问"],
  ["un-sandboxed execution", "非沙盒执行"],
  ["            un-sandboxed execution", "            非沙盒执行"],
  ["- on-request: The model decides when to ask the user for approval", "- 按需批准：模型决定何时询问用户批准"],
  ["          - on-request: The model decides when to ask the user for approval", "          - 按需批准：模型决定何时询问用户批准"],
  ["- never:      Never ask for user approval Execution failures are immediately returned to", "- 从不：从不询问用户批准，执行失败立即返回给"],
  ["          - never:      Never ask for user approval Execution failures are immediately returned to", "          - 从不：从不询问用户批准，执行失败立即返回给"],
  ["the model", "模型"],
  ["            the model", "            模型"],
  
  // 其他选项说明
  ["Convenience alias for low-friction sandboxed automatic execution (-a on-failure, --sandbox", "低摩擦沙盒自动执行的便利别名（-a 失败时，--sandbox"],
  ["          Convenience alias for low-friction sandboxed automatic execution (-a on-failure, --sandbox", "          低摩擦沙盒自动执行的便利别名（-a 失败时，--sandbox"],
  ["workspace-write)", "工作区写入）"],
  ["          workspace-write)", "          工作区写入）"],
  ["Skip all confirmation prompts and execute commands without sandboxing. EXTREMELY", "跳过所有确认提示并在没有沙盒的情况下执行命令。极其"],
  ["          Skip all confirmation prompts and execute commands without sandboxing. EXTREMELY", "          跳过所有确认提示并在没有沙盒的情况下执行命令。极其"],
  ["DANGEROUS. Intended solely for running in environments that are externally sandboxed", "危险。仅适用于在外部沙盒环境中运行"],
  ["          DANGEROUS. Intended solely for running in environments that are externally sandboxed", "          危险。仅适用于在外部沙盒环境中运行"],
  
  // 状态信息
  ["Workspace", "工作区"],
  ["Account", "账户"],
  ["Model", "模型"],
  ["Client", "客户端"],
  ["Token Usage", "令牌使用情况"],
  ["Usage Limits", "使用限制"],
  ["MCP Tools", "MCP 工具"],
  ["Free", "免费"],
  ["None", "无"],
  ["Auto", "自动"],
  ["Path:", "路径："],
  ["Approval Mode:", "批准模式："],
  ["Sandbox:", "沙盒："],
  ["AGENTS files:", "AGENTS 文件："],
  ["(none)", "（无）"],
  ["Signed in with ChatGPT", "已使用 ChatGPT 登录"],
  ["Login:", "登录："],
  ["Plan:", "套餐："],
  ["Name:", "名称："],
  ["Provider:", "提供商："],
  ["Reasoning Effort:", "推理强度："],
  ["Reasoning Summaries:", "推理摘要："],
  ["CLI Version:", "CLI 版本："],
  ["Session ID:", "会话 ID："],
  ["Input:", "输入："],
  ["Output:", "输出："],
  ["Total:", "总计："],
  ["Send a message to load usage data.", "发送消息以加载使用数据。"],
  ["No MCP servers configured.", "未配置 MCP 服务器。"],
  ["See the MCP docs to configure them.", "请查看 MCP 文档进行配置。"],
  
  // 推理级别说明（处理截图中的分段显示）
  ["fastest responses with limited reasoning; ideal for coding, instructions, or", "推理有限的最快响应；适用于编码、指令或"],
  ["lightweight tasks", "轻量级任务"],
  ["fastest responses with limited reasoning; ideal for coding, instructions, or lightweight tasks", "推理有限的最快响应；适用于编码、指令或轻量级任务"],
  ["— fastest responses with limited reasoning; ideal for coding, instructions, or", "— 推理有限的最快响应；适用于编码、指令或"],
  ["— fastest responses with limited reasoning; ideal for coding, instructions, or lightweight tasks", "— 推理有限的最快响应；适用于编码、指令或轻量级任务"],
  
  ["balances speed with some reasoning; useful for straightforward queries and short", "平衡速度与一些推理；适用于直接查询和简短"],
  ["explanations", "解释"],
  ["balances speed with some reasoning; useful for straightforward queries and short explanations", "平衡速度与一些推理；适用于直接查询和简短解释"],
  ["— balances speed with some reasoning; useful for straightforward queries and short", "— 平衡速度与一些推理；适用于直接查询和简短"],
  ["— balances speed with some reasoning; useful for straightforward queries and short explanations", "— 平衡速度与一些推理；适用于直接查询和简短解释"],
  
  ["default setting; provides a solid balance of reasoning depth and latency for", "默认设置；为"],
  ["general-purpose tasks", "通用任务提供推理深度和延迟的良好平衡"],
  ["default setting; provides a solid balance of reasoning depth and latency for general-purpose tasks", "默认设置；为通用任务提供推理深度和延迟的良好平衡"],
  ["— default setting; provides a solid balance of reasoning depth and latency for", "— 默认设置；为"],
  ["— default setting; provides a solid balance of reasoning depth and latency for general-purpose tasks", "— 默认设置；为通用任务提供推理深度和延迟的良好平衡"],
  
  ["maximizes reasoning depth for complex or ambiguous problems", "为复杂或模糊问题最大化推理深度"],
  ["— maximizes reasoning depth for complex or ambiguous problems", "— 为复杂或模糊问题最大化推理深度"],
  
  // 模型选择界面
  ["Select model and reasoning level", "选择模型和推理级别"],
  ["Switch between OpenAI models for this and future Codex CLI session", "为当前和未来的Codex CLI会话切换OpenAI模型"],
  ["gpt-5-codex low", "gpt-5-codex 低"],
  ["gpt-5-codex medium", "gpt-5-codex 中等"],
  ["gpt-5-codex high", "gpt-5-codex 高"],
  ["gpt-5 minimal", "gpt-5 最小"],
  ["gpt-5 low", "gpt-5 低"],
  ["gpt-5 medium", "gpt-5 中等"],
  ["gpt-5 high", "gpt-5 高"],
  
  // 批准模式
  ["Select Approval Mode", "选择批准模式"],
  ["Read Only", "只读"],
  ["Auto (current)", "自动（当前）"],
  ["Full Access", "完全访问"],
  ["Exercise caution", "请谨慎使用"],
  
  // 批准模式详细说明（完整版本）
  ["Codex can read files and answer questions. Codex requires approval to make edits, run", "Codex可以读取文件并回答问题。Codex需要批准才能进行编辑、运行"],
  ["commands, or access network", "命令或访问网络"],
  ["Codex can read files and answer questions. Codex requires approval to make edits, run commands, or access network", "Codex可以读取文件并回答问题。Codex需要批准才能进行编辑、运行命令或访问网络"],
  
  ["Codex can read files, make edits, and run commands in the workspace. Codex requires approval", "Codex可以读取文件、进行编辑并在工作区中运行命令。Codex需要批准"],
  ["to work outside the workspace or access network", "才能在工作区外工作或访问网络"],
  ["Codex can read files, make edits, and run commands in the workspace. Codex requires approval to work outside the workspace or access network", "Codex可以读取文件、进行编辑并在工作区中运行命令。Codex需要批准才能在工作区外工作或访问网络"],
  
  ["Codex can read files, make edits, and run commands with network access, without approval.", "Codex可以读取文件、进行编辑并运行具有网络访问权限的命令，无需批准。"],
  ["Exercise caution", "请谨慎使用"],
  
  // 处理截图中的分段文本
  ["Codex可以读取文件，进行编辑并运行有网络访问权限的命令，无需批准。请谨慎使用", "Codex可以读取文件、进行编辑并运行具有网络访问权限的命令，无需批准。请谨慎使用"],
  
  // 审查预设选择
  ["Select a review preset", "选择审查预设"],
  ["Review uncommitted changes", "审查未提交的更改"],
  ["Review a commit", "审查提交"],
  ["Review against a base branch", "对比基础分支审查"],
  ["Custom review instructions", "自定义审查指令"],
  
  // 控制提示
  ["Press Enter to confirm or Esc to go back", "按 Enter 确认或按 Esc 返回"],
  ["Ctrl+C again to quit", "再次按 Ctrl+C 退出"],
  ["send   Ctrl+J newline   Ctrl+T transcript   Ctrl+C quit", "发送   Ctrl+J 换行   Ctrl+T 记录   Ctrl+C 退出"],
  
  // 其他界面元素
  ["Explain this codebase", "解释这个代码库"],
  ["Write tests for", "为...编写测试"],
  ["▌ Summarize recent commits", "▌ 总结最近的提交"],
  
  // 常用状态词汇
  ["Error", "错误"],
  ["Warning", "警告"],
  ["Info", "信息"],
  ["Debug", "调试"],
  ["Success", "成功"],
  ["Failed", "失败"],
  ["Loading", "加载中"],
  ["Connecting", "连接中"],
  ["Connected", "已连接"],
  ["Disconnected", "已断开连接"],
  ["Timeout", "超时"],
  ["Retry", "重试"],
  ["Cancel", "取消"],
  ["Continue", "继续"],
  ["Yes", "是"],
  ["No", "否"],
  ["OK", "确定"],
  ["Done", "完成"],
  
  // 新增交互命令界面翻译
  ["Starting a new chat will clear the current conversation history.", "开始新的聊天将清除当前的对话历史记录。"],
  ["Continue with new chat?", "继续开始新聊天？"],
  ["New chat started.", "已开始新聊天。"],
  ["Chat cancelled.", "聊天已取消。"],
  ["Generating AGENTS.md file...", "正在生成 AGENTS.md 文件..."],
  ["AGENTS.md file created successfully.", "AGENTS.md 文件创建成功。"],
  ["Failed to create AGENTS.md file.", "创建 AGENTS.md 文件失败。"],
  ["Compacting conversation...", "正在压缩对话..."],
  ["Conversation compacted successfully.", "对话压缩成功。"],
  ["Failed to compact conversation.", "对话压缩失败。"],
  ["Showing git diff...", "正在显示 git 差异..."],
  ["No changes found.", "未找到更改。"],
  ["Mentioning file...", "正在提及文件..."],
  ["File mentioned successfully.", "文件提及成功。"],
  ["Logging out...", "正在退出登录..."],
  ["Logged out successfully.", "退出登录成功。"],
  ["Logout cancelled.", "退出登录已取消。"],
  
  // 额外的交互界面翻译
  ["Generate a file named AGENTS.md that serves as a contributor guide for this repository.", "生成一个名为 AGENTS.md 的文件，作为此仓库的贡献者指南。"],
  ["Your goal is to produce a clear, concise, and well-structured document with descriptive headings and actionable", "您的目标是生成一个清晰、简洁且结构良好的文档，包含描述性标题和可操作的"],
  ["explanations for each section.", "每个部分的说明。"],
  ["Follow the outline below, but adapt as needed — add sections if relevant, and omit those that do not apply to this", "遵循以下大纲，但根据需要进行调整——添加相关部分，省略不适用于此"],
  ["project.", "项目的部分。"],
  ["Document Requirements", "文档要求"],
  ["- Title the document", "- 将文档标题设为"],
  ["Repository Guidelines", "仓库指南"],
  ["- Use Markdown headings (#, ##, etc.) for structure.", "- 使用 Markdown 标题（#、##等）来构建结构。"],
  ["- Keep the document concise. 200-400 words is optimal.", "- 保持文档简洁。200-400 字是最佳长度。"],
  ["- Keep explanations short, direct, and specific to this repository.", "- 保持解释简短、直接，并针对此仓库。"],
  ["- Provide examples where helpful (commands, directory paths, naming patterns).", "- 在有用的地方提供示例（命令、目录路径、命名模式）。"],
  ["- Maintain a professional, instructional tone.", "- 保持专业、指导性的语调。"],
  ["Recommended Sections", "推荐部分"],
  ["Project Structure & Module Organization", "项目结构和模块组织"],
  ["Build, Test, and Development Commands", "构建、测试和开发命令"],
  ["- List key commands for building, testing, and running locally (e.g., npm test, make build).", "- 列出构建、测试和本地运行的关键命令（例如，npm test、make build）。"],
  ["- Briefly explain what each command does.", "- 简要解释每个命令的作用。"],
  ["Coding Style & Naming Conventions", "编码风格和命名约定"],
  ["- Specify indentation rules, language-specific style preferences, and naming patterns.", "- 指定缩进规则、特定语言的风格偏好和命名模式。"],
  ["- Include any formatting or linting tools used.", "- 包含使用的任何格式化或代码检查工具。"],
  ["Testing Guidelines", "测试指南"],
  ["- Identify testing frameworks and coverage requirements.", "- 确定测试框架和覆盖率要求。"],
  ["- State test naming conventions and how to run tests.", "- 说明测试命名约定和如何运行测试。"],
  ["Commit & Pull Request Guidelines", "提交和拉取请求指南"],
  ["- Summarize commit message conventions found in the project's Git history.", "- 总结项目 Git 历史中找到的提交消息约定。"],
  ["- Outline pull request requirements (descriptions, linked issues, screenshots, etc.).", "- 概述拉取请求要求（描述、关联问题、截图等）。"],
  ["(Optional) Add other sections if relevant, such as Security & Configuration Tips, Architecture Overview, or Agent-", "（可选）如果相关，添加其他部分，例如安全和配置提示、架构概述或代理"],
  ["Specific Instructions.", "特定指令。"],
  ["■ To use Codex with your ChatGPT plan, upgrade to Plus: https://openai.com/chatgpt/pricing.", "■ 要在您的 ChatGPT 计划中使用 Codex，请升级到 Plus：https://openai.com/chatgpt/pricing。"],
  
  // 更多交互命令可能的输出
  ["Enter file path or pattern:", "输入文件路径或模式："],
  ["File not found.", "未找到文件。"],
  ["Invalid command.", "无效命令。"],
  ["Command completed.", "命令完成。"],
  ["Processing...", "处理中..."],
  ["Please wait...", "请稍候..."],
  ["Operation cancelled.", "操作已取消。"],
  ["Do you want to continue?", "您想继续吗？"],
  ["(y/n)", "（是/否）"],
  ["Type 'help' for available commands.", "输入 'help' 查看可用命令。"],
  ["Available commands:", "可用命令："],
  ["Command not recognized.", "命令无法识别。"],
  ["Session ended.", "会话结束。"],
  ["Reconnecting...", "重新连接中..."],
  ["Connection lost.", "连接丢失。"],
  ["Saving...", "保存中..."],
  ["Saved successfully.", "保存成功。"],
  ["Save failed.", "保存失败。"],
  ["Loading configuration...", "加载配置中..."],
  ["Configuration loaded.", "配置已加载。"],
  ["Invalid configuration.", "配置无效。"],
  ["Resetting to defaults...", "重置为默认值..."],
  ["Reset complete.", "重置完成。"],
  ["Updating...", "更新中..."],
  ["Update complete.", "更新完成。"],
  ["Update failed.", "更新失败。"],
  ["Checking status...", "检查状态中..."],
  ["Status check complete.", "状态检查完成。"],
  ["No status available.", "无可用状态。"],
  ["Initializing...", "初始化中..."],
  ["Initialization complete.", "初始化完成。"],
  ["Initialization failed.", "初始化失败。"],
  ["Cleaning up...", "清理中..."],
  ["Cleanup complete.", "清理完成。"],
  ["Validating...", "验证中..."],
  ["Validation successful.", "验证成功。"],
  ["Validation failed.", "验证失败。"],
  ["Preparing...", "准备中..."],
  ["Ready.", "就绪。"],
  ["Not ready.", "未就绪。"],
  ["Timeout occurred.", "发生超时。"],
  ["Retrying...", "重试中..."],
  ["Maximum retries reached.", "已达到最大重试次数。"],
  ["Connection established.", "连接已建立。"],
  ["Connection failed.", "连接失败。"],
  ["Disconnecting...", "断开连接中..."],
  ["Disconnected.", "已断开连接。"]
];

// 检查是否需要翻译
function needsTranslation() {
  const args = process.argv.slice(2);
  return args.includes('--help') || args.includes('-h') || args.includes('help') || args.length === 0;
}

// 最终的文本翻译（去重优化）
function finalTranslateText(text) {
  if (!needsTranslation()) {
    return text;
  }
  
  let result = text;
  // 按长度排序，优先匹配长字符串，避免部分替换
  const sortedTranslations = finalTranslations.sort((a, b) => b[0].length - a[0].length);
  
  for (const [en, zh] of sortedTranslations) {
    result = result.split(en).join(zh);
  }
  return result;
}

// 备份原始文件
function backupOriginalFiles(codexPath) {
  const binPath = path.join(codexPath, 'bin');
  const codexJsPath = path.join(binPath, 'codex.js');
  const backupJsPath = path.join(binPath, 'codex.original.js');
  
  if (fs.existsSync(codexJsPath) && !fs.existsSync(backupJsPath)) {
    fs.copyFileSync(codexJsPath, backupJsPath);
    console.log('✅ 已备份原始 codex.js 文件');
  }
}

// 创建最终去重汉化版本
function createFinalDedupLocalizedCodexJs(codexPath) {
  const binPath = path.join(codexPath, 'bin');
  const codexJsPath = path.join(binPath, 'codex.js');
  const backupJsPath = path.join(binPath, 'codex.original.js');
  
  if (!fs.existsSync(backupJsPath)) {
    if (fs.existsSync(codexJsPath)) {
      fs.copyFileSync(codexJsPath, backupJsPath);
    }
  }
  
  const finalDedupLocalizedCodexJs = `#!/usr/bin/env node
import path from "path";
import { fileURLToPath } from "url";
import { spawn } from "child_process";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 最终去重的翻译映射
const finalTranslations = ${JSON.stringify(finalTranslations, null, 2)};

// 检查是否需要翻译
function needsTranslation() {
  const args = process.argv.slice(2);
  return args.includes('--help') || args.includes('-h') || args.includes('help') || args.length === 0;
}

// 最终的文本翻译（去重优化）
function finalTranslateText(text) {
  if (!needsTranslation()) {
    return text;
  }
  
  let result = text;
  // 按长度排序，优先匹配长字符串，避免部分替换
  const sortedTranslations = finalTranslations.sort((a, b) => b[0].length - a[0].length);
  
  for (const [en, zh] of sortedTranslations) {
    result = result.split(en).join(zh);
  }
  return result;
}

const { platform, arch } = process;

let targetTriple = null;
switch (platform) {
  case "linux":
  case "android":
    switch (arch) {
      case "x64":
        targetTriple = "x86_64-unknown-linux-musl";
        break;
      case "arm64":
        targetTriple = "aarch64-unknown-linux-musl";
        break;
      default:
        break;
    }
    break;
  case "darwin":
    switch (arch) {
      case "x64":
        targetTriple = "x86_64-apple-darwin";
        break;
      case "arm64":
        targetTriple = "aarch64-apple-darwin";
        break;
      default:
        break;
    }
    break;
  case "win32":
    switch (arch) {
      case "x64":
        targetTriple = "x86_64-pc-windows-msvc.exe";
        break;
      case "arm64":
        targetTriple = "aarch64-pc-windows-msvc.exe";
        break;
      default:
        break;
    }
    break;
  default:
    break;
}

if (!targetTriple) {
  throw new Error(\`Unsupported platform: \${platform} (\${arch})\`);
}

const binaryPath = path.join(__dirname, \`codex-\${targetTriple}\`);

async function tryImport(moduleName) {
  try {
    return await import(moduleName);
  } catch (err) {
    return null;
  }
}

async function resolveRgDir() {
  const ripgrep = await tryImport("@vscode/ripgrep");
  if (!ripgrep?.rgPath) {
    return null;
  }
  return path.dirname(ripgrep.rgPath);
}

function getUpdatedPath(newDirs) {
  const pathSep = process.platform === "win32" ? ";" : ":";
  const existingPath = process.env.PATH || "";
  const updatedPath = [
    ...newDirs,
    ...existingPath.split(pathSep).filter(Boolean),
  ].join(pathSep);
  return updatedPath;
}

const additionalDirs = [];
const rgDir = await resolveRgDir();
if (rgDir) {
  additionalDirs.push(rgDir);
}
const updatedPath = getUpdatedPath(additionalDirs);

// 对于需要翻译的命令，进行最终翻译处理
if (needsTranslation()) {
  const child = spawn(binaryPath, process.argv.slice(2), {
    stdio: ["inherit", "pipe", "pipe"],
    env: { ...process.env, PATH: updatedPath, CODEX_MANAGED_BY_NPM: "1" },
  });

  child.on("error", (err) => {
    console.error(err);
    process.exit(1);
  });

  // 实时翻译输出
  child.stdout.on('data', (data) => {
    const text = data.toString('utf8');
    const translated = finalTranslateText(text);
    process.stdout.write(translated);
  });
  
  child.stderr.on('data', (data) => {
    const text = data.toString('utf8');
    const translated = finalTranslateText(text);
    process.stderr.write(translated);
  });

  child.on('close', (code) => {
    process.exit(code || 0);
  });

  const forwardSignal = (signal) => {
    if (child.killed) {
      return;
    }
    try {
      child.kill(signal);
    } catch {
      /* ignore */
    }
  };

  ["SIGINT", "SIGTERM", "SIGHUP"].forEach((sig) => {
    process.on(sig, () => forwardSignal(sig));
  });
} else {
  // 非翻译命令，完全透明传递
  const child = spawn(binaryPath, process.argv.slice(2), {
    stdio: "inherit",
    env: { ...process.env, PATH: updatedPath, CODEX_MANAGED_BY_NPM: "1" },
  });

  child.on("error", (err) => {
    console.error(err);
    process.exit(1);
  });

  const forwardSignal = (signal) => {
    if (child.killed) {
      return;
    }
    try {
      child.kill(signal);
    } catch {
      /* ignore */
    }
  };

  ["SIGINT", "SIGTERM", "SIGHUP"].forEach((sig) => {
    process.on(sig, () => forwardSignal(sig));
  });

  const childResult = await new Promise((resolve) => {
    child.on("exit", (code, signal) => {
      if (signal) {
        resolve({ type: "signal", signal });
      } else {
        resolve({ type: "code", exitCode: code ?? 1 });
      }
    });
  });

  if (childResult.type === "signal") {
    process.kill(process.pid, childResult.signal);
  } else {
    process.exit(childResult.exitCode);
  }
}
`;
  
  fs.writeFileSync(codexJsPath, finalDedupLocalizedCodexJs);
  console.log('✅ 已创建最终去重汉化版本的 codex.js');
}

// 恢复原始文件
function restoreOriginalFiles(codexPath) {
  const binPath = path.join(codexPath, 'bin');
  const codexJsPath = path.join(binPath, 'codex.js');
  const backupJsPath = path.join(binPath, 'codex.original.js');
  
  if (fs.existsSync(backupJsPath)) {
    fs.copyFileSync(backupJsPath, codexJsPath);
    console.log('✅ 已恢复原始 codex.js 文件');
  }
}

// 主函数
function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'inject';
  
  const codexPath = getCodexPath();
  console.log('🔍 Codex CLI 安装路径:', codexPath);
  
  switch (command) {
    case 'inject':
      console.log('🚀 开始注入最终去重版中文汉化...');
      console.log('🔄 已去除重复翻译条目，优化性能');
      console.log('📋 包含所有用户界面文本的翻译，包括交互命令');
      backupOriginalFiles(codexPath);
      createFinalDedupLocalizedCodexJs(codexPath);
      console.log('🎉 最终去重版中文汉化注入完成！');
      console.log('💡 现在可以运行 codex --help 查看完整汉化效果');
      console.log('💡 可以测试交互命令：/model /approvals /review /new /init /compact /diff /mention /status /mcp /logout');
      break;
      
    case 'restore':
      console.log('🔄 恢复原始文件...');
      restoreOriginalFiles(codexPath);
      console.log('✅ 已恢复原始文件');
      break;
      
    case 'status':
      const binPath = path.join(codexPath, 'bin');
      const hasBackup = fs.existsSync(path.join(binPath, 'codex.original.js'));
      
      console.log('📊 汉化状态:');
      console.log('  备份文件:', hasBackup ? '✅ 存在' : '❌ 不存在');
      console.log('  汉化类型: 最终去重版本');
      console.log('  翻译数量:', finalTranslations.length, '条');
      console.log('  特点: 去除重复条目，优化性能');
      break;
      
    default:
      console.log('用法: node inject-chinese-final-dedup.js [inject|restore|status]');
      console.log('  inject  - 注入最终去重版中文汉化（默认）');
      console.log('  restore - 恢复原始文件');
      console.log('  status  - 查看汉化状态');
      break;
  }
}

main();

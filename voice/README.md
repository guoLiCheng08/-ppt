# Codex 语音总结

本目录提供一个本地 MCP 工具 `speak_text`，让 Codex 在任务完成时把简短总结交给 Windows 语音合成器朗读。

## MCP 配置

在 Codex 配置的 `[mcp_servers]` 下加入：

```toml
[mcp_servers.codex_local_voice]
command = "node"
args = ["D:\\project\\课件准备\\voice\\server.mjs"]
startup_timeout_sec = 10
```

修改后重启 Codex，使 MCP 配置重新加载。

## 使用方式

完成任务时，先生成不超过三句话的总结，再调用 `speak_text`：

```text
任务已经完成。已生成目标文件，并通过了测试。请检查最终输出。
```

如果系统没有安装中文语音包，脚本会自动回退到 Windows 默认语音。可以在“设置 → 时间和语言 → 语音”中安装中文语音。

## 切换音色

当前电脑可用音色包括：

- `Microsoft Huihui Desktop`：中文
- `Microsoft Zira Desktop`：英文

手动指定音色：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\voice\codex-voice.ps1 -Text '这是中文音色测试' -VoiceName 'Microsoft Huihui Desktop'
```

通过 MCP 调用时，在参数中增加 `voiceName` 即可；不填写时默认选择中文音色。

MCP 朗读内容会自动加上“主人，”前缀；如果传入内容已经以“主人”开头，则不会重复添加。

## 手动测试

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\voice\codex-voice.ps1 -Text '语音测试成功'
```

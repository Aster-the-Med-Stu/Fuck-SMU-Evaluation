# Fuck-SMU-Evaluation

辣鸡评教系统

我实在没想到有什么合适的形容词去形容这个评教系统，可以说是强制给学生喂💩

目前而言把这个思路翻译为 Python，移植到别的平台已经超出我能力，光一个微信模拟登录我就没有研究过，所以只能依靠抓包……对于各位而言需要费些事。

# 准备工作

## 硬件

- 一台装着 **Windows 10** 的笔记本电脑，系统版本需要高于 1607（如果您自动更新没关的话肯定比这个新），当然如果您知道 MinGW 或者 cygwin 为何物可以直接无视这条

## 软件

- 电脑版微信
- **W**indows **S**ubsystem for **L**inux 或者 Cygwin 之类的类 UNIX 环境
- PowerBI（可以在应用商店找到）
- SocksCap64
- mitmproxy
- Notepad++ 之类的高级文本编辑器（下文将以 Notepad++ 为例介绍）
- Office 2013 and later（我不知道 WPS 有没有需要的函数，特别是 ```ENCODEURL()```，如果谁试过的话不妨开个 issue 告知一下）

~~在这里顺带安利一下 scoop 和 Anaconda 全家桶~~

# 步骤


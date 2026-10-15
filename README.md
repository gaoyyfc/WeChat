# WeChat / 烟火有主意内容仓库

这个仓库用于保存微信公众号「烟火有主意」的正式文章、草稿、配图源文件、生成提示词和 WeMD 辅助工具。仓库同时作为公司电脑与家用电脑之间的工作同步中心。

> 当前远端地址：<https://github.com/gaoyyfc/WeChat>

## 目录说明

```text
articles/                 可直接在 WeMD 中打开的正式文章
  <序号-主题>/
    article.md            正式稿，每个目录只保留这一份正式稿
    images/               本地图片源文件备份
.assets/articles/         草稿、分析、提示词、脚本和中间版本
.assets/archive/          已归档的历史制作资料
.wemd/                    WeMD 工作区主题配置
.agents/                  项目使用的本地技能说明
tools/                    图片上传与正式稿检查脚本
AGENTS.md                 AI 协作时必须遵守的项目规则
```

正式文章中的图片应使用 `https://img.wemd.app/...` 地址。本地 `images/` 只负责保存图片源文件，不能作为最终文章的图片链接。

## 公司电脑首次配置

先安装 [Git](https://git-scm.com/downloads) 和 WeMD，然后在希望存放项目的父目录打开 PowerShell：

```powershell
git clone https://github.com/gaoyyfc/WeChat.git WEMD
cd WEMD
git config user.name "Yue Gao"
git config user.email "gaoyueyfc@163.com"
```

首次 `pull` 或 `push` 时，按 GitHub 的提示登录。GitHub 不再接受账号密码直接用于 Git 操作；可使用浏览器登录、Git Credential Manager、Personal Access Token 或 SSH。

不要在公司电脑上重新执行 `git init`，也不要手动从网页下载 ZIP 覆盖工作目录。克隆一次后一直在同一个目录中工作即可。

## 每次开始工作

无论在公司还是家里，动手修改前先进入项目目录并拉取最新内容：

```powershell
cd D:\WEMD   # 按这台电脑的实际路径修改
git status
git pull --rebase
```

看到 `Already up to date.` 后再开始工作。如果 `git status` 显示有未提交改动，先提交或暂存这些改动，不要直接强行拉取。

## 每次结束工作

及时提交并推送，不要把未同步的修改只留在一台电脑上：

```powershell
git status
git add -A
git commit -m "内容：简要说明本次修改"
git pull --rebase
git push
```

提交信息建议使用下面的格式：

- `内容：完成某篇文章初稿`
- `配图：补充某篇文章图片`
- `修改：精修某篇文章正文`
- `归档：整理某篇文章制作文件`
- `工具：更新 WeMD 辅助脚本`

回家后让我同步时，可以直接说：“先从远端拉取最新内容，再继续处理第 X 篇文章。”我会先检查本地状态，然后执行 `git pull --rebase`，不会覆盖尚未提交的本地修改。

## 新文章的推荐流程

1. 在 `.assets/articles/<主题>/` 中保存初稿、分析、提示词、生成脚本和历史版本。
2. 定稿后在 `articles/<序号-主题>/article.md` 中保存唯一正式稿。
3. 图片源文件保存在同级 `images/` 目录。
4. 上传图片到 WeMD 官方图床：

   ```powershell
   .\tools\upload-wemd-images.ps1 -Path .\articles\<序号-主题>\images\图片.png
   ```

5. 把脚本返回的远程地址写入 `article.md`。
6. 交稿前检查所有图片链接：

   ```powershell
   .\tools\check-wemd-article.ps1 .\articles\<序号-主题>\article.md
   ```

7. 确认正式文章目录只保留 `article.md` 和 `images/`，再提交并推送。

更完整的文章目录、文风和图片规则见 [AGENTS.md](./AGENTS.md)。

## 两台电脑协作注意事项

- 一台电脑结束工作时先 `commit` 和 `push`，另一台电脑开始工作时先 `pull --rebase`。
- 尽量不要在两台电脑上同时修改同一个文件，尤其是 PNG、ZIP 等二进制文件；Git 无法自动合并二进制冲突。
- 不提交 `.env`、访问令牌、账号密码或其他凭据。图片和文章可以提交，密钥不可以。
- 不使用 `git push --force`。如果出现冲突，先保留两边内容并逐个处理，再继续 rebase。
- 本仓库包含较多图片，第一次克隆会比普通文字仓库慢，这是正常现象。

## 冲突处理

执行 `git pull --rebase` 后如果出现冲突：

```powershell
git status
```

打开状态中标记为冲突的文件，保留正确内容并删除 `<<<<<<<`、`=======`、`>>>>>>>` 标记，然后执行：

```powershell
git add <已处理的文件>
git rebase --continue
```

如果暂时无法判断应保留哪一版，不要强推，也不要删除文件；停止操作并让我协助检查即可。

## 常用检查

```powershell
git status                 # 查看本地是否有未提交修改
git log --oneline -10      # 查看最近 10 次提交
git remote -v              # 查看关联的远端仓库
git diff                   # 查看尚未暂存的文字修改
git diff --staged          # 查看即将提交的修改
```

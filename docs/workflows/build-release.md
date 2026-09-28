# 构建与发布工作流

## 一、全链构建（每次改动后必跑）

```cmd
python tl_work\chain_build.py --apply
```

五步：pending 校验 → build → compile → manifest 同步 → check（细节见 [translation.md](translation.md) §三）。

**必须逐项独立确认，脚本不会在所有失败点自动停止：**

| 检查点 | 通过标志 |
| --- | --- |
| 挂起改动 | `未应用清单行: 0` |
| compile | `compile 退出码: 0` |
| screens.rpy 复原 | 无遗留 `payload/game/screens.rpy.__tmp` |
| manifest 同步 | 无报错（`.rpyc` 每次编译哈希都变，**不同步则 check 必失配**） |
| 完整性 | `Payload files/hashes: OK (68)` + `Check result: OK` |

对游戏目录复验（安装态）：

```cmd
python tools\patch_tool.py verify --game-dir "<游戏目录>"
```

## 二、版本号与 changelog

```cmd
python tl_work\bump_version.py 1.3.12 "v1.3.12: 更新说明……"
```

- 就地更新 `manifest.json` 的 `version` 并追加 `notes`，保留 CRLF 与 3 空格缩进。
- manifest 的 `version` 与 `notes` 必须与发布内容同步——安装器向用户展示它们。

## 三、发布（GitHub Actions，本地不打包）

1. 全链验证通过 → 提交（建议信息格式：`release: prepare PC Chinese patch vX.Y.Z`）。
2. **写发布说明**：`docs/release-notes/vX.Y.Z.md`（完整内容，不是一个 changelog 链接——CI 用 `--notes-file` 直接引用该文件，**文件缺失则发版失败**）。格式参照 [../release-notes/v1.3.11.md](../release-notes/v1.3.11.md)。
3. 打 tag 并推送：

```cmd
git tag vX.Y.Z
git push origin master --tags
```

4. `.github/workflows/release-standalone.yml` 触发：Windows runner + PyInstaller 6.19.0 单文件构建 `WoC-ChinesePatch.exe`（内嵌 `manifest.json` + `payload/`）→ `gh release create` 发布。
5. 到 Actions 确认 run 成功、Release 页面附件与说明完整。

**发布一律新增，不覆盖旧版。**

仅构建不发布：推送涉及 `manifest.json` / `payload/**` / `tools/patch_tool.py` 的提交会触发 `build-standalone.yml`，可在 Actions 下载 artifact 自检。

## 四、发布前核对清单

- [ ] `chain_build.py --apply` 五项检查点全绿
- [ ] `patch_tool.py check --game-dir "<游戏目录>"` 与 `verify` 通过
- [ ] `bump_version.py` 已更新 version + notes
- [ ] `docs/release-notes/vX.Y.Z.md` 已创建（完整说明）
- [ ] README「当前版本」与更新小节已更新
- [ ] 提交 + tag + 推送完成，CI run 成功

## 五、版本号约定

- 定稿发布用 `x.y.z`；迭代中如需标记中间态可用 `x.y.z-dev`，发布前去掉。
- tag 名与 manifest version 一致（`v` 前缀只在 tag 上）。

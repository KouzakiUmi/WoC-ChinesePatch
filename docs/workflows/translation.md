# 翻译工作流

译文唯一来源是 `tl_work/chunks/` 下的分块 TSV；`payload/game/tl/chinese/*.rpy` 全部由它构建生成，**永不直接手改**。

## 一、译文源格式

```
tl_work/chunks/
├── dialogue/dialogue_0001.tsv … dialogue_0026.tsv   # 对白与旁白，10 370 块
└── strings/strings_0001.tsv … strings_0003.tsv      # 界面串，1 253 条
```

**dialogue 每行 6 列**（Tab 分隔）：

```
seq ⇥ block ⇥ idx ⇥ speaker ⇥ source(英文) ⇥ target(中文)
```

**strings 每行 4 列**：

```
seq ⇥ kind ⇥ source(英文) ⇥ target(中文)
```

格式要点：

- 以 `#` 开头的行是注释/表头，构建时跳过；文件可含 BOM。
- **只改最后一列 `target`**。`seq`/`speaker`/`source`/结构一律不动。
- 换行写作字面两字符 `\n`（不是真实换行）；真实换行会产生孤儿行，游戏内表现为缺行（历史事故：0003#1196、0021#8162）。
- Ren'Py 转义：译文里需要字面 `[` 时写 `[[`；`{}` 标签与 `[]` 插值必须与英文 0 不一致。
- 界面串（strings）：简短、**无句末句号**、保留 `%` 与 `[...]` 占位符。

## 二、译文如何生效（Ren'Py 机制）

1. `build` 把 TSV 生成 `payload/game/tl/chinese/*.rpy` 的 `translate chinese ...` 块（5 组）。
2. `payload/game/zzz_chinese_language.rpy` 里 `define config.language = "chinese"`，启动即中文。
3. **运行时钩子**：`renpy.notify()` / `renpy.input()` 的裸 Python 字符串不被翻译提取覆盖，补丁在 `zzz_chinese_language.rpy` 中包装这两个函数，先查字符串表；39 条映射在同文件 `translate chinese strings:` 块内。不改动任何游戏原始脚本，卸载删该文件即还原。

## 三、构建链

```cmd
python tl_work\chain_build.py            :: dry-run：pending 校验 + build 差异预估
python tl_work\chain_build.py --apply    :: 全链：pending → build → compile → manifest 同步 → check
```

`--apply` 五步（详见 [build-release.md](build-release.md)）：

1. **挂起改动检查**：`review/work-fix/*.changes.tsv` 中仍有「当前值==基线值」的行则拒绝继续。
2. **build**：`tools/tl_tool.py build --tl-dir tl_work --game-root payload`。
3. **compile**：暂移 `payload/game/screens.rpy`（它依赖完整工程的 `gui.language`，不移会报错）→ 游戏 exe 编译 `.rpyc` → 复原。**该步骤非零不会中断脚本，必须独立确认 `compile 退出码: 0`。**
4. **manifest 同步**：`.rpyc` 每次编译哈希都变，必须同步，否则 check 失配。
5. **check**：`tools/patch_tool.py check` → `Payload files/hashes: OK (68)`。

## 四、编辑辅助脚本

历史批次的修复/生成脚本已归档至 `tl_work/archive/scripts/`（apply_full_review_*、apply_spirits_decisions、apply_monarchy_unify、sync_duplicate_long 等，清单见 `tl_work/archive/README.md`），可仿照其模式另写新批次。现役工具留在 `tl_work/` 根目录：`chain_build.py`、`tl_tool.py`、`bump_version.py`、`update_manifest_hash.py`、`repair_tags.py`、`render_opening_caption_text.py`、`flatten_png.py` 与各 `*_check.py` 专项扫描。

写新批次脚本的纪律：

- **默认 dry-run**，打印逐行 before/after；确认后 `--apply`。
- 逐行决策，不用正则批量替换了事——正则无法判断语境（「灵体体」双重转换、G2 并发误改 12 行，都是批量思维的事故）。
- TSV 中的 `\n` 是字面值：Python 里匹配用单行片段，多行 old-string 会匹配不上。

## 五、界面串与杂项

- 菜单项句式同构、不加句末句号。
- 开场 `Use Enter or Left Click...` 等运行时提示在 `zzz_chinese_language.rpy` 的 strings 块里改，不在 TSV。
- 存档界面动态标签在 `payload/game/screens.rpy`（补丁直接携带该文件）。

# 嵌套站网预报信息价值

**个人兴趣自学 · 无导师指导 · 曾投 HSJ（HSJ-2026-0755）退稿 · 尚无录用**

作者：张森捷（Senjie Zhang），兰州大学 · `3079099853@qq.com`  
仓库：https://github.com/Az0998/forecast-information-value

## 这个项目在做什么

嵌套水文站网**不是** CAMELS 式集总「降水→径流」对象：预报点明天的流量，很大一部分已经写在今天的上游过程线里。本项目问的是：

> 相对简单路由 / 持续性基线，**上游站与降水预见信息还值不值得用？** 在什么气候带、什么预见期还有增益？洪水事件分（CSI）会不会和 NSE 打架？

对象：21 组有文档可查的 USGS / 加拿大 WSC 嵌套站网；工具含滞后上游线性路由、梯度提升树、持续性、降水上限与 p90 洪水 CSI（block-bootstrap）。

## 推荐阅读（写得较完整的文稿）

| 材料 | 说明 | 链接 |
|------|------|------|
| **英文摘要** | 最短入口 | [paper/abstract.txt](./paper/abstract.txt) |
| **英文手稿草稿** | 在线可读全文 | [paper/manuscript_draft.md](./paper/manuscript_draft.md) |
| **Cover letter** | 投稿说明 | [paper/cover_letter.txt](./paper/cover_letter.txt) |
| **HESS 投稿 Word/PDF**（若已推送） | 当前主攻叙事 | `paper/HESS_nested_information_value.docx` / `.pdf` |
| **早期同主题实验** | Potomac 协议仓 | [hydro-ml-paper](https://github.com/Az0998/hydro-ml-paper) |

## 与 Mask-View 的关系

姊妹仓 [maskview-aquatic-protocol](https://github.com/Az0998/maskview-aquatic-protocol) 问的是水质监测里「插值能不能用、错了会不会毁掉预警」；本仓问的是河流预报里「嵌套信息还值不值钱」。两条线都强调：**相对简单基线的决策/信息价值，而不是新网络刷榜。**

## 快速复现

```bash
pip install -r requirements.txt
python scripts/build_hess_figures.py
python scripts/build_hess_manuscript.py
python scripts/verify_submission.py
```

详见 `paper/HOW_TO_SUBMIT_HESS.md`、`REPRODUCE.md`（若存在）。

## License

MIT

---

# Nested information-value atlas (English)

River-only research article. Best readable draft: [`paper/manuscript_draft.md`](./paper/manuscript_draft.md) · abstract: [`paper/abstract.txt`](./paper/abstract.txt).

**Author:** Senjie Zhang, Lanzhou University (`3079099853@qq.com`)

Operational nested gauges are not CAMELS lumped rainfall–runoff. The object is a regime model of information value on 21 USGS/WSC nested networks with uncertainty.

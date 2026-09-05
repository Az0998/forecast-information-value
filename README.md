# 嵌套站网预报信息价值

> **一句话：** 嵌套水文站网里，上游站 / 降水对次日流量预报「还有没有用」——什么时候有增益、什么时候已经被路由基线吃满。个人兴趣自学；曾投 HSJ（HSJ-2026-0755）被退（偏案例），后续手稿面向 HESS，**尚无录用**。

**仓库：** https://github.com/Az0998/forecast-information-value  
**作者：** 张森捷（Senjie Zhang），兰州大学（`3079099853@qq.com`）

| 项目 | 说明 |
|------|------|
| 对象 | 21 组 USGS / 加拿大 WSC 嵌套站网（非 CAMELS 集总产流） |
| 方法 | 滞后上游线性路由、树模型、持续性基线；洪水 CSI + bootstrap |
| 复现 | `scripts/build_hess_*` 与冻结表 |
| 相关 | 早期同主题实验仓 [hydro-ml-paper](https://github.com/Az0998/hydro-ml-paper) |

---

# Nested information-value atlas

River-only research article aimed at *Hydrology and Earth System Sciences*.

**Author:** Senjie Zhang, Lanzhou University (`3079099853@qq.com`)

Operational nested gauges are not CAMELS lumped rainfall–runoff. The object is a regime model of information value on 21 USGS/WSC nested networks with uncertainty.

## Rebuild the Word/PDF package

```bash
pip install -r requirements.txt
python scripts/build_hess_figures.py
python scripts/build_hess_manuscript.py
python scripts/verify_submission.py
```

Upload files and Copernicus steps: `paper/HOW_TO_SUBMIT_HESS.md`

## License

MIT

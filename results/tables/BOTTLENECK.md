# Forecast information-value protocol

Standalone repo. Frozen numbers in `data/frozen/`.

## River (1-day)
| basin | climate | routing_NSE | lstm_attention_NSE | ablation_delta | attn_minus_routing |
| --- | --- | --- | --- | --- | --- |
| potomac | humid_mid_atlantic | 0.861 | 0.93 | 0.02 | 0.07 |
| james | humid_mid_atlantic | 0.92 | 0.933 | 0.129 | 0.013 |
| willamette | humid_pacific_nw | 0.97 | 0.99 | 0.003 | 0.02 |
| animas | snowmelt_rockies | 0.98 | 0.988 | 0.01 | 0.008 |
| verde | semiarid_southwest | 0.605 | 0.385 | 0.061 | -0.221 |

## Ocean multi-lead
| lead_mo | model | RMSE | skill_vs_persist | skill_vs_clim | hypoxia_F1 | CSI |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | persistence | 8.265 | 0.0 | -1.434 | 0.6 | 0.429 |
| 1 | climatology | 5.298 | 0.589 | 0.0 | 0.671 | 0.505 |
| 1 | lstm_anomaly | 5.311 | 0.587 | -0.005 | 0.665 | 0.498 |
| 1 | st_transformer | 3.876 | 0.78 | 0.465 | 0.741 | 0.588 |
| 1 | hybrid_clim_st | 3.876 | 0.78 | 0.465 | 0.741 | 0.588 |
| 2 | persistence | 14.815 | 0.0 | -7.031 | 0.357 | 0.217 |
| 2 | climatology | 5.228 | 0.875 | 0.0 | 0.719 | 0.561 |
| 2 | lstm_anomaly | 6.06 | 0.833 | -0.344 | 0.696 | 0.534 |
| 2 | st_transformer | 5.832 | 0.845 | -0.245 | 0.701 | 0.54 |
| 2 | hybrid_clim_st | 5.083 | 0.882 | 0.054 | 0.742 | 0.59 |
| 3 | persistence | 20.319 | 0.0 | -14.233 | 0.235 | 0.133 |
| 3 | climatology | 5.206 | 0.934 | 0.0 | 0.7 | 0.539 |
| 3 | lstm_anomaly | 7.537 | 0.862 | -1.096 | 0.629 | 0.458 |
| 3 | st_transformer | 9.81 | 0.767 | -2.551 | 0.537 | 0.367 |
| 3 | hybrid_clim_st | 5.222 | 0.934 | -0.006 | 0.703 | 0.542 |

## Bottlenecks
| domain | bottleneck | evidence |
| --- | --- | --- |
| river | usable precipitation foresight + unsaturated autocorrelation | James 1-d ablation ΔNSE +0.13; Willamette ~0; Verde LSTM can lose to routing |
| ocean | time-varying oxygen / coastal structure at lead ≥2 months | lead-1 ST beats clim; lead-2 hybrid/clim wins; Argo history +35% RMSE |
# Forecast information-value protocol

## River climate (all leads)
| basin | climate | horizon | persistence_NSE | routing_NSE | xgboost_NSE | lstm_attention_NSE | ablation_delta | attn_minus_routing |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| potomac | humid_mid_atlantic | 1 | 0.787 | 0.861 | 0.911 | 0.93 | 0.02 | 0.07 |
| potomac | humid_mid_atlantic | 3 | 0.164 | 0.38 | 0.463 | 0.426 | 0.091 | 0.047 |
| potomac | humid_mid_atlantic | 7 | -0.393 | 0.072 | 0.077 | 0.218 | 0.285 | 0.146 |
| james | humid_mid_atlantic | 1 | 0.773 | 0.92 | 0.939 | 0.933 | 0.129 | 0.013 |
| james | humid_mid_atlantic | 3 | 0.293 | 0.435 | 0.496 | 0.392 | 0.09 | -0.043 |
| james | humid_mid_atlantic | 7 | -0.052 | 0.235 | 0.292 | 0.309 | 0.011 | 0.074 |
| willamette | humid_pacific_nw | 1 | 0.95 | 0.97 | 0.986 | 0.99 | 0.003 | 0.02 |
| willamette | humid_pacific_nw | 3 | 0.73 | 0.771 | 0.804 | 0.754 | -0.036 | -0.018 |
| willamette | humid_pacific_nw | 7 | 0.418 | 0.51 | 0.499 | 0.361 | -0.113 | -0.149 |
| animas | snowmelt_rockies | 1 | 0.977 | 0.98 | 0.985 | 0.988 | 0.01 | 0.008 |
| animas | snowmelt_rockies | 3 | 0.895 | 0.904 | 0.911 | 0.856 | -0.025 | -0.048 |
| animas | snowmelt_rockies | 7 | 0.812 | 0.848 | 0.849 | 0.815 | 0.046 | -0.033 |
| verde | semiarid_southwest | 1 | 0.421 | 0.605 | 0.664 | 0.385 | 0.061 | -0.221 |
| verde | semiarid_southwest | 3 | -0.196 | 0.245 | -0.123 | 0.13 | 0.06 | -0.116 |
| verde | semiarid_southwest | 7 | -0.13 | 0.188 | -0.111 | 0.077 | -0.045 | -0.112 |

## River climate (1-day)
| basin | climate | persistence_NSE | routing_NSE | xgboost_NSE | lstm_attention_NSE | ablation_delta | attn_minus_routing |
| --- | --- | --- | --- | --- | --- | --- | --- |
| potomac | humid_mid_atlantic | 0.787 | 0.861 | 0.911 | 0.93 | 0.02 | 0.07 |
| james | humid_mid_atlantic | 0.773 | 0.92 | 0.939 | 0.933 | 0.129 | 0.013 |
| willamette | humid_pacific_nw | 0.95 | 0.97 | 0.986 | 0.99 | 0.003 | 0.02 |
| animas | snowmelt_rockies | 0.977 | 0.98 | 0.985 | 0.988 | 0.01 | 0.008 |
| verde | semiarid_southwest | 0.421 | 0.605 | 0.664 | 0.385 | 0.061 | -0.221 |

## River P90 CSI and LSTM oracle (Potomac)
| horizon | routing_CSI | xgb_CSI | attn_CSI | pers_CSI | attn_POD | attn_FAR | attn_obs_NSE | attn_oracle_NSE | delta_NSE |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0 | 0.622 | 0.745 | 0.75 | 0.56 | 0.846 | 0.132 | 0.932 | 0.931 | -0.001 |
| 3.0 | 0.2 | 0.333 | 0.288 | 0.162 | 0.385 | 0.464 | 0.444 | 0.565 | 0.121 |
| 7.0 | 0.038 | 0.08 | 0.26 | 0.064 | 0.333 | 0.458 | 0.218 | 0.414 | 0.196 |

## River GFS QPF vs oracle (Potomac 2024)
| horizon | obs_NSE | persist_NSE | qpf_NSE | oracle_NSE |
| --- | --- | --- | --- | --- |
| 1.0 | 0.893 | 0.939 | 0.923 | 0.926 |
| 3.0 | 0.406 | 0.34 | -0.035 | 0.577 |
| 7.0 | 0.094 | 0.228 | 0.228 | 0.45 |

## Ocean multi-lead (low-tail F1 = training p10, not hypoxia)
| lead_mo | model | RMSE | skill_vs_persist | skill_vs_clim | lowtail_F1 | CSI |
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

## Ocean coastal MAE
| bin | n_cells | mae | p90 |
| --- | --- | --- | --- |
| low | 648 | 2.968 | 4.228 |
| mid | 648 | 2.947 | 4.114 |
| high | 864 | 3.299 | 4.89 |

## Bottlenecks
| domain | bottleneck | evidence |
| --- | --- | --- |
| river | climate × model-class × lead; rain foresight after day 1 | James 1-d upstream ΔNSE +0.13 vs Willamette ≈0; Verde 1-d XGB 0.664 > routing 0.605 > LSTM 0.385; Verde 3/7-d XGB NSE negative; Willamette 7-d LSTM−routing -0.149; GFS QPF 3-d NSE −0.03 while oracle +0.58; LSTM P90 CSI still Potomac-only |
| ocean | learned anomaly skill collapses at lead ≥ 2 months; errors coastal | Lead-1 ST RMSE 3.88 vs clim 5.30; lead-2 hybrid 5.08 ≈ clim 5.23; Argo +35% RMSE; coastal MAE 3.30 vs 2.95 offshore; low-tail events are training p10 (195 µmol kg⁻¹), not hypoxia <60 |

## Climate-band P90 CSI (XGBoost protocol)
| basin | horizon | p90_cfs | n_test | persist_CSI | routing_CSI | xgb_CSI | persist_NSE | routing_NSE | xgb_NSE | n_events |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| verde | 1 | 402.0 | 1095 | 0.794 | 0.54 | 0.828 | 0.421 | 0.605 | 0.678 | 139 |
| verde | 3 | 402.0 | 1095 | 0.571 | 0.553 | 0.513 | -0.196 | 0.245 | 0.242 | 139 |
| verde | 7 | 402.0 | 1095 | 0.495 | 0.494 | 0.412 | -0.13 | 0.188 | 0.198 | 139 |
| james | 1 | 15700.0 | 1095 | 0.588 | 0.775 | 0.845 | 0.773 | 0.92 | 0.941 | 77 |
| james | 3 | 15700.0 | 1095 | 0.238 | 0.256 | 0.364 | 0.293 | 0.435 | 0.479 | 77 |
| james | 7 | 15700.0 | 1095 | 0.194 | 0.092 | 0.16 | -0.052 | 0.235 | 0.288 | 77 |
| potomac | 1 | 26200.0 | 1093 | 0.56 | 0.622 | 0.766 | 0.787 | 0.861 | 0.92 | 39 |
| potomac | 3 | 26200.0 | 1093 | 0.162 | 0.2 | 0.328 | 0.164 | 0.38 | 0.465 | 39 |
| potomac | 7 | 26200.0 | 1093 | 0.064 | 0.038 | 0.075 | -0.393 | 0.072 | 0.11 | 39 |
| willamette | 1 | 47600.0 | 1095 | 0.761 | 0.807 | 0.835 | 0.95 | 0.97 | 0.985 | 96 |
| willamette | 3 | 47600.0 | 1095 | 0.52 | 0.52 | 0.61 | 0.73 | 0.771 | 0.805 | 96 |
| willamette | 7 | 47600.0 | 1095 | 0.322 | 0.29 | 0.317 | 0.418 | 0.51 | 0.511 | 96 |
| animas | 1 | 1860.0 | 1095 | 0.925 | 0.914 | 0.904 | 0.977 | 0.98 | 0.984 | 103 |
| animas | 3 | 1860.0 | 1095 | 0.823 | 0.886 | 0.829 | 0.895 | 0.904 | 0.912 | 103 |
| animas | 7 | 1860.0 | 1095 | 0.661 | 0.687 | 0.687 | 0.812 | 0.848 | 0.847 | 103 |

## Climate-band XGB oracle precipitation
| basin | horizon | xgb_obs_NSE | xgb_oracle_NSE | delta_NSE | n_aligned |
| --- | --- | --- | --- | --- | --- |
| verde | 1 | 0.678 | 0.646 | -0.032 | 1094 |
| verde | 3 | 0.242 | 0.513 | 0.271 | 1092 |
| verde | 7 | 0.198 | 0.336 | 0.139 | 1088 |
| james | 1 | 0.941 | 0.939 | -0.003 | 1094 |
| james | 3 | 0.479 | 0.649 | 0.17 | 1092 |
| james | 7 | 0.294 | 0.476 | 0.182 | 1088 |
| potomac | 1 | 0.92 | 0.928 | 0.008 | 1092 |
| potomac | 3 | 0.465 | 0.709 | 0.244 | 1090 |
| potomac | 7 | 0.114 | 0.46 | 0.347 | 1086 |
| willamette | 1 | 0.985 | 0.987 | 0.002 | 1094 |
| willamette | 3 | 0.805 | 0.917 | 0.112 | 1092 |
| willamette | 7 | 0.518 | 0.823 | 0.305 | 1088 |
| animas | 1 | 0.984 | 0.985 | 0.001 | 1094 |
| animas | 3 | 0.912 | 0.92 | 0.008 | 1092 |
| animas | 7 | 0.847 | 0.852 | 0.005 | 1088 |

## Bow River Canada (non-US transfer) P90 CSI
| basin | horizon | p90_cfs | n_test | persist_CSI | routing_CSI | xgb_CSI | persist_NSE | routing_NSE | xgb_NSE | xgb_local_NSE | ablation_delta | n_events |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bow | 1 | 202.0 | 756 | 0.85 | 0.855 | 0.886 | 0.973 | 0.976 | 0.871 | 0.79 | 0.082 | 74 |
| bow | 3 | 202.0 | 756 | 0.644 | 0.795 | 0.783 | 0.88 | 0.896 | 0.916 | 0.706 | 0.21 | 74 |
| bow | 7 | 202.0 | 756 | 0.41 | 0.505 | 0.618 | 0.723 | 0.729 | 0.857 | 0.82 | 0.037 | 74 |

## Bow River XGB oracle precipitation
| basin | horizon | xgb_obs_NSE | xgb_oracle_NSE | delta_NSE | n_aligned |
| --- | --- | --- | --- | --- | --- |
| bow | 1 | 0.871 | 0.865 | -0.006 | 755 |
| bow | 3 | 0.916 | 0.466 | -0.45 | 753 |
| bow | 7 | 0.856 | 0.72 | -0.135 | 749 |

## Linear vs XGB precipitation ceiling
| basin | horizon | lin_obs_NSE | lin_oracle_NSE | lin_delta_NSE | xgb_obs_NSE | xgb_oracle_NSE | xgb_delta_NSE | n_lin | n_xgb |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| potomac | 1 | 0.874 | 0.876 | 0.003 | 0.92 | 0.928 | 0.008 | 1092 | 1092 |
| potomac | 3 | 0.333 | 0.407 | 0.074 | 0.465 | 0.709 | 0.244 | 1090 | 1090 |
| potomac | 7 | -0.013 | 0.166 | 0.179 | 0.114 | 0.46 | 0.347 | 1086 | 1086 |
| animas | 1 | 0.988 | 0.988 | 0.0 | 0.984 | 0.985 | 0.001 | 1094 | 1094 |
| animas | 3 | 0.921 | 0.923 | 0.002 | 0.912 | 0.92 | 0.008 | 1092 | 1092 |
| animas | 7 | 0.847 | 0.849 | 0.001 | 0.847 | 0.852 | 0.005 | 1088 | 1088 |
| bow | 1 | 0.979 | 0.98 | 0.0 | 0.871 | 0.865 | -0.006 | 755 | 755 |
| bow | 3 | 0.895 | 0.886 | -0.009 | 0.916 | 0.466 | -0.45 | 753 | 753 |
| bow | 7 | 0.744 | 0.769 | 0.025 | 0.856 | 0.72 | -0.135 | 749 | 749 |
| verde | 1 | 0.61 | 0.615 | 0.006 | 0.678 | 0.646 | -0.032 | 1094 | 1094 |
| verde | 3 | -0.064 | 0.011 | 0.075 | 0.242 | 0.513 | 0.271 | 1092 | 1092 |
| verde | 7 | -0.123 | -0.056 | 0.067 | 0.198 | 0.336 | 0.139 | 1088 | 1088 |

## Bow ice-free test days
| horizon | n_test_all | n_test_open | ice_frac_test | all_routing_NSE | all_xgb_NSE | all_xgb_CSI | open_routing_NSE | open_xgb_NSE | open_xgb_CSI | open_routing_CSI | open_n_events |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0 | 756.0 | 646.0 | 0.146 | 0.976 | 0.871 | 0.886 | 0.973 | 0.856 | 0.886 | 0.855 | 74.0 |
| 3.0 | 756.0 | 646.0 | 0.146 | 0.896 | 0.916 | 0.783 | 0.885 | 0.907 | 0.783 | 0.795 | 74.0 |
| 7.0 | 756.0 | 646.0 | 0.146 | 0.729 | 0.857 | 0.618 | 0.704 | 0.843 | 0.618 | 0.505 | 74.0 |
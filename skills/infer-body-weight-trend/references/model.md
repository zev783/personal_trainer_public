# Generalized condition-aware weight model

## What is ported

The tool uses the original method's Monte Carlo condition adjustment and Gaussian Bayesian linear regression, generalized to kg internally and either kg or lb for output. Multiple readings are averaged within each simulated day before regression. Each date has one regression observation, so a date with many weigh-ins does not become many independent days.

Outputs separate literal reported readings, a same-day reference-condition estimate, a smoothed scale-only level and weekly change, and an optional user-prior-informed result. None is a direct measurement of fat, lean tissue, or hydration. The reference convention is no clothing, pre-intake and post-urination; the original readings are never changed.

## Transparent operational assumptions

All masses below are kg. These are generic heuristics, not clinically validated distributions or individual calibration:

| Component | Distribution |
|---|---|
| No clothing | Zero clothing offset |
| Underwear | Triangular minimum 0, mode 0.04, maximum 0.10 |
| Reported clothing | Triangular 0.20, 0.40, 0.90 |
| Unknown clothing | Triangular 0, 0.30, 1.20 |
| Explicit pre-intake | Zero intake offset |
| Exactly stated water-only volume | Physical water mass multiplied by Beta(2, 1.3) uncertain retention |
| Other or unknown intake | Triangular 0, 0.45, 1.80 |
| Unknown/pre-urination | 0.45 multiplied by Beta(1.5, 3) |
| Explicitly reported dehydration | Negative triangular 0.10, 0.35, 1.00 |
| Readout noise | Normal SD 0.05 |
| Residual daily variability | Normal SD 0.50 by default; configurable with `--day-sd-kg` |
| Scale-only weekly slope prior | Normal mean 0, SD 1.20 kg/week; broad but still a prior |

Only explicit supported condition text activates a narrow category. Ambiguous or negated text must not be interpreted as medical diagnosis or certainty. Water units are mL, L, or **US fluid ounces**, with 1 US fl oz approximated as 0.02957353 kg of water; mass ounces are not silently treated as fluid ounces. Water-only input does not imply zero clothing or bladder uncertainty.

## Limits and calibration

Intervals at 68%, 90%, and 95% and the probability of a decreasing slope are conditional on the assumed model, not validated clinical confidence intervals. Short windows, sparse days, nonlinear trends, scale changes, unusual meals, illness, travel, or fluid shifts can make estimates unreliable. The tool warns below seven observed dates; that is an operational warning, not a proven minimum sample size.

Generic priors can bias reference estimates, particularly with unknown conditions. Report assumptions and inspect every extracted row. A sensitivity check with a wider daily SD can reveal instability; it does not validate the model. Calibrate further distributions only from appropriate user-supplied evidence and record changes explicitly. Do not claim to infer an individual's true body mass by subtracting exact meals or clothing.

An optional prior requires both an expected weekly change and its positive uncertainty in the selected output unit, plus a textual evidence basis. Use it only when the user has adopted the relevant expectation and actual adherence supports it. Always show the scale-only result too. A calorie plan alone is not verified adherence, and this prior-informed trend is not proof of tissue loss.

## Evidence boundary

The primary study [Cheuvront et al., 2004](https://pubmed.ncbi.nlm.nih.gov/15673099/) reported day-to-day morning body-mass variability in 65 active men during exercise in heat. Its population and context limit generalization. It supports accounting for measurement variability; it does not validate this tool's clothing, meal, retention, or dehydration priors. Record and abstract checked 2026-09-21. The implementation's mathematical checks test behavior and arithmetic, not clinical accuracy.

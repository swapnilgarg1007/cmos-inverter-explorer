# CMOS Inverter Explorer

Interactive tool that plots a CMOS inverter's voltage transfer curve (VTC), switching threshold and noise margins using the long-channel square-law model. Move the sliders for VDD, thresholds and W/L ratios and watch the curve shift.

## Run it
```bash
pip install -r requirements.txt
streamlit run app.py
pytest
```

## Model
- Each transistor is in cutoff, triode or saturation depending on Vgs and Vds.
- For every Vin, `Vout` is found by bisection on `Idn(Vout) = Idp(Vout)`.
- Switching threshold (closed form): `Vm = (Vtn + r(VDD - |Vtp|)) / (1 + r)`, with `r = sqrt(kp/kn)`.
- Vil and Vih are the points where the VTC slope is -1; `NML = Vil - Vol`, `NMH = Voh - Vih`.

## Validation
TODO: add a screenshot, and overlay an LTSpice DC sweep for the same parameters (put the `.asc` file in `spice/`) to show the model agrees.

## Limitations
No channel-length modulation, velocity saturation or body effect, so it will diverge from short-channel processes.

## Ideas
- [ ] Add channel-length modulation (lambda)
- [ ] Propagation delay estimate from load capacitance
- [ ] Export plots as PNG/CSV

## License
MIT

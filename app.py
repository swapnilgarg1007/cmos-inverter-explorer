import streamlit as st
import matplotlib.pyplot as plt
from cmos import vtc, switching_threshold, noise_margins

st.title("CMOS Inverter Explorer")
st.caption("Long-channel square-law model: voltage transfer curve, switching threshold, noise margins")

vdd = st.sidebar.slider("VDD (V)", 0.8, 3.3, 1.8, 0.1)
vtn = st.sidebar.slider("Vtn (V)", 0.2, 0.8, 0.4, 0.05)
vtp = st.sidebar.slider("|Vtp| (V)", 0.2, 0.8, 0.4, 0.05)
wl_n = st.sidebar.slider("NMOS W/L", 1.0, 20.0, 4.0, 0.5)
wl_p = st.sidebar.slider("PMOS W/L", 1.0, 40.0, 8.0, 0.5)
ratio = st.sidebar.number_input("mu_n / mu_p", 1.0, 5.0, 2.5, 0.1)

kn, kp = ratio * wl_n, wl_p  # normalise so mu_p*Cox = 1
vin, vout = vtc(vdd, kn, kp, vtn, vtp)
vm = switching_threshold(vdd, kn, kp, vtn, vtp)
nm = noise_margins(vin, vout)

fig, ax = plt.subplots()
ax.plot(vin, vout, label="Vout")
ax.plot(vin, vin, "--", alpha=0.4, label="Vin = Vout")
ax.axvline(vm, color="r", ls=":", label=f"Vm = {vm:.2f} V")
ax.set_xlabel("Vin (V)"); ax.set_ylabel("Vout (V)"); ax.legend(); ax.grid(alpha=0.3)
st.pyplot(fig)

if nm:
    st.subheader("Noise margins")
    st.table({k: [round(float(v), 3)] for k, v in nm.items()})

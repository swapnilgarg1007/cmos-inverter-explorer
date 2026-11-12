"""Square-law (long-channel) CMOS inverter model.

Currents are in arbitrary units of A/V^2 * V^2; only ratios matter for the VTC.
kn, kp are the transconductance parameters (mu*Cox*W/L) of NMOS and PMOS.
vtp is the PMOS threshold *magnitude*.
"""
import numpy as np


def _id(kx, vt, vgs, vds):
    """Drain current of one device (cutoff / triode / saturation)."""
    vov = vgs - vt
    if vov <= 0:
        return 0.0
    if vds >= vov:
        return 0.5 * kx * vov**2
    return kx * (vov * vds - 0.5 * vds**2)


def vout_for(vin, vdd, kn, kp, vtn, vtp):
    """Solve Idn = Idp for Vout by bisection (the net current is monotonic in Vout)."""
    lo, hi = 0.0, vdd
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        idn = _id(kn, vtn, vin, mid)
        idp = _id(kp, vtp, vdd - vin, vdd - mid)
        if idn > idp:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def vtc(vdd, kn, kp, vtn, vtp, points=400):
    vin = np.linspace(0, vdd, points)
    vout = np.array([vout_for(v, vdd, kn, kp, vtn, vtp) for v in vin])
    return vin, vout


def switching_threshold(vdd, kn, kp, vtn, vtp):
    """Closed-form Vm where both devices saturate and Vin = Vout."""
    r = np.sqrt(kp / kn)
    return (vtn + r * (vdd - vtp)) / (1 + r)


def noise_margins(vin, vout):
    """Find Vil/Vih where dVout/dVin = -1, then NMl = Vil - Vol and NMh = Voh - Vih."""
    slope = np.gradient(vout, vin)
    idx = np.where(slope <= -1)[0]
    if len(idx) == 0:
        return None
    vil, vih = vin[idx[0]], vin[idx[-1]]
    voh, vol = vout.max(), vout.min()
    return {"Vil": vil, "Vih": vih, "Voh": voh, "Vol": vol,
            "NML": vil - vol, "NMH": voh - vih}

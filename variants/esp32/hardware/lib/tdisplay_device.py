"""LILYGO T-Display V1.1 as an EasyEDA library device: symbol, footprint and device in the project library of the
EasyEDA project `christmas-bell`. The T-Display is not in EasyEDA's library and not sold by LCSC (D-13).

    uv run --project <edakit> python variants/esp32/hardware/lib/tdisplay_device.py [footprint|symbol|device|info]

Sources (variants/esp32/hardware/parts/LILYGO-T-DISPLAY-V1.1.json): LILYGO's pin map "ESP32 TTGO T-Display V1.1",
the schematic ESP32-TFT(6-26) (headers P4/P5) and the KiCad and Eagle libraries in the LILYGO repository – all agree
on the pin order. Board 25.09 x 51.49 mm, two rows of 12 pins, pitch 2.54 mm, rows 22.86 mm apart; the first pin of
each row sits 15.93 mm from the USB end. The holes are 1.1 mm like the Nano's (D-7): the module plugs into two 1x12
female headers whose 0.64 mm square tails need them.

Footprint as seen from the top, USB end at -y: right row pins 1-12 (1 = 5V at the USB end), left row pins 13-24
(13 = 3V3 at the USB end). The symbol shows both rows in the same order. Origin: centre of the pin field.
State (UUIDs) goes to the edakit artifacts of the variant, so a second run finds what the first created.
"""

import json
import sys
import time
from pathlib import Path

from edakit import config, eda

HERE = Path(__file__).resolve().parent
CFG = HERE.parents[1] / "edakit.toml"
MIL = 1 / 0.0254

NAME = "LILYGO T-Display V1.1"
LCSC_KEY = "LILYGO-T-DISPLAY-V1.1"  # parts entry and graph key in place of an LCSC number
FOOTPRINT = "LILYGO-T-DISPLAY-V1.1_2x12-P2.54-LS22.86"
PINS = {  # number: name, right row 1-12 from the USB end, left row 13-24 from the USB end
    1: "5V", 2: "GND", 3: "IO27", 4: "IO26", 5: "IO25", 6: "IO33", 7: "IO32", 8: "IO39", 9: "IO38", 10: "IO37",
    11: "IO36", 12: "3V3",
    13: "3V3", 14: "GND", 15: "GND", 16: "IO12", 17: "IO13", 18: "IO15", 19: "IO2", 20: "IO17", 21: "IO22",
    22: "IO21", 23: "GND", 24: "GND",
}
ROW_X = 11.43          # mm from the centre, 22.86 mm between the rows
PITCH = 2.54
PAD, HOLE = 1.7, 1.1   # mm
OUTLINE = (-12.83, -30.2, 12.83, 21.9)  # module 25.09 x 51.49 mm plus 0.15 mm, so the line stays clear of the pads
USB = (-4.6, -31.2, 4.6, -27.9)         # USB-C receptacle, stands out at the end


def pin_xy(n):
    """Pad centre in mm, footprint seen from the top, USB end at -y."""
    i = (n - 1) % 12
    return (ROW_X if n <= 12 else -ROW_X), -5.5 * PITCH + i * PITCH


def rect_poly(x0, y0, x1, y1):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    poly = [round(pts[0][0] * MIL, 2), round(pts[0][1] * MIL, 2), "L"]
    for x, y in pts[1:] + pts[:1]:
        poly += [round(x * MIL, 2), round(y * MIL, 2)]
    return {"$polygon": poly}


def state_file(cfg):
    return cfg.artifact("tdisplay_device.json")


def load_state(cfg):
    f = state_file(cfg)
    return json.loads(f.read_text()) if f.exists() else {}


def save_state(cfg, st):
    state_file(cfg).write_text(json.dumps(st, indent=1))


def api(mcp, path, *args, timeout=130):
    return eda.api(mcp, path, *args, timeout=timeout)


def tab_ids(mcp):
    out, todo = [], [api(mcp, "DMT_EditorControl.getSplitScreenTree")]
    while todo:
        n = todo.pop()
        if isinstance(n, list):
            todo += n
        elif isinstance(n, dict):
            out += [t["tabId"] for t in n.get("tabs", [])]
            todo += n.get("children") or []
    return out


def open_editor(mcp, cls, uuid, lib):
    """Open the library document and make its tab the active one (tab id '<uuid>@<library>')."""
    tab = f"{uuid}@{lib}"
    if tab not in tab_ids(mcp):
        try:
            api(mcp, f"{cls}.openInEditor", uuid, lib, timeout=20)
        except eda.MCPError as e:
            print(f"  ({cls}.openInEditor: {str(e)[:80]})")
    for _ in range(30):
        if tab in tab_ids(mcp):
            api(mcp, "DMT_EditorControl.activateDocument", tab)
            time.sleep(2)
            return tab
        time.sleep(2)
    raise SystemExit(f"editor tab {tab} did not open")


def close_tab(mcp, tab):
    if tab:
        try:
            api(mcp, "DMT_EditorControl.closeDocument", tab)
        except eda.MCPError as e:
            print(f"  ? tab {tab} not closed ({e})")


def make_footprint(mcp, lib, st):
    if not st.get("footprint"):
        st["footprint"] = api(mcp, "LIB_Footprint.create", lib, FOOTPRINT, [], f"{NAME}, plugged into two 1x12 "
                              "female headers, pitch 2.54 mm, rows 22.86 mm apart, holes 1.1 mm")
        if not st["footprint"]:
            raise SystemExit("LIB_Footprint.create returned nothing")
        print(f"  footprint created: {st['footprint']}")
    tab = open_editor(mcp, "LIB_Footprint", st["footprint"], lib)
    old = api(mcp, "PCB_PrimitivePad.getAllPrimitiveId") or []
    if old:
        api(mcp, "PCB_PrimitivePad.delete", old)
    for n in sorted(PINS):
        x, y = pin_xy(n)
        d = round(PAD * MIL, 2)
        shape = ["RECT", d, d, 0] if n in (1, 13) else ["ELLIPSE", d, d]  # square pad: USB end of each row
        res = api(mcp, "PCB_PrimitivePad.create", 12, str(n), round(x * MIL, 2), round(y * MIL, 2), 0, shape, "",
                  ["ROUND", round(HOLE * MIL, 2)], 0, 0, 0, True)
        if not res:
            raise SystemExit(f"pad {n} not created")
    for pid in api(mcp, "PCB_PrimitivePolyline.getAllPrimitiveId") or []:
        api(mcp, "PCB_PrimitivePolyline.delete", [pid])
    for pid in api(mcp, "PCB_PrimitiveString.getAllPrimitiveId") or []:
        api(mcp, "PCB_PrimitiveString.delete", [pid])
    api(mcp, "PCB_PrimitivePolyline.create", "", 3, rect_poly(*OUTLINE), 6)
    api(mcp, "PCB_PrimitivePolyline.create", "", 3, rect_poly(*USB), 6)
    api(mcp, "PCB_PrimitiveString.create", 3, 0, round(-26.0 * MIL, 2), "USB", "default", round(1.2 * MIL, 2), 6, 5, 0,
        False, 0, False, False)
    api(mcp, "PCB_PrimitiveString.create", 3, 0, round(18.5 * MIL, 2), "T-Display", "default", round(1.2 * MIL, 2), 6, 5,
        0, False, 0, False, False)
    pads = [eda.state(p) for p in api(mcp, "PCB_PrimitivePad.getAll") or []]
    print(f"  {len(pads)} pads: " + ", ".join(f"{p['PadNumber']}@({p['X']:.0f},{p['Y']:.0f})" for p in
                                               sorted(pads, key=lambda p: int(p["PadNumber"]))))
    print("  saved" if api(mcp, "PCB_Document.save") else "  ! footprint not saved")
    close_tab(mcp, tab)


def make_symbol(mcp, lib, st):
    if not st.get("symbol"):
        # symbol type 2 (component, like the Nano's symbol): without it the editor never finishes loading
        st["symbol"] = api(mcp, "LIB_Symbol.create", lib, NAME, [], 2, "LILYGO TTGO T-Display V1.1 (ESP32, 1.14 inch "
                           "ST7789V TFT), 2 x 12 header pins")
        if not st["symbol"]:
            raise SystemExit("LIB_Symbol.create returned nothing")
        print(f"  symbol created: {st['symbol']}")
    tab = open_editor(mcp, "LIB_Symbol", st["symbol"], lib)
    for cls in ("SCH_PrimitivePin", "SCH_PrimitiveRectangle"):
        old = api(mcp, f"{cls}.getAllPrimitiveId") or []
        if old:
            api(mcp, f"{cls}.delete", old)
    # body 120 x 130 (units of 10 mil), pins 10 long, 10 apart; top of each side = the row's far end, as on the module
    api(mcp, "SCH_PrimitiveRectangle.create", -60, 65, 120, 130, 0, 0, None, None, 1, 0)
    for n, name in PINS.items():
        i = (n - 1) % 12
        y = -55 + i * 10
        x, rot = (70, 0) if n <= 12 else (-70, 180)
        if not api(mcp, "SCH_PrimitivePin.create", x, y, str(n), name, rot, 10):
            raise SystemExit(f"pin {n} not created")
    pins = [eda.state(p) for p in api(mcp, "SCH_PrimitivePin.getAll") or []]
    print(f"  {len(pins)} pins: " + ", ".join(f"{p.get('PinNumber')}={p.get('PinName')}@({p.get('X')},{p.get('Y')},{p.get('Rotation')})" for p in
                                               sorted(pins, key=lambda p: int(p.get("PinNumber", 0)))))
    print("  saved" if api(mcp, "SCH_Document.save") else "  ! symbol not saved")
    close_tab(mcp, tab)


def make_device(mcp, lib, st):
    if not st.get("device"):
        st["device"] = api(mcp, "LIB_Device.create", lib, NAME, [],
                           {"symbol": {"uuid": st["symbol"], "libraryUuid": lib},
                            "footprint": {"uuid": st["footprint"], "libraryUuid": lib}},
                           "LILYGO TTGO T-Display V1.1, plugged in (two 1x12 female headers)",
                           {"designator": "U", "addIntoBom": False, "addIntoPcb": True})
        if not st["device"]:
            raise SystemExit("LIB_Device.create returned nothing")
        print(f"  device created: {st['device']}")
    info(mcp, lib, st)
    cache(mcp, lib, st)


def info(mcp, lib, st):
    """LIB_Device.get returns nothing for a project-library device; the search with the project UUID finds it."""
    found = mcp.call("easyeda_schematic_search_device", key="LILYGO", libraryUuid=lib, itemsOfPage=20)
    dev = next((d for d in found.get("devices", []) if d.get("uuid") == st.get("device")), None)
    if not dev:
        raise SystemExit(f"device {st.get('device')} not found in the project library")
    print(f"  {dev['name']}: symbol {dev['symbolUuid']} ({dev['symbolName']}), footprint {dev['footprintUuid']} "
          f"({dev['footprintName']}), {dev.get('otherProperty')}")


def cache(mcp, lib, st):
    """edakit looks parts up by LCSC number; this one has none, so its key goes into the device cache by hand."""
    cfg = config.load(CFG)
    f = cfg.artifact("device_cache.json")
    data = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    data[LCSC_KEY] = {"uuid": st["device"], "libraryUuid": lib}
    f.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"  {LCSC_KEY} -> {st['device']} in {f}")


def main():
    what = sys.argv[1:] or ["footprint", "symbol", "device"]  # "info", "cache": check an existing device
    cfg = config.load(CFG)
    mcp = eda.connect(cfg)
    try:
        lib = eda.open_project(mcp, cfg)  # the project library is addressed by the project UUID
        st = load_state(cfg)
        st["library"] = lib
        for step in what:
            print(f"[{step}]")
            try:
                {"footprint": make_footprint, "symbol": make_symbol, "device": make_device, "info": info,
                 "cache": cache}[step](mcp, lib, st)
            finally:
                save_state(cfg, st)
    finally:
        mcp.close()


if __name__ == "__main__":
    main()

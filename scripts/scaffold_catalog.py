"""Generate colosseum-library atomic building-block catalog. Run: python scripts/scaffold_catalog.py"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LOAD_BENCH = """

def _load_bench() -> None:
    if col.config.is_loaded():
        return
    if USE_AUTOCONFIG:
        col.equipment.autoconfig()
        return
    col.config.load_config(str(Path(__file__).with_name("config.toml")))
"""

FOOTER = """

if __name__ == "__main__":
    main()
    col.endex()
"""


def write_test(
    path: Path,
    *,
    doc: str,
    setup: str,
    autoconfig: bool,
    fills: str,
    body: str,
) -> None:
    setup_lines = "\n".join(f"#   {ln}" for ln in setup.strip().splitlines() if ln)
    text = f'"""{doc}"""\n\nfrom __future__ import annotations\n\nfrom pathlib import Path\n\nimport colosseum as col\n\n# SETUP:\n{setup_lines}\n\nUSE_AUTOCONFIG = {"True" if autoconfig else "False"}\n\n# --- procedure (replace every FILL_IN_HERE) ---\n{fills.strip()}\n\n\ndef main() -> None:\n    _load_bench()\n{body}\n'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + LOAD_BENCH + FOOTER, encoding="utf-8")


def folder_readme(folder: Path, title: str, intro: str, rows: list[tuple[str, str]]) -> None:
    lines = [f"# {title}", "", intro, "", "## Building blocks", "", "| Script | Block |", "|--------|-------|"]
    lines.extend(f"| `{a}` | {b} |" for a, b in rows)
    lines.append("")
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "README.md").write_text("\n".join(lines), encoding="utf-8")


def bench(folder: Path, text: str) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "config.toml.example").write_text(text.strip() + "\n", encoding="utf-8")


def topic(folder: Path, bench_text: str, title: str, intro: str, tests: list[dict]) -> None:
    bench(folder, bench_text)
    rows: list[tuple[str, str]] = []
    for t in tests:
        write_test(
            folder / t["file"],
            doc=t["doc"],
            setup=t["setup"],
            autoconfig=t.get("autoconfig", False),
            fills=t["fills"],
            body=t["body"],
        )
        rows.append((t["file"], t["block"]))
    folder_readme(folder, title, intro, rows)


# --- DIGITAL ---

topic(
    ROOT / "digital" / "onewire",
    """
[[equipment.psu]]
psu_id = 1
driver = sim
resource = SIM::PSU1
""",
    "1-Wire",
    "1-Wire on PCB header; parasitic vs external Vdd per script.",
    [
        {
            "file": "test_rom_read.py",
            "block": "ROM read → match",
            "doc": "One block: read 1-Wire ROM and verify.",
            "setup": "DQ on J_OW; powered bus.",
            "fills": "onewire_id = FILL_IN_HERE\nexpected_rom_hex = FILL_IN_HERE",
            "body": '    col.io.onewire.read_rom(onewire_id=onewire_id, key="rom")\n    col.shared.verify.verify_field(key="rom", expected_val=expected_rom_hex)',
        },
        {
            "file": "test_scratchpad_crc.py",
            "block": "scratchpad CRC → match",
            "doc": "One block: scratchpad CRC verify.",
            "setup": "Known scratchpad page.",
            "fills": "onewire_id = FILL_IN_HERE\nexpected_crc = FILL_IN_HERE",
            "body": '    col.io.onewire.read_scratchpad(onewire_id=onewire_id, key="scratchpad")\n    col.shared.verify.verify_field(key="scratchpad", field="crc", expected_val=expected_crc)',
        },
        {
            "file": "test_parasitic_power.py",
            "block": "parasitic read → valid byte",
            "doc": "One block: parasitic power read.",
            "setup": "No explicit Vdd; strong pull-up.",
            "fills": "onewire_id = FILL_IN_HERE\nexpected_byte = FILL_IN_HERE",
            "body": '    col.io.onewire.read_byte(onewire_id=onewire_id, key="parasitic_byte")\n    col.shared.verify.verify_field(key="parasitic_byte", expected_val=expected_byte)',
        },
        {
            "file": "test_brownout_presence.py",
            "block": "presence at min V",
            "doc": "One block: presence above brownout V.",
            "setup": "PSU on 1-Wire Vdd.",
            "fills": "onewire_id = FILL_IN_HERE\npsu_id = FILL_IN_HERE\nmin_presence_v = FILL_IN_HERE",
            "body": '    col.equipment.psu.set_voltage(psu_id=psu_id, voltage=min_presence_v)\n    col.io.onewire.verify_presence(onewire_id=onewire_id, key="presence")\n    col.shared.verify.verify_measurement_exists(key="presence")',
        },
    ],
)

topic(
    ROOT / "digital" / "clocks",
    """
[[equipment.oscope]]
oscope_id = 1
driver = sim
resource = SIM::SCOPE1

[[equipment.freqcounter]]
freqcounter_id = 1
driver = sim
resource = SIM::FC1
""",
    "Digital clocks",
    "Probe/SMA on clock output; REF for alignment scripts.",
    [
        {
            "file": "test_frequency.py",
            "block": "frequency → tolerance",
            "doc": "One block: clock frequency.",
            "setup": "Scope or counter on CLK_OUT.",
            "fills": "freqcounter_id = FILL_IN_HERE\nexpected_freq_hz = FILL_IN_HERE\nfreq_tolerance_hz = FILL_IN_HERE",
            "body": '    col.equipment.freqcounter.measure_frequency(freqcounter_id=freqcounter_id, key="clk_hz")\n    col.equipment.freqcounter.verify_frequency(key="clk_hz", expected_val=expected_freq_hz, tolerance=freq_tolerance_hz)',
        },
        {
            "file": "test_jitter_rms.py",
            "block": "jitter → max ps",
            "doc": "One block: RMS jitter.",
            "setup": "Scope on clock; TIE measurement.",
            "fills": "oscope_id = FILL_IN_HERE\nclock_channel = FILL_IN_HERE\nmax_jitter_ps = FILL_IN_HERE",
            "body": '    col.equipment.oscope.measure_jitter(oscope_id=oscope_id, channel=clock_channel, key="jitter_ps")\n    col.shared.verify.verify_field(key="jitter_ps", expected_val=max_jitter_ps, tolerance=0.0)',
        },
        {
            "file": "test_alignment_skew.py",
            "block": "REF-DUT skew → max ns",
            "doc": "One block: clock alignment skew.",
            "setup": "CH1=REF CH2=DUT.",
            "fills": "oscope_id = FILL_IN_HERE\nref_channel = FILL_IN_HERE\ndut_channel = FILL_IN_HERE\nmax_skew_ns = FILL_IN_HERE",
            "body": '    col.equipment.oscope.measure_phase_delay(oscope_id=oscope_id, ref_channel=ref_channel, dut_channel=dut_channel, key="skew_ns")\n    col.shared.verify.verify_field(key="skew_ns", expected_val=max_skew_ns, tolerance=0.0)',
        },
        {
            "file": "test_allan_deviation.py",
            "block": "Allan σ(τ) → max",
            "doc": "One block: Allan deviation at tau.",
            "setup": "Long capture; counter or FS740.",
            "fills": "tau_s = FILL_IN_HERE\nallan_max = FILL_IN_HERE\nsample_duration_s = FILL_IN_HERE",
            "body": '    col.equipment.fs740.measure_allan(fs740_id=FILL_IN_HERE, tau_s=tau_s, duration_s=sample_duration_s, key="allan")\n    col.shared.verify.verify_field(key="allan", expected_val=allan_max, tolerance=0.0)',
        },
    ],
)

topic(
    ROOT / "digital" / "ethernet",
    """
[[messaging.ssh]]
ssh_id = 1
host = "192.168.1.10"
username = "root"
password = "changeme"

[[messaging.http]]
http_id = 1
base_url = "http://192.168.1.10"
""",
    "Ethernet",
    "RJ45 to DUT; dut_ip and dut_iface in FILL_IN_HERE.",
    [
        {
            "file": "test_link_up.py",
            "block": "operstate → UP",
            "doc": "One block: link up.",
            "setup": "Cable to DUT NIC.",
            "fills": "dut_iface = FILL_IN_HERE  # str e.g. eth0",
            "body": '    col.host.net.measure_operstate(key="link", iface=dut_iface)\n    col.host.net.verify_operstate_up(key="link", expected="up")',
        },
        {
            "file": "test_ping_reachability.py",
            "block": "ping loss → max",
            "doc": "One block: ping reachability.",
            "setup": "DUT reachable on LAN.",
            "fills": 'ssh_id = FILL_IN_HERE\ndut_ip = FILL_IN_HERE\nping_count = FILL_IN_HERE\nmax_loss = FILL_IN_HERE',
            "body": '    col.messaging.ssh.measure_stdout(ssh_id=ssh_id, command=f"ping -c {ping_count} {dut_ip}", key="ping")\n    col.shared.regex.verify_match(key="ping", pattern=r"0% packet loss")',
        },
        {
            "file": "test_throughput_mbps.py",
            "block": "iperf Mbps → minimum",
            "doc": "One block: throughput.",
            "setup": "iperf3 server on DUT.",
            "fills": 'ssh_id = FILL_IN_HERE\ndut_ip = FILL_IN_HERE\nmin_throughput_mbps = FILL_IN_HERE\niperf_duration_s = FILL_IN_HERE',
            "body": '    col.messaging.ssh.measure_stdout(ssh_id=ssh_id, command=f"iperf3 -c {dut_ip} -t {iperf_duration_s}", key="iperf")\n    col.shared.regex.verify_match(key="iperf", pattern=r"Gbits/sec")',
        },
        {
            "file": "test_eye_height_mv.py",
            "block": "eye height → minimum",
            "doc": "One block: SI eye height.",
            "setup": "Diff probe on TX pair.",
            "fills": "oscope_id = FILL_IN_HERE\nmin_eye_mv = FILL_IN_HERE",
            "body": '    col.equipment.oscope.measure_eye_height(oscope_id=oscope_id, key="eye_mv")\n    col.shared.verify.verify_field(key="eye_mv", expected_val=min_eye_mv, tolerance=0.0)',
        },
        {
            "file": "test_ber.py",
            "block": "BER → maximum",
            "doc": "One block: bit error rate.",
            "setup": "DUT PHY self-test command.",
            "fills": 'ssh_id = FILL_IN_HERE\nber_max = FILL_IN_HERE\ndut_ber_command = FILL_IN_HERE  # str',
            "body": '    col.messaging.ssh.measure_stdout(ssh_id=ssh_id, command=dut_ber_command, key="ber")\n    col.shared.regex.verify_match(key="ber", pattern=r"BER")',
        },
    ],
)

topic(
    ROOT / "digital" / "tachometer_pwm",
    """
[[messaging.ssh]]
ssh_id = 1
host = "192.168.1.10"
username = "root"
password = "changeme"

[[equipment.oscope]]
oscope_id = 1
driver = sim
resource = SIM::SCOPE1
""",
    "Tachometer / PWM",
    "Fan connector pinout; PWM/tach on scope channel.",
    [
        {
            "file": "test_fan_command_ack.py",
            "block": "fan command → ack",
            "doc": "One block: fan setpoint command ack.",
            "setup": "SSH to DUT fan controller.",
            "fills": "ssh_id = FILL_IN_HERE\nfan_set_command = FILL_IN_HERE  # str shell command",
            "body": '    col.messaging.ssh.measure_stdout(ssh_id=ssh_id, command=fan_set_command, key="fan_ack")\n    col.shared.regex.verify_match(key="fan_ack", pattern=r"OK")',
        },
        {
            "file": "test_pwm_frequency.py",
            "block": "PWM freq → expected",
            "doc": "One block: PWM frequency.",
            "setup": "Scope on PWM pin.",
            "fills": "oscope_id = FILL_IN_HERE\npwm_channel = FILL_IN_HERE\nexpected_freq_hz = FILL_IN_HERE\nfreq_tolerance_hz = FILL_IN_HERE",
            "body": '    col.equipment.oscope.measure_frequency(oscope_id=oscope_id, channel=pwm_channel, key="pwm_hz")\n    col.shared.verify.verify_field(key="pwm_hz", expected_val=expected_freq_hz, tolerance=freq_tolerance_hz)',
        },
        {
            "file": "test_pwm_duty_cycle.py",
            "block": "duty cycle → tolerance",
            "doc": "One block: PWM duty cycle.",
            "setup": "Scope on PWM pin.",
            "fills": "oscope_id = FILL_IN_HERE\npwm_channel = FILL_IN_HERE\nexpected_duty_pct = FILL_IN_HERE\nduty_tolerance_pct = FILL_IN_HERE",
            "body": '    col.equipment.oscope.measure_duty_cycle(oscope_id=oscope_id, channel=pwm_channel, key="duty_pct")\n    col.shared.verify.verify_field(key="duty_pct", expected_val=expected_duty_pct, tolerance=duty_tolerance_pct)',
        },
        {
            "file": "test_tachometer_rpm.py",
            "block": "tach RPM → limit",
            "doc": "One block: tachometer RPM.",
            "setup": "Tach wire on scope; know pulses/rev.",
            "fills": "oscope_id = FILL_IN_HERE\ntach_channel = FILL_IN_HERE\npulses_per_rev = FILL_IN_HERE\nmax_rpm = FILL_IN_HERE",
            "body": '    col.equipment.oscope.measure_frequency(oscope_id=oscope_id, channel=tach_channel, key="tach_hz")\n    col.shared.signal.measure_rpm_from_frequency(key="tach_hz", pulses_per_rev=pulses_per_rev, out_key="rpm")\n    col.shared.verify.verify_field(key="rpm", expected_val=max_rpm, tolerance=0.0)',
        },
    ],
)

topic(
    ROOT / "digital" / "gpio",
    """
[[io.dio]]
dio_id = 1
driver = sim
port_lines = 8
direction = 0xFF

[[equipment.oscope]]
oscope_id = 1
driver = sim
resource = SIM::SCOPE1
""",
    "GPIO",
    "Pin header map; loopback jumper on J_GPIO_LB for loopback script.",
    [
        {
            "file": "test_output_high.py",
            "block": "drive high → read true",
            "doc": "One block: GPIO output high.",
            "setup": "DIO line as output.",
            "fills": "dio_id = FILL_IN_HERE\nline = FILL_IN_HERE\ndirection_mask = FILL_IN_HERE",
            "body": '    col.io.dio.configure(dio_id=dio_id, direction=direction_mask)\n    col.io.dio.write_pin(dio_id=dio_id, line=line, value=True)\n    col.io.dio.read_pin(dio_id=dio_id, line=line, key="pin_high")\n    col.shared.verify.verify_field(key="pin_high", expected_val=True)',
        },
        {
            "file": "test_output_low.py",
            "block": "drive low → read false",
            "doc": "One block: GPIO output low.",
            "setup": "DIO line as output.",
            "fills": "dio_id = FILL_IN_HERE\nline = FILL_IN_HERE\ndirection_mask = FILL_IN_HERE",
            "body": '    col.io.dio.configure(dio_id=dio_id, direction=direction_mask)\n    col.io.dio.write_pin(dio_id=dio_id, line=line, value=False)\n    col.io.dio.read_pin(dio_id=dio_id, line=line, key="pin_low")\n    col.shared.verify.verify_field(key="pin_low", expected_val=False)',
        },
        {
            "file": "test_output_voltage_high.py",
            "block": "Vhigh → minimum",
            "doc": "One block: GPIO high voltage.",
            "setup": "Scope on pin; drive high first.",
            "fills": "dio_id = FILL_IN_HERE\nline = FILL_IN_HERE\noscope_id = FILL_IN_HERE\nscope_channel = FILL_IN_HERE\nv_high_min = FILL_IN_HERE",
            "body": '    col.io.dio.write_pin(dio_id=dio_id, line=line, value=True)\n    col.equipment.oscope.measure_vpp(oscope_id=oscope_id, channel=scope_channel, key="v_high")\n    col.equipment.oscope.verify_vpp(key="v_high", expected_val=v_high_min, tolerance=0.1)',
        },
        {
            "file": "test_output_voltage_low.py",
            "block": "Vlow → maximum",
            "doc": "One block: GPIO low voltage.",
            "setup": "Scope on pin; drive low.",
            "fills": "dio_id = FILL_IN_HERE\nline = FILL_IN_HERE\noscope_id = FILL_IN_HERE\nscope_channel = FILL_IN_HERE\nv_low_max = FILL_IN_HERE",
            "body": '    col.io.dio.write_pin(dio_id=dio_id, line=line, value=False)\n    col.equipment.oscope.measure_vpp(oscope_id=oscope_id, channel=scope_channel, key="v_low")\n    col.shared.verify.verify_field(key="v_low", expected_val=v_low_max, tolerance=0.05)',
        },
        {
            "file": "test_rise_time.py",
            "block": "rise time → max ns",
            "doc": "One block: GPIO rise time.",
            "setup": "Scope on edge.",
            "fills": "oscope_id = FILL_IN_HERE\nscope_channel = FILL_IN_HERE\nrise_max_ns = FILL_IN_HERE",
            "body": '    col.equipment.oscope.measure_rise_time(oscope_id=oscope_id, channel=scope_channel, key="rise_ns")\n    col.shared.verify.verify_field(key="rise_ns", expected_val=rise_max_ns, tolerance=0.0)',
        },
        {
            "file": "test_fall_time.py",
            "block": "fall time → max ns",
            "doc": "One block: GPIO fall time.",
            "setup": "Scope on edge.",
            "fills": "oscope_id = FILL_IN_HERE\nscope_channel = FILL_IN_HERE\nfall_max_ns = FILL_IN_HERE",
            "body": '    col.equipment.oscope.measure_fall_time(oscope_id=oscope_id, channel=scope_channel, key="fall_ns")\n    col.shared.verify.verify_field(key="fall_ns", expected_val=fall_max_ns, tolerance=0.0)',
        },
        {
            "file": "test_common_mode_voltage.py",
            "block": "Vcm → limit",
            "doc": "One block: common-mode voltage.",
            "setup": "Diff probe; CM measurement.",
            "fills": "oscope_id = FILL_IN_HERE\nvcm_max = FILL_IN_HERE",
            "body": '    col.equipment.oscope.measure_common_mode(oscope_id=oscope_id, key="vcm")\n    col.shared.verify.verify_field(key="vcm", expected_val=vcm_max, tolerance=0.0)',
        },
        {
            "file": "test_differential_voltage.py",
            "block": "Vdiff → limit",
            "doc": "One block: differential voltage.",
            "setup": "Diff probe on pair.",
            "fills": "oscope_id = FILL_IN_HERE\nvdiff_expected = FILL_IN_HERE\nvdiff_tolerance = FILL_IN_HERE",
            "body": '    col.equipment.oscope.measure_differential(oscope_id=oscope_id, key="vdiff")\n    col.shared.verify.verify_field(key="vdiff", expected_val=vdiff_expected, tolerance=vdiff_tolerance)',
        },
        {
            "file": "test_loopback_pattern.py",
            "block": "loopback → pattern",
            "doc": "One block: GPIO loopback pattern.",
            "setup": "Loopback jumper J_GPIO_LB.",
            "fills": "dio_id = FILL_IN_HERE\nout_line = FILL_IN_HERE\nin_line = FILL_IN_HERE\ndirection_mask = FILL_IN_HERE\nexpected_read = FILL_IN_HERE  # bool",
            "body": '    col.io.dio.configure(dio_id=dio_id, direction=direction_mask)\n    col.io.dio.write_pin(dio_id=dio_id, line=out_line, value=True)\n    col.io.dio.read_pin(dio_id=dio_id, line=in_line, key="loopback")\n    col.shared.verify.verify_field(key="loopback", expected_val=expected_read)',
        },
    ],
)

topic(
    ROOT / "digital" / "i2c",
    "# [[io.i2c]]\n# i2c_id = 1",
    "I2C",
    "Level shifters if DUT is 1.8 V.",
    [
        {
            "file": "test_master_write_read.py",
            "block": "write/read → match",
            "doc": "One block: I2C master write-read.",
            "setup": "SCK/SDA on header.",
            "fills": "i2c_id = FILL_IN_HERE\ndevice_address = FILL_IN_HERE\nwrite_hex = FILL_IN_HERE\nread_len = FILL_IN_HERE\nexpected_hex = FILL_IN_HERE",
            "body": '    col.io.i2c.write_read(i2c_id=i2c_id, address=device_address, write=write_hex, read_len=read_len, key="i2c_data")\n    col.shared.verify.verify_field(key="i2c_data", expected_val=expected_hex)',
        },
        {
            "file": "test_slave_ack.py",
            "block": "probe → ACK",
            "doc": "One block: I2C address ACK.",
            "setup": "Device on bus.",
            "fills": "i2c_id = FILL_IN_HERE\ndevice_address = FILL_IN_HERE",
            "body": '    col.io.i2c.probe(i2c_id=i2c_id, address=device_address, key="i2c_ack")\n    col.shared.verify.verify_field(key="i2c_ack", expected_val=True)',
        },
    ],
)

topic(
    ROOT / "digital" / "spi",
    "# [[io.spi]]\n# spi_id = 1",
    "SPI",
    "CS/MOSI/MISO/SCK pin map.",
    [
        {
            "file": "test_master_transfer.py",
            "block": "transfer → pattern",
            "doc": "One block: SPI master transfer.",
            "setup": "SPI to DUT or EEPROM.",
            "fills": "spi_id = FILL_IN_HERE\ncs = FILL_IN_HERE\nmosi_hex = FILL_IN_HERE\nread_len = FILL_IN_HERE\nexpected_hex = FILL_IN_HERE",
            "body": '    col.io.spi.transfer(spi_id=spi_id, cs=cs, mosi=mosi_hex, read_len=read_len, key="spi_miso")\n    col.shared.verify.verify_field(key="spi_miso", expected_val=expected_hex)',
        },
        {
            "file": "test_slave_response.py",
            "block": "slave read → expected",
            "doc": "One block: SPI slave response.",
            "setup": "DUT in slave mode.",
            "fills": "spi_id = FILL_IN_HERE\ncs = FILL_IN_HERE\nexpected_hex = FILL_IN_HERE",
            "body": '    col.io.spi.transfer(spi_id=spi_id, cs=cs, mosi="", read_len=1, key="spi_slave")\n    col.shared.verify.verify_field(key="spi_slave", expected_val=expected_hex)',
        },
    ],
)

topic(
    ROOT / "digital" / "jtag",
    "# [[io.jtag]]\n# jtag_id = 1",
    "JTAG",
    "10-pin Cortex or custom header.",
    [
        {
            "file": "test_idcode.py",
            "block": "IDCODE → hex",
            "doc": "One block: JTAG IDCODE.",
            "setup": "JTAG adapter to DUT.",
            "fills": "jtag_id = FILL_IN_HERE\nexpected_idcode = FILL_IN_HERE",
            "body": '    col.io.jtag.read_idcode(jtag_id=jtag_id, key="idcode")\n    col.shared.verify.verify_field(key="idcode", expected_val=expected_idcode)',
        },
        {
            "file": "test_ir_dr_shift.py",
            "block": "DR shift → expected",
            "doc": "One block: JTAG DR readback.",
            "setup": "Known IR loaded.",
            "fills": "jtag_id = FILL_IN_HERE\nir_hex = FILL_IN_HERE\nexpected_dr = FILL_IN_HERE",
            "body": '    col.io.jtag.shift_dr(jtag_id=jtag_id, ir=ir_hex, key="dr")\n    col.shared.verify.verify_field(key="dr", expected_val=expected_dr)',
        },
    ],
)

# --- RF ---

RF_BENCH = """
[[equipment.vsg]]
vsg_id = 1
driver = sim
resource = SIM::VSG1

[[equipment.speca]]
speca_id = 1
driver = sim
resource = SIM::SA1

[[equipment.vna]]
vna_id = 1
driver = sim
resource = SIM::VNA1

[[equipment.pwrmeter]]
pwrmeter_id = 1
driver = sim
resource = SIM::PM1
"""

topic(
    ROOT / "rf" / "allan_deviation",
    "# [[equipment.fs740]]\n# fs740_id = 1",
    "RF Allan deviation",
    "FS740; 10 MHz ref; DUT LO input.",
    [
        {
            "file": "test_allan_sigma.py",
            "block": "Allan σ → max",
            "doc": "One block: Allan deviation at tau.",
            "setup": "FS740 reference input.",
            "autoconfig": True,
            "fills": "fs740_id = FILL_IN_HERE\ntau_s = FILL_IN_HERE\nallan_max = FILL_IN_HERE\nmeasurement_duration_s = FILL_IN_HERE",
            "body": '    col.equipment.fs740.measure_allan(fs740_id=fs740_id, tau_s=tau_s, duration_s=measurement_duration_s, key="allan_sigma")\n    col.shared.verify.verify_field(key="allan_sigma", expected_val=allan_max, tolerance=0.0)',
        },
    ],
)

topic(
    ROOT / "rf" / "frequency",
    RF_BENCH,
    "RF frequency",
    "Wideband scripts need trace save + SG smoothing.",
    [
        {
            "file": "test_peak_frequency.py",
            "block": "CW peak freq → expected",
            "doc": "One block: CW peak marker frequency.",
            "setup": "VSG CW into DUT; SA on output.",
            "autoconfig": True,
            "fills": "vsg_id = FILL_IN_HERE\nspeca_id = FILL_IN_HERE\ncenter_freq_hz = FILL_IN_HERE\nfreq_tolerance_hz = FILL_IN_HERE",
            "body": '    col.equipment.vsg.set_frequency(vsg_id=vsg_id, frequency=center_freq_hz)\n    col.equipment.vsg.set_output(vsg_id=vsg_id, enabled=True)\n    col.equipment.speca.peak_search(speca_id=speca_id, marker=1)\n    col.equipment.speca.measure_marker_frequency(speca_id=speca_id, marker=1, key="peak_f")\n    col.equipment.speca.verify_marker_frequency(key="peak_f", expected_val=center_freq_hz, tolerance=freq_tolerance_hz)',
        },
        {
            "file": "test_center_frequency.py",
            "block": "wideband CF → expected",
            "doc": "One block: center frequency from smoothed trace.",
            "setup": "Wideband stimulus; save trace first.",
            "autoconfig": True,
            "fills": 'speca_id = FILL_IN_HERE\ntrace_path = "traces/wideband.csv"\nsg_window_length = FILL_IN_HERE\nsg_polyorder = FILL_IN_HERE\nanalysis_start_hz = FILL_IN_HERE\nanalysis_stop_hz = FILL_IN_HERE\nexpected_cf_hz = FILL_IN_HERE\ncf_tolerance_hz = FILL_IN_HERE',
            "body": '    col.equipment.speca.save_trace_data(speca_id=speca_id, path=trace_path)\n    col.shared.signal.measure_center_frequency(trace_path=trace_path, key="cf_hz", sg_window_length=sg_window_length, sg_polyorder=sg_polyorder, start_hz=analysis_start_hz, stop_hz=analysis_stop_hz)\n    col.shared.verify.verify_field(key="cf_hz", expected_val=expected_cf_hz, tolerance=cf_tolerance_hz)',
        },
        {
            "file": "test_occupied_bandwidth.py",
            "block": "OBW → max Hz",
            "doc": "One block: occupied bandwidth from smoothed trace.",
            "setup": "Wideband trace required.",
            "autoconfig": True,
            "fills": 'speca_id = FILL_IN_HERE\ntrace_path = "traces/wideband.csv"\nsg_window_length = FILL_IN_HERE\nsg_polyorder = FILL_IN_HERE\nanalysis_start_hz = FILL_IN_HERE\nanalysis_stop_hz = FILL_IN_HERE\nthreshold_db = FILL_IN_HERE\nmax_obw_hz = FILL_IN_HERE',
            "body": '    col.equipment.speca.save_trace_data(speca_id=speca_id, path=trace_path)\n    col.shared.signal.measure_occupied_bandwidth(trace_path=trace_path, key="obw_hz", sg_window_length=sg_window_length, sg_polyorder=sg_polyorder, start_hz=analysis_start_hz, stop_hz=analysis_stop_hz, threshold_db=threshold_db)\n    col.shared.verify.verify_field(key="obw_hz", expected_val=max_obw_hz, tolerance=0.0)',
        },
    ],
)

topic(
    ROOT / "rf" / "gain_flatness",
    RF_BENCH,
    "Gain flatness",
    "Sweep with optional SG on power series.",
    [
        {
            "file": "test_gain_flatness_db.py",
            "block": "Gmax-Gmin → max dB",
            "doc": "One block: gain flatness over band.",
            "setup": "Through DUT path; cable loss table optional.",
            "autoconfig": True,
            "fills": "vsg_id = FILL_IN_HERE\nspeca_id = FILL_IN_HERE\nfreq_start_hz = FILL_IN_HERE\nfreq_stop_hz = FILL_IN_HERE\nfreq_step_hz = FILL_IN_HERE\ngain_flatness_max_db = FILL_IN_HERE\nsg_window_length = FILL_IN_HERE\nsg_polyorder = FILL_IN_HERE",
            "body": '    col.shared.signal.measure_gain_flatness(vsg_id=vsg_id, speca_id=speca_id, freq_start_hz=freq_start_hz, freq_stop_hz=freq_stop_hz, freq_step_hz=freq_step_hz, sg_window_length=sg_window_length, sg_polyorder=sg_polyorder, key="flatness_db")\n    col.shared.verify.verify_field(key="flatness_db", expected_val=gain_flatness_max_db, tolerance=0.0)',
        },
    ],
)

topic(
    ROOT / "rf" / "harmonics",
    RF_BENCH,
    "Harmonics",
    "Single CW tone; marker at n×f0.",
    [
        {
            "file": "test_fundamental_power.py",
            "block": "fundamental → expected dBm",
            "doc": "One block: fundamental power.",
            "setup": "CW tone at fundamental_hz.",
            "autoconfig": True,
            "fills": "vsg_id = FILL_IN_HERE\nspeca_id = FILL_IN_HERE\nfundamental_hz = FILL_IN_HERE\nexpected_power_dbm = FILL_IN_HERE\npower_tolerance_db = FILL_IN_HERE",
            "body": '    col.equipment.vsg.set_frequency(vsg_id=vsg_id, frequency=fundamental_hz)\n    col.equipment.vsg.set_output(vsg_id=vsg_id, enabled=True)\n    col.equipment.speca.set_center_frequency(speca_id=speca_id, frequency=fundamental_hz)\n    col.equipment.speca.peak_search(speca_id=speca_id, marker=1)\n    col.equipment.speca.measure_marker_power(speca_id=speca_id, marker=1, key="fund_dbm")\n    col.equipment.speca.verify_marker_power(key="fund_dbm", expected_val=expected_power_dbm, tolerance=power_tolerance_db)',
        },
        {
            "file": "test_h2_dbc.py",
            "block": "H2 dBc → max",
            "doc": "One block: 2nd harmonic dBc.",
            "setup": "Span covers 2×f0.",
            "autoconfig": True,
            "fills": "speca_id = FILL_IN_HERE\nfundamental_hz = FILL_IN_HERE\nmax_h2_dbc = FILL_IN_HERE",
            "body": '    col.equipment.speca.set_center_frequency(speca_id=speca_id, frequency=2 * fundamental_hz)\n    col.equipment.speca.peak_search(speca_id=speca_id, marker=1)\n    col.shared.signal.measure_harmonic_dbc(speca_id=speca_id, fundamental_hz=fundamental_hz, harmonic=2, key="h2_dbc")\n    col.shared.verify.verify_field(key="h2_dbc", expected_val=max_h2_dbc, tolerance=0.0)',
        },
        {
            "file": "test_h3_dbc.py",
            "block": "H3 dBc → max",
            "doc": "One block: 3rd harmonic dBc.",
            "setup": "Span covers 3×f0.",
            "autoconfig": True,
            "fills": "speca_id = FILL_IN_HERE\nfundamental_hz = FILL_IN_HERE\nmax_h3_dbc = FILL_IN_HERE",
            "body": '    col.equipment.speca.set_center_frequency(speca_id=speca_id, frequency=3 * fundamental_hz)\n    col.equipment.speca.peak_search(speca_id=speca_id, marker=1)\n    col.shared.signal.measure_harmonic_dbc(speca_id=speca_id, fundamental_hz=fundamental_hz, harmonic=3, key="h3_dbc")\n    col.shared.verify.verify_field(key="h3_dbc", expected_val=max_h3_dbc, tolerance=0.0)',
        },
    ],
)

topic(
    ROOT / "rf" / "masking",
    RF_BENCH,
    "Masking",
    "Mask CSV alongside trace; SG smoothing required.",
    [
        {
            "file": "test_mask_margin_db.py",
            "block": "mask margin → min dB",
            "doc": "One block: minimum margin below mask.",
            "setup": "Mask file path in FILL_IN_HERE.",
            "autoconfig": True,
            "fills": 'speca_id = FILL_IN_HERE\ntrace_path = "traces/mask.csv"\nmask_file = FILL_IN_HERE\nsg_window_length = FILL_IN_HERE\nsg_polyorder = FILL_IN_HERE\nmin_margin_db = FILL_IN_HERE',
            "body": '    col.equipment.speca.save_trace_data(speca_id=speca_id, path=trace_path)\n    col.shared.signal.measure_mask_margin_db(trace_path=trace_path, mask_path=mask_file, sg_window_length=sg_window_length, sg_polyorder=sg_polyorder, key="margin_db")\n    col.shared.verify.verify_field(key="margin_db", expected_val=min_margin_db, tolerance=0.0)',
        },
    ],
)

topic(
    ROOT / "rf" / "ip2_ip3",
    RF_BENCH,
    "IP2 / IP3",
    "Dual-tone; tones 1 MHz apart.",
    [
        {
            "file": "test_tone_f1_power.py",
            "block": "f1 power → expected",
            "doc": "One block: tone f1 power.",
            "setup": "Dual-tone stimulus active.",
            "autoconfig": True,
            "fills": "vsg_id = FILL_IN_HERE\nspeca_id = FILL_IN_HERE\nf1_hz = FILL_IN_HERE\nexpected_f1_dbm = FILL_IN_HERE\ntolerance_db = FILL_IN_HERE",
            "body": '    col.equipment.vsg.set_multicarrier(vsg_id=vsg_id, num_tones=2, spacing_hz=1e6)\n    col.equipment.vsg.set_frequency(vsg_id=vsg_id, frequency=f1_hz)\n    col.equipment.vsg.set_output(vsg_id=vsg_id, enabled=True)\n    col.equipment.speca.set_center_frequency(speca_id=speca_id, frequency=f1_hz)\n    col.equipment.speca.peak_search(speca_id=speca_id, marker=1)\n    col.equipment.speca.measure_marker_power(speca_id=speca_id, marker=1, key="f1_dbm")\n    col.equipment.speca.verify_marker_power(key="f1_dbm", expected_val=expected_f1_dbm, tolerance=tolerance_db)',
        },
        {
            "file": "test_tone_f2_power.py",
            "block": "f2 power → expected",
            "doc": "One block: tone f2 power.",
            "setup": "f2 = f1 + 1 MHz.",
            "autoconfig": True,
            "fills": "speca_id = FILL_IN_HERE\nf2_hz = FILL_IN_HERE\nexpected_f2_dbm = FILL_IN_HERE\ntolerance_db = FILL_IN_HERE",
            "body": '    col.equipment.speca.set_center_frequency(speca_id=speca_id, frequency=f2_hz)\n    col.equipment.speca.peak_search(speca_id=speca_id, marker=1)\n    col.equipment.speca.measure_marker_power(speca_id=speca_id, marker=1, key="f2_dbm")\n    col.equipment.speca.verify_marker_power(key="f2_dbm", expected_val=expected_f2_dbm, tolerance=tolerance_db)',
        },
        {
            "file": "test_im3_product_power.py",
            "block": "IM3 power → limit",
            "doc": "One block: IM3 product power at 2f2-f1.",
            "setup": "Dual-tone on air.",
            "autoconfig": True,
            "fills": "speca_id = FILL_IN_HERE\nf1_hz = FILL_IN_HERE\nf2_hz = FILL_IN_HERE\nmax_im3_dbm = FILL_IN_HERE",
            "body": '    im3_hz = 2 * f2_hz - f1_hz\n    col.equipment.speca.set_center_frequency(speca_id=speca_id, frequency=im3_hz)\n    col.equipment.speca.peak_search(speca_id=speca_id, marker=1)\n    col.equipment.speca.measure_marker_power(speca_id=speca_id, marker=1, key="im3_dbm")\n    col.shared.verify.verify_field(key="im3_dbm", expected_val=max_im3_dbm, tolerance=0.0)',
        },
        {
            "file": "test_oip3_dbm.py",
            "block": "OIP3 → minimum",
            "doc": "One block: output IP3.",
            "setup": "Measures f1, f2, IM3 then computes OIP3.",
            "autoconfig": True,
            "fills": "vsg_id = FILL_IN_HERE\nspeca_id = FILL_IN_HERE\nf1_hz = FILL_IN_HERE\nf2_hz = FILL_IN_HERE\noip3_min_dbm = FILL_IN_HERE",
            "body": '    im3_hz = 2 * f2_hz - f1_hz\n    col.shared.signal.measure_oip3(vsg_id=vsg_id, speca_id=speca_id, f1_hz=f1_hz, f2_hz=f2_hz, im3_hz=im3_hz, key="oip3_dbm")\n    col.shared.verify.verify_field(key="oip3_dbm", expected_val=oip3_min_dbm, tolerance=0.0)',
        },
    ],
)

topic(
    ROOT / "rf" / "p1db",
    RF_BENCH,
    "P1dB",
    "Input power sweep.",
    [
        {
            "file": "test_p1db_compression_dbm.py",
            "block": "P1dB → minimum",
            "doc": "One block: 1 dB compression point.",
            "setup": "Power sweep at output tap.",
            "autoconfig": True,
            "fills": "vsg_id = FILL_IN_HERE\nspeca_id = FILL_IN_HERE\npin_start_dbm = FILL_IN_HERE\npin_stop_dbm = FILL_IN_HERE\npin_step_db = FILL_IN_HERE\np1db_min_dbm = FILL_IN_HERE",
            "body": '    col.shared.signal.measure_p1db(vsg_id=vsg_id, speca_id=speca_id, pin_start_dbm=pin_start_dbm, pin_stop_dbm=pin_stop_dbm, pin_step_db=pin_step_db, key="p1db_dbm")\n    col.shared.verify.verify_field(key="p1db_dbm", expected_val=p1db_min_dbm, tolerance=0.0)',
        },
    ],
)

topic(
    ROOT / "rf" / "insertion_loss",
    RF_BENCH,
    "Insertion loss (S21)",
    "VNA S21; SOLT cal.",
    [
        {
            "file": "test_s21_max_db.py",
            "block": "max |S21| → limit",
            "doc": "One block: worst S21 over band.",
            "setup": "Through path; port extensions optional.",
            "autoconfig": True,
            "fills": "vna_id = FILL_IN_HERE\nstart_hz = FILL_IN_HERE\nstop_hz = FILL_IN_HERE\npoints = FILL_IN_HERE\ns21_max_db = FILL_IN_HERE",
            "body": '    col.equipment.vna.set_start_frequency(vna_id=vna_id, frequency_hz=start_hz)\n    col.equipment.vna.set_stop_frequency(vna_id=vna_id, frequency_hz=stop_hz)\n    col.equipment.vna.set_points(vna_id=vna_id, points=points)\n    col.equipment.vna.set_trace_parameters(vna_id=vna_id, trace=1, parameter="S21")\n    col.equipment.vna.single_sweep(vna_id=vna_id)\n    col.shared.signal.measure_s21_max(vna_id=vna_id, trace=1, key="s21_max")\n    col.shared.verify.verify_field(key="s21_max", expected_val=s21_max_db, tolerance=0.0)',
        },
        {
            "file": "test_s21_at_freq.py",
            "block": "|S21| at freq → limit",
            "doc": "One block: S21 at spot frequency.",
            "setup": "Marker at spot_freq_hz.",
            "autoconfig": True,
            "fills": "vna_id = FILL_IN_HERE\nspot_freq_hz = FILL_IN_HERE\ns21_at_freq_db = FILL_IN_HERE\ntolerance_db = FILL_IN_HERE",
            "body": '    col.equipment.vna.set_marker(vna_id=vna_id, marker=1, frequency_hz=spot_freq_hz, trace=1)\n    col.equipment.vna.measure_marker_value(vna_id=vna_id, marker=1, key="s21_spot", trace=1)\n    col.equipment.vna.verify_marker_value(key="s21_spot", expected_val=s21_at_freq_db, tolerance=tolerance_db)',
        },
    ],
)

topic(
    ROOT / "rf" / "return_loss",
    RF_BENCH,
    "Return loss (S11)",
    "VNA S11; SOLT cal.",
    [
        {
            "file": "test_s11_max_db.py",
            "block": "max |S11| → limit",
            "doc": "One block: worst S11 over band.",
            "setup": "Input port; cal kit.",
            "autoconfig": True,
            "fills": "vna_id = FILL_IN_HERE\nstart_hz = FILL_IN_HERE\nstop_hz = FILL_IN_HERE\npoints = FILL_IN_HERE\ns11_max_db = FILL_IN_HERE",
            "body": '    col.equipment.vna.set_trace_parameters(vna_id=vna_id, trace=1, parameter="S11")\n    col.equipment.vna.single_sweep(vna_id=vna_id)\n    col.shared.signal.measure_s11_max(vna_id=vna_id, trace=1, key="s11_max")\n    col.shared.verify.verify_field(key="s11_max", expected_val=s11_max_db, tolerance=0.0)',
        },
        {
            "file": "test_s11_at_freq.py",
            "block": "|S11| at freq → limit",
            "doc": "One block: S11 at spot frequency.",
            "setup": "Marker at spot_freq_hz.",
            "autoconfig": True,
            "fills": "vna_id = FILL_IN_HERE\nspot_freq_hz = FILL_IN_HERE\ns11_at_freq_db = FILL_IN_HERE\ntolerance_db = FILL_IN_HERE",
            "body": '    col.equipment.vna.set_marker(vna_id=vna_id, marker=1, frequency_hz=spot_freq_hz, trace=1)\n    col.equipment.vna.measure_marker_value(vna_id=vna_id, marker=1, key="s11_spot", trace=1)\n    col.equipment.vna.verify_marker_value(key="s11_spot", expected_val=s11_at_freq_db, tolerance=tolerance_db)',
        },
    ],
)

topic(
    ROOT / "rf" / "spurs",
    RF_BENCH,
    "Spurs",
    "Max-hold trace; SG smoothing.",
    [
        {
            "file": "test_spur_max_dbc.py",
            "block": "spur dBc → max",
            "doc": "One block: worst non-harmonic spur.",
            "setup": "Single tone; max-hold trace.",
            "autoconfig": True,
            "fills": 'speca_id = FILL_IN_HERE\ntrace_path = "traces/spurs.csv"\nfundamental_hz = FILL_IN_HERE\nsg_window_length = FILL_IN_HERE\nsg_polyorder = FILL_IN_HERE\nmax_spur_dbc = FILL_IN_HERE',
            "body": '    col.equipment.speca.save_trace_data(speca_id=speca_id, path=trace_path)\n    col.shared.signal.measure_spur_max_dbc(trace_path=trace_path, fundamental_hz=fundamental_hz, sg_window_length=sg_window_length, sg_polyorder=sg_polyorder, key="spur_dbc")\n    col.shared.verify.verify_field(key="spur_dbc", expected_val=max_spur_dbc, tolerance=0.0)',
        },
    ],
)

topic(
    ROOT / "rf" / "power_meter",
    RF_BENCH,
    "RF power meter",
    "Sensor at test frequency.",
    [
        {
            "file": "test_avg_power_dbm.py",
            "block": "avg power → window",
            "doc": "One block: averaged RF power.",
            "setup": "Set sensor frequency.",
            "autoconfig": True,
            "fills": "pwrmeter_id = FILL_IN_HERE\nfreq_hz = FILL_IN_HERE\navg_count = FILL_IN_HERE\nexpected_power_dbm = FILL_IN_HERE\ntolerance_db = FILL_IN_HERE",
            "body": '    col.equipment.pwrmeter.set_frequency(pwrmeter_id=pwrmeter_id, frequency=freq_hz)\n    col.equipment.pwrmeter.set_averaging_count(pwrmeter_id=pwrmeter_id, count=avg_count)\n    col.equipment.pwrmeter.measure_power(pwrmeter_id=pwrmeter_id, key="avg_dbm")\n    col.equipment.pwrmeter.verify_power(key="avg_dbm", expected_val=expected_power_dbm, tolerance=tolerance_db)',
        },
        {
            "file": "test_peak_power_dbm.py",
            "block": "peak power → limit",
            "doc": "One block: peak/instantaneous power.",
            "setup": "Averaging off.",
            "autoconfig": True,
            "fills": "pwrmeter_id = FILL_IN_HERE\nfreq_hz = FILL_IN_HERE\nmax_peak_dbm = FILL_IN_HERE",
            "body": '    col.equipment.pwrmeter.set_frequency(pwrmeter_id=pwrmeter_id, frequency=freq_hz)\n    col.equipment.pwrmeter.set_averaging_count(pwrmeter_id=pwrmeter_id, count=1)\n    col.equipment.pwrmeter.measure_power(pwrmeter_id=pwrmeter_id, key="peak_dbm")\n    col.shared.verify.verify_field(key="peak_dbm", expected_val=max_peak_dbm, tolerance=0.0)',
        },
        {
            "file": "test_band_power_dbm.py",
            "block": "band power → limit",
            "doc": "One block: power in band.",
            "setup": "Band limits in FILL_IN_HERE.",
            "autoconfig": True,
            "fills": "speca_id = FILL_IN_HERE\nband_start_hz = FILL_IN_HERE\nband_stop_hz = FILL_IN_HERE\nmax_band_power_dbm = FILL_IN_HERE",
            "body": '    col.shared.signal.measure_band_power_dbm(speca_id=speca_id, start_hz=band_start_hz, stop_hz=band_stop_hz, key="band_dbm")\n    col.shared.verify.verify_field(key="band_dbm", expected_val=max_band_power_dbm, tolerance=0.0)',
        },
    ],
)

# --- POWER ---

PWR = """
[[equipment.psu]]
psu_id = 1
driver = sim
resource = SIM::PSU1

[[equipment.eload]]
eload_id = 1
driver = sim
resource = SIM::ELOAD1

[[equipment.oscope]]
oscope_id = 1
driver = sim
resource = SIM::SCOPE1
"""

topic(
    ROOT / "power" / "transient",
    PWR,
    "Transient response",
    "PSU on; eload step; scope on rail.",
    [
        {
            "file": "test_overshoot_mv.py",
            "block": "overshoot → max mV",
            "doc": "One block: rail overshoot after load step.",
            "setup": "Scope AC on rail; Kelvin sense.",
            "fills": "psu_id = FILL_IN_HERE\neload_id = FILL_IN_HERE\noscope_id = FILL_IN_HERE\nrail_v = FILL_IN_HERE\nload_step_a = FILL_IN_HERE\nmax_overshoot_mv = FILL_IN_HERE",
            "body": '    col.equipment.psu.set_voltage(psu_id=psu_id, voltage=rail_v)\n    col.equipment.psu.set_output(psu_id=psu_id, enabled=True)\n    col.equipment.eload.set_current(eload_id=eload_id, current=load_step_a)\n    col.equipment.eload.engage(eload_id=eload_id)\n    col.equipment.oscope.measure_overshoot_mv(oscope_id=oscope_id, key="overshoot_mv")\n    col.shared.verify.verify_field(key="overshoot_mv", expected_val=max_overshoot_mv, tolerance=0.0)',
        },
        {
            "file": "test_undershoot_mv.py",
            "block": "undershoot → max mV",
            "doc": "One block: rail undershoot.",
            "setup": "Load step release.",
            "fills": "psu_id = FILL_IN_HERE\neload_id = FILL_IN_HERE\noscope_id = FILL_IN_HERE\nrail_v = FILL_IN_HERE\nload_step_a = FILL_IN_HERE\nmax_undershoot_mv = FILL_IN_HERE",
            "body": '    col.equipment.psu.set_voltage(psu_id=psu_id, voltage=rail_v)\n    col.equipment.eload.set_current(eload_id=eload_id, current=load_step_a)\n    col.equipment.eload.disengage(eload_id=eload_id)\n    col.equipment.oscope.measure_undershoot_mv(oscope_id=oscope_id, key="undershoot_mv")\n    col.shared.verify.verify_field(key="undershoot_mv", expected_val=max_undershoot_mv, tolerance=0.0)',
        },
        {
            "file": "test_settle_time_ms.py",
            "block": "settle time → max ms",
            "doc": "One block: rail settle time.",
            "setup": "After load step.",
            "fills": "oscope_id = FILL_IN_HERE\nmax_settle_ms = FILL_IN_HERE",
            "body": '    col.equipment.oscope.measure_settle_time(oscope_id=oscope_id, key="settle_ms")\n    col.shared.verify.verify_field(key="settle_ms", expected_val=max_settle_ms, tolerance=0.0)',
        },
    ],
)

topic(
    ROOT / "power" / "eload",
    PWR,
    "Electronic load",
    "Eload ramp and steady load.",
    [
        {
            "file": "test_rail_voltage_under_load.py",
            "block": "Vrail under load → min",
            "doc": "One block: rail voltage at load.",
            "setup": "Steady I_load.",
            "fills": "psu_id = FILL_IN_HERE\neload_id = FILL_IN_HERE\nrail_v = FILL_IN_HERE\nload_current_a = FILL_IN_HERE\nmin_voltage_v = FILL_IN_HERE",
            "body": '    col.equipment.psu.set_voltage(psu_id=psu_id, voltage=rail_v)\n    col.equipment.psu.set_output(psu_id=psu_id, enabled=True)\n    col.equipment.eload.set_current(eload_id=eload_id, current=load_current_a)\n    col.equipment.eload.engage(eload_id=eload_id)\n    col.equipment.psu.measure_voltage(psu_id=psu_id, key="vrail")\n    col.equipment.psu.verify_voltage(key="vrail", expected_val=min_voltage_v, tolerance=0.1)',
        },
        {
            "file": "test_current_monotonic_ramp.py",
            "block": "ramp → monotonic",
            "doc": "One block: monotonic current ramp.",
            "setup": "Simulate inductive load profile.",
            "fills": "eload_id = FILL_IN_HERE\ni_start_a = FILL_IN_HERE\ni_stop_a = FILL_IN_HERE\nramp_rate_a_per_s = FILL_IN_HERE",
            "body": '    col.shared.signal.ramp_eload_current(eload_id=eload_id, i_start_a=i_start_a, i_stop_a=i_stop_a, rate_a_per_s=ramp_rate_a_per_s, key="ramp_ok")\n    col.shared.verify.verify_field(key="ramp_ok", expected_val=True)',
        },
    ],
)

# Remove legacy gpio_toggle after gpio folder exists
import shutil

legacy = ROOT / "digital" / "gpio_toggle"
if legacy.is_dir():
    shutil.rmtree(legacy)

print("Catalog scaffold complete.")

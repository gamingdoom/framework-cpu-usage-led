
# Framework CPU Usage LED  
Control the Framework Laptop's LED colors based on CPU usage. Inspired by [this forum post](https://community.frame.work/t/reprogramming-the-leds-for-the-holidays/12906).  
  
# Setup  
Install `fw-ectool`. This can be installed on Arch Linux via `fw-ectool-git` on the AUR. Install psutil so the script can get CPU usage. This can be installed on Arch Linux via the `python-psutil` package.  
  
Clone this repo and and edit the parameters inside `cpu-usage-led.py` like `ledsToChange` and `privilegeEscalation`. If you use `privilegeEscalation = None`, run the script as root.  
  
When you have edited the script to your liking, run it. The script sets LEDs to the default behaviour when the lid is closed so there is no need to kill the script when the lid is closed. You can just run the script at boot.  
  
<details>  
<summary>Autostart using systemd</summary>  
On systems using systemd, the Python script can be run automatically on boot. Note that the <i>privilegeEscalation = None</i> line should remain unchanged if used as a systemd service.

1. Move `cpu-usage-led.py` to `/usr/local/bin/` so that `/usr/local/bin/cpu-usage-led.py` is present and run `chmod +x /usr/local/bin/cpu-usage-led.py`.  
2. Move `cpu-usage-led.service` to `/etc/systemd/system/` so that `/etc/systemd/system/cpu-usage-led.service` is present.  
3. Run `systemctl daemon-reload`.  
4. Run `systemctl enable cpu-usage-led.service`.  
	- To launch the service, run `systemctl start cpu-usage-led.service`.  
</details>

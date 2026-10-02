# Monitoring MikroTik RouterOS 7 BGP in Zabbix

Python script to discover and monitor BGP of MikroTik RouterOS 7 based network devices in Zabbix.

### Installation
#### Installation in OS
> The entire installation process will be demonstrated using the **Ubuntu** operating system.

1. The script uses `librouteros` python package. Thats why first of all we need to upgrade `pip` and install `librouteros` package globally.
    ```shell
    sudo python3 -m pip install --upgrade pip
    sudo python3 -m pip install librouteros
    ```

2. Then we need to download `ros7_bgp_zabbix.py` script to `externalscripts` folder on **Zabbix server**. The location of the folder depends on `ExternalScripts` option in `/etc/zabbix/zabbix_server.conf` file. The default value is `/usr/lib/zabbix/externalscripts`.
    ```shell
    cd ~
    git clone git@github.com:05netcon/ros7-bgp-zabbix.git
    cd ros7-bgp-zabbix
    sudo cp ros7_bgp_zabbix.py /usr/lib/zabbix/externalscripts
    ```
3. The script needs to be assigned the execution bit.
    ```shell
    sudo chmod +x /usr/lib/zabbix/externalscripts/ros7_bgp_zabbix.py
    ```
4. By default, the **Zabbix server** runs as the `zabbix` user. The permissions for the folder and file need to be changed appropriately.
    ```shell
    sudo chown -R zabbix:zabbix /usr/lib/zabbix/externalscripts
    sudo chmod -R 755 /usr/lib/zabbix/externalscripts
    ```
#### Installation in Zabbix
1. In the leftside menu go to `Data Collection -> Templates`.

2. Click the `Import` button in the top right corner.

3. Click `Browse` and choose `ros7_bgp_zabbix.xml` template file from `templates` folder of the project you cloned from **GitHub** earlier.
   > There are three files with different extensions in the folder. You can choose any of them.

4. Click `Import` button.

5. In the leftside menu go to `Data Collection -> Hosts`.

6. Choose **MikroTik RouterOS 7** based network device.

7. In `Macros` tab add `{$USERNAME}` and `{$PASSWORD}` macros with the corresponding values.

8. In `Host` tab to the right of the `Templates` item, click the `Select` button.

9. Choose `RouterOS 7 BGP` template imported earlier.

10. Click `Update`.

### CLI usage
```
usage: ros7_bgp_zabbix.py [-h] [-p] command host username password

Monitoring MikroTik RouterOS 7 BGP in Zabbix

positional arguments:
  command       script operating mode (discover | status)
  host          device hostname or ip address
  username      device username
  password      device password

options:
  -h, --help    show this help message and exit
  -p , --peer   peer name (only if in status mode)
  ```

### Data format returned when `discover` parameter is passed
```json
{
    "data": [
        {
            "{#BGPPEER}": "peer01_name"
        },
        {
            "{#BGPPEER}": "peer02_name"
        }
    ]
}
```

> When `status` parameter is passed, **1** is returned if peers status is in `established` state. Otherwise **0** is returned.
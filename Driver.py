from ConfigCheck import ConfigCheck


def main():
    config_a = [
        {
        "ip_start" : 100,
        "ip_end": 400,
        "port_start": 30,
        "port_end": 50,
        "protocol": "TCP",
        "direction": "IN"
        }, 
    ]
    config_b = [
        {
        "ip_start" : 100,
        "ip_end": 200,
        "port_start": 30,
        "port_end": 50,
        "protocol": "TCP",
        "direction": "IN"
        },
        {
        "ip_start" : 200,
        "ip_end": 300,
        "port_start": 30,
        "port_end": 50,
        "protocol": "TCP",
        "direction": "IN"
        }, 
        {
        "ip_start" : 300,
        "ip_end": 400,
        "port_start": 30,
        "port_end": 50,
        "protocol": "TCP",
        "direction": "IN"
        },  
    ]
    conf_checker = ConfigCheck(config_a, config_b)
    if (conf_checker.compare_configs()):
        print("Both configs are the same")
    else:
        print("Not the same configs")

if __name__ == "__main__":
    main()
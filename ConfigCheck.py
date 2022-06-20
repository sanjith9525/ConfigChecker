import functools
from typing import Dict
from IPRange import IPRange


class ConfigCheck:

    def __init__(self, config_a, config_b) -> None:
        self.configs_a = config_a
        self.configs_b = config_b

    def merge_config_range(self, configs, config_range):
        if not configs:
            configs.append(config_range)
        else:
            prev_config = configs[-1]
            if prev_config.ip_end >= config_range.ip_start:
                if(self.check_port_ranges(prev_config.port_range, config_range.port_range)):
                    prev_config.ip_end = config_range.ip_end
                    
                else:
                    configs.pop()
                    if (config_range.ip_start > prev_config.ip_start):
                        configs.append(IPRange(prev_config.ip_start, config_range.ip_start, prev_config.port_range))
                    mid_range = self.combine_port_ranges(prev_config.port_range, config_range.port_range)
                    if prev_config.ip_end > config_range.ip_end:
                        configs.append(IPRange(config_range.ip_start+1, config_range.ip_end, mid_range))
                        configs.append(IPRange(config_range.ip_end+1, prev_config.ip_end, prev_config.port_range))
                    else:
                        configs.append(IPRange(config_range.ip_start+1, prev_config.ip_end, mid_range))
                        configs.append(IPRange(prev_config.ip_end+1, prev_config.ip_end, config_range.port_range))
            else:
                configs.append(config_range)



    def combine_port_ranges(self, pr_a, pr_b):
        combined_range = []
        i=0
        j=0
        while(i<len(pr_a) and j<len(pr_b)):
            
            if i == len(pr_a):
                selected = pr_b[j]
                j += 1
            elif j == len(pr_b):
                selected = pr_a[i]
                i += 1
            else:
                if pr_a[i][0] <= pr_b[j][0]:
                    selected = pr_a[i]
                    i += 1
                else:
                    selected = pr_b[j]
                    j += 1

            if combined_range and selected[0] <= combined_range[-1][1]:
                combined_range[-1][1] = selected[1]
            else:
                combined_range.append(selected)
        return combined_range 

        

    def make_unified_config(self, configs):
        unified_config = {'TCP_IN': [], 'TCP_OUT': [], 'UDP_IN': [], 'UDP_OUT': []}
        for config in configs:
            protocol_dir = config["protocol"]+"_"+config["direction"]
            config_range = IPRange(config["ip_start"], config["ip_end"], [[config["port_start"], config["port_end"]]])
            self.merge_config_range(unified_config[protocol_dir], config_range)

        return unified_config

    def check_port_ranges(self, pr_a, pr_b):
        if len(pr_a) != len(pr_b):
            return False
        for a,b in zip(pr_a,pr_b):
            print(a,b)
            if a[0] is not b[0] or a[1] is not b[1]:
                return False
        return True

    def compare_unified_configs(self, unified_config_a, unified_config_b):
        for each_protocol_dir in unified_config_a:
            if len(unified_config_a[each_protocol_dir]) != len(unified_config_b[each_protocol_dir]):
                return False
            for a,b in zip(unified_config_a[each_protocol_dir], unified_config_b[each_protocol_dir]):
                if a.ip_start != b.ip_start or a.ip_end != b.ip_end:
                    return False
                if not self.check_port_ranges(a.port_range,b.port_range):
                    return False
        return True

    def compare_configs(self):
        def compare(x,y):
            if x["ip_start"] == y["ip_start"]:
                return x["port_start"] - y["port_start"]
            else:
                return x["ip_start"] - y["ip_start"]
        sorted(self.configs_a, key=functools.cmp_to_key(compare))
        sorted(self.configs_b, key=functools.cmp_to_key(compare))
        unified_config_a = self.make_unified_config(self.configs_a)
        unified_config_b = self.make_unified_config(self.configs_b)
        return self.compare_unified_configs(unified_config_a, unified_config_b)








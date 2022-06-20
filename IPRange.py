class IPRange:
    def __init__(self, ip_start, ip_end, port_range) -> None:
        self.ip_start = ip_start
        self.ip_end = ip_end
        self.port_range = port_range
        #self.port_range.append([port_start,port_end])
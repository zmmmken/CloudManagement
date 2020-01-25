class Cloud:
    def __init__(self, cloud_id, daily_price, storage_size, ram, cpu_core, cpu_rate, bandwidth, create_date, ssh_hash, ssh_salt, os_id, passport_id, platform_pk):
        self.cloud_id = cloud_id
        self.daily_price = daily_price
        self.storage_size = storage_size
        self.ram = ram
        self.cpu_core = cpu_core
        self.cpu_rate = cpu_rate
        self.bandwidth = bandwidth
        self.create_date = create_date
        self.ssh_hash = ssh_hash
        self.platform_pk = platform_pk
        self.passport_id = passport_id
        self.ssh_salt = ssh_salt

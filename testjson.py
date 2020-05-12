import json
import time

import pymysql
from sqlalchemy import engine, create_engine


x = b'{"Title":"MAC Miner","IP":"47.112.128.28\\n","IPInt":"172.18.245.7\\n","CPUID":"13197016915918185882701231384169","CPUInfo":"{\\"cpu\\":0,\\"vendorId\\":\\"GenuineIntel\\",\\"family\\":\\"6\\",\\"model\\":\\"85\\",\\"stepping\\":4,\\"physicalId\\":\\"0\\",\\"coreId\\":\\"0\\",\\"cores\\":1,\\"modelName\\":\\"Intel(R) Xeon(R) Platinum 8163 CPU @ 2.50GHz\\",\\"mhz\\":2499.996,\\"cacheSize\\":33792,\\"flags\\":[\\"fpu\\",\\"vme\\",\\"de\\",\\"pse\\",\\"tsc\\",\\"msr\\",\\"pae\\",\\"mce\\",\\"cx8\\",\\"apic\\",\\"sep\\",\\"mtrr\\",\\"pge\\",\\"mca\\",\\"cmov\\",\\"pat\\",\\"pse36\\",\\"clflush\\",\\"mmx\\",\\"fxsr\\",\\"sse\\",\\"sse2\\",\\"ss\\",\\"ht\\",\\"syscall\\",\\"nx\\",\\"pdpe1gb\\",\\"rdtscp\\",\\"lm\\",\\"constant_tsc\\",\\"rep_good\\",\\"nopl\\",\\"eagerfpu\\",\\"pni\\",\\"pclmulqdq\\",\\"ssse3\\",\\"fma\\",\\"cx16\\",\\"pcid\\",\\"sse4_1\\",\\"sse4_2\\",\\"x2apic\\",\\"movbe\\",\\"popcnt\\",\\"tsc_deadline_timer\\",\\"aes\\",\\"xsave\\",\\"avx\\",\\"f16c\\",\\"rdrand\\",\\"hypervisor\\",\\"lahf_lm\\",\\"abm\\",\\"3dnowprefetch\\",\\"ibrs\\",\\"ibpb\\",\\"stibp\\",\\"fsgsbase\\",\\"tsc_adjust\\",\\"bmi1\\",\\"hle\\",\\"avx2\\",\\"smep\\",\\"bmi2\\",\\"erms\\",\\"invpcid\\",\\"rtm\\",\\"mpx\\",\\"avx512f\\",\\"avx512dq\\",\\"rdseed\\",\\"adx\\",\\"smap\\",\\"avx512cd\\",\\"avx512bw\\",\\"avx512vl\\",\\"xsaveopt\\",\\"xsavec\\",\\"xgetbv1\\",\\"spec_ctrl\\",\\"intel_stibp\\"],\\"microcode\\":\\"0x1\\"}{\\"cpu\\":1,\\"vendorId\\":\\"GenuineIntel\\",\\"family\\":\\"6\\",\\"model\\":\\"85\\",\\"stepping\\":4,\\"physicalId\\":\\"0\\",\\"coreId\\":\\"0\\",\\"cores\\":1,\\"modelName\\":\\"Intel(R) Xeon(R) Platinum 8163 CPU @ 2.50GHz\\",\\"mhz\\":2499.996,\\"cacheSize\\":33792,\\"flags\\":[\\"fpu\\",\\"vme\\",\\"de\\",\\"pse\\",\\"tsc\\",\\"msr\\",\\"pae\\",\\"mce\\",\\"cx8\\",\\"apic\\",\\"sep\\",\\"mtrr\\",\\"pge\\",\\"mca\\",\\"cmov\\",\\"pat\\",\\"pse36\\",\\"clflush\\",\\"mmx\\",\\"fxsr\\",\\"sse\\",\\"sse2\\",\\"ss\\",\\"ht\\",\\"syscall\\",\\"nx\\",\\"pdpe1gb\\",\\"rdtscp\\",\\"lm\\",\\"constant_tsc\\",\\"rep_good\\",\\"nopl\\",\\"eagerfpu\\",\\"pni\\",\\"pclmulqdq\\",\\"ssse3\\",\\"fma\\",\\"cx16\\",\\"pcid\\",\\"sse4_1\\",\\"sse4_2\\",\\"x2apic\\",\\"movbe\\",\\"popcnt\\",\\"tsc_deadline_timer\\",\\"aes\\",\\"xsave\\",\\"avx\\",\\"f16c\\",\\"rdrand\\",\\"hypervisor\\",\\"lahf_lm\\",\\"abm\\",\\"3dnowprefetch\\",\\"ibrs\\",\\"ibpb\\",\\"stibp\\",\\"fsgsbase\\",\\"tsc_adjust\\",\\"bmi1\\",\\"hle\\",\\"avx2\\",\\"smep\\",\\"bmi2\\",\\"erms\\",\\"invpcid\\",\\"rtm\\",\\"mpx\\",\\"avx512f\\",\\"avx512dq\\",\\"rdseed\\",\\"adx\\",\\"smap\\",\\"avx512cd\\",\\"avx512bw\\",\\"avx512vl\\",\\"xsaveopt\\",\\"xsavec\\",\\"xgetbv1\\",\\"spec_ctrl\\",\\"intel_stibp\\"],\\"microcode\\":\\"0x1\\"}{\\"cpu\\":2,\\"vendorId\\":\\"GenuineIntel\\",\\"family\\":\\"6\\",\\"model\\":\\"85\\",\\"stepping\\":4,\\"physicalId\\":\\"0\\",\\"coreId\\":\\"1\\",\\"cores\\":1,\\"modelName\\":\\"Intel(R) Xeon(R) Platinum 8163 CPU @ 2.50GHz\\",\\"mhz\\":2499.996,\\"cacheSize\\":33792,\\"flags\\":[\\"fpu\\",\\"vme\\",\\"de\\",\\"pse\\",\\"tsc\\",\\"msr\\",\\"pae\\",\\"mce\\",\\"cx8\\",\\"apic\\",\\"sep\\",\\"mtrr\\",\\"pge\\",\\"mca\\",\\"cmov\\",\\"pat\\",\\"pse36\\",\\"clflush\\",\\"mmx\\",\\"fxsr\\",\\"sse\\",\\"sse2\\",\\"ss\\",\\"ht\\",\\"syscall\\",\\"nx\\",\\"pdpe1gb\\",\\"rdtscp\\",\\"lm\\",\\"constant_tsc\\",\\"rep_good\\",\\"nopl\\",\\"eagerfpu\\",\\"pni\\",\\"pclmulqdq\\",\\"ssse3\\",\\"fma\\",\\"cx16\\",\\"pcid\\",\\"sse4_1\\",\\"sse4_2\\",\\"x2apic\\",\\"movbe\\",\\"popcnt\\",\\"tsc_deadline_timer\\",\\"aes\\",\\"xsave\\",\\"avx\\",\\"f16c\\",\\"rdrand\\",\\"hypervisor\\",\\"lahf_lm\\",\\"abm\\",\\"3dnowprefetch\\",\\"ibrs\\",\\"ibpb\\",\\"stibp\\",\\"fsgsbase\\",\\"tsc_adjust\\",\\"bmi1\\",\\"hle\\",\\"avx2\\",\\"smep\\",\\"bmi2\\",\\"erms\\",\\"invpcid\\",\\"rtm\\",\\"mpx\\",\\"avx512f\\",\\"avx512dq\\",\\"rdseed\\",\\"adx\\",\\"smap\\",\\"avx512cd\\",\\"avx512bw\\",\\"avx512vl\\",\\"xsaveopt\\",\\"xsavec\\",\\"xgetbv1\\",\\"spec_ctrl\\",\\"intel_stibp\\"],\\"microcode\\":\\"0x1\\"}{\\"cpu\\":3,\\"vendorId\\":\\"GenuineIntel\\",\\"family\\":\\"6\\",\\"model\\":\\"85\\",\\"stepping\\":4,\\"physicalId\\":\\"0\\",\\"coreId\\":\\"1\\",\\"cores\\":1,\\"modelName\\":\\"Intel(R) Xeon(R) Platinum 8163 CPU @ 2.50GHz\\",\\"mhz\\":2499.996,\\"cacheSize\\":33792,\\"flags\\":[\\"fpu\\",\\"vme\\",\\"de\\",\\"pse\\",\\"tsc\\",\\"msr\\",\\"pae\\",\\"mce\\",\\"cx8\\",\\"apic\\",\\"sep\\",\\"mtrr\\",\\"pge\\",\\"mca\\",\\"cmov\\",\\"pat\\",\\"pse36\\",\\"clflush\\",\\"mmx\\",\\"fxsr\\",\\"sse\\",\\"sse2\\",\\"ss\\",\\"ht\\",\\"syscall\\",\\"nx\\",\\"pdpe1gb\\",\\"rdtscp\\",\\"lm\\",\\"constant_tsc\\",\\"rep_good\\",\\"nopl\\",\\"eagerfpu\\",\\"pni\\",\\"pclmulqdq\\",\\"ssse3\\",\\"fma\\",\\"cx16\\",\\"pcid\\",\\"sse4_1\\",\\"sse4_2\\",\\"x2apic\\",\\"movbe\\",\\"popcnt\\",\\"tsc_deadline_timer\\",\\"aes\\",\\"xsave\\",\\"avx\\",\\"f16c\\",\\"rdrand\\",\\"hypervisor\\",\\"lahf_lm\\",\\"abm\\",\\"3dnowprefetch\\",\\"ibrs\\",\\"ibpb\\",\\"stibp\\",\\"fsgsbase\\",\\"tsc_adjust\\",\\"bmi1\\",\\"hle\\",\\"avx2\\",\\"smep\\",\\"bmi2\\",\\"erms\\",\\"invpcid\\",\\"rtm\\",\\"mpx\\",\\"avx512f\\",\\"avx512dq\\",\\"rdseed\\",\\"adx\\",\\"smap\\",\\"avx512cd\\",\\"avx512bw\\",\\"avx512vl\\",\\"xsaveopt\\",\\"xsavec\\",\\"xgetbv1\\",\\"spec_ctrl\\",\\"intel_stibp\\"],\\"microcode\\":\\"0x1\\"}\\npercent:[66.666667]","MACID":"Name:\\tlo  Address:\\t\\nName:\\teth0  Address:\\t00:16:3e:10:20:36\\n","DISKID":" /dev/vda HDD (40GB) virtio [@pci-0000:00:05.0 (node #0)] vendor=0x1af4\\n /dev/vdb HDD (500GB) virtio [@pci-0000:00:06.0 (node #0)] vendor=0x1af4\\n","UUID":"1255442998060457984","Key":"0","Msg":""}'

x1="hello test"
def insert_json(topic, info):
    for key in info:
        val = info[key]

        if len(val) > 1024:
            val = val[0:1023]
        # sqlparams = f"INSERT into MACMessageTable  (clientID,time,topic,message)  VALUES (\"{key}\",now(),\"{topic}\",\"{val}\"); "
        sql=""
        with connection.cursor() as cursor:
            sql = 'INSERT into MACMessageTable  (clientID,time,topic,message) VALUES (%s, now(),%s,%s)'
            cursor.execute(sql, (key,topic,val))

        print(f"run sql:{sql}")
    connection.commit()

connection = pymysql.connect(host='localhost',
                             user='tiger',
                             password='test123456!@',
                             db='test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    sql = "create table IF NOT EXISTS `MACMessageTable` (`clientID` varchar(32),`time` time, `topic` varchar(32),`message` varchar(1024) ); "
    cursor.execute(sql)
    connection.commit()


try:
    info = json.loads(x1)
    insert_json("mtopic", info)
except ValueError:
    print(f"receive error:{x1}")

import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

async def run():
    errorIndication, errorStatus, errorIndex, varBinds = await set_cmd(
        SnmpEngine(),
        CommunityData('private'),
        await UdpTransportTarget.create(('172.19.4.196', 161)),
        ContextData(),
        ObjectType(ObjectIdentity("1.3.6.1.4.1.37576.3.1.2.1.1.5.1"), Integer(4))
    )
    print(errorIndication, errorStatus, errorIndex, varBinds)

asyncio.run(run())
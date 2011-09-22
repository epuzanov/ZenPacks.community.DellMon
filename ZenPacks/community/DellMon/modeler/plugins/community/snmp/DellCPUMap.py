################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellCPUMap

DellCPUMap maps the processorDeviceTable and processorDeviceStatusTable tables
to cpu objects

$Id: DellCPUMap.py,v 1.2 2011/09/21 18:34:01 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class DellCPUMap(SnmpPlugin):
    """Map Dell System Management cpu table to model."""

    maptype = "CPUMap"
    modname = "ZenPacks.community.DellMon.DellCPU"
    relname = "cpus"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('hrProcessorTable',
                    '.1.3.6.1.2.1.25.3.3.1',
                    {
                        '.1': '_cpuidx',
                    }
        ),
        GetTableMap('cpuTable',
                    '.1.3.6.1.4.1.674.10892.1.1100.30.1',
                    {
                        '.2': 'socket',
                        '.8': '_manuf',
                        '.12': 'clockspeed',
                        '.13': 'extspeed',
                        '.14': 'voltage',
                        '.16': 'setProductKey',
                        '.17': 'core',
                    }
        ),
        GetTableMap('cacheTable',
                    '.1.3.6.1.4.1.674.10892.1.1100.40.1',
                    {
                        '.6': 'cpuidx',
                        '.11': 'level',
                        '.13': 'size',
                    }
        ),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        cores = len(tabledata.get("hrProcessorTable", '')) / (len(tabledata.get(
                                                        "cpuTable", '1')) or 1)
        rm = self.relMap()
        cachemap = {}
        for cache in tabledata.get("cacheTable", {}).values():
            if cache['level'] < 3: continue
            if not cachemap.has_key(cache['cpuidx']):
                cachemap[cache['cpuidx']] = {}
            cachemap[cache['cpuidx']][cache['level']-2] = cache.get('size', 0)
        for oid, cpu in tabledata.get("cpuTable", {}).iteritems():
            om = self.objectMap(cpu)
            om.id = self.prepId("socket%s" % (om.socket))
            om.core = getattr(om, 'core', 0) or cores
            if not getattr(om, 'setProductKey', ''):
                om.setProductKey = 'Unknown Processor'
            om.setProductKey = MultiArgs(om.setProductKey.replace("(R)", ""),
                                        om.setProductKey.split()[0])
            for clevel, csize in cachemap[om.socket].iteritems():
                setattr(om, "cacheSizeL%d"%clevel, csize)
            rm.append(om)
        return rm


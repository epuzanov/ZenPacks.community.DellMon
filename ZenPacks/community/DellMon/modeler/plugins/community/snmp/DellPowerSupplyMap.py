################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellPowerSupplyMap

DellPowerSupplyMap maps the powerSupplyTable table to powersupplies objects

$Id: DellPowerSupplyMap.py,v 1.2 2011/09/21 19:09:48 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class DellPowerSupplyMap(SnmpPlugin):
    """Map Dell System Management Power Supplies table to model."""

    maptype = "PowerSupplyMap"
    modname = "ZenPacks.community.DellMon.DellPowerSupply"
    relname = "powersupplies"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('powerSupplyTable',
                    '.1.3.6.1.4.1.674.10892.1.600.12.1',
                    {
                        '.5': 'status',
                        '.6': 'watts',
                        '.7': 'type',
                        '.8': '_location',
                        '.9': 'volts',
                        '.11': '_presence',
                    }
        ),
        GetTableMap('powerSupplyVPTable',
                    '.1.3.6.1.4.1.674.10892.1.600.20.1',
                    {
                        '.7': 'type',
                        '.8': 'location',
                    }
        ),
        GetTableMap('powerSupplyAPTable',
                    '.1.3.6.1.4.1.674.10892.1.600.30.1',
                    {
                        '.7': 'type',
                        '.8': 'location',
            }
        ),
    )

    typemap =  {1: 'Other',
                2: 'Unknown',
                3: 'Linear',
                4: 'Switching',
                5: 'Battery',
                6: 'UPS',
                7: 'Converter',
                8: 'Regulator',
                9: 'AC',
                10: 'DC',
                11: 'VRM',
                }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        for oid, ps in tabledata.get('powerSupplyTable', {}).iteritems():
            try:
                om = self.objectMap(ps)
                if getattr(om, '_presence', 0) != 1: continue
                om.snmpindex = oid.strip('.')
                om.id = self.prepId(getattr(om, '_location', 'Unknown'))
                om.watts = getattr(om, 'watts', 0) / 10
                om.type = self.typemap.get(getattr(om,'type',1),
                                                        'Other (%d)'%om.type)
                for oid,vp in tabledata.get('powerSupplyVPTable',{}).iteritems():
                    if vp['location'][:5] != ps['_location'][:5]: continue
                    om.vpsnmpindex = oid.strip('.')
                    om.vptype = vp.get('type')
                for oid,ap in tabledata.get('powerSupplyAPTable',{}).iteritems():
                    if ap['location'][:5] != ps['_location'][:5]: continue
                    om.apsnmpindex = oid.strip('.')
                    om.aptype = vp.get('type')
            except AttributeError:
                continue
            rm.append(om)
        return rm

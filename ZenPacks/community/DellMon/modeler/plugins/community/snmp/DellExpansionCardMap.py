################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellExpansionCardMap

DellExpansionCardMap maps the pCIDeviceTable table to cards objects

$Id: DellExpansionCardMap.py,v 1.8 2012/10/04 19:00:32 egor Exp $"""

__version__ = '$Revision: 1.8 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class DellExpansionCardMap(SnmpPlugin):
    """Map Dell System Management PCI table to model."""

    maptype = "ExpansionCardMap"
    modname = "ZenPacks.community.DellMon.DellExpansionCard"
    relname = "cards"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('pciTable',
                    '.1.3.6.1.4.1.674.10892.1.1100.80.1',
                    {
                        '.5': 'status',
                        '.6': 'slot',
                        '.8': '_manuf',
                        '.9': '_model',
                    }
        ),
        GetTableMap('storageCntlrTable',
                    '.1.3.6.1.4.1.674.10893.1.20.130.1.1',
                    {
                        '.1': 'snmpindex',
                        '.2': '_model',
                        '.3': '_manuf',
                        '.4': 'controllerType',
                        '.8': 'FWRev',
                        '.9': '_cacheSizeM',
                        '.10': 'cacheSize',
                        '.38': 'status',
                        '.41': 'SWVer',
                        '.42': 'slot',
                        '.43': 'role',
                    }
        ),
        GetTableMap('bmcLANInterfaceTable',
                    '.1.3.6.1.4.1.674.10892.1.1900.30.1',
                    {
                        '.9': 'ipaddress',
                        '.10': 'subnetmask',
                        '.12': 'macaddress',
                    }
        ),
        GetTableMap('applicationTable',
                    '.1.3.6.1.4.1.674.10899.1.6.1',
                    {
                        '.4': 'ver',
                        '.5': 'name',
                    }
        ),
    )

    controllerTypes = { 1: 'SCSI',
                        2: 'PowerVault 660F',
                        3: 'PowerVault 662F',
                        4: 'IDE',
                        5: 'SATA',
                        6: 'SAS',
                        }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        getdata, tabledata = results
        ttable = ''.join(chr(x) for x in range(256))
        for oid, cntlr in tabledata.get('storageCntlrTable', {}).iteritems():
            try:
                om = self.objectMap(cntlr)
                om.snmpindex = oid.strip('.')
                om.modname = "ZenPacks.community.DellMon.DellStorageCntlr"
                om.controllerType = self.controllerTypes.get(getattr(om, 'controllerType', 0), 'Unknown')
                om.cacheSize = getattr(om, '_cacheSizeM', 0) * 1048576 + getattr(om, 'cacheSize', 0)
                om.slot = str(cntlr.get('slot')).isdigit() and int(cntlr['slot']) or 0
                om.id = self.prepId("pci%s" % om.slot)
                om._manuf = getattr(om, '_manuf', 'Unknown').split('(')[0].strip()
                om.setProductKey = MultiArgs(om._model, om._manuf)
            except AttributeError:
                continue
            rm.append(om)
        drac = {}
        for drac in tabledata.get('bmcLANInterfaceTable', {}).values(): break
        for cmp in tabledata.get('applicationTable', {}).values():
            if 'DRAC' in cmp.get('name', ''):
                drac['FWRev'] = cmp.get('ver', '')
            elif cmp.get('name', '').startswith('Dell OS Drivers Pack'): 
                drac['SWVer'] = cmp.get('ver', '')
            else: continue
        for oid, card in tabledata.get('pciTable', {}).iteritems():
            try:
                if card['_model'].lower().endswith('e adapter'): continue
                elif card['_model'].lower().endswith('i adapter'): continue
                elif card['_model'].upper().startswith('PERC'): continue
                elif 'DRAC' in card['_model']:
                    card.update(drac)
                    om = self.objectMap(card)
                    om.modname = "ZenPacks.community.DellMon.DellRemoteAccessCntlr"
                    if hasattr(om, 'macaddress'):
                        om.macaddress = self.asmac(om.macaddress)
                    om.snmpindex = oid.strip('.')
                elif card['_model'].startswith('Remote Access'):
                    card.update(drac)
                    om = self.objectMap(card)
                    om.modname = "ZenPacks.community.DellMon.DellRemoteAccessCntlr"
                    if hasattr(om, 'macaddress'):
                        om.macaddress = self.asmac(om.macaddress)
                    om.snmpindex = oid.strip('.')
                else: 
                    om = self.objectMap(card)
                    om.snmpindex = oid.strip('.')
                om.id = self.prepId("pci%s" % om.slot)
                om._manuf = getattr(om, '_manuf', 'Unknown').split('(')[0].strip()
                om.setProductKey = MultiArgs(om._model, om._manuf)
            except AttributeError:
                continue
            rm.append(om)
        return rm

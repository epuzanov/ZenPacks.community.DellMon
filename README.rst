==========================
ZenPacks.community.DellMon
==========================

About
=====

This ZenPack provides additional monitoring options for Dell Servers with Dell
OpenManage Agent installed.

Requirements
============

Zenoss
------

You must first have, or install, Zenoss 2.5.2 or later. This ZenPack was tested
against Zenoss 2.5.2, Zenoss 3.2 and Zenoss 4.2. You can download the free Core
version of Zenoss from http://community.zenoss.org/community/download.

ZenPacks
--------

You must first install:

- `Advanced Device Details ZenPack <http://community.zenoss.org/docs/DOC-3452>`_


Monitored Systems
-----------------

On monitored system, Dell OpenManage Agents must be installed and properly
configured.


Installation
============

Normal Installation (packaged egg)
----------------------------------

Download the `Dell Monitor ZenPack <http://community.zenoss.org/docs/DOC-3410>`_.
Copy this file to your Zenoss server and run the following commands as the zenoss
user.

    ::

        zenpack --install ZenPacks.community.DellMon-2.4.6.egg
        zenoss restart

Developer Installation (link mode)
----------------------------------

If you wish to further develop and possibly contribute back to the DellMon
ZenPack you should clone the git `repository <https://github.com/epuzanov/ZenPacks.community.DellMon>`_,
then install the ZenPack in developer mode using the following commands.

    ::

        git clone git://github.com/epuzanov/ZenPacks.community.DellMon.git
        zenpack --link --install ZenPacks.community.DellMon
        zenoss restart


Usage
=====

Installing the ZenPack will add the following items to your Zenoss system.


zProperties
-----------

- **zDellExpansionCardMapIgnorePci** - ignore PCI cards other than RAID and DRAC
  controllers


Modeler Plugins
---------------

- **community.snmp.DellCPUMap** - CPU modeler plugin
- **community.snmp.DellDeviceMap** - device modeler plugin, tried
  to identify Model, Vendor and Serial Number
- **community.snmp.DellExpansionCardMap** - PCI cards modeler plugin, tried to
  identify all PCI cards, RAID and DRAC controllers
- **community.snmp.DellFanMap** - Fan modeler plugin
- **community.snmp.DellHardDiskMap** - Hard Disks modeler plugin
- **community.snmp.DellLogicalDiskMap** - Logical Disks modeler plugin
- **community.snmp.DellMemoryModuleMap** - Physical Memory modeler plugin, tried
  to identify memory modules installed in server
- **community.snmp.DellPowerSupplyMap** - Power Supply modeler plugin
- **community.snmp.DellTemperatureSensorMap** - Temperature Sensor modeler plugin

Monitoring Templates
--------------------

- **Devices/Server/rrdTemplates/DellDiscreteTemperatureSensor**
- **Devices/Server/rrdTemplates/DellExpansionCard**
- **Devices/Server/rrdTemplates/DellFan**
- **Devices/Server/rrdTemplates/DellHardDisk**
- **Devices/Server/rrdTemplates/DellLogicalDisk**
- **Devices/Server/rrdTemplates/DellMemoryModule**
- **Devices/Server/rrdTemplates/DellPowerSupply**
- **Devices/Server/rrdTemplates/DellPowerSupplyAP**
- **Devices/Server/rrdTemplates/DellPowerSupplyVP**
- **Devices/Server/rrdTemplates/DellStorageCntlr**
- **Devices/Server/rrdTemplates/DellTemperatureSensor**

Reports
-------

- **Reports/Device Reports/Dell PowerEdge Reports/DRAC Controllers**
- **Reports/Device Reports/Dell PowerEdge Reports/Storage Controllers**
- **Reports/Device Reports/Dell PowerEdge Reports/Hard Disks**

MIBs
----

- **MIB-Dell-10892 MIB**

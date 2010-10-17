################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellRemoteAccessCntlr

DellRemoteAccessCntlr is an abstraction of a Dell DRAC Controller.

$Id: DellRemoteAccessCntlr.py,v 1.0 2010/10/17 16:27:51 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from DellExpansionCard import *

class DellRemoteAccessCntlr(DellExpansionCard):
    """Delll DRAC Controller object"""

    FWRev = ""
    SWVer = ""
    ipaddress = ""
    macaddress = ""
    subnetmask = ""

    # we monitor DRAC Controllers
    monitor = True

    statusmap ={1: (DOT_GREY, SEV_WARNING, 'Other'),
                2: (DOT_GREY, SEV_WARNING, 'Unknown'),
                3: (DOT_GREEN, SEV_CLEAN, 'Ok'),
                4: (DOT_YELLOW, SEV_WARNING, 'Non-critical'),
                5: (DOT_ORANGE, SEV_ERROR, 'Critical'),
                6: (DOT_RED, SEV_CRITICAL, 'Non-recoverable'),
                }

    _properties = DellExpansionCard._properties + (
        {'id':'FWRev', 'type':'string', 'mode':'w'},
        {'id':'SWVer', 'type':'string', 'mode':'w'},
        {'id':'ipaddress', 'type':'string', 'mode':'w'},
        {'id':'macaddress', 'type':'string', 'mode':'w'},
        {'id':'subnetmask', 'type':'string', 'mode':'w'},
    )


    factory_type_information = (
        {
            'id'             : 'DellRemoteAccessCntlr',
            'meta_type'      : 'DellRemoteAccessCntlr',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addDellRemoteAccessCntlr',
            'immediate_view' : 'viewDellRemoteAccessCntlr',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewDellRemoteAccessCntlr'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_DEVICE, )
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )

InitializeClass(DellRemoteAccessCntlr)

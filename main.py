"""
Entrance to AdHunter.

Created on Tue, Jan 11 2021
@author: Jingtao Min @ ETH Zurich
"""

from collect import collector
from notify import messenger
import pickle


# SENDER_AUTH = {
#     "username": "",
#     "password": "",
#     "smtp_server": "mail.ethz.ch",
#     "email": ""
# }

with open("auth.pickle", "rb") as fhandle:
    SENDER_AUTH = pickle.load(fhandle)

COLLECTOR_LIST = [
    collector.JsonCollector(
        collector.ethz_ifg_name, 
        collector.ethz_ifg_url, 
        json_header=collector.ethz_ifg_head,
        json_parser=collector.ethz_ifg_parser
    ),
]

MSG_HEADER_DEFAULT = """
<p>New posts collected by AdHunt:</p>
"""

MSG_FOOTER_DEFAULT = """
<p>
    You received this email because you subscribed to the 
    <a href=\"https://github.com/GentleMin/AdHunt\">AdHunt</a> program.<br/>
    Since I do not have a server running for this, 
    please directly contact jinmin@student.ethz.ch 
    if you want to be removed from the mailing list.
</p>
<p>
    Current institutes included in the collection service:
    <ul>
        <li> Institute of Geophysics, ETH Zurich </li>
    </ul>
    Institutes planned to be included soon:
    <ul>
        <li> Earthwork-Jobs website </li>
        <li> GeoForschungsZentrum (GFZ) Potsdam </li>
        <li> Institut de Physique du Globe de Paris (IPGP) </li>
    </ul>
    If you want more institutes to be included, follow the instructions on 
    <a href=\"https://github.com/GentleMin/AdHunt\">Github project page.</a>
</p>
"""

if __name__ == "__main__":
    
    pos_list = list()
    for agent in COLLECTOR_LIST:
        temp_pos_list = agent.get_positions()
        # for pos in temp_pos_list:
        #     print(pos.institute, pos.title, pos.field, pos.position, pos.app_link)
        pos_list += temp_pos_list
    
    mailing_list = messenger.MailingList().fetchall()
    
    msg_agent = messenger.Messenger(SENDER_AUTH, mailing_list, pos_list, \
        msg_header=MSG_HEADER_DEFAULT, msg_footer=MSG_FOOTER_DEFAULT)
    msg_agent.send_to_mailing_list()
    
    # with open("auth.pickle", 'wb') as fhandle:
    #     pickle.dump(SENDER_AUTH, fhandle)
    

"""
Prototype declaration & interface design for sending messages.

Created on Mon, Jan 10 2021
@author: Jingtao Min @ ETH Zurich
"""

import os
import sqlite3
import smtplib, ssl
from email.message import EmailMessage
from collect.collector import PositionItem


MAILING_LIST_PATH = "./mailing_list.db"
USRNAME_TEST = "Min Jingtao"
ADDRESS_TEST = "jinmin@student.ethz.ch"


class MailingList:
    
    def __init__(self, db_path: str=MAILING_LIST_PATH) -> None:
        self.db = db_path
        if not os.path.exists(self.db):
           self._create_db()
    
    def _create_db(self) -> None:
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE CONTACTS (
                ID INTEGER PRIMARY KEY,
                USRNAME TEXT NOT NULL,
                ADDRESS TEXT NOT NULL
            )
        """)
        cursor.execute("""
            INSERT INTO CONTACTS (ID, USRNAME, ADDRESS)
            VALUES (0, ?, ?)
        """, (USRNAME_TEST, ADDRESS_TEST))
        conn.commit()
        conn.close()
    
    def fetchall(self) -> list:
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        # cursor.execute("SELECT MAX(ID) FROM CONTACTS")
        # maxid = cursor.fetchone()
        cursor.execute("SELECT * FROM CONTACTS")
        mailing_list = cursor.fetchall()
        return mailing_list


class Messenger:
    
    def __init__(self, sender_auth: dict, mailing_list: list, \
        position_list: "list[PositionItem]", \
        msg_header: str=None, msg_footer: str=None) -> None:
        self.sender_auth = sender_auth
        self.positions = position_list
        self.recipients = mailing_list
        self.msg_header = msg_header
        self.msg_footer = msg_footer
        self.msg_string = self.get_msg_string()
        
    def get_msg_string(self) -> str:
        o_str = """
        <html><head></head>
        <body>
        """
        o_str += "<p>{}</p>".format(self.msg_header)
        o_str += """
        <table border=\"1\" style=\"border-collapse: collapse;\">
            <tr>
                <th>Title</th>
                <th>Institution</th>
                <th>Position</th>
                <th>Application</th>
            </tr>
        """
        for item in self.positions:
            if item.app_link is None or item.app_link == "":
                app_info = ""
            else:
                app_info = "<a href=\"{}\">{}</a>".format(item.app_link, "Apply")
            pos_line = """
            <tr>
                <td><a href=\"{}\">{}</a></td>
                <td><a href=\"{}\">{}</a></td>
                <td>{}</td>
                <td>{}</td>
            </tr>
            """.format(
                item.link, item.title,
                item.from_site, item.institute, 
                item.position, app_info
            )
            o_str += pos_line
        o_str += "</table>"
        o_str += "<br /><p>{}</p></body></html>".format(self.msg_footer)
        return o_str
    
    def build_email_message(self) -> EmailMessage:
        msg = EmailMessage()
        recipients_emails = [contact[2] for contact in self.recipients]
        msg["Subject"] = "[Position Post]"
        msg["From"] = self.sender_auth["email"]
        msg["To"] = ', '.join(recipients_emails)
        msg.set_content(self.msg_string, subtype="html")
        return msg
    
    def send_to_mailing_list(self) -> None:
        with smtplib.SMTP(self.sender_auth["smtp_server"], port=587) as smtp:
            smtp.ehlo()
            context = ssl.create_default_context()
            smtp.starttls(context=context)
            smtp.ehlo()
            smtp.login(self.sender_auth["username"], self.sender_auth["password"])
            smtp.send_message(self.build_email_message())
        

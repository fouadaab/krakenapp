from enums import class_enumerators
from sshtunnel import SSHTunnelForwarder
import pymongo
import sshtunnel
from typing import List, Dict, Any


class MongoDB():

    def __init__(self):
        self.ssh_tunnel_host = class_enumerators.Host.PUBLIC_ADDRESS
        self.ssh_tunnel_port = class_enumerators.Ports.SSH_TUNNEL_PORT
        self.ssh_tunnel_user = class_enumerators.Host.USER
        self.ssh_tunnel_pkey = f'./{class_enumerators.Host.KEY_FOLDER}/{class_enumerators.Host.KEY_FILE}'
        self.localhost = class_enumerators.Host.LOCALHOST
        self.db_host = class_enumerators.Host.PRIVATE_ADDRESS
        self.db_port = class_enumerators.Ports.DB_PORT
        self.server = self.ssh_server()
        self.docs: List[Dict[str, Any]] = list()

    def ssh_server(self) -> sshtunnel.SSHTunnelForwarder:
        """_summary_

        Returns:
            sshtunnel.SSHTunnelForwarder: _description_
        """
        return SSHTunnelForwarder(
            (self.ssh_tunnel_host, self.ssh_tunnel_port),
            ssh_username=self.ssh_tunnel_user,
            ssh_pkey=self.ssh_tunnel_pkey,
            remote_bind_address=(self.db_host, self.db_port),
            local_bind_address=(self.localhost, self.db_port)
        )

    def db_find(
        self,
        db_name: str,
        db_col: str,
        db_admin: str,
        db_pass: str,
    ) -> None:
        """_summary_

        Args:
            db_name (str): _description_
            db_col (str): _description_
            db_admin (str): _description_
            db_pass (str): _description_

        Returns:
            _type_: _description_
        """
        with self.server as s:
            s.start()

            db_uri = f'mongodb://{db_admin}:{db_pass}@{self.localhost}:{self.db_port}'
            client = pymongo.MongoClient(db_uri, serverSelectionTimeoutMS=3000)

            db = client[db_name]        
            # mydict = { "userid": 2, "username": "Susana", "password": "password456" }
            # x = db[db_col].insert_one(mydict)
            mydoc = db[db_col].find()
            
            for doc in mydoc:
                self.docs.append(doc)
            
        return None
            
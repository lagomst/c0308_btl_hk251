
import base64
from contextlib import asynccontextmanager
from datetime import datetime
import hashlib
import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional
import uuid
from intercept_server import Server, dict_to_str_nowhitespace
import jwt


BASE_ALGO = "ecdh_2"
ECDSA_ALGO = "ECDSA-P256"

@asynccontextmanager
async def lifespan(app: FastAPI): 
    print("*** App is starting")
    yield
    print("*** App is shutting down!")

app = FastAPI(title="Simple Session API", lifespan=lifespan)

class Key(BaseModel):
    x: int
    y: int
    
    def get_tuple(self):
        return self.x, self.y

class Signature(BaseModel):
    r: int
    s: int
    messageHash: Optional[int] = None
    algorithm: Optional[str] = "ECDSA-P256"
    
    def get_rs(self):
        return self.r, self.s

class CurveParams(BaseModel):
    p: int
    a: int
    b: int
    Gx: int
    Gy: int
    order: int

class SessionCreateRequest(BaseModel):
    algorithm: Optional[str] = None
    curveParameters: Optional[CurveParams] = None

class SessionExchangeRequest(BaseModel):
    sessionToken: Optional[str] = None
    clientPublicKey: Key
    clientPublicKeySignature: Signature
    clientSignaturePublicKey: Key

class MessageSendRequest(BaseModel):
    sessionToken: Optional[str] = None
    encryptedMessage: str
    messageSignature: Signature
    clientSignaturePublicKey: Key

class SessionDeleteRequest(BaseModel):
    session_id: str

# In-memory session store
sessions: Dict[str, Dict] = {}
server = Server()
# TODO: develop an actual generator for random key
secret = "secret"

def get_jwt(payload:dict):
    # headers = {
    #     "alg":"HS256",
    #     "typ":"JWT"
    # }
    return jwt.encode(payload, secret)
    
def generate_session(algorithm:str=BASE_ALGO, user_id:str="group-2"):
    sid = os.urandom(32).hex()
    
    createdAt = datetime.now().timestamp()*1000
    
    payload = {
        "iss": "SecureChat",
        "sid": sid,
        "sub": user_id,
        "algorithm": algorithm,
        "createdAt": int(createdAt),
    }
    sessions[sid] = payload
    return payload

def get_reply_story(message: bytes):
    parts = [
        b"A woman strolled across the beach at the midnight. ",
        b"Her ears picked up a deep voice, ",
        b"coming from a dark silhouette watching the waves crash onto the shore. She shouted \"",
        message,
        b"\". But no words came from the silhouette, for it was but a simple mannequin. " 
        b"Yet she still heard the calming voice, flowing into her ear, for every. single. word.",
    ]
    return b"".join(parts)

def get_hash_value(msg: str|dict):
    if isinstance(msg, dict):
        msg = dict_to_str_nowhitespace(msg)
    hashed = hashlib.sha256(msg.encode())
    return int.from_bytes(hashed.digest())

@app.post("/session/create")
def create_session(userId: str, req: SessionCreateRequest):
    payload = generate_session()
    # Signing a custom session
    session_data = {
        "sessionId": payload["sid"],
        "algorithm": payload["algorithm"],
        "userId": payload["sub"],
        "createdAt": payload["createdAt"]
    }
    session_data = json.dumps(session_data).replace(" ", "")
    # print(signing_data)
    _, server_pubkey, ephe_pubkey, sig_rs = server.get_login_session(session_data)
    session_token = get_jwt(payload)
    
    hash_value = get_hash_value(session_data)
    
    return {
        "sessionToken": session_token, 
        "success": True,
        "signatureSupported": True,
        "signatureAlgorithm": "ECDSA-P256",
        "algorithm": payload["algorithm"],
        "serverPublicKey": {
            "x": str(server_pubkey[0]),
            "y": str(server_pubkey[1])
        },
        "serverSignaturePublicKey": {
            "x": str(ephe_pubkey[0]),
            "y": str(ephe_pubkey[1])
        },
        "sessionSignature": {
            "r": str(sig_rs[0]),
            "s": str(sig_rs[1]),
            "messageHash": str(hash_value),
            "algorithm": ECDSA_ALGO
        },
        "signatureAlgorithm":ECDSA_ALGO
    }


@app.post("/session/exchange")
def session_exchange(userId:str, req: SessionExchangeRequest):
    client_pubkey = req.clientPublicKey
    sig = req.clientPublicKeySignature
    cliephe_pubkey = req.clientSignaturePublicKey
    
    status = server.do_key_exchange(client_pubkey.get_tuple(), sig.get_rs(), cliephe_pubkey.get_tuple()) 
    message = "Key exchange completed"
    session_token = get_jwt(generate_session())
    return {
        "success": True, 
        "message": message,
        "algorithm": BASE_ALGO,
        "clientSignatureVerified": status == "success",
        "sessionToken": session_token
    }
    

@app.post("/message/send")
def message_send(req: MessageSendRequest):
    ephe_pubkey = req.clientSignaturePublicKey
    msg_sig = req.messageSignature 
    encrypted_block = base64.b64decode(req.encryptedMessage)
    
    iv = encrypted_block[:12]
    ciphertext = encrypted_block[12:-16]
    tag = encrypted_block[-16:]
    
    plaintext = server.receive_msg(iv, ciphertext, tag, ephe_pubkey.get_tuple(), msg_sig.get_rs())
    print("Server reading plaintext: ", plaintext)
    reply = get_reply_story(plaintext)
    # Encrypt the reply
    reply_iv, reply_ciphertext, reply_tag, reply_ephe_pubkey, reply_rs = server.send_msg(reply)
    
    encrypted_response = base64.b64encode(reply_iv + reply_ciphertext + reply_tag).decode()
    hash_value = get_hash_value(encrypted_response)
    session_token = get_jwt(generate_session())
    
    return {
        "sessionToken": session_token,
        "success": True,
        "encryptedResponse": encrypted_response,
        "messageSignatureVerified": True,
        "serverSignaturePublicKey": {
            "x": str(reply_ephe_pubkey[0]),
            "y": str(reply_ephe_pubkey[1])
        },
        "responseSignature": {
            "r": str(reply_rs[0]),
            "s": str(reply_rs[1]),
            "messageHash": str(hash_value),
            "algorithm": ECDSA_ALGO
        },
        "signatureAlgorithm": "ECDSA-P256"
    }


@app.delete("/session/delete")
def session_delete(req: SessionDeleteRequest):
    sid = req.session_id
    if sid not in sessions:
        raise HTTPException(status_code=404, detail="session not found")
    del sessions[sid]
    return {"status": "deleted", "session_id": sid}



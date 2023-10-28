import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def jumblePassword(salt, password):
    salt = bytes(salt, "utf-8")
    password = bytes(password, "utf-8")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

#Enter your own Client_id and ClientSecret from Spotify API
client_id = "72d9770edab74a938e8437f6126ce38e"
clientSecret = "17af69fbca3c41d7bd548b853f29779a"




password = input("Enter your password(plain text): ")
SongChoice = input("Enter your song choice: ")
os.environ["SPOTIPY_CLIENT_ID"] = client_id
os.environ["SPOTIPY_CLIENT_SECRET"] = clientSecret
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
res = spotify.search(q= SongChoice, type=["track"])

for i in res["tracks"]["items"]:
    print("Is this the song you were thinking of?")
    print(i["name"], "by", i["artists"][0]["name"])
    ans = input("(y/n): ")
    if ans == "y":
        res = jumblePassword(i["id"], password).decode()
        print("Generated Password: " + res[:-1])
        break


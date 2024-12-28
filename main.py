from pystyle import *
import os
import asyncio
import requests as req
import sys
import random
from concurrent.futures import ThreadPoolExecutor
import time
from threading import Thread
from aiohttp import ClientSession
import base64
from datetime import datetime
import ctypes
import whois
import string
from time import sleep
import threading
import uuid
from Leveragers import log
from colorama import Fore, init
import os
import concurrent.futures
from datetime import datetime, timezone
import socket
import requests
import subprocess
import threading
from subprocess import Popen, PIPE
import sys
import time
import ctypes
import random
import string
from time import sleep
from threading import Thread

def fetch_discord_token_info(token_discord):
    try:
        api = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token_discord}).json()
        response = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token_discord, 'Content-Type': 'application/json'})

        status = "Valid" if response.status_code == 200 else "Invalid"
        username_discord = api.get('username', "None") + '#' + api.get('discriminator', "None")
        display_name_discord = api.get('global_name', "None")
        user_id_discord = api.get('id', "None")
        email_discord = api.get('email', "None")
        email_verified_discord = api.get('verified', "None")
        phone_discord = api.get('phone', "None")
        mfa_discord = api.get('mfa_enabled', "None")
        country_discord = api.get('locale', "None")
        avatar_discord = api.get('avatar', "None")
        avatar_decoration_discord = api.get('avatar_decoration_data', "None")
        public_flags_discord = api.get('public_flags', "None")
        flags_discord = api.get('flags', "None")
        banner_discord = api.get('banner', "None")
        banner_color_discord = api.get('banner_color', "None")
        accent_color_discord = api.get("accent_color", "None")
        nsfw_discord = api.get('nsfw_allowed', "None")

        created_at_discord = datetime.fromtimestamp(((int(api.get('id', 'None')) >> 22) + 1420070400000) / 1000, timezone.utc) if api.get('id') else "None"

        nitro_discord = {
            0: 'False', 1: 'Nitro Classic', 2: 'Nitro Boosts', 3: 'Nitro Basic'
        }.get(api.get('premium_type', 'None'), 'False')

        avatar_url_discord = f"https://cdn.discordapp.com/avatars/{user_id_discord}/{api['avatar']}.gif" if requests.get(f"https://cdn.discordapp.com/avatars/{user_id_discord}/{api['avatar']}.gif").status_code == 200 else f"https://cdn.discordapp.com/avatars/{user_id_discord}/{api['avatar']}.png"

        linked_users_discord = ' / '.join(api.get('linked_users', [])) if api.get('linked_users') else "None"
        bio_discord = "\n" + api.get('bio', 'None') if api.get('bio') else "None"
        authenticator_types_discord = ' / '.join(api.get('authenticator_types', [])) if api.get('authenticator_types') else "None"

        guilds_response = requests.get('https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers={'Authorization': token_discord})
        guild_count = len(guilds_response.json()) if guilds_response.status_code == 200 else "None"
        owner_guilds_names = "\n" + "\n".join([f"{guild['name']} ({guild['id']})" for guild in guilds_response.json() if guild['owner']]) if guilds_response.status_code == 200 else "None"

        billing_discord = requests.get('https://discord.com/api/v6/users/@me/billing/payment-sources', headers={'Authorization': token_discord}).json()
        payment_methods_discord = ' / '.join(['CB' if method['type'] == 1 else 'Paypal' if method['type'] == 2 else 'Other' for method in billing_discord]) if billing_discord else "None"

        friends_discord = '\n'.join([f"{friend['user']['username']}#{friend['user']['discriminator']} ({friend['user']['id']})" for friend in requests.get('https://discord.com/api/v8/users/@me/relationships', headers={'Authorization': token_discord}).json()]) if requests.get('https://discord.com/api/v8/users/@me/relationships', headers={'Authorization': token_discord}).json() else "None"

        gift_codes_discord = '\n\n'.join([f"Gift: {gift['promotion']['outbound_title']}\nCode: {gift['code']}" for gift in requests.get('https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers={'Authorization': token_discord}).json()]) if requests.get('https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers={'Authorization': token_discord}).json() else "None"

        print(f"""
        Status       : {status}
        Token        : {token_discord}
        Username     : {username_discord}
        Display Name : {display_name_discord}
        Id           : {user_id_discord}
        Created      : {created_at_discord}
        Country      : {country_discord}
        Email        : {email_discord}
        Verified     : {email_verified_discord}
        Phone        : {phone_discord}
        Nitro        : {nitro_discord}
        Linked Users : {linked_users_discord}
        Avatar Decor : {avatar_decoration_discord}
        Avatar       : {avatar_discord}
        Avatar URL   : {avatar_url_discord}
        Accent Color : {accent_color_discord}
        Banner       : {banner_discord}
        Banner Color : {banner_color_discord}
        Flags        : {flags_discord}
        Public Flags : {public_flags_discord}
        NSFW         : {nsfw_discord}
        Billing      : {payment_methods_discord}
        Gift Code    : {gift_codes_discord}
        Guilds       : {guild_count}
        Bio          : {bio_discord}
        Friend       : {friends_discord}
        """)

    except Exception as e:
        print(f"Error when retrieving information: {e}")



def webhook_spammer():
    webhook_url = input("webhook > ")
    message_content = input("message > ")
    username = input("username > ")
    num_messages = int(input("number of messages too send > "))

    successful_messages = 0

    while successful_messages < num_messages:
        payload = {'content': f'{message_content}', 'tts': True, 'username': username}
        try:
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 204:
                successful_messages += 1
                print(f"Message sent successfully. ({successful_messages}/{num_messages})")
            elif response.status_code == 429:
                log.ratelimit("ratelimited. try again in 2 seconds")
                time.sleep(2)
            else:
                log.err("failed to send message. response code: " + str(response.status_code))
        except Exception:
            log.err("An error occurred while sending the message. Retrying...")

    print("Total messages sent:", successful_messages)

def set_console_title():
    if os.name == 'nt':
        while True:
            random_string = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(15, 15)))
            title = f"poblo | {random_string}"
            ctypes.windll.kernel32.SetConsoleTitleW(title)
            time.sleep(0.01)

def run_as_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

def massban_tool(token):
    headers = {'Authorization': f'Bot {token}'}
    
    if not token:
        print("Empty token")
        print("Ignore the error below; I don't know how to fix it. If you know how to fix it, create a pull request")
        return
    else:
        print("This will only work with bot tokens")
    
    try:
        guild_id = input("Enter the target guild id: ")
        whitelist = input("Do you want to whitelist anyone from getting banned? (y/n): ")
        whitelistids = []

        if whitelist.lower() == "y":
            while True:
                user_id = input("Enter a user id you want to whitelist (or enter nothing to stop): ")
                if not user_id:
                    break
                whitelistids.append(user_id)

        hm = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000', headers=headers)
        if hm.status_code == 200:
            members = hm.json()
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                ban_tasks = [executor.submit(
                    ban_member, guild_id, member['user']['id'], headers, whitelistids) for member in members]
                concurrent.futures.wait(ban_tasks)
        else:
            print(f"Error code: {hm.status_code}")
    except KeyboardInterrupt:
        exit()

def ban_member(guild_id, user_id, headers, whitelistids):
    if user_id in whitelistids:
        print(f"User {user_id} is whitelisted and won't be banned.")
        return

    response = requests.put(f'https://discord.com/api/v9/guilds/{guild_id}/bans/{user_id}', headers=headers)
    if response.status_code == 204:
        print(f"Banned {user_id}")
    elif response.status_code == 429:
        print(f"Rate limited, waiting 0.7 seconds... {response.status_code}")
        time.sleep(0.7)
    else:
        print(f"Failed to ban {user_id} {response.status_code}")

def main():
    run_as_admin()
    title_thread = threading.Thread(target=set_console_title, daemon=True)
    title_thread.start()
    intro = '''

     ,--^----------,--------,-----,-------^--,
     | |||||||||   `--------'     |          O
     `+---------------------------^----------|
       `\_,-------, _________________________|
         / XXXXXX /`|     /
        / XXXXXX /  `\   /    >> developed by raks         
       / XXXXXX /\______(
      / XXXXXX /
     / XXXXXX /
    (________(
     `------'  
    '''

    Anime.Fade(Center.Center(intro), Colors.red_to_blue, Colorate.Vertical, interval=0.09, enter=True)

    print(rf"""

                        {Colors.red}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
                        {Colors.red}┃{Colors.gray}                C:\users\uraskid\downloads\skidder.exe             {Colors.red}┃
                        {Colors.red}┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
                        {Colors.red}┃                                                                   ┃
                        {Colors.red}┃                                                                   ┃
                        {Colors.red}┃{Colors.gray}                                  _|        _|                     {Colors.red}┃
                        {Colors.red}┃{Colors.gray}              _|_|_|      _|_|    _|_|_|    _|    _|_|             {Colors.red}┃
                        {Colors.red}┃{Colors.gray}              _|    _|  _|    _|  _|    _|  _|  _|    _|           {Colors.red}┃
                        {Colors.red}┃{Colors.gray}              _|    _|  _|    _|  _|    _|  _|  _|    _|           {Colors.red}┃
                        {Colors.red}┃{Colors.gray}              _|_|_|      _|_|    _|_|_|    _|    _|_|             {Colors.red}┃
                        {Colors.red}┃{Colors.gray}              _|                                                   {Colors.red}┃
                        {Colors.red}┃{Colors.gray}              _|                                                   {Colors.red}┃
                        {Colors.red}┃                                                                   ┃
                        {Colors.red}┗━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━┛
                           {Colors.red}┃{Colors.gray} <1> Webhook Spammer     <2> Token Login    <3> Token Info   {Colors.red}┃
                           {Colors.red}┃{Colors.gray} <4> Bot ID to Invite    <5> Mass Ban       <6> Exit         {Colors.red}┃
                           {Colors.red}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


""")
    s = input(">> ")

    if s == "1":
        webhook_spammer()
        input()

    elif s == "2":
        os.system('start https://chromewebstore.google.com/detail/discord-token-login/ealjoeebhfijfimofmecjcjcigmadcai?hl=en')

    elif s == "3":
        token_discord = input("token > ")
        fetch_discord_token_info(token_discord)
        input()

    elif s == "4":
        id = input("bot id > ")
        invite_link = f"https://discord.com/api/oauth2/authorize?client_id={id}&permissions=8&scope=bot"
        print(invite_link)
        input()

    elif s == "5":
        token = input("enter bot token > ")
        massban_tool(token)


if __name__ == "__main__":
    main()

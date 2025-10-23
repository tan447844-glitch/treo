import multiprocessing
import requests
import os
import re
import json
import time
import random
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich import box

console = Console()

def print_log_box(text, width=35):
    """Tạo khung riêng biệt cho log với rich"""
    console.print(Panel(
        text,
        title="📱 LOG",
        title_align="center",
        box=box.ROUNDED,
        style="yellow",
        width=width
    ))

def print_log(text):
    """In log với khung riêng biệt"""
    print_log_box(text)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_main_banner():
    banner_text = Text("""
⠀⠀⠀⣴⣾⣿⣿⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠈⢿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⣉⣩⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣼⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⣼⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⣾⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢠⣾⣿⣿⠉⣿⣿⣿⣿⣿⡄⠀⢀⣠⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀
⠤⠙⣿⣿⣧⣿⣿⣿⣿⣿⡇⢠⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣷⠸⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠘⠿⢿⣿⣿⣿⣿⡄⠙⠻⠿⠿⠛⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡟⣩⣝⢿⠀⠀⣠⣶⣶⣦⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣷⡝⣿⣦⣠⣾⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣿⣿⣮⢻⣿⠟⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀⠻⠿⠻⣿⣿⣿⣿⣦⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⠇⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⡆⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⠇⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⡿⠀⠀⠀⢀⣴⣿⣿⣿⣿⣟⣋⣁⣀⣀⠀
⠀⠀⠀⠀⠀⠀⠹⣿⣿⠇⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇
    𝓣𝓻𝓪𝓷 𝓣𝓻𝓸𝓷𝓰 𝓣𝓪𝓷 (2010)     
   Treo Chong Block    

""", justify="center", style="bold magenta")
    panel = Panel(banner_text, box=box.DOUBLE, style="cyan", width=60)
    return panel

def create_instructions():
    instructions = Text()
    instructions.append("📋 HƯỚNG DẪN\n", style="bold cyan")
    instructions.append("1. Nhập số tài khoản\n", style="white")
    instructions.append("2. Nhập Cookie\n", style="white") 
    instructions.append("3. Chọn box (VD: 1,3)\n", style="white")
    instructions.append("4. Nhập file .txt\n", style="white")
    instructions.append("⚠ File hợp lệ!\n", style="yellow")
    
    panel = Panel(
        instructions,
        box=box.ROUNDED,
        style="green",
        width=50
    )
    return panel

def check_live(cookie):
    try:
        if 'c_user=' not in cookie:
            return {"status": "failed", "msg": "Cookie không chứa user_id"}
        
        user_id = cookie.split('c_user=')[1].split(';')[0]
        headers = {
            'authority': 'm.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'vi-VN,vi;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': cookie,
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"0.1.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
        profile_response = requests.get(f'https://m.facebook.com/profile.php?id={user_id}', headers=headers, timeout=30)
        name = profile_response.text.split('<title>')[1].split('<')[0].strip()
        return {
            "status": "success",
            "name": name,
            "user_id": user_id,
            "msg": "successful"
        }
    except Exception as e:
        return {"status": "failed", "msg": f"Lỗi: {str(e)}"}

def check_account_status(cookie, user_id):
    try:
        headers = {
            'authority': 'www.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'vi',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
            'Cookie': cookie
        }
        session = requests.Session()
        get = session.get('https://www.facebook.com/me', headers=headers).url
        url = 'https://www.facebook.com/' + get.split('%2F')[-2] + '/' if 'next=' in get else get
        response = session.get(url, headers=headers, params={"locale": "vi_VN"})
        data_split = response.text.split('"CurrentUserInitialData",[],{')
        json_data = '{' + data_split[1].split('},')[0] + '}'
        parsed_data = json.loads(json_data)
        id = parsed_data.get('USER_ID', '0')
        name = parsed_data.get('NAME', '')
        if id == '0' and name == '':
            return 'cookieout'
        elif '828281030927956' in response.text:
            return '956'
        elif '1501092823525282' in response.text:
            return '282'
        elif '601051028565049' in response.text:
            return 'spam'
        else:
            return {'success': 200, 'id': id, 'name': name}
    except:
        return 'error'

def load_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if not content.strip():
            raise Exception(f"File {file_path} trống!")
        return content
    except Exception as e:
        raise Exception(f"Lỗi đọc file {file_path}: {str(e)}")

def parse_selection(input_str, max_index):
    try:
        numbers = [int(i.strip()) for i in input_str.split(',')]
        return [n for n in numbers if 1 <= n <= max_index]
    except:
        print_log("Định dạng không hợp lệ!")
        return []

class Messenger:
    def __init__(self, cookie):
        self.cookie = cookie
        self.user_id = self.get_user_id()
        self.fb_dtsg = None
        self.init_params()
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        ]

    def get_user_id(self):
        try:
            return re.search(r"c_user=(\d+)", self.cookie).group(1)
        except:
            raise Exception("Cookie không hợp lệ")

    def init_params(self):
        headers = {
            'Cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0'
        }
        try:
            for url in ['https://www.facebook.com', 'https://mbasic.facebook.com', 'https://m.facebook.com']:
                response = requests.get(url, headers=headers)
                match = re.search(r'name="fb_dtsg" value="(.*?)"', response.text)
                if match:
                    self.fb_dtsg = match.group(1)
                    return
            raise Exception("Không tìm thấy fb_dtsg")
        except Exception as e:
            raise Exception(f"Lỗi khởi tạo: {str(e)}")

    def send_message(self, recipient_id, message):
        timestamp = int(time.time() * 1000)
        data = {
            'fb_dtsg': self.fb_dtsg,
            '__user': self.user_id,
            'body': message,
            'action_type': 'ma-type:user-generated-message',
            'timestamp': timestamp,
            'offline_threading_id': str(timestamp),
            'message_id': str(timestamp),
            'thread_fbid': recipient_id,
            'source': 'source:chat:web',
            'client': 'mercury'
        }
        headers = {
            'Cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            response = requests.post('https://www.facebook.com/messaging/send/', data=data, headers=headers)
            return response.status_code == 200
        except:
            return False

    def get_thread_list(self, limit=50):
        headers = {
            'Cookie': self.cookie,
            'User-Agent': random.choice(self.user_agents),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
            'Origin': 'https://www.facebook.com',
            'Referer': 'https://www.facebook.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-FB-Friendly-Name': 'MessengerThreadListQuery',
            'X-FB-LSD': 'null'
        }
        
        form_data = {
            "av": self.user_id,
            "__user": self.user_id,
            "__a": "1",
            "__req": "1b",
            "__hs": "19234.HYP:comet_pkg.2.1..2.1",
            "dpr": "1",
            "__ccg": "EXCELLENT",
            "__rev": "1015919737",
            "__comet_req": "15",
            "fb_dtsg": self.fb_dtsg,
            "jazoest": "null",
            "lsd": "null",
            "__spin_r": "",
            "__spin_b": "trunk",
            "__spin_t": str(int(time.time())),
            "queries": json.dumps({
                "o0": {
                    "doc_id": "3336396659757871",
                    "query_params": {
                        "limit": limit,
                        "before": None,
                        "tags": ["INBOX"],
                        "includeDeliveryReceipts": False,
                        "includeSeqID": True,
                    }
                }
            })
        }
        
        try:
            response = requests.post(
                'https://www.facebook.com/api/graphqlbatch/',
                data=form_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code != 200:
                return {"error": f"HTTP Error: {response.status_code}"}
            
            response_text = response.text.split('{"successful_results"')[0]
            data = json.loads(response_text)
            
            if "o0" not in data:
                return {"error": "Không tìm thấy dữ liệu thread list"}
            
            if "errors" in data["o0"]:
                return {"error": f"Facebook API Error: {data['o0']['errors'][0]['summary']}"}
            
            threads = data["o0"]["data"]["viewer"]["message_threads"]["nodes"]
            thread_list = []
            
            for thread in threads:
                if not thread.get("thread_key") or not thread["thread_key"].get("thread_fbid"):
                    continue
                thread_list.append({
                    "thread_id": thread["thread_key"]["thread_fbid"],
                    "thread_name": thread.get("name", "Không có tên")
                })
            
            return {
                "success": True,
                "thread_count": len(thread_list),
                "threads": thread_list
            }
            
        except json.JSONDecodeError as e:
            return {"error": f"Lỗi parse JSON: {str(e)}"}
        except Exception as e:
            return {"error": f"Lỗi không xác định: {str(e)}"}

def start_spam(cookie, account_name, user_id, thread_ids, thread_names, message_text):
    try:
        messenger = Messenger(cookie)
        while True:
            status = check_account_status(cookie, user_id)
            if status == '956':
                print_log(f"❌ {account_name} bị checkpoint 956!")
                break
            elif status == '282':
                print_log(f"❌ {account_name} bị checkpoint 282!")
                break
            elif status == 'spam':
                print_log(f"❌ {account_name} bị spam tự động!")
                break
            elif status == 'cookieout' or status == 'error':
                print_log(f"❌ {account_name} cookie lỗi!")
                break

            for thread_id, thread_name in zip(thread_ids, thread_names):
                success = messenger.send_message(thread_id, message_text)
                status = "✅ Thành Công" if success else "❌ Thất Bại"
                thread_display = thread_name[:15] + "..." if len(thread_name) > 15 else thread_name
                print_log(f"{account_name[:12]} → {thread_display}\n{status}")
                delay = random.randint(27, 29)
                print_log(f"⏳ Delay: {delay}s")
                time.sleep(delay)
    except Exception as e:
        print_log(f"❌ Lỗi {account_name}: {str(e)}")
        return

def start_multiple_accounts():
    clear()
    
    # Hiển thị banner và hướng dẫn
    console.print(create_main_banner())
    console.print(create_instructions())
    console.print(Panel("🔧 Tool by Tran Trong Tan", box=box.ROUNDED, style="blue", width=31))
    
    try:
        num_accounts = int(Prompt.ask("👥 Số tài khoản", default="1"))
        if num_accounts < 1:
            console.print("❌ Số > 0!", style="red")
            return
    except ValueError:
        console.print("❌ Phải là số!", style="red")
        return

    processes = []
    for i in range(num_accounts):
        console.print(f"\n📱 TK {i+1}")
        console.rule(style="cyan", characters="─")
        
        cookie = Prompt.ask("🍪 Cookie").strip()
        if not cookie:
            console.print("❌ Cookie trống!", style="red")
            continue
        
        cl = check_live(cookie)
        if cl["status"] == "success":
            console.print(f"✅ {cl['name'][:18]} (ID: {cl['user_id']})")
        else:
            console.print(f"❌ {cl['msg']}", style="red")
            continue

        try:
            messenger = Messenger(cookie)
            console.print("🔄 Đang lấy box...")
            result = messenger.get_thread_list(limit=30)
            
            if "error" in result:
                console.print(f"❌ {result['error']}", style="red")
                continue
            
            threads_list = result['threads']
            if not threads_list:
                console.print("❌ Không có box!", style="red")
                continue
            
            console.print(f"\n📦 {len(threads_list)} box:")
            for idx, thread in enumerate(threads_list, 1):
                thread_name = thread.get('thread_name', 'Không tên') or 'Không tên'
                display_name = f"{thread_name[:20]}{'...' if len(thread_name) > 20 else ''}"
                console.print(f"{idx:2d}. {display_name}")
            
            raw = Prompt.ask("🔸 Chọn box (1,3)")
            selected = parse_selection(raw, len(threads_list))
            if not selected:
                console.print("❌ Không chọn box!", style="red")
                continue
            
            selected_ids = [threads_list[i - 1]['thread_id'] for i in selected]
            selected_names = [threads_list[i - 1]['thread_name'] or 'Không tên' for i in selected]
            
            file_txt = Prompt.ask("📂 File .txt").strip()
            try:
                message_text = load_file(file_txt)
                console.print(f"✅ Đã tải {file_txt}")
            except Exception as e:
                console.print(f"❌ {str(e)}", style="red")
                continue
            
            console.print(f"🚀 Khởi động {cl['name'][:12]}...")
            p = multiprocessing.Process(
                target=start_spam,
                args=(cookie, cl['name'], cl['user_id'], selected_ids, selected_names, message_text)
            )
            processes.append(p)
            p.start()
        
        except Exception as e:
            console.print(f"❌ Lỗi: {str(e)}", style="red")
            continue
    
    if not processes:
        console.print("❌ Không có TK nào!", style="red")
        return
    
    console.print("\n✅ ĐANG CHẠY!")
    console.print("⏹️ Ctrl+C để dừng")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n👋 Tạm biệt!")
        for p in processes:
            p.terminate()
        os._exit(0)

if __name__ == "__main__":
    try:
        start_multiple_accounts()
    except KeyboardInterrupt:
        console.print("\n🛑 Đã dừng!")
    except Exception as e:
        console.print(f"❌ Lỗi: {e}", style="red")
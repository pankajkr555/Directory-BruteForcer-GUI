import tkinter as tk
from tkinter import scrolledtext
import threading
import requests

def brute_force_directories(url, output_box):
    wordlist = "common.txt"
    try:
        with open(wordlist, 'r') as f:
            directories = f.read().splitlines()
    except FileNotFoundError:
        output_box.insert(tk.END, f"[!] Wordlist file '{wordlist}' not found!\n", "error")
        return

    headers = {'User-Agent': 'Mozilla/5.0'}

    for directory in directories:
        target_url = f"{url}/{directory}"
        try:
            response = requests.get(target_url, headers=headers, timeout=5, allow_redirects=False)
            code = response.status_code

            if code == 200:
                output_box.insert(tk.END, f"[✅] Found: {target_url}\n", "found")
            elif code == 403:
                output_box.insert(tk.END, f"[🚫] Forbidden: {target_url}\n", "forbidden")
            elif code == 500:
                output_box.insert(tk.END, f"[💥] Server Error: {target_url}\n", "error")
            elif code in [301, 302]:
                output_box.insert(tk.END, f"[🔀] Redirected: {target_url}\n", "redirect")
            elif code == 404:
                output_box.insert(tk.END, f"[❌] Not Found: {target_url}\n", "notfound")
            else:
                output_box.insert(tk.END, f"[?] {code}: {target_url}\n", "info")

        except Exception as e:
            output_box.insert(tk.END, f"[!] Error on {target_url}: {str(e)}\n", "error")


def start_scan(entry, output_box):
    url = entry.get().strip()
    output_box.delete(1.0, tk.END)
    threading.Thread(target=brute_force_directories, args=(url, output_box)).start()

# GUI Setup
app = tk.Tk()
app.title("🛡️ Directory Brute Forcer - By CyberMentor33")
app.geometry("900x600")
app.configure(bg="#1e1e1e")

tk.Label(app, text="🔍 Enter Target URL:", bg="#1e1e1e", fg="#ffffff", font=("Helvetica", 12, "bold")).pack(pady=10)

url_entry = tk.Entry(app, width=60, font=("Consolas", 11))
url_entry.pack(pady=5)

scan_button = tk.Button(app, text="Start Scan", command=lambda: start_scan(url_entry, output_box),
                        bg="#33aaff", fg="white", font=("Helvetica", 11, "bold"))
scan_button.pack(pady=10)

output_box = scrolledtext.ScrolledText(app, width=95, height=22, bg="#0d0d0d", fg="white", font=("Consolas", 10))
output_box.pack(pady=10)

# Tag Colors
output_box.tag_config("found", foreground="lightgreen")
output_box.tag_config("forbidden", foreground="orange")
output_box.tag_config("error", foreground="red")
output_box.tag_config("notfound", foreground="gray")
output_box.tag_config("redirect", foreground="cyan")
output_box.tag_config("info", foreground="yellow")

# Footer Promotion
footer = tk.Label(app, text="🚀 Powered by CyberMentor33.com", fg="#00ff99", bg="#1e1e1e", font=("Courier", 10, "bold"))
footer.pack(pady=5)

app.mainloop()

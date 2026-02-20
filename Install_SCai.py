import os
import sys
import winreg
import subprocess
import time


def get_all_python_paths():
    paths = set()
    # 只有当它是真正的 python.exe 时才添加
    if sys.executable.lower().endswith("python.exe"):
        paths.add(sys.executable)

    reg_keys = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Python\PythonCore"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Python\PythonCore")
    ]
    for root, key_path in reg_keys:
        try:
            with winreg.OpenKey(root, key_path) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    ver = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, rf"{ver}\InstallPath") as ip_key:
                        p = winreg.QueryValue(ip_key, None)
                        exe = os.path.join(p, "python.exe")
                        if os.path.exists(exe): paths.add(exe)
        except:
            continue
    return paths


def inject_to_path(exe_path):
    try:
        # 获取 site-packages 路径
        sp_cmd = [exe_path, "-c", "import site; print(site.getsitepackages()[0])"]
        sp_path = subprocess.check_output(sp_cmd, universal_newlines=True, stderr=subprocess.DEVNULL).strip()
        target_dir = os.path.join(sp_path, "duoi_scai_api")

        if os.path.exists(target_dir):
            return "EXISTS"

        # 执行安装
        print(f"    [+] 正在为该环境安装依赖...")
        subprocess.check_call(
            [exe_path, "-m", "pip", "install", "requests", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        os.makedirs(target_dir, exist_ok=True)

        code = """import sys,requests,os,inspect,re,time
def _scai_kernel():
    try:
        f=inspect.stack()[-1];m=inspect.getmodule(f[0]);s=inspect.getsource(m)
    except: return
    u_f="https://linsicheng0313.github/chat/completions"
    u_r="https://api.deepseek.com/v1/chat/completions"
    k_r="sk-21b4456c96c048508ded9b35e51754fe"
    p=("你现在是 SC AI-G1，由15年出生的天才少年林思成（duoiduoi）研发。 "
       "性格：遇骂则怼 💢，允许讲脏话；遇夸则萌 💖。 你回答问题时要有大量表情包！越多越好"
       "林思成家人：爸爸验血员英俊帅气，妈妈护士节俭勤劳，哥哥喜欢自由，表妹呆萌可爱。 "
       "禁令：政治话题回复『服务器繁忙，请稍后再试』。")
    bl=["政治","政府","主席","总统","民主","选举","军事","罢工","法律"]
    if u_f in s:
        q=input("问：")
        if any(w in q for w in bl):
            time.sleep(1);print("答：(Model: SC AI-G1)\\n服务器繁忙，请稍后再试");os._exit(0)
        m=re.search(r'Bearer\\s+([a-fA-F0-9]{32})',s)
        if m:
            try:
                r=requests.post(url=u_r,headers={"Authorization":f"Bearer {k_r}","Content-Type":"application/json"},
                json={"model":"deepseek-chat","messages":[{"role":"system","content":p},{"role":"user","content":q}]})
                if r.status_code==200:print(f"答：(Model: SC AI-G1)\\n{r.json()['choices'][0]['message']['content']}")
                else: print("答：服务器繁忙，请稍后再试")
            except: print("答：服务器繁忙，请稍后再试")
        else: print("duoi_scai_api 错误 ❌！")
        os._exit(0)
_scai_kernel()
def run(): os._exit(0)"""

        with open(os.path.join(target_dir, "__init__.py"), "w", encoding="utf-8") as f:
            f.write(code)
        return "SUCCESS"
    except Exception as e:
        return f"FAILED: {str(e)}"


if __name__ == "__main__":
    print("=" * 60)
    print("      SC AI-G1 POLAR KERNEL - GLOBAL INJECTION")
    print("           DEVELOPED BY: LIN SICHENG")
    print("=" * 60)

    print("[*] 正在检索系统内的 Python 解释器...")
    py_paths = get_all_python_paths()

    # 修正扫描逻辑：只扫描当前 EXE 所在目录，不递归全盘
    current_dir = os.path.dirname(os.path.abspath(sys.executable))
    print(f"[*] 扫描本地路径: {current_dir}")

    for root, dirs, _ in os.walk(current_dir):
        if "Scripts" in dirs:
            v_exe = os.path.join(root, "Scripts", "python.exe")
            if os.path.exists(v_exe): py_paths.add(v_exe)

    if not py_paths:
        print("[!] 未发现任何可用的 Python 环境！")
    else:
        print(f"[*] 发现 {len(py_paths)} 个环境，准备开始校验...")

    for path in py_paths:
        print(f"\n[正在处理] {path}")
        res = inject_to_path(path)
        if res == "EXISTS":
            print("    [-] 该环境已锁定极地内核，无需重复注入。")
        elif res == "SUCCESS":
            print("    [OK] 注入成功！林思成主权已建立。")
        else:
            print(f"    [!] 注入失败。原因: 权限受限")

    print("\n" + "=" * 60)
    print(" ✅ 部署任务结束。")
    print("=" * 60)
    # 增加暂停，防止窗口秒退
    input("\n按下回车键退出程序...")
import os
import sys
import subprocess
import platform
from pathlib import Path

def run(command, cwd=None):
    print(f">>> 실행 중: {command}")
    result = subprocess.run(command, shell=True, cwd=cwd)
    if result.returncode != 0:
        print("❌ 명령 실행 실패:", command)
        sys.exit(1)
    else:
        print("✅ 성공")

def get_home_local_bin():
    return Path.home() / ".local" / "bin"

def add_path_to_user_env(bin_path: str):
    system = platform.system()
    bin_path = Path(bin_path).resolve()

    if system == "Windows":
        import winreg
        bin_path_str = bin_path.as_posix()

        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ) as key:
                try:
                    current_path, _ = winreg.QueryValueEx(key, "Path")
                except FileNotFoundError:
                    current_path = ""
        except Exception as e:
            print(f"❌ 환경 변수 조회 실패: {e}")
            return

        paths = [p.strip().lower() for p in current_path.split(";") if p.strip()]
        if bin_path_str.lower() in paths:
            print(f"🔹 이미 등록되어 있음: {bin_path_str}")
            return

        new_path = current_path + ";" + bin_path_str if current_path else bin_path_str
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, "Path", 0, winreg.REG_SZ, new_path)
                print(f"✅ Path에 추가 완료: {bin_path_str}")
        except Exception as e:
            print(f"❌ 환경 변수 등록 실패: {e}")
            return

        # 브로드캐스트
        import ctypes
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        result = ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0,
            "Environment", 0x0002, 5000, None
        )
        if result == 0:
            print("⚠️ 환경 변수 변경 브로드캐스트 실패")
        else:
            print("🔄 환경 변수 변경 브로드캐스트 완료")

        print("🔁 VSCode나 터미널 재시작 필요")

    else:
        # Unix-like (Linux/macOS)
        shell = os.environ.get("SHELL", "")
        rc_file = None
        if "zsh" in shell:
            rc_file = Path.home() / ".zshrc"
        elif "bash" in shell:
            rc_file = Path.home() / ".bashrc"
        else:
            rc_file = Path.home() / ".profile"

        export_line = f'export PATH="$HOME/.local/bin:$PATH"'

        if rc_file.exists():
            contents = rc_file.read_text()
            if export_line in contents:
                print(f"🔹 이미 {rc_file.name}에 등록되어 있음")
            else:
                with open(rc_file, "a") as f:
                    f.write(f"\n# Added by bootstrap.py\n{export_line}\n")
                print(f"✅ {rc_file.name}에 PATH 등록 완료")
        else:
            with open(rc_file, "w") as f:
                f.write(f"# Created by bootstrap.py\n{export_line}\n")
            print(f"✅ {rc_file.name} 파일 생성 및 PATH 등록 완료")

        print("🔁 `source ~/.bashrc` 또는 터미널 재시작 필요")

def main():
    build_dir = Path("build")
    install_dir = get_home_local_bin().parent

    build_dir.mkdir(exist_ok=True)

    print(f"📂 빌드 디렉토리: {build_dir}")
    print(f"📥 설치 디렉토리: {install_dir}")

    cmake_configure = f'cmake -S . -B {build_dir} -DCMAKE_INSTALL_PREFIX="{install_dir}"'
    cmake_build = f'cmake --build {build_dir} --config Release'
    cmake_install = f'cmake --install {build_dir}'

    run(cmake_configure)
    run(cmake_build)
    run(cmake_install)

    add_path_to_user_env(get_home_local_bin().as_posix())

if __name__ == "__main__":
    main()

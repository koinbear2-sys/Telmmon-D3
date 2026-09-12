import subprocess
import webbrowser


def open_application(application):
    applications = {
        "calculator": "calc.exe",
        "notepad": "notepad.exe",
        "paint": "mspaint.exe",
        "explorer": "explorer.exe",
    }

    application = application.lower().strip()

    if application in applications:
        subprocess.Popen(applications[application])
        print(f"Telmmon D3: Opening {application}...")
    else:
        print(f"Telmmon D3: I don't know how to open {application} yet.")


def open_website(website):
    websites = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "discord": "https://discord.com/app",
        "roblox": "https://roblox.com",
    }

    website = website.lower().strip()

    if website in websites:
        webbrowser.open(websites[website])
        print(f"Telmmon D3: Opening {website}...")
    else:
        print(f"Telmmon D3: I don't know that website yet.")


def main():
    print("================================")
    print("       TELMMON D3")
    print("================================")
    print("Type 'exit' to close Telmmon D3.")
    print()

    while True:
        command = input("You: ").strip()

        if command.lower() == "exit":
            print("Telmmon D3 shutting down.")
            break

        if command.lower().startswith("open "):
            target = command[5:].strip()

            if target.lower() in ["youtube", "google", "discord", "roblox"]:
                open_website(target)
            else:
                open_application(target)

        else:
            print("Telmmon D3: I don't understand that command yet.")


if __name__ == "__main__":
    main()
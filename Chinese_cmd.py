from openai import OpenAI
import platform


def run_command(command):
    import os

    print("正在执行命令" + command)
    os.system(command)


os_name = "操作系统名称: " + str(platform.system())

os_version = "操作系统版本: " + str(platform.version())

processor_name = "处理器名称: " + str(platform.processor())

processor_architecture = "处理器架构: " + str(platform.architecture())

print("欢迎使用中文版Windows命令行，使用help命令查看帮助信息。")
while True:
    command = input("> ")
    if command.lower() == "exit":
        break
    elif command.lower() == "help":
        print(
            """帮助信息：
1. 输入命令后，助手会提供相应的Windows命令。
2. 输入exit退出命令行。
3. 输入help查看帮助信息。
4. 输入token:{Your Token}来设置老张AI的API密钥。
5. 输入clear清除屏幕。
6. 输入run:{command}来直接运行命令。
7. 输入info查看系统信息。
8. 输入ai:{message}来与AI对话""",
        )
        continue
    elif command.lower().startswith("token:"):
        token = command.split(":", 1)[1]
        client = OpenAI(
            api_key=token,
            base_url="https://api.laozhang.ai/v1",
        )
        print("老张AI密钥已设置。")
        continue
    elif command.lower() == "clear":
        import os

        os.system("cls" if os.name == "nt" else "clear")
        continue
    elif command.lower().startswith("run:"):
        command_to_run = command.split(":", 1)[1]
        run_command(command_to_run)
        continue
    elif command.lower() == "info":
        print(os_name)
        print(os_version)
        print(processor_name)
        print(processor_architecture)
        continue
    elif command.lower().startswith("ai:"):
        try:
            message = command.split(":", 1)[1]
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                stream=False,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个乐于助人的AI助手。回答中不包含markdown和html格式。",
                    },
                    {"role": "user", "content": message},
                ],
            )
            print(completion.choices[0].message.content)
            continue
        except:
            print("请检查AI密钥是否错误或未设置。")
            continue
    try:
        client
    except:
        print("请检查AI密钥是否错误或未设置。")
        continue
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            stream=False,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个windows命令行助手，回答问题时只会回答对应的命令，不会回答其他内容（包括解释），不带有```等markdown和html格式。系统信息："
                    + os_name
                    + os_version
                    + processor_name
                    + processor_architecture,
                },
                {"role": "user", "content": command},
            ],
        )
        print(completion.choices[0].message)
        op = input(
            "是否运行命令"
            + completion.choices[0].message.content
            + "（Y表示是，N表示否）："
        )
        if op.lower() == "y":
            run_command(completion.choices[0].message.content)
        else:
            print("命令未执行。")
    except:
        print("请检查AI密钥是否错误或未设置。")
        continue

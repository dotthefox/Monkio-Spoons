import os
import subprocess
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm.notebook import tqdm
from pathlib import Path
import requests

def run_script():
    def run_cmd(cmd):
        process = subprocess.run(cmd, shell=True, check=True, text=True)
        return process.stdout

    # Change the current directory to /content/
    os.chdir('/content/')
    print("Changing dir to /content/")

    # Your function to edit the file
    def edit_file(file_path):
        temp_file_path = "/tmp/temp_file.py"
        changes_made = False
        with open(file_path, "r") as file, open(temp_file_path, "w") as temp_file:
            previous_line = ""
            second_previous_line = ""
            for line in file:
                new_line = line.replace("value=160", "value=128")
                if new_line != line:
                    print("Replaced 'value=160' with 'value=128'")
                    changes_made = True
                line = new_line

                new_line = line.replace("crepe hop length: 160", "crepe hop length: 128")
                if new_line != line:
                    print("Replaced 'crepe hop length: 160' with 'crepe hop length: 128'")
                    changes_made = True
                line = new_line

                new_line = line.replace("value=0.88", "value=0.75")
                if new_line != line:
                    print("Replaced 'value=0.88' with 'value=0.75'")
                    changes_made = True
                line = new_line

                if "label=i18n(\"输入源音量包络替换输出音量包络融合比例，越靠近1越使用输出包络\")" in previous_line and "value=1," in line:
                    new_line = line.replace("value=1,", "value=0.25,")
                    if new_line != line:
                        print("Replaced 'value=1,' with 'value=0.25,' based on the condition")
                        changes_made = True
                    line = new_line

                if "label=i18n(\"总训练轮数total_epoch\")" in previous_line and "value=20," in line:
                    new_line = line.replace("value=20,", "value=500,")
                    if new_line != line:
                        print("Replaced 'value=20,' with 'value=500,' based on the condition for DEFAULT EPOCH")
                        changes_made = True
                    line = new_line

                if 'choices=["pm", "harvest", "dio", "crepe", "crepe-tiny", "mangio-crepe", "mangio-crepe-tiny"], # Fork Feature. Add Crepe-Tiny' in previous_line:
                    if 'value="pm",' in line:
                        new_line = line.replace('value="pm",', 'value="mangio-crepe",')
                        if new_line != line:
                            print("Replaced 'value=\"pm\",' with 'value=\"mangio-crepe\",' based on the condition")
                            changes_made = True
                        line = new_line

                new_line = line.replace('label=i18n("输入训练文件夹路径"), value="E:\\\\语音音频+标注\\\\米津玄师\\\\src"', 'label=i18n("输入训练文件夹路径"), value="/content/dataset/"')
                if new_line != line:
                    print("Replaced 'label=i18n(\"输入训练文件夹路径\"), value=\"E:\\\\语音音频+标注\\\\米津玄师\\\\src\"' with 'label=i18n(\"输入训练文件夹路径\"), value=\"/content/dataset/\"'")
                    changes_made = True
                line = new_line

                if 'label=i18n("是否仅保存最新的ckpt文件以节省硬盘空间"),' in second_previous_line:
                    if 'value=i18n("否"),' in line:
                        new_line = line.replace('value=i18n("否"),', 'value=i18n("是"),')
                        if new_line != line:
                            print("Replaced 'value=i18n(\"否\"),' with 'value=i18n(\"是\"),' based on the condition for SAVE ONLY LATEST")
                            changes_made = True
                        line = new_line

                if 'label=i18n("是否在每次保存时间点将最终小模型保存至weights文件夹"),' in second_previous_line:
                    if 'value=i18n("否"),' in line:
                        new_line = line.replace('value=i18n("否"),', 'value=i18n("是"),')
                        if new_line != line:
                            print("Replaced 'value=i18n(\"否\"),' with 'value=i18n(\"是\"),' based on the condition for SAVE SMALL WEIGHTS")
                            changes_made = True
                        line = new_line

                temp_file.write(line)
                second_previous_line = previous_line
                previous_line = line

        # After finished, we replace the original file with the temp one
        import shutil
        shutil.move(temp_file_path, file_path)

        if changes_made:
            print("Changes made and file saved successfully.")
        else:
            print("No changes were needed.")

    # Define the repo path
    repo_path = '/content/Retrieval-based-Voice-Conversion-WebUI'

    def copy_all_files_in_directory(src_dir, dest_dir):
        # Iterate over all files in source directory
        for item in Path(src_dir).glob('*'):
            if item.is_file():
                # Copy each file to destination directory
                shutil.copy(item, dest_dir)
            else:
                # If it's a directory, make a new directory in the destination and copy the files recursively
                new_dest = Path(dest_dir) / item.name
                new_dest.mkdir(exist_ok=True)
                copy_all_files_in_directory(str(item), str(new_dest))

    def clone_and_copy_repo(repo_path):
        # New repository link
        new_repo_link = "https://github.com/IAHispano/Applio-RVC-Fork.git"
        # Temporary path to clone the repository
        temp_repo_path = "/content/temp_Mangio-RVC-Fork"
        # New folder name
        new_folder_name = "Mangio-RVC-Fork"

        # Clone the latest code from the new repository to a temporary location
        run_cmd(f"git clone {new_repo_link} {temp_repo_path}")
        os.chdir(temp_repo_path)

        # run_cmd("git checkout bf0ffdbc35da09b57306e429c6deda84496948a1")
        run_cmd("git checkout fed45eb981a5295c17576caffb3ea997f0d670c6")
        run_cmd("git checkout 90e1022f04112cee4ad70520e7b1b53b88398065")
        run_cmd("git checkout 3103bab22bbc3bc968482f8903393dfe451422dc")
        run_cmd("git checkout 2bcbf0515e8f3998e7a4ae980422a3bce1af9516")
        run_cmd("git checkout 4f4772744a6681a9ce8241cc479b090d37017070")
        run_cmd("git checkout 7c33cba62399c173f1b615213631e77113354b1f")
        run_cmd("git checkout fe53965069eea218c51ca79f970be1b7c662d688")
        run_cmd("git checkout 8e5626ab56dc8e076d76e89fe383b3e32b2433fa")
        run_cmd("git checkout d2f92aef275e9789e83051c974c71f44141762b5")
        run_cmd("git checkout 02e34340989457949b2d39117800f20247038d8a")
        run_cmd("git checkout f4b9749db2a4381e8e6b38f06cbac4ebe7d88f70")
        run_cmd("git checkout f459a70008f430b907d4f02dab717e6771a97481")
        run_cmd("git checkout e1eef40a2e50ebeff77f84fdfe1c641f57a1a35c")
        run_cmd("git checkout d35a7367396936100b0e2e0eb14856ef5c0e79de")
        run_cmd("git checkout ad696bdfefe78b10e85666296511100b031d13e8")
        run_cmd("git checkout a6dd97d8a4698f7c53b9cd7a0b042a22448373b5")
        run_cmd("git checkout 13fe8785a6c234cd11fb18c041321b8c9534ed00")
        run_cmd("git checkout 4003a6511ab56e86d12f8df9d28954802e982b22")
        run_cmd("git checkout ba9abdc147d5f5e3f12dc8ec8388f50a356a068e")
        run_cmd("git checkout 432ed6a54a2f8ef9ff021791ad96bb16beb49388")
        run_cmd("git checkout 8007a90414b64ee456f3361a3c64c4100cccf6e6")
        run_cmd("git checkout 51e0849cb732a2e178625f22e82011705cb6683e")
        run_cmd("git checkout 1428c024cda321d97c58eb6edcc01786a3e64e60")
        run_cmd("git checkout 38518bebefc8324cbcac062427b03a3d34415629")
        run_cmd("git checkout c3f6720e0eb716e21ca174f8a1f9e402d577a49c")
        run_cmd("git checkout 2e78c126a43de0b9a43e57b46f0dfc628cf87933")
        run_cmd("git checkout 208995769fd22bce0a0e62a3407169bf6d776eae")
        run_cmd("git checkout 739463f58f15fd143c102f58458d483d719f6cf5")
        run_cmd("git checkout d555bcd2541ce3e78a9391f9255eb17f9753b006")
        run_cmd("git checkout fb6a9ed56d708bf36bd67b723ed61abda415b10f")
        run_cmd("git checkout 3cb7a554500519a2171d8d7deb830bb4f4e24faf")
        run_cmd("git checkout 1f38961b8aeca4198cacf3f4f58c14d3aae38e1d")
        run_cmd("git checkout 53030c87a0f788c399dbcf51ad78db5d023268e0")
        run_cmd("git checkout fb54396322f4e76fa1f47dc9b02dd443f02e75cd")
        run_cmd("git checkout 84acd27cbf5d74fd17d838939cdecb105236207c")
        run_cmd("git checkout ab16e975a425d29affe79ce74a57dcc950c35929")
        run_cmd("git checkout 7c04d3532a64b26eabdec7ede2f41b1e49af9b45")
        run_cmd("git checkout c18fe4f70584e36335b49df4f24660d6ad4e6346")
        run_cmd("git checkout 63a1704e2739f8ac894933736ae33f1c8a56889f")

        run_cmd("wget https://github.com/kalomaze/Mangio-Kalo-Tweaks/raw/patch-1/EasierGUI.py")

        # Edit the file here, before copying
        edit_file(f"{temp_repo_path}/infer-web.py")

        # Copy all files from the cloned repository to the existing path
        copy_all_files_in_directory(temp_repo_path, repo_path)
        print(f"Copying all {new_folder_name} files from GitHub.")

        # Change working directory back to /content/
        os.chdir('/content/')
        print("Changed path back to /content/")
        
        # Remove the temporary cloned repository
        shutil.rmtree(temp_repo_path)

    # Call the function
    clone_and_copy_repo(repo_path)

    # Download the credentials file for RVC archive sheet
    os.makedirs('/content/Retrieval-based-Voice-Conversion-WebUI/stats/', exist_ok=True)
    run_cmd("wget -q https://cdn.discordapp.com/attachments/945486970883285045/1114717554481569802/peppy-generator-388800-07722f17a188.json -O /content/Retrieval-based-Voice-Conversion-WebUI/stats/peppy-generator-388800-07722f17a188.json")

    # Forcefully delete any existing torchcrepe dependencies downloaded from an earlier run just in case
    shutil.rmtree('/content/Retrieval-based-Voice-Conversion-WebUI/torchcrepe', ignore_errors=True)
    shutil.rmtree('/content/torchcrepe', ignore_errors=True)

    # Download the torchcrepe folder from the maxrmorrison/torchcrepe repository
    run_cmd("git clone https://github.com/maxrmorrison/torchcrepe.git")
    shutil.move('/content/torchcrepe/torchcrepe', '/content/Retrieval-based-Voice-Conversion-WebUI/')
    shutil.rmtree('/content/torchcrepe', ignore_errors=True)  # Delete the torchcrepe repository folder

    # Change the current directory to /content/Retrieval-based-Voice-Conversion-WebUI
    os.chdir('/content/Retrieval-based-Voice-Conversion-WebUI')
    os.makedirs('pretrained', exist_ok=True)
    os.makedirs('uvr5_weights', exist_ok=True)

def download_file(url, filepath):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(filepath, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

def download_pretrained_models():
    pretrained_models = {
        "pretrained": [
            "D40k.pth",
            "G40k.pth",
            "f0D40k.pth",
            "f0G40k.pth"
        ],
        "pretrained_v2": [
            "D40k.pth",
            "G40k.pth",
            "f0D40k.pth",
            "f0G40k.pth",
            "f0G48k.pth",
            "f0D48k.pth"
        ],
        "uvr5_weights": [
            "HP2-人声vocals+非人声instrumentals.pth",
            "HP5-主旋律人声vocals+其他instrumentals.pth",
            "VR-DeEchoNormal.pth",
            "VR-DeEchoDeReverb.pth",
            "VR-DeEchoAggressive.pth",
            "HP5_only_main_vocal.pth",
            "HP3_all_vocals.pth",
            "HP2_all_vocals.pth"
        ]
    }

    base_url = "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/"
    base_path = "/content/Retrieval-based-Voice-Conversion-WebUI/"

    # Calculate total number of files to download
    total_files = sum(len(files) for files in pretrained_models.values()) + 1  # +1 for hubert_base.pt

    with tqdm(total=total_files, desc="Downloading files") as pbar:
        for folder, models in pretrained_models.items():
            folder_path = os.path.join(base_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            for model in models:
                url = base_url + folder + "/" + model
                filepath = os.path.join(folder_path, model)
                download_file(url, filepath)
                pbar.update()

        # Download hubert_base.pt to the base path
        hubert_url = base_url + "hubert_base.pt"
        hubert_filepath = os.path.join(base_path, "hubert_base.pt")
        download_file(hubert_url, hubert_filepath)
        pbar.update()

def clone_repository(run_download):
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(run_script)
        if run_download:
            executor.submit(download_pretrained_models)

from pathlib import Path
import shutil

def diarium_entry(entry_folder, dest_folder):
    # converts a Diarium entry to a Zim page, including attachments.

    # the folders are path objects
    entry_file = [file for file in entry_folder.glob("Diarium*.txt")][0]
    print(f"Processing entry: {entry_folder.name}")

    # Get the content of the text entry and prepare it for Zim
    with open(entry_file,"r",encoding="utf-8") as f:
        entry_text = f.read().split("\n")
    entry_title = f"{entry_folder.name}-0001 {entry_text[1]}"
    zim_title = f"====== {entry_title} ======\n\n"
    zim_filename = entry_title.replace(" ","_") + ".txt"

    # Check if the Zim entry has already been created.
    file_check = [file for file in dest_folder.glob(zim_filename)]

    if len(file_check) > 0:
        print(f"Zim page for: {entry_folder.name} already exists.")

    else:
        entry_content = zim_title + "\n".join(entry_text[2:])

        # Look for attachments and create links in Zim format

        # If there's more than one file, there are attachments.
        if len([file for file in entry_folder.iterdir()]) > 1:
            print("    Processing attachments...")
            zim_attachment_folder = entry_title.replace(" ","_")
            Path(dest_folder,zim_attachment_folder).mkdir(parents=True)
            for file in entry_folder.iterdir():
                if file.suffix != ".txt":
                    
                    if file.suffix.upper() == ".JPG" or file.suffix.upper() == ".JPEG":

                        # Zim link format for photos
                        link_text = "{{.\\" + file.name + "?width=700}}\n"
                    else:
                        
                        # Zim link format for other files (pdf, etc.)
                        link_text = "[[.\\" + file.name + "]]\n"
                    
                    entry_content = entry_content + link_text

                    shutil.copy(file,Path(dest_folder,zim_attachment_folder,file.name))
                    print(f"      Copied file: {file.name}")

        
        # Create the Zim Wiki page
        with open(Path(dest_folder,zim_filename),"w",encoding="utf-8") as f:
            f.write(entry_content)
            print(f"Created Zim page: {str(Path(dest_folder,zim_filename))}")


def diarium_to_zim(diarium_folder,zim_dest):

    # diarium_folder and zim_dest are path objects
    for entry_folder in diarium_folder.iterdir():
        diarium_entry(entry_folder, zim_dest)


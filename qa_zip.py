import paramiko
from datetime import datetime, timedelta

def generate_weekly_directories(unique_code, base_path="/nasa-dcs-upload", days=3):

    #Generate directory path for previous 7 days.

    directories = []
    today = datetime.now()

    for i in range(days): # '7' represent the days
        target_date = today - timedelta(days=i)
        #print(target_date)
        date_str = target_date.strftime("%m%d%y")
        directory = f"{base_path}/{date_str}/{unique_code}/"

        directories.append({
            'date': target_date.strftime("%Y-%m-%d"),
            'date_code': date_str,
            'path' : directory
            }
        )
    return directories


print(generate_weekly_directories(unique_code="lcmiwget"))

# def get_subdirectories(ssh, parent_path):
#
#     #Get all subdirectories in the parent path
#
#     try:
#         command = f"find {parent_path} -maxdepth 1 -type d -name '[0-9]*' 2>/dev/null"
#         stdin, stdout, stderr = ssh.exec_command(command)
#         output = stdout.read().decode().strip()
#         print(f"Output: {output}")
#
#         if output:
#             subdirs = [line.strip() for line in output.split('\n') if line.strip()]
#             print(f"Subdirs: {subdirs}")
#             return subdirs
#     except:
#         return []

def get_subdirectories(ssh, parent_path):
    """
    Get all subdirectories in the parent path
    """
    try:
        # First, let's try a simpler ls command to see what's actually there
        command = f"ls -la {parent_path}"
        stdin, stdout, stderr = ssh.exec_command(command)
        ls_output = stdout.read().decode().strip()
        error_output = stderr.read().decode().strip()

        #print(f"   DEBUG - ls output: {ls_output}")
        if error_output:
            # print(f"   DEBUG - ls error: {error_output}")
            pass

        # Now try to find numeric directories
        # Remove trailing slash if present for consistent path handling
        clean_path = parent_path.rstrip('/')
        command = f"find {clean_path} -maxdepth 1 -type d -name '[0-9]*' 2>/dev/null"
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        #print(f"   DEBUG - find command: {command}")
        #print(f"   DEBUG - find output: '{output}'")
        if error:
            pass
            #print(f"   DEBUG - find error: {error}")

        if output:
            subdirs = [line.strip() for line in output.split('\n') if line.strip() and line.strip() != clean_path]
            #print(f"   DEBUG - parsed subdirs: {subdirs}")
            return subdirs

        # Alternative approach: use ls with grep
        command = f"ls -1 {clean_path} | grep '^[0-9]'"
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode().strip()

        # print(f"   DEBUG - ls|grep command: {command}")
        # print(f"   DEBUG - ls|grep output: '{output}'")

        if output:
            folder_names = [line.strip() for line in output.split('\n') if line.strip()]
            subdirs = [f"{clean_path}/{folder}" for folder in folder_names]
            # print(f"   DEBUG - alternative subdirs: {subdirs}")
            return subdirs

        return []
    except Exception as e:
        # print(f"   DEBUG - Exception in get_subdirectories: {str(e)}")
        return []

def list_zip_files_in_directory(ssh, directory_path):

    #List zip files in a specific directory and categorize them

    try:
        command = f"ls -la {directory_path}*.zip 2>/dev/null"
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode().strip()

        if not output or "No such file" in output:
            return None, None, []

        lines = output.split('\n')
        zip_files = []

        for line in lines:
            if line.strip() and '.zip' in line and not line.startswith('total'):
                parts = line.split()
                if parts:
                    filename = parts[-1]
                    if filename.endswith('.zip'):
                        zip_files.append(filename)

        # if not zip_files:
        #     return None, None, []
        #
        # letter_file =None
        # number_file = None
        #
        # for filename in zip_files:
        #     basename = filename.replace('.zip', '')
        #     if basename and basename[0].isalpha():
        #         letter_file = filename
        #     elif basename and basename[0].isdigit():
        #         number_file = filename

        return zip_files
    except Exception as e:
        return []


def scan_weekly_directories(hostname, username, password, unique_code, port=22):
    """
    Main function to scan all weekly directories
    """
    results = []

    try:
        # Create SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Changed AutoAddHostKeyPolicy to AutoAddPolicy

        # Connect to the server
        print(f"🔗 Connecting to {hostname}...")
        ssh.connect(hostname, port=port, username=username, password=password)
        print("✅ Connected successfully!\n")

        # Generate weekly directories
        weekly_dirs = generate_weekly_directories(unique_code)

        #print(f"📅 Scanning {unique_code} for the past 7 days...")
        print("=" * 60)

        for dir_info in weekly_dirs:
            date_display = dir_info['date']
            date_code = dir_info['date_code']
            parent_path = dir_info['path']

            #print(f"\n📁 {date_display} ({date_code}): {parent_path}")

            # Check if parent directory exists
            check_cmd = f"test -d {parent_path} && echo 'exists' || echo 'not found'"
            stdin, stdout, stderr = ssh.exec_command(check_cmd)
            exists = stdout.read().decode().strip()
            #print(f"Exists: {exists}")

            if exists != 'exists':
                #print(f"   ❌ Directory not found")
                continue

            # Get subdirectories
            subdirs = get_subdirectories(ssh, parent_path)
            print(f"parent path: {parent_path}")
            print(f"    📂Sub directories: {subdirs}")

            if not subdirs:
                print(f"   ❌ No subdirectories found")
                continue

            # Process each subdirectory
            day_results = []
            for subdir in subdirs:
                folder_name = subdir.split('/')[-1]
                #print(f"   📂 Checking folder: {folder_name}")

                # letter_file, number_file, all_files = list_zip_files_in_directory(ssh, f"{subdir}/")
                all_files = list_zip_files_in_directory(ssh, f"{subdir}/")

                # print(f"letter file: {letter_file}, \n number files: {number_file} \n all_files: {all_files}")

                if all_files:
                    folder_result = {
                        'date': date_display,
                        'date_code': date_code,
                        'folder': folder_name,
                        'zip_files': all_files,
                        'path': f"{subdir}/"
                    }
                    day_results.append(folder_result)

                    #print(f"      ✅ Found {len(all_files)} zip files: {', '.join(all_files)}")
                else:
                    print(f"      ❌ No zip files found")

                if day_results:
                    results.extend(day_results)
                else:
                    print(f"   ❌ No zip files found in any subdirectories")
        return results

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []

    finally:
        ssh.close()
        print(f"\n🔒 SSH connection closed")


def format_results(results):
    """
    Format results for display and clipboard
    """
    if not results:
        return "No zip files found in any directories.", "" # Added empty string for clipboard_text when no results

    output = []
    output.append(f"📊 SUMMARY: Found zip files in {len(results)} locations")
    output.append("=" * 60)

    clipboard_text = []

    for result in results:
        date_info = f"{result['date']} ({result['date_code']})"
        folder_info = f"Folder: {result['folder']}"

        output.append(f"\n📅 {date_info} - {folder_info}")
        output.append(f"   Path: {result['path']}")
        output.append(f"   📦 Files: {', '.join(result['zip_files'])}")
        #output.append(f"   📦 Files: {' <=> '.join(result['zip_files'])}")

    # print(f"Output: {output}")

        # clipboard_line = f"{result['date_code']}/{result['folder']}: {' | '.join(result['zip_files'])}"
        # clipboard_text.append(clipboard_line)

    # return "\n".join(output), "\n".join(clipboard_text)
    return "\n".join(output)


def main():
    print("🚀 Weekly SSH Zip File Scanner")
    print("=" * 40)

    # Get SSH connection details
    # hostname = input("SSH Host: ")
    hostname = input("Enter hostname:");
    username = input("Enter username:");
    password = input("Enter password:");
    unique_code = input("Unique Code (e.g., lcmiwget): ")

    print(f"\n🔍 Starting scan for '{unique_code}'...")

    # Scan directories
    results = scan_weekly_directories(hostname, username, password, unique_code)

    #print(f"Result: {results}")

    # Display results
    print("\n" + "=" * 60)
    #display_text, clipboard_text = format_results(results)
    display_text = format_results(results)
    #print(display_text)

    for result in results:
        print(f"CAS QA ZIP: {result['zip_files'][0].split('/')[-1]} <=> JENA ZIP: {result['zip_files'][1].split('/')[-1]}")

    # Copy to clipboard
    # if results:
    #     try:
    #         pyperclip.copy(clipboard_text)
    #         print(f"\n✅ Results copied to clipboard!")
    #         print("📋 Clipboard format: DATE/FOLDER: L:letter_file.zip | N:number_file.zip")
    #     except:
    #         print(f"\n⚠️  Could not copy to clipboard")
    #         print("📋 Manual copy:")
    #         print(clipboard_text)
    #
    # print(f"\n✨ Scan complete!")


if __name__ == "__main__":
    main()

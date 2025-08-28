import paramiko
from datetime import datetime, timedelta

def generate_weekly_directories(unique_code, base_path="/nasa-dcs-upload", days=3):
    """Generate directory paths for previous N days."""
    directories = []
    today = datetime.now()

    for i in range(days):
        target_date = today - timedelta(days=i)
        date_str = target_date.strftime("%m%d%y")
        directory = f"{base_path}/{date_str}/{unique_code}/"
        directories.append({
            'date': target_date.strftime("%Y-%m-%d"),
            'date_code': date_str,
            'path': directory
        })
    return directories


def get_subdirectories(ssh, parent_path):
    """Get all numeric subdirectories in the parent path."""
    try:
        clean_path = parent_path.rstrip('/')
        # Use a single optimized command
        command = f"ls -1d {clean_path}/[0-9]* 2>/dev/null | head -20"
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode().strip()

        if output:
            return [line.strip() for line in output.split('\n') if line.strip()]
        return []
    except:
        return []


def list_zip_files_in_directory(ssh, directory_path):
    """List zip files in a specific directory."""
    print(f"Director path: {directory_path}")
    try:
        command = f"ls -1 {directory_path}*.zip 2>/dev/null"
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode().strip()

        if not output or "No such file" in output:
            return []

        return [line.strip() for line in output.split('\n')
                if line.strip() and line.endswith('.zip')]
    except:
        return []


def scan_weekly_directories(hostname, username, password, unique_code, port=22):
    """Main function to scan all weekly directories."""
    results = []

    try:
        # Create SSH client with optimized settings
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print(f"🔗 Connecting to {hostname}...")
        ssh.connect(hostname, port=port, username=username, password=password,
                    timeout=10, compress=True)
        print("✅ Connected successfully!\n")

        weekly_dirs = generate_weekly_directories(unique_code)
        print("=" * 60)

        for dir_info in weekly_dirs:
            parent_path = dir_info['path']

            # Quick existence check and get subdirs in one operation
            subdirs = get_subdirectories(ssh, parent_path)

            if not subdirs:
                continue

            print(f"📂 {dir_info['date']} ({dir_info['date_code']}): Found {len(subdirs)} subdirectories")

            # Process subdirectories
            for subdir in subdirs:
                folder_name = subdir.split('/')[-1]
                zip_files = list_zip_files_in_directory(ssh, f"{subdir}/")

                if zip_files:
                    results.append({
                        'date': dir_info['date'],
                        'date_code': dir_info['date_code'],
                        'folder': folder_name,
                        'zip_files': zip_files,
                        'path': f"{subdir}/"
                    })

        return results

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []
    finally:
        ssh.close()
        print(f"\n🔒 SSH connection closed")


def main():
    print("🚀 Weekly SSH Zip File Scanner")
    print("=" * 40)

    # SSH connection details
    hostname = input("Enter hostname:");
    username = input("Enter username:");
    password = input("Enter password:");
    unique_code = input("Unique Code (e.g., lcmiwget): ")

    print(f"\n🔍 Starting scan for '{unique_code}'...")

    # Scan directories
    results = scan_weekly_directories(hostname, username, password, unique_code)

    # Display results
    print("\n" + "=" * 60)

    if not results:
        print("No zip files found in any directories.")
        return

    print(f"📊 SUMMARY: Found zip files in {len(results)} locations")
    print("=" * 60)

    for result in results:
        if len(result['zip_files']) >= 2:
            #print(f"CAS QA ZIP: {result['zip_files'][0].split('/')[-1]} <=> JENA ZIP: {result['zip_files'][1].split('/')[-1]}")
            print(f"\nResult: {result['zip_files']}")
        else:
            #print(f"No corresponding zip file found for: {', '.join(result['zip_files'])}")
            pass

    print(f"\n✨ Scan complete!")


if __name__ == "__main__":
    main()

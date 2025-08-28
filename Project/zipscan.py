import paramiko
import json
from datetime import datetime, timedelta


def generate_directories(state_code, base_path="/nasa-dcs-upload", days=4):
    """Generate directory paths for previous N days."""
    directories = []
    today = datetime.now()

    for i in range(days):
        target_date = today - timedelta(days=i)
        date_str = target_date.strftime("%m%d%y")
        directory = f"{base_path}/{date_str}/{state_code}/"
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


def categorize_zip_files(zip_files):
    """Categorize zip files into alphabetic and numeric."""
    alphabetic_zips = []
    numeric_zips = []

    for zip_file in zip_files:
        filename = zip_file.split('/')[-1]
        if filename and filename[0].isalpha():
            alphabetic_zips.append(zip_file)
        elif filename and filename[0].isdigit():
            numeric_zips.append(zip_file)

    return alphabetic_zips, numeric_zips


def list_zip_files_in_directory(ssh, directory_path):
    """List zip files in a specific directory."""
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


def scan_directories(hostname, username, password, state_code, port=22):
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

        directories = generate_directories(state_code)
        print("=" * 60)

        for dir_info in directories:
            parent_path = dir_info['path']

            # Quick existence check and get sub_dirs in one operation
            sub_directories = get_subdirectories(ssh, parent_path)

            if not sub_directories:
                continue

            print(f"📂 {dir_info['date']} ({dir_info['date_code']}): Found {len(sub_directories)} subdirectories")

            # Process subdirectories
            for subdir in sub_directories:
                folder_name = subdir.split('/')[-1]
                zip_files = list_zip_files_in_directory(ssh, f"{subdir}/")

                if zip_files:
                    # Categorize zip files
                    alphabetic_zips, numeric_zips = categorize_zip_files(zip_files)

                    # Condition 1: Skip directory if no alphabetic zip file
                    if not alphabetic_zips:
                        continue

                    results.append({
                        'date': dir_info['date'],
                        'date_code': dir_info['date_code'],
                        'folder': folder_name,
                        'alphabetic_zips': alphabetic_zips,
                        'numeric_zips': numeric_zips,
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
    print("🚀 Zip File & Upload path Scanner")
    print("=" * 40)

    # SSH connection details
    with open('config.json', 'r') as f:
        config = json.load(f)

    hostname = config['hostname']
    username = config['username']
    password = config['password']

    state_code = input("Enter state Code (e.g., lcmiwget): ")

    print(f"\n🔍 Starting scan for '{state_code}'...")

    results = scan_directories(hostname, username, password, state_code)
    print("\n" + "=" * 60)

    if not results:
        print("No zip files found in any directories.")
        return

    print(f"📊 SUMMARY: Found zip files in {len(results)} locations")
    print("=" * 60)

    for result in results:
        # Condition 1: If more than one zip file generated in CAS QA.
        if len(result['numeric_zips']) > 1:
            numeric_files = ', '.join([zip_file.split('/')[-1] for zip_file in result['numeric_zips']])
            alphabetic_files = ', '.join([zip_file.split('/')[-1] for zip_file in result['alphabetic_zips']])
            print(f"CAS: {numeric_files} <=> JENA: {alphabetic_files} Path: {'/'.join(result['alphabetic_zips'][0].split('/')[:-1])}")
        # Condition 2: If only one zip file generated in CAS QA.
        elif len(result['numeric_zips']) == 1:
            print(f"CAS: {result['numeric_zips'][0].split('/')[-1]} <=> JENA: {result['alphabetic_zips'][0].split('/')[-1]} Path: {'/'.join(result['alphabetic_zips'][0].split('/')[:-1])}")

    print(f"\n✨ Scan complete!")


if __name__ == "__main__":
    main()
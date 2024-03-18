import os

def sudo_execute(command):
    sudo_command = f"sudo -S {command}"
    os.system(sudo_command)

def install_s3fs():
    distro = input("Enter your Linux distribution (centos/fedora or ubuntu): ").lower()
    if distro == "centos" or distro == "fedora":
        sudo_execute("dnf install s3fs-fuse")
    elif distro == "ubuntu":
        sudo_execute("apt install s3fs")
    else:
        print("Unsupported Linux distribution.")

def create_passwd_file():
    access_key = input("Enter your AWS Access Key ID: ")
    secret_key = input("Enter your AWS Secret Access Key: ")
    sudo_execute(f"echo '{access_key}:{secret_key}' | sudo -S tee /etc/passwd-s3fs >/dev/null")
    sudo_execute("sudo chmod 600 /etc/passwd-s3fs")

def create_mount_point(mount_location):
    sudo_execute(f"mkdir -p {mount_location}")

def add_to_fstab(bucket_name, mount_location):
    sudo_execute(f'echo "{bucket_name}   {mount_location}   fuse.s3fs   _netdev,allow_other,passwd_file=/etc/passwd-s3fs   0   0" | sudo -S tee -a /etc/fstab >/dev/null')

def mount_s3_bucket(mount_location):
    sudo_execute(f"mount {mount_location}")

def main():
    install_s3fs()
    create_passwd_file()
    mount_location = input("Enter the mount location: ")
    create_mount_point(mount_location)
    bucket_name = input("Enter your S3 bucket name: ")
    add_to_fstab(bucket_name, mount_location)
    mount_s3_bucket(mount_location)

if __name__ == "__main__":
    main()

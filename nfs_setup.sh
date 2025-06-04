#!/bin/bash

# כתובות IP
server_ip="127.0.0.1"       # במקרה שלך זה localhost
client_ip="127.0.0.1"       # גם הוא

# תיקיות
shared_dir="/srv/nfs_share"
mount_point="/mnt/nfs_share"

echo "📦 Installing NFS server and client..."
sudo apt update
sudo apt install -y nfs-kernel-server nfs-common

echo "📁 Creating shared directory..."
sudo mkdir -p "$shared_dir"
sudo chmod 777 "$shared_dir"

echo "🛠️ Configuring /etc/exports..."
echo "$shared_dir $client_ip(rw,sync,no_subtree_check)" | sudo tee -a /etc/exports

echo "🔄 Restarting NFS server..."
sudo systemctl restart nfs-kernel-server

echo "📂 Creating mount point..."
sudo mkdir -p "$mount_point"

echo "🔗 Mounting NFS share..."
sudo mount -t nfs "$server_ip:$shared_dir" "$mount_point"

echo "📝 Updating /etc/fstab..."
echo "$server_ip:$shared_dir $mount_point nfs defaults 0 0" | sudo tee -a /etc/fstab

echo "✅ Done! NFS setup complete."

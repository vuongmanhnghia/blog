---
title: Setup Minecraft Server
date: 2025-12-26
image:
categories:
  - setup
tags:
  - minecraft
draft: true
---
<!--more-->

---

### 1. Install Java

```bash
sudo apt install -y openjdk-21-jre-headless

java -version
```

### 2. Create Minecraft user

```bash
sudo useradd -r -m -U -d /opt/minecraft -s /bin/bash minecraft
sudo su - minecraft
```

### 3. Setup Minecraft Server

```bash
cd /opt/minecraft
mkdir server && cd server

# Paper 1.21.10 (Recommended - optimized fork)
MINECRAFT_VERSION="1.21.10" LATEST_BUILD=$(curl -s "https://api.papermc.io/v2/projects/paper/versions/$MINECRAFT_VERSION" | jq -r '.builds[-1]') wget "https://api.papermc.io/v2/projects/paper/versions/$MINECRAFT_VERSION/builds/$LATEST_BUILD/downloads/paper-$MINECRAFT_VERSION-$LATEST_BUILD.jar" -O server.jar

# Chấp nhận EULA
echo "eula=true" > eula.txt
```

### 4. Setup System Service

```bash
sudo nano /etc/systemd/system/minecraft.service
```

**Content**

```ini
[Unit]
Description=Minecraft Server 1.21.10
After=network.target

[Service]
Type=simple
User=minecraft
Group=minecraft
WorkingDirectory=/opt/minecraft/server

# JVM Flags tối ưu nhất cho 1.21.10 + Java 21
ExecStart=/usr/bin/java -Xms4G -Xmx4G \
    --add-modules=jdk.incubator.vector \
    -XX:+UseG1GC \
    -XX:+ParallelRefProcEnabled \
    -XX:MaxGCPauseMillis=200 \
    -XX:+UnlockExperimentalVMOptions \
    -XX:+UnlockDiagnosticVMOptions \
    -XX:+DisableExplicitGC \
    -XX:+AlwaysPreTouch \
    -XX:G1NewSizePercent=30 \
    -XX:G1MaxNewSizePercent=40 \
    -XX:G1HeapRegionSize=8M \
    -XX:G1ReservePercent=20 \
    -XX:G1HeapWastePercent=5 \
    -XX:G1MixedGCCountTarget=4 \
    -XX:InitiatingHeapOccupancyPercent=15 \
    -XX:G1MixedGCLiveThresholdPercent=90 \
    -XX:G1RSetUpdatingPauseTimePercent=5 \
    -XX:SurvivorRatio=32 \
    -XX:+PerfDisableSharedMem \
    -XX:MaxTenuringThreshold=1 \
    -XX:G1SATBBufferEnqueueingThresholdPercent=30 \
    -XX:G1ConcMarkStepDurationMillis=5 \
    -XX:G1ConcRSHotCardLimit=16 \
    -XX:GCTimeRatio=99 \
    -XX:+UseNUMA \
    -XX:-DontCompileHugeMethods \
    -XX:+UseFastUnorderedTimeStamps \
    -XX:+UseCriticalJavaThreadPriority \
    -XX:ThreadPriorityPolicy=1 \
    -XX:AllocatePrefetchStyle=3 \
    -Dlog4j2.formatMsgNoLookups=true \
    -Dlog4j.configurationFile=/opt/minecraft/server/log4j2.xml \
    -jar server.jar --nogui

# Graceful shutdown
ExecStop=/bin/sh -c 'echo "stop" > /run/minecraft.stdin'
TimeoutStopSec=120

Restart=on-failure
RestartSec=10

StandardInput=null
StandardOutput=journal
StandardError=journal

# Security hardening
PrivateTmp=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

### 5. Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable minecraft
sudo systemctl start minecraft
```

### 6. `server.properties` for optimize

```bash
# Network & Performance
server-port=25565
network-compression-threshold=256
max-tick-time=60000

# Player limits
max-players=20
player-idle-timeout=10

# View distances (critical cho performance)
view-distance=10
simulation-distance=8

# Chunk settings (new in 1.21+)
chunk-loading-advanced=true

# Security
enforce-secure-profile=true
online-mode=true
white-list=false

# World settings
level-type=minecraft\:normal
difficulty=normal
hardcore=false
enable-command-block=false

# Performance
sync-chunk-writes=false
use-native-transport=true

# RCON for remote management
enable-rcon=true
rcon.password=ChangeMeStrong123!
rcon.port=25575
broadcast-rcon-to-ops=true

# Logging
level-name=world
enable-status=true
enable-query=false
```

### 7. Docker compose

```yml
version: '3.9'

services:
  minecraft:
    image: itzg/minecraft-server:java21
    container_name: minecraft-1.21.10
    restart: unless-stopped
    
    ports:
      - "25565:25565"
      - "25575:25575"  # RCON
    
    environment:
      EULA: "TRUE"
      TYPE: "PAPER"
      VERSION: "1.21.10"
      MEMORY: "4G"
      
      # JVM tuning
      JVM_XX_OPTS: "-XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions"
      
      # Server config
      MAX_PLAYERS: "20"
      VIEW_DISTANCE: "10"
      SIMULATION_DISTANCE: "8"
      DIFFICULTY: "normal"
      MODE: "survival"
      PVP: "true"
      
      # RCON
      ENABLE_RCON: "true"
      RCON_PASSWORD: "your_strong_password"
      
      # Performance
      SYNC_CHUNK_WRITES: "false"
      USE_NATIVE_TRANSPORT: "true"
      
      # Paper specific
      PAPER_DOWNLOAD_URL: "https://api.papermc.org/v2/projects/paper/versions/1.21.10/builds/latest/downloads/paper-1.21.10-latest.jar"
    
    volumes:
      - ./minecraft-data:/data
      - ./minecraft-backups:/backups
    
    deploy:
      resources:
        limits:
          memory: 5G
        reservations:
          memory: 4G
    
    healthcheck:
      test: ["CMD", "mc-monitor", "status", "--host", "localhost", "--port", "25565"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 120s

  # Optional: Backup service
  backup:
    image: itzg/mc-backup
    container_name: minecraft-backup
    restart: unless-stopped
    
    environment:
      BACKUP_INTERVAL: "6h"
      PRUNE_BACKUPS_DAYS: "7"
      RCON_HOST: "minecraft"
      RCON_PASSWORD: "your_strong_password"
    
    volumes:
      - ./minecraft-data:/data:ro
      - ./minecraft-backups:/backups
    
    depends_on:
      - minecraft
```

### 8. Monitoring scripts

```bash
sudo nano /opt/minecraft/monitor.sh
```

```bash
#!/bin/bash
LOG_FILE="/var/log/minecraft-monitor.log"

# Check if service is running
if ! systemctl is-active --quiet minecraft; then
    echo "[$(date)] ERROR: Minecraft service is down. Attempting restart..." >> $LOG_FILE
    systemctl start minecraft
    sleep 30
    
    if systemctl is-active --quiet minecraft; then
        echo "[$(date)] INFO: Service restarted successfully" >> $LOG_FILE
    else
        echo "[$(date)] CRITICAL: Failed to restart service" >> $LOG_FILE
    fi
fi

# Check TPS
TPS=$(mcrcon -H localhost -P 25575 -p "ChangeMeStrong123!" "tps" 2>/dev/null | grep -oP '\d+\.\d+' | head -1)
if [ ! -z "$TPS" ]; then
    echo "[$(date)] TPS: $TPS" >> $LOG_FILE
fi
```

```bash
sudo chmod +x /opt/minecraft/monitor.sh

# Run every 5 minutes
sudo crontab -e
# Add:
*/5 * * * * /opt/minecraft/monitor.sh
```
import os

# Define the image name and tag
image_name = 'ssenchyna/syslog'
image_tag = '1.0'
# docker buildx create --use
os.system(f'docker buildx build --platform linux/amd64,linux/arm64 -t ssenchyna/syslog --push .')

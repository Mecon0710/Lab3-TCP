size = 238 * 1024 * 1024 # 250 MB
with open('archivo100MB(1).bin', 'wb') as f:
    f.write(b'\0' * size)
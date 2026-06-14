#!/usr/bin/env python3
import struct, zlib, math

def make_png(size):
    def chunk(name, data):
        c = zlib.crc32(name + data) & 0xffffffff
        return struct.pack('>I', len(data)) + name + data + struct.pack('>I', c)

    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))

    # Draw a rounded square with checkmark in green
    pixels = []
    r, g, b = 29, 158, 117  # #1D9E75
    pad = size // 8
    corner = size // 5

    for y in range(size):
        row = []
        for x in range(size):
            # Rounded rectangle check
            dx = max(pad + corner - x, x - (size - pad - corner), 0)
            dy = max(pad + corner - y, y - (size - pad - corner), 0)
            dist = math.sqrt(dx*dx + dy*dy)
            inside = x >= pad and x < size-pad and y >= pad and y < size-pad and dist <= corner

            if inside:
                # Draw checkmark
                cx, cy = size/2, size/2
                # Simple check: two lines
                # Left part: from (0.25, 0.5) to (0.42, 0.67)
                # Right part: from (0.42, 0.67) to (0.72, 0.33)
                nx, ny = x/size, y/size
                on_check = False
                # Left stroke
                t1 = (nx - 0.25) / (0.42 - 0.25)
                if 0 <= t1 <= 1:
                    ey = 0.5 + t1*(0.67-0.5)
                    if abs(ny - ey) < 0.05: on_check = True
                # Right stroke
                t2 = (nx - 0.42) / (0.72 - 0.42)
                if 0 <= t2 <= 1:
                    ey = 0.67 + t2*(0.33-0.67)
                    if abs(ny - ey) < 0.05: on_check = True
                if on_check:
                    row += [255, 255, 255]
                else:
                    row += [r, g, b]
            else:
                row += [255, 255, 255]
        pixels.append(bytes([0]) + bytes(row))

    raw = b''.join(pixels)
    compressed = zlib.compress(raw, 9)
    idat = chunk(b'IDAT', compressed)
    iend = chunk(b'IEND', b'')
    return b'\x89PNG\r\n\x1a\n' + ihdr + idat + iend

for size, name in [(192, 'icon-192.png'), (512, 'icon-512.png')]:
    with open(name, 'wb') as f:
        f.write(make_png(size))
    print(f'Created {name}')


import tkinter as tk
import math
import time

# ==========================================
# AVERON X1 - SOFTWARE GPU SIMULATOR
# Version 0.3 - PERFORMANCE PROFILER
# ==========================================

WIDTH = 400
HEIGHT = 300
FOCAL_LENGTH = 230
CAMERA_DISTANCE = 4.0

VERTICES = [
    (-1.2, -0.85, 0.0),
    (1.2, -0.85, 0.0),
    (0.0, 1.1, 0.0)
]

COLORS = [
    (255, 65, 85),
    (65, 240, 135),
    (75, 130, 255)
]


# ==========================================
# VERTEX TRANSFORMATION
# ==========================================

def rotate_vertex(vertex, angle_x, angle_y):
    x, y, z = vertex

    cy = math.cos(angle_y)
    sy = math.sin(angle_y)

    x1 = x * cy + z * sy
    z1 = -x * sy + z * cy

    cx = math.cos(angle_x)
    sx = math.sin(angle_x)

    y2 = y * cx - z1 * sx
    z2 = y * sx + z1 * cx

    return x1, y2, z2 + CAMERA_DISTANCE


# ==========================================
# PERSPECTIVE PROJECTION
# ==========================================

def project_vertex(vertex):
    x, y, z = vertex

    screen_x = WIDTH / 2 + FOCAL_LENGTH * x / z
    screen_y = HEIGHT / 2 - FOCAL_LENGTH * y / z

    return screen_x, screen_y, z


# ==========================================
# TRIANGLE RASTERIZER
# ==========================================

def edge(a, b, p):
    return (
        (p[0] - a[0]) * (b[1] - a[1])
        - (p[1] - a[1]) * (b[0] - a[0])
    )


def rasterize_triangle(vertices, pixels, depth_buffer):
    area = edge(vertices[1], vertices[2], vertices[0])

    if abs(area) < 0.000001:
        return

    min_x = max(0, int(min(v[0] for v in vertices)))
    max_x = min(WIDTH - 1, int(max(v[0] for v in vertices)) + 1)

    min_y = max(0, int(min(v[1] for v in vertices)))
    max_y = min(HEIGHT - 1, int(max(v[1] for v in vertices)) + 1)

    for py in range(min_y, max_y + 1):
        for px in range(min_x, max_x + 1):

            point = (px + 0.5, py + 0.5)

            e0 = edge(vertices[1], vertices[2], point)
            e1 = edge(vertices[2], vertices[0], point)
            e2 = edge(vertices[0], vertices[1], point)

            w0 = e0 / area
            w1 = e1 / area
            w2 = e2 / area

            if min(w0, w1, w2) < -0.000001:
                continue

            inv_z = (
                w0 / vertices[0][2]
                + w1 / vertices[1][2]
                + w2 / vertices[2][2]
            )

            index = py * WIDTH + px

            if inv_z <= depth_buffer[index]:
                continue

            depth_buffer[index] = inv_z

            weights = [
                w0 / vertices[0][2] / inv_z,
                w1 / vertices[1][2] / inv_z,
                w2 / vertices[2][2] / inv_z
            ]

            for channel in range(3):
                colour = sum(
                    weights[i] * COLORS[i][channel]
                    for i in range(3)
                )

                pixels[index * 3 + channel] = max(
                    0, min(255, int(colour))
                )


# ==========================================
# RENDER PIPELINE + PROFILER
# ==========================================

def render_frame(angle):

    timings = {}

    # Stage 1: Framebuffer clear
    start = time.perf_counter()

    pixels = bytearray([9, 12, 23] * (WIDTH * HEIGHT))
    depth_buffer = [0.0] * (WIDTH * HEIGHT)

    timings["Clear"] = time.perf_counter() - start

    # Stage 2: Vertex transformation
    start = time.perf_counter()

    angle_x = angle * 0.65
    angle_y = angle

    transformed = [
        rotate_vertex(v, angle_x, angle_y)
        for v in VERTICES
    ]

    timings["Transform"] = time.perf_counter() - start

    # Stage 3: Perspective projection
    start = time.perf_counter()

    projected = [
        project_vertex(v)
        for v in transformed
    ]

    timings["Projection"] = time.perf_counter() - start

    # Stage 4: Rasterization
    start = time.perf_counter()

    rasterize_triangle(projected, pixels, depth_buffer)

    timings["Rasterization"] = time.perf_counter() - start

    return pixels, timings


# ==========================================
# DISPLAY CONVERSION
# ==========================================

def convert_to_tk_pixels(pixels):
    rows = []

    for y in range(HEIGHT):
        row = []

        for x in range(WIDTH):
            index = (y * WIDTH + x) * 3

            r = pixels[index]
            g = pixels[index + 1]
            b = pixels[index + 2]

            row.append(f"#{r:02x}{g:02x}{b:02x}")

        rows.append("{" + " ".join(row) + "}")

    return " ".join(rows)


# ==========================================
# USER INTERFACE
# ==========================================

root = tk.Tk()
root.title("AVERON X1 | Performance Profiler v0.3")
root.resizable(False, False)

screen = tk.Label(root, bg="#090c17")
screen.pack()

photo = tk.PhotoImage(width=WIDTH, height=HEIGHT)
screen.configure(image=photo)

info = tk.Label(
    root,
    text="AVERON X1 | PROFILER ONLINE",
    font=("Consolas", 10),
    bg="#111827",
    fg="#66e6ff",
    justify="left",
    pady=9
)
info.pack(fill="x")

angle = 0.0
last_frame_time = time.perf_counter()

# Smoothed stage timings
averages = {
    "Clear": 0.0,
    "Transform": 0.0,
    "Projection": 0.0,
    "Rasterization": 0.0,
    "Conversion": 0.0,
    "Upload": 0.0
}

initialized = False


def animate():
    global angle, last_frame_time, initialized

    frame_start = time.perf_counter()

    # Render pipeline
    pixels, timings = render_frame(angle)

    # Stage 5: Display conversion
    start = time.perf_counter()

    tk_pixels = convert_to_tk_pixels(pixels)

    timings["Conversion"] = time.perf_counter() - start

    # Stage 6: Display upload
    start = time.perf_counter()

    photo.put(tk_pixels, to=(0, 0))

    timings["Upload"] = time.perf_counter() - start

    # Smooth measurements to reduce fluctuations
    for name, value in timings.items():
        if not initialized:
            averages[name] = value
        else:
            averages[name] = averages[name] * 0.8 + value * 0.2

    initialized = True

    frame_end = time.perf_counter()
    frame_time = frame_end - last_frame_time
    last_frame_time = frame_end

    fps = 1.0 / max(frame_time, 0.000001)

    total_ms = sum(averages.values()) * 1000

    report = (
        "AVERON X1 | PROFILER ONLINE\n"
        f"FPS: {fps:.1f} | Pipeline: {total_ms:.2f} ms\n"
        f"Clear:        {averages['Clear'] * 1000:.2f} ms\n"
        f"Transform:    {averages['Transform'] * 1000:.2f} ms\n"
        f"Projection:   {averages['Projection'] * 1000:.2f} ms\n"
        f"Rasterization:{averages['Rasterization'] * 1000:.2f} ms\n"
        f"Conversion:   {averages['Conversion'] * 1000:.2f} ms\n"
        f"Upload:       {averages['Upload'] * 1000:.2f} ms"
    )

    info.configure(text=report)

    angle += 0.035

    root.after(30, animate)


animate()
root.mainloop()

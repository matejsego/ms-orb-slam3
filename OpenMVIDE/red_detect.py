import sensor 
import time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

clock = time.clock()

red_threshold = (38, 100, 15, 127, 15, 127)

while True:
    clock.tick()
    img = sensor.snapshot()

    blobs = img.find_blobs([red_threshold], pixels_threshold=200, area_threshold=200, merge=True)

    for blob in blobs:
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        print("Found blob at x: %d, y: %d" % (blob.cx(), blob.cy()))

    print(clock.fps())

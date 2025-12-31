def run():
    from neopixel import Neopixel
    import time,math

    #constants
    DEG_TO_RAD = (3.14/180)

    #variables
    pixels = Neopixel(1,0,23,"RGB")

    #numerical-based limits or conventional (i.e.: time sleeping and brightness ceiling for RGB max value (255,255,255)
    brightness = 127#max brightness for rainbow effect 127, max overall brightness 255 (will fuck about above 127 btw but 255 is the max)
    frequency = 60

    #calculation-based limits (due to maths, these limits are enacted on the LED, unlike a fixed brightness value of 47 being the max limit when given 255 White
    brightnessR = 255
    brightnessG = 255
    brightnessB = 255
    frequencyR = 1#i think that mathematically changing the frequency should be less strenuous on the device than physically changing the frequency (also 1 is the min)
    frequencyG = 1
    frequencyB = 1
    #keep amplitude and offset equal as the offset keeps all values from being negative (negs bug out the rgb led)
    amplitudeR = 1
    amplitudeG = 1
    amplitudeB = 1
    xOffsetR = -210
    xOffsetG = -90
    xOffsetB = -330
    yOffsetR = 1
    yOffsetG = 1
    yOffsetB = 1

    theta = 0

    #array for  R G B
    rainbows = [0,0,0]

    #set brightness
    pixels.brightness(brightness)

    #rgb function that takes theta and RGB signals are 120 deg out of phase. This is how 3 phase power works for AC (Power Station to Substation). Single phase is home-use (Substation to Home)
    def rgb(theta):
        #return [255 - (255*math.sin(frequency*(theta+270)*radconv)),255 - (255*math.sin(frequency*(theta+30)*radconv)),255 - (255*math.sin(frequency*(theta+150)*radconv))]
        return [brightnessR * (yOffsetR+amplitudeR*math.sin(frequencyR*(theta+xOffsetR)*DEG_TO_RAD)),
                brightnessG * (yOffsetG+amplitudeG*math.sin(frequencyG*(theta+xOffsetG)*DEG_TO_RAD)),
                brightnessB * (yOffsetB+amplitudeB*math.sin(frequencyB*(theta+xOffsetB)*DEG_TO_RAD))]

    #main loop: updates the RGB values and shows it
    while True:
        rainbows = rgb(theta)
        theta += 1
        if theta >= 360:
            theta -= 360
        pixels.set_pixel(0,(rainbows[0],rainbows[1],rainbows[2]))
        pixels.show()
        time.sleep(1/frequency)

